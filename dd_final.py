import os
import re
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
args = parser.parse_args()

# Convert consider string to a dictionary
if args.consider:
    key, value = args.consider.split('=')
    consider_findings = {key: int(value)}
else:
    consider_findings = {}

print("Considered findings for thresholds:", consider_findings)

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
    print("COMPARISONS")
    print(f"Original findings: {original_findings}")
    print(f"Modified findings: {modified_findings}")
    for finding, threshold in consider_findings.items():
        original_count = original_findings.get(finding, 0)
        modified_count = modified_findings.get(finding, 0)
        if original_count != modified_count or original_count > threshold or modified_count > threshold:
            print("Findings do not match criteria. Not replacing the original file.")
            return False
    print("Findings match criteria. Replacing the original file.")
    return True

# ANTLR listener for removing contract and function definitions
class RemovalListener(SolidityListener):
    def __init__(self, nodes_to_remove):
        super().__init__()
        self.removals = []
        self.replacements = []
        self.nodes_to_remove = nodes_to_remove


    def enterFunctionDefinition(self, ctx: SolidityParser.FunctionDefinitionContext):
        functions_name = ctx.getChild(0).getText()  # Extract the function name from the context
        function_name = functions_name.replace("function","")
        if function_name in self.nodes_to_remove:
            print(f"Attempting to remove node: {function_name}")
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

                # Ensure we include the semicolon if it is within the range
                if stop < ctx.stop.stop and text[stop - ctx.start.start] == ';':
                    stop += 1
                # Add removal range
                stop -= 1
                self.removals.append((start, stop))
                print(f"Removing code from {start} to {stop}")
            else:
                self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterVariableDeclarationStatement(self, ctx: SolidityParser.VariableDeclarationStatementContext):
        text = ctx.getText()
        if any(node + "(" in text for node in self.nodes_to_remove):
            equal_sign_index = text.find('=')
            if equal_sign_index != -1:
                start = ctx.start.start + equal_sign_index + 1
                stop = ctx.stop.stop

                # Ensure we include the semicolon if it is within the range
                if stop < ctx.stop.stop and text[stop - ctx.start.start] == ';':
                    stop += 1
                # Add removal range
                stop -= 1
                self.removals.append((start, stop))
                print(f"Removing code from {start} to {stop}")


def remove_with_antlr(source_code, nodes_to_remove):
    lexer = SolidityLexer(InputStream(source_code))
    stream = CommonTokenStream(lexer)
    parser = SolidityParser(stream)
    tree = parser.sourceUnit()

    listener = RemovalListener(nodes_to_remove)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    # Remove code blocks in reverse order to avoid shifting indices
    for start, stop in sorted(listener.removals, reverse=True):
        # Check if the identified block corresponds to a node we want to remove
        code_block = source_code[start:stop+1]
        # Assuming nodes_to_remove are names of functions or contracts
#        print(source_code[:start] + source_code[stop+1:])
        if any(node in code_block for node in nodes_to_remove):
            print(source_code[start:stop+1])
            source_code = source_code[:start] + (len(code_block) * " ") + source_code[stop+1:]
        # Remove code blocks in reverse order to avoid shifting indices

    source_code = source_code.replace(r"/\s\s+/g", ' ');
    return re.sub(r'\n\s*\n', '\n\n', source_code)


class Interesting():
    def __init__(self, graph, content, findings, file_path):
        self.graph = graph
        self.content = content
        self.original_findings = findings
        self.file_path = file_path

    def __call__(self, nodes, config_id):
        nodes_to_remove = [n for n in self.graph.nodes() if n not in nodes]
        print("NODES TO REMOVE ", nodes_to_remove)
        if not nodes_to_remove:
            return picire.Outcome.FAIL
        new_content = self.test_removing_functions(nodes_to_remove,
                                                   self.content)
        if new_content is not None:
            self.content = new_content
            return picire.Outcome.FAIL
        else:
            return picire.Outcome.PASS

    def test_removing_functions(self, nodes_to_remove, content):
        modified_content = content
        modified_content = remove_with_antlr(modified_content, nodes_to_remove)

        # Write the modified content to a temporary file for Slither analysis
        temp_file_path = "temp_sol_file.sol"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(modified_content)

        # Run Slither on the modified content
        print(f"Running Slither for nodes: {nodes_to_remove}")
        modified_slither_output = run_slither_analysis(temp_file_path)
        if modified_slither_output:
            modified_findings = parse_slither_findings(modified_slither_output, consider_findings)
            print(f"Original findings: {self.original_findings}")
            print(f"Modified findings: {modified_findings}")
            if compare_slither_outputs(self.original_findings,
                                       modified_findings, consider_findings):
                print(f"Slither analysis passed for nodes {nodes_to_remove}. Writing changes.")
                with open(self.file_path, 'w') as file:
                    file.write(modified_content)
                os.remove(temp_file_path)  # Clean up the temporary file
                return modified_content
            else:
                print(f"Modifications for nodes {nodes_to_remove} did not meet criteria and were not applied.")
                return None
        else:
            print(f"Slither analysis failed for nodes {nodes_to_remove}. No changes made.")
            return None



def parse_nodes(file_path):
    """Parses a file to build a graph of nodes with their inbound and outbound connections."""
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
            if outbound_edges == ['None']: outbound_edges = []
            if inbound_edges == ['None']: inbound_edges = []

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



def main():
    nodes_file_path = 'nodes.txt'
    sol_file_path = 'ext_changed.sol'
    graph = parse_nodes(nodes_file_path)

    # Run initial Slither analysis to get the original findings
    original_slither_output = run_slither_analysis(sol_file_path)
    original_findings = parse_slither_findings(original_slither_output, consider_findings) if original_slither_output else {}
    with open(sol_file_path, 'r') as file:
        original_content = file.read()

    interesting = Interesting(graph, original_content, original_findings,
                              sol_file_path)
    nodes = list(graph.nodes())
    dd_obj = picire.DD(interesting,
                       split=picire.splitter.ZellerSplit(n=4),
                       cache=picire.cache.ConfigCache(),
                       config_iterator=picire.iterator.CombinedIterator(
                           True, picire.iterator.forward,
                           picire.iterator.backward))
    output = [x for x in dd_obj(nodes)]

    # Process each node based on the defined steps
    #ddcall = DDCallGraph(original_findings, sol_file_path)
    #ddcall.process_input(graph)


if __name__ == "__main__":
    main()
