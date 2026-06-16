import subprocess

import pytest

from scythe import parsers
from scythe.graph import build_graph_from_file
from scythe.rewrites import AST_REMOVALS

SOLC_VERSION = "0.5.0"

SNIPPET = """pragma solidity 0.5.0;

contract Base {
    address public owner;
    event Logged(uint256 value);
    modifier onlyOwner() { require(msg.sender == owner); _; }
    constructor() public { owner = msg.sender; }
    function ping() public onlyOwner { emit Logged(1); }
}

contract Token is Base {
    uint256 public total;
    function setTotal(uint256 v) public onlyOwner { total = v; emit Logged(v); }
}

contract Unused {
    function noop() public pure returns (uint256) { return 0; }
}
"""


def _solc_available():
    try:
        return subprocess.run(
            ["solc-select", "use", SOLC_VERSION], capture_output=True
        ).returncode == 0
    except FileNotFoundError:
        return False


SOLC_OK = _solc_available()


def _parses_clean(code):
    return not parsers.PARSERS["solidity"].parse(code.encode("utf-8")).root_node.has_error


def _compiles(code, tmp_path):
    f = tmp_path / "out.sol"
    f.write_text(code)
    result = subprocess.run(["solc", str(f)], capture_output=True, text=True)
    return result.returncode == 0, result.stderr


@pytest.fixture
def graph_and_src(tmp_path):
    f = tmp_path / "snippet.sol"
    f.write_text(SNIPPET)
    return build_graph_from_file(str(f), "solidity"), SNIPPET


def _remove(graph, src, node_type, name):
    nodes = {n for n in graph.nodes
             if n.node_type == node_type and n.name == name}
    assert nodes, f"no {node_type} named {name!r} found in graph"
    return AST_REMOVALS["solidity"](src, graph).remove_nodes(nodes, "removal")


@pytest.mark.skipif(not SOLC_OK, reason=f"solc {SOLC_VERSION} not installed")
def test_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(SNIPPET, tmp_path)
    assert ok, f"baseline snippet should compile:\n{stderr}"


@pytest.mark.parametrize("node_type,name,declaration", [
    ("modifier", "onlyOwner", "modifier onlyOwner"),
    ("event", "Logged", "event Logged"),
    ("contract", "Unused", "contract Unused"),
    ("contract", "Base", "contract Base"),
])
def test_removal_keeps_program_valid(graph_and_src, tmp_path, node_type, name, declaration):
    graph, src = graph_and_src
    out = _remove(graph, src, node_type, name)
    assert declaration not in out
    assert _parses_clean(out)
    if SOLC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"removing {node_type} {name} left a reference error:\n{stderr}"


def test_modifier_usages_are_removed(graph_and_src):
    graph, src = graph_and_src
    out = _remove(graph, src, "modifier", "onlyOwner")
    assert "onlyOwner" not in out


def test_event_emits_are_removed(graph_and_src):
    graph, src = graph_and_src
    out = _remove(graph, src, "event", "Logged")
    assert "Logged" not in out


def test_base_contract_removal_cascades(graph_and_src):
    graph, src = graph_and_src
    out = _remove(graph, src, "contract", "Base")
    assert "contract Base" not in out
    assert "is Base" not in out
    assert "onlyOwner" not in out
    assert "Logged" not in out
    assert "contract Token" in out


def test_unselected_declarations_are_kept(graph_and_src):
    graph, src = graph_and_src
    out = _remove(graph, src, "modifier", "onlyOwner")
    assert "event Logged" in out
    assert "contract Token" in out
    assert "contract Unused" in out


GAPS_SNIPPET = """pragma solidity 0.5.0;

contract C {
    struct Pair { uint256 a; uint256 b; }
    uint256 public counter;
    uint256 public total;

    function bump() public { counter = counter + 1; }
    function addTotal(uint256 v) public { total = total + v; }
    function f(uint256 v) public pure returns (uint256) {
        uint256 tmp = v + 1;
        Pair memory p = Pair(1, 2);
        return v;
    }
}
"""


@pytest.fixture
def gaps_graph_and_src(tmp_path):
    f = tmp_path / "gaps.sol"
    f.write_text(GAPS_SNIPPET)
    return build_graph_from_file(str(f), "solidity"), GAPS_SNIPPET


