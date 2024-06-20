import os
import re
import subprocess
import argparse
import tempfile
import networkx as nx
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
    def __init__(self, nodes_to_remove, inheritance_graph):
        super().__init__()
        self.removals = []
        self.replacements = []
        self.nodes_to_remove = nodes_to_remove
        self.inheritance_graph = inheritance_graph
        print(f"Nodes to remove: {self.nodes_to_remove}")

    def enterContractDefinition(self, ctx: SolidityParser.ContractDefinitionContext):
        contract_type = ctx.getChild(0).getText()
        identifier = ctx.identifier().getText()

        print(f"Entering contract definition: {identifier}")
        if identifier in self.nodes_to_remove:
            # Remove the entire contract definition if the contract is in nodes_to_remove
            self.removals.append((ctx.start.start, ctx.stop.stop))
            print(f"Marked for removal: contract {identifier}")
            # Update children to inherit from this contract's parents
            parents = list(self.inheritance_graph.predecessors(identifier))
            children = list(self.inheritance_graph.successors(identifier))
            for child in children:
                self.inheritance_graph.remove_edge(identifier, child)
                for parent in parents:
                    self.inheritance_graph.add_edge(parent, child)
        else:
            # Check and remove inheritance specifiers if they are in nodes_to_remove
            if ctx.inheritanceSpecifier():
                inheritance_specifiers = ctx.inheritanceSpecifier()
                to_remove = []
                updated_inheritance = []
                for i, spec in enumerate(inheritance_specifiers):
                    spec_text = spec.getText()
                    if spec_text in self.nodes_to_remove:
                        print(f"Marked for removal: inheritance specifier {spec_text}")
                        if len(inheritance_specifiers) == 1:
                            # Remove the entire "is inheritanceSpecifier"
                            print("removal for one specifier: ", ctx.children[3].getText())
                            to_remove.append((ctx.children[3].start.start-3, spec.stop.stop))
                        else:
                            if i == 0:
                                # Remove first inheritance specifier with comma
                                to_remove.append((spec.start.start, inheritance_specifiers[i + 1].start.start - 2))
                            elif i == len(inheritance_specifiers) - 1:
                                # Remove last inheritance specifier with preceding comma
                                to_remove.append((inheritance_specifiers[i - 1].stop.stop + 1, spec.stop.stop))
                            else:
                                # Remove middle inheritance specifier with surrounding commas
                                to_remove.append((inheritance_specifiers[i - 1].stop.stop + 1, inheritance_specifiers[i + 1].start.start - 2))
                    else:
                        updated_inheritance.append(spec_text)

                # Update inheritance if needed
                if updated_inheritance:
                    updated_inheritance_text = ", ".join(updated_inheritance)
                    self.replacements.append((ctx.identifier().getText(), updated_inheritance_text))
                else:
                    self.removals.extend(to_remove)
            print(f"Current removals: {self.removals}")
            print(f"Current replacements: {self.replacements}")

    def exitSourceUnit(self, ctx: SolidityParser.SourceUnitContext):
        # Update inheritance for remaining contracts
        for identifier in self.inheritance_graph.nodes:
            parents = list(self.inheritance_graph.predecessors(identifier))
            if parents:
                new_inheritance_specifiers = ", ".join(parents)
                self.replacements.append((identifier, new_inheritance_specifiers))
        print(f"Final removals: {self.removals}")
        print(f"Final replacements: {self.replacements}")

# Function to remove nodes using ANTLR
def remove_with_antlr(source_code, nodes_to_remove, inheritance_graph):
    lexer = SolidityLexer(InputStream(source_code))
    stream = CommonTokenStream(lexer)
    parser = SolidityParser(stream)
    tree = parser.sourceUnit()

    listener = RemovalListener(nodes_to_remove, inheritance_graph)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    # Remove code blocks in reverse order to avoid shifting indices
    for start, stop in sorted(listener.removals, reverse=True):
        print(f"Removing code block from {start} to {stop}")
        removals=list(listener.removals)
        print(removals)
        print(source_code[:start] + source_code[stop+1:])
        source_code = source_code[:start] + (len(source_code[start:stop+1]) * " ") + source_code[stop+1:]
#        print(source_code)

    # Apply replacements
    for identifier, new_inheritance_specifiers in listener.replacements:
        # Only replace the inheritance specifier part, not the entire contract definition
        pattern = re.compile(rf"(\b{identifier}\b\s+is\s+)[^{{]*")
        replacement_text = f"{identifier} is {new_inheritance_specifiers}" if new_inheritance_specifiers else f"{identifier}"
        source_code = pattern.sub(replacement_text, source_code)
        print(f"Replacing inheritance for {identifier} with {new_inheritance_specifiers}")

    source_code = source_code.replace(r"/\s\s+/g", ' ');
    return re.sub(r'\n\s*\n', '\n\n', source_code)

# Function to process each node
def process_node(graph, node, children, sol_file_path, original_findings, removed_nodes):
    if node in removed_nodes:
        return
    with open(sol_file_path, 'r') as file:
        original_content = file.read()

    modified_content = original_content  # Start with original content for modifications

    print(f"Attempting to remove node: {node}")
    modified_content = remove_with_antlr(modified_content, {node}, graph)

    # Write the modified content to a temporary file for Slither analysis
    temp_file_path = "temp_sol_file.sol"
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(modified_content)

    # Run Slither on the modified content
    modified_slither_output = run_slither_analysis(temp_file_path)
    print(f"Running Slither for node removal: {node}")
    if modified_slither_output:
        modified_findings = parse_slither_findings(modified_slither_output, consider_findings)
        print(f"Original findings: {original_findings}")
        print(f"Modified findings: {modified_findings}")
        if compare_slither_outputs(original_findings, modified_findings, consider_findings):
            print(f"Slither analysis passed for node {node}. Writing changes.")
            with open(sol_file_path, 'w') as file:
                file.write(modified_content)
            removed_nodes.add(node)
        else:
            print(f"Modifications for node {node} did not meet criteria and were not applied.")
    else:
        print(f"Slither analysis failed for node {node}. No changes made.")

    os.remove(temp_file_path)  # Clean up the temporary file

# Function to parse nodes from a file
def parse_nodes(file_path):
    """Parses a file to build a graph of contracts with their inheritance relationships."""
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

# Function to print nodes sorted by edges and process each node
def print_sorted_nodes_by_edges(graph, sol_file_path, original_findings, removed_nodes):
    nodes_with_edges = [(node, len(list(graph.successors(node)))) for node in graph.nodes]
    
    nodes_with_edges_sorted = sorted(nodes_with_edges, key=lambda x: x[1], reverse=True)
    
    for node, num_children in nodes_with_edges_sorted:
        children = list(graph.successors(node))
        print(node)
        print(f"Processing parent node {node} with children: {', '.join(children) if children else 'None'}")
        process_node(graph, node, children, sol_file_path, original_findings, removed_nodes)

file_path = 'inheritance.txt'
sol_file_path = 'ext_changed.sol'
original_slither_output = run_slither_analysis(sol_file_path)
original_findings = parse_slither_findings(original_slither_output, consider_findings) if original_slither_output else {}
removed_nodes = set()

inheritance_graph = parse_nodes(file_path)
print_sorted_nodes_by_edges(inheritance_graph, sol_file_path, original_findings, removed_nodes)

