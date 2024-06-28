import os
import re
import string
import random
import time
import subprocess
import argparse
import networkx as nx
import picire
from universal import build_graph_from_file
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from SolidityLexer import SolidityLexer
from SolidityParser import SolidityParser
from SolidityListener import SolidityListener


# Argument parsing
parser = argparse.ArgumentParser(description='Modify Solidity files based on node removal and Slither analysis, considering specified findings.')
parser.add_argument('--consider', type=str, help='Findings to consider in the format "finding=threshold"', default="")
args = parser.parse_args()

# Convert consider string to a dictionary
if args.consider:
    key, value = args.consider.split('=')
    consider_findings = {key: int(value)}
else:
    consider_findings = {}

# Slither analysis
def run_slither_analysis(file_path):
    """Runs Slither on a given Solidity file and captures the output."""
    command = ["slither", file_path]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stderr  # Slither typically outputs warnings and errors to stderr.
    except subprocess.CalledProcessError as e:
        print("Slither analysis failed.")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return Code: {e.returncode}")
        print(f"Error Output: {e.stderr}")
        return None

# Parsing Slither findings
def parse_slither_findings(slither_output, consider_findings):
    """Parses the Slither output to only count occurrences of specified patterns."""
    findings = {}
    for key in consider_findings.keys():
        pattern = re.compile(re.escape(key))
        findings_count = sum(1 for _ in pattern.findall(slither_output))
        if findings_count > 0:
            findings[key] = findings_count
    return findings

# Comparing Slither outputs
def compare_slither_outputs(original_findings, modified_findings, consider_findings):
    """Compares Slither findings, considering specified findings."""
    for finding, threshold in consider_findings.items():
        original_count = original_findings.get(finding, 0)
        modified_count = modified_findings.get(finding, 0)
        if original_count != modified_count or original_count > threshold or modified_count > threshold:
            return False
    return True


# ANTLR listener for removing contract and function definitions
class RemovalListener(SolidityListener):
    def __init__(self, nodes_to_remove):
        super().__init__()
        self.removals = []
        self.nodes_to_remove = nodes_to_remove

    def enterFunctionDefinition(self, ctx: SolidityParser.FunctionDefinitionContext):
        functions_name = ctx.getChild(0).getText()
        function_name = functions_name.replace("function", "").strip()
        if any(node.name == function_name for node in self.nodes_to_remove):
            print(f"Marking function '{function_name}' for removal.")
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterModifierInvocation(self, ctx: SolidityParser.ModifierInvocationContext):
        if any(node.name == ctx.getChild(0).getText() for node in self.nodes_to_remove):
            print(f"Marking modifier invocation '{ctx.getChild(0).getText()}' for removal.")
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterModifierDefinition(self, ctx: SolidityParser.ModifierDefinitionContext):
        self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterExpressionStatement(self, ctx: SolidityParser.ExpressionStatementContext):
        text = ctx.getText()
        if any(node.name + "(" in text for node in self.nodes_to_remove):
            equal_sign_index = text.find('=')
            if equal_sign_index != -1:
                start = ctx.start.start + equal_sign_index + 1
                stop = ctx.stop.stop
                if stop < ctx.stop.stop and text[stop - ctx.start.start] == ';':
                    stop += 1
                stop -= 1
                self.removals.append((start, stop))
            else:
                self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterVariableDeclarationStatement(self, ctx: SolidityParser.VariableDeclarationStatementContext):
        text = ctx.getText()
        if any(node.name + "(" in text for node in self.nodes_to_remove):
            equal_sign_index = text.find('=')
            if equal_sign_index != -1:
                start = ctx.start.start + equal_sign_index + 1
                stop = ctx.stop.stop
                if stop < ctx.stop.stop and text[stop - ctx.start.start] == ';':
                    stop += 1
                stop -= 1
                self.removals.append((start, stop))


