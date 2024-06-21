import os
import re
import string
import random
import subprocess
import argparse
import tempfile
import networkx as nx
import picire
from antlr4 import *
from SolidityLexer import SolidityLexer
from SolidityParser import SolidityParser
from SolidityListener import SolidityListener

# Argument parsing
parser = argparse.ArgumentParser(description='Modify Solidity files based on node removal and Slither analysis, considering specified findings.')
parser.add_argument('--consider', type=str, help='Findings to consider in the format "finding=threshold"', default="")
parser.add_argument('--mode', type=str, choices=['functions', 'contracts'], help='Mode of operation: functions or contracts', required=True)
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
        self.replacements = []
        self.nodes_to_remove = nodes_to_remove

    def enterFunctionDefinition(self, ctx: SolidityParser.FunctionDefinitionContext):
        functions_name = ctx.getChild(0).getText()
        function_name = functions_name.replace("function", "")
        if function_name in self.nodes_to_remove:
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterModifierInvocation(self, ctx: SolidityParser.ModifierInvocationContext):
        if ctx.getChild(0).getText() in self.nodes_to_remove:
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterModifierDefinition(self, ctx: SolidityParser.ModifierDefinitionContext):
        self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterExpressionStatement(self, ctx: SolidityParser.ExpressionStatementContext):
        text = ctx.getText()
        if any(node + "(" in text for node in self.nodes_to_remove):
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
        if any(node + "(" in text for node in self.nodes_to_remove):
            equal_sign_index = text.find('=')
            if equal_sign_index != -1:
                start = ctx.start.start + equal_sign_index + 1
                stop = ctx.stop.stop
                if stop < ctx.stop.stop and text[stop - ctx.start.start] == ';':
                    stop += 1
                stop -= 1
                self.removals.append((start, stop))

class RemovalListener2(SolidityListener):
    def __init__(self, nodes_to_remove, inheritance_graph):
        super().__init__()
        self.removals = []
        self.replacements = []
        self.nodes_to_remove = nodes_to_remove
        self.inheritance_graph = inheritance_graph
        self.temp_graph = inheritance_graph.copy()
        print(f"Nodes to remove: {self.nodes_to_remove}")

    def enterContractDefinition(self, ctx: SolidityParser.ContractDefinitionContext):
        contract_type = ctx.getChild(0).getText()

        # Find the identifier in the children
        identifier = None
        for i in range(ctx.getChildCount()):
            if isinstance(ctx.getChild(i), SolidityParser.IdentifierContext):
                identifier = ctx.getChild(i).getText()
                break

        if identifier is None:
            print("Identifier not found in contract definition context")
            return

        print(f"Entering contract definition: {identifier}")
        if identifier in self.nodes_to_remove:
            self.removals.append((ctx.start.start, ctx.stop.stop))
            print(f"Marked for removal: contract {identifier}")
            parents = list(self.temp_graph.predecessors(identifier))
            children = list(self.temp_graph.successors(identifier))
            for child in children:
                self.temp_graph.remove_edge(identifier, child)
                for parent in parents:
                    self.temp_graph.add_edge(parent, child)
        else:
            if ctx.inheritanceSpecifier():
                inheritance_specifiers = ctx.inheritanceSpecifier()
                to_remove = []
                updated_inheritance = []
                for i, spec in enumerate(inheritance_specifiers):
                    spec_text = spec.getText()
                    if spec_text in self.nodes_to_remove:
                        print(f"Marked for removal: inheritance specifier {spec_text}")
                        if len(inheritance_specifiers) == 1:
                            to_remove.append((ctx.children[3].start.start - 3, spec.stop.stop))
                        else:
                            if i == 0:
                                to_remove.append((spec.start.start, inheritance_specifiers[i + 1].start.start - 2))
                            elif i == len(inheritance_specifiers) - 1:
                                to_remove.append((inheritance_specifiers[i - 1].stop.stop + 1, spec.stop.stop))
                            else:
                                to_remove.append((inheritance_specifiers[i - 1].stop.stop + 1, inheritance_specifiers[i + 1].start.start - 2))
                    else:
                        updated_inheritance.append(spec_text)
                if updated_inheritance:
                    updated_inheritance_text = ", ".join(updated_inheritance)
                    self.replacements.append((ctx.getChild(1).getText(), updated_inheritance_text))
                else:
                    self.removals.extend(to_remove)
            print(f"Current removals: {self.removals}")
            print(f"Current replacements: {self.replacements}")

    def exitSourceUnit(self, ctx: SolidityParser.SourceUnitContext):
        for identifier in self.temp_graph.nodes:
            parents = list(self.temp_graph.predecessors(identifier))
            if parents:
                new_inheritance_specifiers = ", ".join(parents)
                self.replacements.append((identifier, new_inheritance_specifiers))
        print(f"Final removals: {self.removals}")
        print(f"Final replacements: {self.replacements}")

