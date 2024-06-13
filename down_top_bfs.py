import os
import re
import subprocess
import argparse
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
        print(self.nodes_to_remove)


    def enterFunctionDefinition(self, ctx: SolidityParser.FunctionDefinitionContext):
        functions_name = ctx.getChild(0).getText()  # Extract the function name from the context
        function_name = functions_name.replace("function","")
#        print(function_name)
        if function_name in self.nodes_to_remove:
            print(f"Attempting to remove node: {function_name}")
            self.removals.append((ctx.start.start, ctx.stop.stop))
       
    def enterModifierDefinition(self, ctx: SolidityParser.ModifierDefinitionContext):
        self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterExpressionStatement(self, ctx: SolidityParser.ExpressionStatementContext):
        text = ctx.getText()
        if any(node in text for node in self.nodes_to_remove):
            print("EXPRESSION FOUUUND")
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterVariableDeclarationStatement(self, ctx: SolidityParser.VariableDeclarationStatementContext):
        text = ctx.getText()
        if any(node in text for node in self.nodes_to_remove):
            equal_sign_index = text.find('=')
            print("VARIABLE DECLERATIONNNN")
            print(text)
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
    print("KOUUUUUUUUUUUUUUUUU")
    # Remove code blocks in reverse order to avoid shifting indices
    for start, stop in sorted(listener.removals, reverse=True):
        # Check if the identified block corresponds to a node we want to remove
        code_block = source_code[start:stop]
        # Assuming nodes_to_remove are names of functions or contracts
#        print(source_code[:start] + source_code[stop+1:])
        if any(node in code_block for node in nodes_to_remove):
            print(source_code[start:stop+1])
            source_code = source_code[:start] + source_code[stop+1:]
        # Remove code blocks in reverse order to avoid shifting indices
        
    return source_code

def process_node(graph, node, sol_file_path, original_findings, processed_nodes):
    """Process a node based on its connections and attempt removal if isolated."""
    with open(sol_file_path, 'r') as file:
        original_content = file.read()

    modified_content = original_content  # Start with original content for modifications
    processed_nodes = set()  # Track nodes that have been processed to avoid duplication
   
    # Determine if the node is isolated
    if (not graph[node]['outbound'] or graph[node]['outbound'] == ['None']) and \
   (not graph[node]['inbound'] or graph[node]['inbound'] == ['None']):
        is_isolated = True
    elif graph[node]['outbound'] == ['transfer'] and (not graph[node]['inbound'] or graph[node]['inbound'] == ['None']):
        is_isolated = True
    elif graph[node]['outbound'] == ['push'] and (not graph[node]['inbound'] or graph[node]['inbound'] == ['None']):
        is_isolated = True
    else:
        is_isolated = False

    if is_isolated:
        nodes_to_remove = {node}
        print(f"Attempting to remove isolated node: {node}")
        modified_content = remove_with_antlr(modified_content, nodes_to_remove)

        # Write the modified content to a temporary file for Slither analysis
        temp_file_path = "temp_sol_file.sol"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(modified_content)

        # Run Slither on the modified content
        modified_slither_output = run_slither_analysis(temp_file_path)
        print(f"Running Slither for isolated node removal: {node}")
        if modified_slither_output:
            modified_findings = parse_slither_findings(modified_slither_output, consider_findings)
            print(f"Original findings: {original_findings}")
            print(f"Modified findings: {modified_findings}")
            if compare_slither_outputs(original_findings, modified_findings, consider_findings):
                print(f"Slither analysis passed for isolated node {node}. Writing changes.")
                with open(sol_file_path, 'w') as file:
                    file.write(modified_content)
                return True
        print(f"Slither analysis failed for isolated node {node}. No changes made.")
        os.remove(temp_file_path)  # Clean up the temporary file
        return False

    def collect_nodes_to_remove(start_node, graph, nodes_to_remove):
        """Recursively collect nodes to remove, including inbounds and their inbounds."""
        if start_node not in graph or start_node in nodes_to_remove:
            return
        nodes_to_remove.add(start_node)
        for inbound in graph[start_node]['inbound']:
            if inbound != 'None':
                nodes_to_remove.add(inbound)
                if inbound in graph and graph[inbound]['inbound'] and graph[inbound]['inbound'] != ['None']:
                    nodes_to_remove.update(graph[inbound]['inbound'])
#                collect_nodes_to_remove(inbound, graph, nodes_to_remove)

    for inbound in graph[node]['inbound']:
        if inbound == 'None':
            continue

        nodes_to_remove = set([node])
        collect_nodes_to_remove(inbound, graph, nodes_to_remove)

        for removal_node in nodes_to_remove:
            if removal_node not in processed_nodes and removal_node != 'None':  # Ensure each node is processed once
                processed_nodes.add(removal_node)
                print(f"Attempting to remove node: {removal_node}")
                modified_content = remove_with_antlr(modified_content, {removal_node})

        # Write the modified content to a temporary file for Slither analysis
        temp_file_path = "temp_sol_file.sol"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(modified_content)

        # Run Slither on the modified content
        print(f"Running Slither for nodes: {nodes_to_remove}")
        modified_slither_output = run_slither_analysis(temp_file_path)
        if modified_slither_output:
            modified_findings = parse_slither_findings(modified_slither_output, consider_findings)
            print(f"Original findings: {original_findings}")
            print(f"Modified findings: {modified_findings}")
            if compare_slither_outputs(original_findings, modified_findings, consider_findings):
                print(f"Slither analysis passed for nodes {nodes_to_remove}. Writing changes.")
                with open(sol_file_path, 'w') as file:
                    file.write(modified_content)
                os.remove(temp_file_path)  # Clean up the temporary file
                return True
            else:
                print(f"Modifications for nodes {nodes_to_remove} did not meet criteria and were not applied.")
        else:
            print(f"Slither analysis failed for nodes {nodes_to_remove}. No changes made.")

        os.remove(temp_file_path)  # Clean up the temporary file

    return False

def parse_nodes(file_path):
    """Parses a file to build a graph of nodes with their inbound and outbound connections."""
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            node_info, edges_info = line.split(' has ')
            node = node_info.strip()
            edges_parts = edges_info.split(' - ')
            outbound_info = edges_parts[1].split(': ')[1]
            inbound_info = edges_parts[2].split(': ')[1]

            outbound_edges = outbound_info.strip()[1:-1].split(', ')
            inbound_edges = inbound_info.strip()[1:-1].split(', ')
            if outbound_edges == ['None']: outbound_edges = []
            if inbound_edges == ['None']: inbound_edges = []

            graph[node] = {'outbound': outbound_edges, 'inbound': inbound_edges}
    return graph

def main():
    nodes_file_path = 'nodes.txt'
    sol_file_path = 'ext_changed.sol'
    graph = parse_nodes(nodes_file_path)

    # Run initial Slither analysis to get the original findings
    original_slither_output = run_slither_analysis(sol_file_path)
    original_findings = parse_slither_findings(original_slither_output, consider_findings) if original_slither_output else {}

    processed_nodes = set()

    # First, process isolated nodes
    for node in list(graph.keys()):  # Convert to list to avoid runtime modification issues
        if (not graph[node]['outbound'] or graph[node]['outbound'] == ['None']) and \
           (not graph[node]['inbound'] or graph[node]['inbound'] == ['None']):
            process_node(graph, node, sol_file_path, original_findings, processed_nodes)

    # Process remaining nodes
    for node in graph:
        process_node(graph, node, sol_file_path, original_findings, processed_nodes)

if __name__ == "__main__":
    main()