def test_graph_emits_struct_statevar_var(gaps_graph_and_src):
    graph, _ = gaps_graph_and_src
    by_type = {}
    for n in graph.nodes:
        by_type.setdefault(n.node_type, set()).add(n.name)
    assert "Pair" in by_type.get("struct", set())
    assert {"counter", "total"} <= by_type.get("state_var", set())
    assert {"tmp", "p"} <= by_type.get("var", set())


@pytest.mark.skipif(not SOLC_OK, reason=f"solc {SOLC_VERSION} not installed")
def test_gaps_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(GAPS_SNIPPET, tmp_path)
    assert ok, f"baseline snippet should compile:\n{stderr}"


@pytest.mark.parametrize("node_type,name", [
    ("struct", "Pair"),
    ("state_var", "counter"),
    ("var", "tmp"),
])
def test_struct_statevar_var_removal_is_valid(gaps_graph_and_src, tmp_path, node_type, name):
    graph, src = gaps_graph_and_src
    out = _remove(graph, src, node_type, name)
    assert name not in out
    assert _parses_clean(out)
    if SOLC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"removing {node_type} {name} left a reference error:\n{stderr}"


def test_state_var_use_sites_removed(gaps_graph_and_src):
    graph, src = gaps_graph_and_src
    out = _remove(graph, src, "state_var", "counter")
    assert "counter" not in out
    assert "total" in out
    assert "function bump" in out


CASCADE_SNIPPET = """pragma solidity 0.5.0;

contract Helper {
    function ping() public pure returns (uint256) { return 1; }
}

contract Main {
    struct Pair { uint256 a; uint256 b; }
    Pair internal origin;
    Helper internal helper;

    function getA() public view returns (uint256) { return origin.a; }
    function useHelper() public view returns (uint256) { return helper.ping(); }
    function keep() public pure returns (uint256) { return 42; }
}
"""


@pytest.fixture
def cascade_graph_and_src(tmp_path):
    f = tmp_path / "cascade.sol"
    f.write_text(CASCADE_SNIPPET)
    return build_graph_from_file(str(f), "solidity"), CASCADE_SNIPPET


def test_uses_type_edges_built(cascade_graph_and_src):
    graph, _ = cascade_graph_and_src
    uses = {(u.name, v.name) for u, v, d in graph.edges(data=True)
            if d.get("label") == "uses-type"}
    assert ("Pair", "origin") in uses
    assert ("Helper", "helper") in uses


@pytest.mark.parametrize("node_type,name,typed_var", [
    ("struct", "Pair", "origin"),
    ("contract", "Helper", "helper"),
])
def test_type_use_cascade_is_valid(cascade_graph_and_src, tmp_path, node_type, name, typed_var):
    graph, src = cascade_graph_and_src
    out = _remove(graph, src, node_type, name)
    assert f"{node_type} {name}" not in out
    assert typed_var not in out
    assert _parses_clean(out)
    assert "function keep" in out
    if SOLC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"type-use cascade for {name} left a reference error:\n{stderr}"


FLATTEN_SNIPPET = """pragma solidity 0.5.0;

contract Base {
    uint256 internal shared;
    function setShared(uint256 v) internal { shared = v; }
}

contract Derived is Base {
    function use() public returns (uint256) { setShared(7); return shared; }
}
"""


@pytest.fixture
def flatten_graph_and_src(tmp_path):
    f = tmp_path / "flatten.sol"
    f.write_text(FLATTEN_SNIPPET)
    return build_graph_from_file(str(f), "solidity"), FLATTEN_SNIPPET


def _flatten(graph, src, name):
    nodes = {n for n in graph.nodes if n.node_type == "contract" and n.name == name}
    assert nodes, f"no contract {name!r} in graph"
    return AST_REMOVALS["solidity"](src, graph).flatten_inheritance(nodes)


def test_flatten_eliminates_base_and_promotes_members(flatten_graph_and_src, tmp_path):
    graph, src = flatten_graph_and_src
    out = _flatten(graph, src, "Base")
    assert "contract Base" not in out
    assert "is Base" not in out
    assert "shared" in out
    assert "function setShared" in out
    assert "contract Derived" in out
    assert _parses_clean(out)
    if SOLC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"flattened program failed to compile:\n{stderr}"


