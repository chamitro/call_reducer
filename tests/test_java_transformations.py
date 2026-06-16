import subprocess

import pytest

from scythe import parsers
from scythe.graph import build_graph_from_file
from scythe.rewrites import AST_REMOVALS


def _javac_available():
    try:
        return subprocess.run(["javac", "-version"],
                              capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


JAVAC_OK = _javac_available()


def _parses_clean(code):
    return not parsers.PARSERS["java"].parse(
        code.encode("utf-8")).root_node.has_error


def _compiles(code, tmp_path):
    f = tmp_path / "Main.java"
    f.write_text(code)
    out = tmp_path / "out"
    out.mkdir(exist_ok=True)
    r = subprocess.run(["javac", "-d", str(out), str(f)],
                       capture_output=True, text=True)
    return r.returncode == 0, r.stderr


def _build_graph(code, tmp_path):
    f = tmp_path / "Main.java"
    f.write_text(code)
    return build_graph_from_file(str(f), "java")


NEST_SNIPPET = """class A {
    int f;
    int m() { int x = 1; return x; }
}
class B {
    int m() { return 2; }
}
"""


def test_graph_nesting_parents(tmp_path):
    g = _build_graph(NEST_SNIPPET, tmp_path)
    funcs = [n for n in g.nodes if n.node_type == "function" and n.name == "m"]
    assert len(funcs) == 2, "expected two distinct m() nodes"
    assert sorted((n.parent.name if n.parent else None) for n in funcs) == ["A", "B"]

    fields = [n for n in g.nodes if n.node_type == "field" and n.name == "f"]
    assert fields and fields[0].parent is not None and fields[0].parent.name == "A"

    locs = [n for n in g.nodes if n.node_type == "local_variable" and n.name == "x"]
    assert locs and locs[0].parent is not None
    assert locs[0].parent.node_type == "function" and locs[0].parent.name == "m"


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_nest_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(NEST_SNIPPET, tmp_path)
    assert ok, f"baseline snippet should compile:\n{stderr}"


def _replace(graph, src, node_type, name):
    nodes = {n for n in graph.nodes
             if n.node_type == node_type and n.name == name}
    assert nodes, f"no {node_type} named {name!r} in graph"
    return AST_REMOVALS["java"](src, graph).remove_nodes(nodes, "replacement")


REPL_SNIPPET = """class C {
    int g() { return 1; }
    void v() {}
    Foo mk() { return null; }

    int useFn() {
        g();
        v();
        int a = g() + 1;
        mk().bar();
        return a;
    }
}
class Foo { void bar() {} }
"""


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_repl_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(REPL_SNIPPET, tmp_path)
    assert ok, f"baseline should compile:\n{stderr}"


def test_replace_function_int(tmp_path):
    g = _build_graph(REPL_SNIPPET, tmp_path)
    out = _replace(g, REPL_SNIPPET, "function", "g")
    assert "int g()" not in out
    assert "g()" not in out
    assert "42 + 1" in out
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"replacing g left an error:\n{stderr}"


def test_replace_void_function(tmp_path):
    g = _build_graph(REPL_SNIPPET, tmp_path)
    out = _replace(g, REPL_SNIPPET, "function", "v")
    assert "void v()" not in out
    assert "v();" not in out
    assert "int a = g() + 1" in out
    assert _parses_clean(out)


def test_replace_function_receiver_is_parenthesized(tmp_path):
    g = _build_graph(REPL_SNIPPET, tmp_path)
    out = _replace(g, REPL_SNIPPET, "function", "mk")
    assert "((Foo) null).bar()" in out
    assert "Foo mk()" not in out
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"replacing mk left an error:\n{stderr}"


FIELD_LOCAL_SNIPPET = """class C {
    int f = 5;
    int useField() {
        f = 3;
        return f + 1;
    }
    int useLocal() {
        int x = 5;
        x = x + 1;
        return x + 2;
    }
}
"""


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_field_local_baseline_compiles(tmp_path):
    ok, stderr = _compiles(FIELD_LOCAL_SNIPPET, tmp_path)
    assert ok, f"baseline should compile:\n{stderr}"


def test_replace_field(tmp_path):
    g = _build_graph(FIELD_LOCAL_SNIPPET, tmp_path)
    out = _replace(g, FIELD_LOCAL_SNIPPET, "field", "f")
    assert "int f = 5" not in out
    assert "f = 3" not in out
    assert "42 + 1" in out
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"replacing field f left an error:\n{stderr}"


def test_replace_local(tmp_path):
    g = _build_graph(FIELD_LOCAL_SNIPPET, tmp_path)
    out = _replace(g, FIELD_LOCAL_SNIPPET, "local_variable", "x")
    assert "int x = 5" not in out
    assert "x = x + 1" not in out
    assert "42 + 2" in out
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"replacing local x left an error:\n{stderr}"


CLASS_SNIPPET = """class A {
    int x;
    int foo() { return x; }
    void bar() {}
}
class Use {
    A field;
    int m(A p) {
        A a = new A();
        a.bar();
        int v = a.foo() + a.x;
        return v;
    }
    void make() { new A().bar(); }
}
"""


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_class_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(CLASS_SNIPPET, tmp_path)
    assert ok, f"baseline should compile:\n{stderr}"


def test_class_removal_uses_placeholder(tmp_path):
    g = _build_graph(CLASS_SNIPPET, tmp_path)
    out = _replace(g, CLASS_SNIPPET, "class", "A")
    assert "class A {" not in out
    assert "class __A" in out
    assert "((__A) null)" in out
    assert "__A a" in out and "__A field" in out
    assert "foo" in out and "bar" in out and "x" in out
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"class placeholder left an error:\n{stderr}"


def test_new_as_receiver_is_parenthesized(tmp_path):
    g = _build_graph(CLASS_SNIPPET, tmp_path)
    out = _replace(g, CLASS_SNIPPET, "class", "A")
    assert "((__A) null).bar()" in out


INTERFACE_SNIPPET = """interface I { int g(); }
class C implements I {
    public int g() { return 1; }
    int use(I obj) { return obj.g(); }
}
"""


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_interface_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(INTERFACE_SNIPPET, tmp_path)
    assert ok, f"baseline should compile:\n{stderr}"


def test_interface_removal_drops_implements(tmp_path):
    g = _build_graph(INTERFACE_SNIPPET, tmp_path)
    out = _replace(g, INTERFACE_SNIPPET, "class", "I")
    assert "interface I" not in out
    assert "implements I" not in out
    assert "class C" in out
    assert "__A obj" in out
    assert "class __A" in out
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"interface placeholder left an error:\n{stderr}"


def _flatten(graph, src, name):
    nodes = {n for n in graph.nodes if n.node_type == "class" and n.name == name}
    assert nodes, f"no class {name!r} in graph"
    return AST_REMOVALS["java"](src, graph).flatten_inheritance(nodes)


FLATTEN_SNIPPET = """class Base {
    int shared;
    int helper() { return shared; }
}
class Derived extends Base {
    int use() { return helper() + shared; }
}
"""


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_flatten_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(FLATTEN_SNIPPET, tmp_path)
    assert ok, f"baseline should compile:\n{stderr}"


def test_flatten_promotes_members_and_deletes_base(tmp_path):
    g = _build_graph(FLATTEN_SNIPPET, tmp_path)
    out = _flatten(g, FLATTEN_SNIPPET, "Base")
    assert "class Base" not in out
    assert "extends Base" not in out
    assert "int helper()" in out
    assert "int shared" in out
    assert "class Derived" in out
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"flattened program failed to compile:\n{stderr}"


OVERRIDE_SNIPPET = """class Base { void run() {} }
class Derived extends Base {
    @Override
    void run() { }
    void m() { run(); }
}
"""


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_override_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(OVERRIDE_SNIPPET, tmp_path)
    assert ok, f"baseline should compile:\n{stderr}"


def test_flatten_strips_override(tmp_path):
    g = _build_graph(OVERRIDE_SNIPPET, tmp_path)
    out = _flatten(g, OVERRIDE_SNIPPET, "Base")
    assert "class Base" not in out
    assert "@Override" not in out
    assert out.count("void run()") == 1
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"flatten left an @Override error:\n{stderr}"


def test_flatten_leaf_is_noop(tmp_path):
    g = _build_graph(FLATTEN_SNIPPET, tmp_path)
    out = _flatten(g, FLATTEN_SNIPPET, "Derived")
    assert out == FLATTEN_SNIPPET


SUPER_SNIPPET = """class Base {
    int v() { return 1; }
    void p() {}
}
class Derived extends Base {
    int v() { return 2; }
    void run() {
        super.p();
        int y = super.v();
        compute();
    }
    void compute() {}
}
"""


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_super_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(SUPER_SNIPPET, tmp_path)
    assert ok, f"baseline should compile:\n{stderr}"


def test_flatten_removes_super_statements(tmp_path):
    g = _build_graph(SUPER_SNIPPET, tmp_path)
    out = _flatten(g, SUPER_SNIPPET, "Base")
    assert "class Base" not in out
    assert "super" not in out
    assert "extends Base" not in out
    assert "void p()" in out
    assert "compute();" in out
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"flatten left a dangling super:\n{stderr}"


SUPER_CTOR_SNIPPET = """class Base {
    int x;
    Base() {}
}
class Derived extends Base {
    Derived() { super(); }
    int use() { return x; }
}
"""


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_super_ctor_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(SUPER_CTOR_SNIPPET, tmp_path)
    assert ok, f"baseline should compile:\n{stderr}"


def test_flatten_removes_super_ctor_call(tmp_path):
    g = _build_graph(SUPER_CTOR_SNIPPET, tmp_path)
    out = _flatten(g, SUPER_CTOR_SNIPPET, "Base")
    assert "class Base" not in out
    assert "super(" not in out
    assert "int x" in out
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"flatten left a dangling super():\n{stderr}"


RETURN_SUPER_SNIPPET = """class Base {
    int v() { return 1; }
    int x = 5;
}
class Derived extends Base {
    int v() { return super.v() + 1; }
    int w() { return super.v(); }
    int x = 9;
    int get() { return super.x; }
}
"""


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_return_super_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(RETURN_SUPER_SNIPPET, tmp_path)
    assert ok, f"baseline should compile:\n{stderr}"


def test_flatten_constant_replaces_super_in_return(tmp_path):
    g = _build_graph(RETURN_SUPER_SNIPPET, tmp_path)
    out = _flatten(g, RETURN_SUPER_SNIPPET, "Base")
    assert "class Base" not in out
    assert "super" not in out
    assert "return 42 + 1" in out
    assert out.count("return 42;") == 2
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"flatten left a broken return:\n{stderr}"


SUPER_CHAIN_SNIPPET = """class Base {
    Base(int a, int b) {}
}
class Mid extends Base {
    Mid(Base x, float y) { super(1, 2); }
}
class Leaf extends Mid {
    Leaf() { super(null, 3.0f); }
    int keep() { return 7; }
}
"""


def _remove_classes(graph, src, names):
    nodes = {n for n in graph.nodes if n.node_type == "class" and n.name in names}
    assert nodes, f"no classes {names!r} in graph"
    return AST_REMOVALS["java"](src, graph).remove_nodes(nodes, "replacement")


@pytest.mark.skipif(not JAVAC_OK, reason="javac not available")
def test_super_chain_snippet_baseline_compiles(tmp_path):
    ok, stderr = _compiles(SUPER_CHAIN_SNIPPET, tmp_path)
    assert ok, f"baseline should compile:\n{stderr}"


def test_class_removal_cleans_subclass_super(tmp_path):
    g = _build_graph(SUPER_CHAIN_SNIPPET, tmp_path)
    out = _remove_classes(g, SUPER_CHAIN_SNIPPET, {"Base", "Mid"})
    assert "class Mid" not in out and "class Base" not in out
    assert "extends" not in out
    assert "super(" not in out
    assert "keep" in out
    assert _parses_clean(out)
    if JAVAC_OK:
        ok, stderr = _compiles(out, tmp_path)
        assert ok, f"standalone subclass should compile:\n{out}\n{stderr}"