class RemovalListener2(SolidityListener):
    def __init__(self, nodes_to_remove, graph):
        super().__init__()
        self.removals = []
        self.replacements = []
        self.nodes_to_remove = nodes_to_remove
        self.graph = graph
        self.temp_graph = self.graph.copy()

    def get_node_by_name(self, node_name):
        nodes = [n for n in self.graph.nodes()
                 if n.node_type == "contract" and n.name == node_name]
        assert len(nodes) == 1
        return nodes[0]

    def enterContractDefinition(self,
                                ctx: SolidityParser.ContractDefinitionContext):
        contract_type = ctx.getChild(0).getText()

        # Find the identifier in the children
        identifier = None
        for i in range(ctx.getChildCount()):
            if isinstance(ctx.getChild(i), SolidityParser.IdentifierContext):
                identifier = ctx.getChild(i).getText()
                break

        if identifier is None:
            return

        if any(node.name == identifier for node in self.nodes_to_remove):
            print(f"Marking contract '{identifier}' for removal.")
            self.removals.append((ctx.start.start, ctx.stop.stop))
            contract_node = self.get_node_by_name(identifier)
            parents = list(self.temp_graph.predecessors(contract_node))
            children = list(self.temp_graph.successors(contract_node))
            for child in children:
                self.temp_graph.remove_edge(contract_node, child)
                for parent in parents:
                    self.temp_graph.add_edge(parent, child, label="inherits")

    def exitSourceUnit(self, ctx: SolidityParser.SourceUnitContext):
        sorted_nodes = list(nx.topological_sort(self.graph))
        for contract_node in [n for n in self.temp_graph
                              if n.node_type == "contract" and
                              n not in self.nodes_to_remove]:
            parents = list(self.temp_graph.predecessors(contract_node))
            if parents:
                sorted_parents = []
                for n in sorted_nodes:
                    if n not in parents:
                        continue
                    pred_nodes = set(nx.ancestors(self.graph, n))
                    sorted_parents.append(n)
                    for pred in pred_nodes:
                        if pred in sorted_parents:
                            sorted_parents.remove(pred)

                new_inheritance_specifiers = ", ".join(
                    parent.name for parent in sorted_parents)
                self.replacements.append((contract_node.name,
                                          new_inheritance_specifiers))


class Interesting():
    def __init__(self, graph, content, findings, file_path, mode):
        self.graph = graph
        self.mode = mode
        self.content = content
        self.content_ = content
        self.original_findings = findings
        self.file_path = file_path
        self.removed_nodes = set()
        self.cache = {}
        lexer = SolidityLexer(InputStream(content))
        stream = CommonTokenStream(lexer)
        parser = SolidityParser(stream)
        self.tree = parser.sourceUnit()

    def remove_functions(self, nodes):
        nodes_to_remove = [
            n for n in self.graph.nodes()
            if n.node_type == 'function' and n not in nodes
        ]
        fr_nodes = frozenset(nodes)
        if fr_nodes in self.cache:
            return self.cache.get(fr_nodes)
        if not nodes_to_remove:
            return picire.Outcome.FAIL
        new_content = self.test_removing_functions(nodes_to_remove,
                                                   self.content)
        if new_content is not None:
            self.content = new_content
            self.update_file(new_content)
            res = picire.Outcome.FAIL
        else:
            res = picire.Outcome.PASS
        self.cache[fr_nodes] = res
        return res

    def remove_contracts(self, nodes):
        nodes_to_remove = [
            n for n in self.graph.nodes()
            if n.node_type == 'contract' and n not in nodes
        ]
        fr_nodes = frozenset(nodes)
        if fr_nodes in self.cache:
            return self.cache.get(fr_nodes)
        if not nodes_to_remove:
            return picire.Outcome.FAIL
        new_content = self.test_removing_contracts(nodes_to_remove,
                                                   self.content)
        if new_content is not None:
            self.content = new_content
            self.update_file(new_content)
            res = picire.Outcome.FAIL
        else:
            res = picire.Outcome.PASS
        self.cache[fr_nodes] = res
        return res

    def __call__(self, nodes, config_id):
        if self.mode == 'functions':
            return self.remove_functions(nodes)
        if self.mode == 'contracts':
            return self.remove_contracts(nodes)
        raise NotImplementedError(f"Unimplemented mode {self.mode}")

    def test_removing_functions(self, nodes_to_remove, content):
        nodes_to_remove = set(nodes_to_remove).union(self.removed_nodes)
        modified_content = remove_with_antlr(self.content_, self.tree,
                                             nodes_to_remove)
        name = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        temp_file_path = f"{name}.sol"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(modified_content)
        modified_slither_output = run_slither_analysis(temp_file_path)
        if modified_slither_output:
            modified_findings = parse_slither_findings(
                modified_slither_output, consider_findings)
            if compare_slither_outputs(self.original_findings,
                                       modified_findings, consider_findings):
                print("Keep property: Writing modified content to temp file")
                os.remove(temp_file_path)
                self.removed_nodes = nodes_to_remove
                return modified_content
            else:
                os.remove(temp_file_path)
                return None
        else:
            os.remove(temp_file_path)
            return None

    def test_removing_contracts(self, nodes_to_remove, content):
        temp_graph = self.graph.copy()  # Create a temporary copy of the graph
        modified_content = remove_with_antlr2(self.content,
                                              nodes_to_remove, temp_graph)
        name = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        temp_file_path = f"{name}.sol"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(modified_content)
        modified_slither_output = run_slither_analysis(temp_file_path)
        if modified_slither_output:
            modified_findings = parse_slither_findings(modified_slither_output, consider_findings)
            if compare_slither_outputs(self.original_findings, modified_findings, consider_findings):
                print("Keep property: Writing modified content to temp file")
                os.remove(temp_file_path)
                self.update_graph(nodes_to_remove, remove_contracts=True)
                return modified_content
            else:
                os.remove(temp_file_path)
                return None
        else:
            os.remove(temp_file_path)
            return None

    def get_contract_by_name(self, contract_name):
        nodes = [n for n in self.graph.nodes()
                 if n.node_type == "contract" and n.name == contract_name]
        assert len(nodes) == 1
        return nodes[0]

    def update_inheritance_tree(self, node):
        parents = list(self.graph.predecessors(node))
        children = set()
        for child, data in self.graph[node].items():
            if data["label"] == "inherits":
                children.add(child)
        for child in children:
            self.graph.remove_edge(node, child)
            for parent in parents:
                self.graph.add_edge(parent, child, label="inherits")

    def update_graph(self, nodes_to_remove, remove_contracts=False):
        nodes = set()
        excluded_nodes = set()
        for node in nodes_to_remove:
            if remove_contracts:
                self.update_inheritance_tree(node)
            if node not in self.graph:
                continue
            for k, v, label in nx.dfs_labeled_edges(self.graph, source=node):
                if label == "inherits":
                    excluded_nodes.add(v)
                    continue

                if k in excluded_nodes:
                    excluded_nodes.add(v)
                    continue

                nodes.add(k)
                nodes.add(v)
        self.graph.remove_nodes_from(nodes)

    def update_file(self, new_content):
        print("Updating file with new content")
        with open(self.file_path, 'w') as file:
            file.write(new_content)
        print("File updated successfully")