def remove_with_antlr(source_code, tree, nodes_to_remove):
    listener = RemovalListener(nodes_to_remove)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    for start, stop in sorted(listener.removals, reverse=True):
        code_block = source_code[start:stop + 1]
        if any(node in code_block for node in nodes_to_remove):
            source_code = source_code[:start] + (len(code_block) * " ") + source_code[stop + 1:]
    source_code = source_code.replace(r"/\s\s+/g", ' ')
    return re.sub(r'\n\s*\n', '\n\n', source_code)

def remove_with_antlr2(source_code, nodes_to_remove, inheritance_graph):
    lexer = SolidityLexer(InputStream(source_code))
    stream = CommonTokenStream(lexer)
    parser = SolidityParser(stream)
    tree = parser.sourceUnit()

    listener = RemovalListener2(nodes_to_remove, inheritance_graph)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    for start, stop in sorted(listener.removals, reverse=True):
        print(f"Removing code block from {start} to {stop}")
        source_code = source_code[:start] + (len(source_code[start:stop + 1]) * " ") + source_code[stop + 1:]

    for identifier, new_inheritance_specifiers in listener.replacements:
        pattern = re.compile(rf"(\b{identifier}\b\s+is\s+)[^{{]*")
        replacement_text = f"{identifier} is {new_inheritance_specifiers}" if new_inheritance_specifiers else f"{identifier}"
        source_code = pattern.sub(replacement_text, source_code)
        print(f"Replacing inheritance for {identifier} with {new_inheritance_specifiers}")

    source_code = source_code.replace(r"/\s\s+/g", ' ')
    return re.sub(r'\n\s*\n', '\n\n', source_code)

class Interesting():
    def __init__(self, graph, content, findings, file_path, mode):
        self.graph = graph
        self.mode = mode
        self.content = content
        self.content_ = content
        self.original_findings = findings
        self.file_path = file_path
        self.cache = {}
        lexer = SolidityLexer(InputStream(content))
        stream = CommonTokenStream(lexer)
        parser = SolidityParser(stream)
        self.tree = parser.sourceUnit()

    def __call__(self, nodes, config_id):
        if self.mode == 'functions':
            nodes_to_remove = [n for n in self.graph.nodes() if n not in nodes]
            fr_nodes = frozenset(nodes)
            if fr_nodes in self.cache:
                return self.cache.get(fr_nodes)
            if not nodes_to_remove:
                return picire.Outcome.FAIL
            new_content = self.test_removing_functions(nodes_to_remove, self.content)
            if new_content is not None:
                self.content = new_content
                res = picire.Outcome.FAIL
            else:
                res = picire.Outcome.PASS
            self.cache[fr_nodes] = res
            return res
        if self.mode == 'contracts':
            nodes_to_remove = [n for n in self.graph.nodes() if n not in nodes]
            fr_nodes = frozenset(nodes)
            if fr_nodes in self.cache:
                return self.cache.get(fr_nodes)
            if not nodes_to_remove:
                return picire.Outcome.FAIL
            new_content = self.test_removing_contracts(nodes_to_remove, self.content)
            if new_content is not None:
                self.content = new_content
                res = picire.Outcome.FAIL
            else:
                res = picire.Outcome.PASS
            self.cache[fr_nodes] = res
            return res

    def test_removing_functions(self, nodes_to_remove, content):
        modified_content = content
        modified_content = remove_with_antlr(self.content_, self.tree, nodes_to_remove)
        name = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        temp_file_path = f"{name}.sol"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(modified_content)
        modified_slither_output = run_slither_analysis(temp_file_path)
        if modified_slither_output:
            modified_findings = parse_slither_findings(modified_slither_output, consider_findings)
            if compare_slither_outputs(self.original_findings, modified_findings, consider_findings):
                with open(self.file_path, 'w') as file:
                    file.write(modified_content)
                os.remove(temp_file_path)
                return modified_content
            else:
                os.remove(temp_file_path)
                return None
        else:
            os.remove(temp_file_path)
            return None

    def test_removing_contracts(self, nodes_to_remove, content):
        modified_content = content
        temp_graph = self.graph.copy()  # Create a temporary copy of the graph
        modified_content = remove_with_antlr2(self.content_, nodes_to_remove, temp_graph)
        name = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        temp_file_path = f"{name}.sol"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(modified_content)
        modified_slither_output = run_slither_analysis(temp_file_path)
        if modified_slither_output:
            modified_findings = parse_slither_findings(modified_slither_output, consider_findings)
            if compare_slither_outputs(self.original_findings, modified_findings, consider_findings):
                self.graph = temp_graph  # Commit the changes to the graph only if the removal is successful
                with open(self.file_path, 'w') as file:
                    file.write(modified_content)
                os.remove(temp_file_path)
                return modified_content
            else:
                os.remove(temp_file_path)
                return None
        else:
            os.remove(temp_file_path)
            return None