def test_flatten_leaf_contract_is_noop(flatten_graph_and_src):
    graph, src = flatten_graph_and_src
    out = _flatten(graph, src, "Derived")
    assert out == src


PLACEHOLDER_SNIPPET = """pragma solidity 0.5.0;

contract C {
    struct Point { uint256 x; uint256 y; }
    struct Pair { uint256 a; uint256 b; }

    Point internal origin;

    function dist(Point memory p) internal pure returns (uint256) {
        return p.x + p.y;
    }
    function viaField() public view returns (uint256) { return origin.x; }
    function usesPair() public pure returns (uint256) {
        Pair memory q = Pair(1, 2);
        return q.a;
    }
    function keep() public pure returns (uint256) { return 42; }
}
"""


@pytest.fixture
def placeholder_graph_and_src(tmp_path):
    f = tmp_path / "placeholder.sol"
    f.write_text(PLACEHOLDER_SNIPPET)
    return build_graph_from_file(str(f), "solidity"), PLACEHOLDER_SNIPPET


@pytest.mark.skipif(not SOLC_OK, reason=f"solc {SOLC_VERSION} not installed")
def test_placeholder_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(PLACEHOLDER_SNIPPET, tmp_path)
    assert ok, f"baseline snippet should compile:\n{stderr}"


def test_struct_param_retyped_to_placeholder(placeholder_graph_and_src, tmp_path):
    graph, src = placeholder_graph_and_src
    out = _remove(graph, src, "struct", "Point")
    assert "struct Point" not in out
    assert "origin" not in out
    assert "struct __S" in out
    assert "__S memory p" in out
    assert "uint256 x" in out and "uint256 y" in out
    assert "p.x + p.y" in out
    assert "function dist" in out
    assert "function keep" in out
    assert _parses_clean(out)
    if SOLC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"placeholder retyping left an error:\n{stderr}"


def test_placeholder_injected_inside_contract(placeholder_graph_and_src):
    graph, src = placeholder_graph_and_src
    out = _remove(graph, src, "struct", "Point")
    assert out.index("contract C") < out.index("struct __S")


def test_fully_deletable_struct_needs_no_placeholder(placeholder_graph_and_src, tmp_path):
    graph, src = placeholder_graph_and_src
    out = _remove(graph, src, "struct", "Pair")
    assert "struct Pair" not in out
    assert "__S" not in out
    assert _parses_clean(out)
    if SOLC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"removing fully-deletable struct left an error:\n{stderr}"


CONTROLFLOW_SNIPPET = """pragma solidity 0.5.0;

contract C {
    uint256[] public xs;

    function total() public view returns (uint256) {
        uint256 n = xs.length;
        uint256 s = 0;
        for (uint256 i = 0; i < n; i++) {
            s += xs[i];
        }
        if (xs.length > 0) {
            s += 1;
        }
        return s;
    }
    function keep() public pure returns (uint256) { return 7; }
}
"""


@pytest.fixture
def controlflow_graph_and_src(tmp_path):
    f = tmp_path / "controlflow.sol"
    f.write_text(CONTROLFLOW_SNIPPET)
    return build_graph_from_file(str(f), "solidity"), CONTROLFLOW_SNIPPET


@pytest.mark.skipif(not SOLC_OK, reason=f"solc {SOLC_VERSION} not installed")
def test_controlflow_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(CONTROLFLOW_SNIPPET, tmp_path)
    assert ok, f"baseline snippet should compile:\n{stderr}"


def test_state_var_removal_cleans_loops_and_dead_locals(controlflow_graph_and_src, tmp_path):
    graph, src = controlflow_graph_and_src
    out = _remove(graph, src, "state_var", "xs")
    assert "xs" not in out
    assert "for (" not in out
    assert "n = " not in out
    assert "if (" not in out
    assert "uint256 s = 0" in out
    assert "return s" in out
    assert "function keep" in out
    assert _parses_clean(out)
    if SOLC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"removing xs left a dangling control-flow reference:\n{stderr}"