# Modified remove_with_antlr function
def remove_with_antlr(source_code, tree, nodes_to_remove):
    listener = RemovalListener(nodes_to_remove)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    for start, stop in sorted(listener.removals, reverse=True):
        code_block = source_code[start:stop + 1]
        if any(node.name in code_block for node in nodes_to_remove):
            source_code = source_code[:start] + (len(code_block) * " ") + source_code[stop + 1:]
    source_code = source_code.replace(r"/\s\s+/g", ' ')
    modified_source_code = re.sub(r'\n\s*\n', '\n\n', source_code)
#    print("Modified source code after removal:")
#    print(modified_source_code)
    return modified_source_code


# Modified remove_with_antlr2 function
def remove_with_antlr2(source_code, nodes_to_remove, inheritance_graph):
    lexer = SolidityLexer(InputStream(source_code))
    stream = CommonTokenStream(lexer)
    parser = SolidityParser(stream)
    tree = parser.sourceUnit()

    listener = RemovalListener2(nodes_to_remove, inheritance_graph)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    for start, stop in sorted(listener.removals, reverse=True):
        source_code = source_code[:start] + (len(source_code[start:stop + 1]) * " ") + source_code[stop + 1:]

    for identifier, new_inheritance_specifiers in listener.replacements:
        pattern = re.compile(rf"(\b{identifier}\b\s+is\s+)[^{{]*")
        replacement_text = f"{identifier} is {new_inheritance_specifiers}" if new_inheritance_specifiers else f"{identifier}"
        source_code = pattern.sub(replacement_text, source_code)

    source_code = source_code.replace(r"/\s\s+/g", ' ')
    modified_source_code = re.sub(r'\n\s*\n', '\n\n', source_code)
#    print("Modified source code after removal:")
#    print(modified_source_code)
    return modified_source_code


def main():
    # Record the start time
    start_time = time.time()
    sol_file_path = 'ext_changed.sol'
    graph = build_graph_from_file(sol_file_path)

    original_slither_output = run_slither_analysis(sol_file_path)

    original_findings = (
        parse_slither_findings(original_slither_output, consider_findings)
        if original_slither_output else {}
    )

    if not original_findings:
        raise Exception(
            f"The given property {consider_findings} does not hold")

    with open(sol_file_path, 'r') as file:
        original_content = file.read()

    # Functions mode
    interesting = Interesting(graph, original_content,
                              original_findings, sol_file_path,
                              'functions')
    function_nodes = [n for n in graph.nodes()
                      if n.node_type == "function"]
    dd_obj_functions = picire.ParallelDD(
        interesting,
        split=picire.splitter.ZellerSplit(n=4),
        cache=picire.cache.ConfigCache(),
        config_iterator=picire.iterator.CombinedIterator(
            False, picire.iterator.skip,
            picire.iterator.random
        )
    )
    output_functions = [x for x in dd_obj_functions(function_nodes)]
    interesting.update_graph([f for f in function_nodes
                              if f not in output_functions])

    interesting.mode = "contracts"
    contract_nodes = [n for n in graph.nodes()
                      if n.node_type == "contract"]
    dd_obj_functions = picire.DD(
        interesting,
        split=picire.splitter.ZellerSplit(n=4),
        cache=picire.cache.ConfigCache(),
        config_iterator=picire.iterator.CombinedIterator(
            False, picire.iterator.skip,
            picire.iterator.random
        )
    )
    output_contracts = [x for x in dd_obj_functions(contract_nodes)]

    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")


if __name__ == "__main__":
    main()