def parse_contracts(file_path):
    graph = nx.DiGraph()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if ' has children: ' in line:
                try:
                    parent_info, children_info = line.split(' has children: ')
                    parent = parent_info.split(' ')[2].strip()
                    children = children_info.split(', ')
                    graph.add_node(parent)
                    for child in children:
                        graph.add_node(child)
                        graph.add_edge(parent, child)
                except ValueError as e:
                    print(f"Error processing line: {line} - {e}")
            elif ' has no children' in line:
                try:
                    parent = line.split(' ')[2].strip()
                    graph.add_node(parent)
                except ValueError as e:
                    print(f"Error processing line: {line} - {e}")
    return graph

def parse_nodes(file_path):
    graph = nx.DiGraph()
    with open(file_path, 'r') as file:
        for line in file:
            node_info, edges_info = line.split(' has ')
            node = node_info.strip()
            graph.add_node(node)
            edges_parts = edges_info.split(' - ')
            outbound_info = edges_parts[1].split(': ')[1]
            inbound_info = edges_parts[2].split(': ')[1]
            outbound_edges = outbound_info.strip()[1:-1].split(', ')
            inbound_edges = inbound_info.strip()[1:-1].split(', ')
            if outbound_edges == ['None']:
                outbound_edges = []
            if inbound_edges == ['None']:
                inbound_edges = []
            for target in outbound_edges:
                if target is None or target == "None":
                    continue
                graph.add_node(target)
                graph.add_edge(node, target)
            for target in inbound_edges:
                if target is None or target == "None":
                    continue
                graph.add_node(target)
                graph.add_edge(target, node)
    return graph

def parse_inherit(file_path):
    graph = nx.DiGraph()
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if ' has children: ' in line:
                try:
                    parent_info, children_info = line.split(' has children: ')
                    parent = parent_info.split(' ')[2].strip()
                    children = children_info.split(', ')
                    graph.add_node(parent)
                    for child in children:
                        graph.add_node(child)
                        graph.add_edge(parent, child)
                except ValueError as e:
                    print(f"Error processing line: {line} - {e}")
            elif ' has no children' in line:
                try:
                    parent = line.split(' ')[2].strip()
                    graph.add_node(parent)
                except ValueError as e:
                    print(f"Error processing line: {line} - {e}")
    return graph

def main():
    mode = args.mode
    nodes_file_path = 'nodes.txt'
    sol_file_path = 'ext_changed.sol'
    inherit_file_path = 'inheritance.txt'
    original_slither_output = run_slither_analysis(sol_file_path)
    original_findings = parse_slither_findings(original_slither_output, consider_findings) if original_slither_output else {}
    with open(sol_file_path, 'r') as file:
        original_content = file.read()
    if mode == 'functions':
        graph = parse_nodes(nodes_file_path)
        interesting = Interesting(graph, original_content, original_findings, sol_file_path, mode)
        nodes = list(graph.nodes())
        dd_obj = picire.ParallelDD(interesting,
                                   split=picire.splitter.ZellerSplit(n=4),
                                   cache=picire.cache.ConfigCache(),
                                   config_iterator=picire.iterator.CombinedIterator(
                                       False, picire.iterator.skip,
                                       picire.iterator.random))
        output = [x for x in dd_obj(nodes)]
    if mode == 'contracts':
        graph = parse_inherit(inherit_file_path)
        interesting = Interesting(graph, original_content, original_findings, sol_file_path, mode)
        nodes = list(graph.nodes())
        dd_obj = picire.DD(interesting,
                           split=picire.splitter.ZellerSplit(n=4),
                           cache=picire.cache.ConfigCache(),
                           config_iterator=picire.iterator.CombinedIterator(
                               False, picire.iterator.skip,
                               picire.iterator.random))
        output = [x for x in dd_obj(nodes)]
        print("KOUKA")

if __name__ == "__main__":
    main()
