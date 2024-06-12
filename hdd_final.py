import os
import re
import subprocess
import argparse
from itertools import groupby
from antlr4 import *
from SolidityLexer import SolidityLexer
from SolidityParser import SolidityParser
from SolidityListener import SolidityListener

# Setup command-line argument parsing
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

# ANTLR listener for removing contract, function, and modifier definitions
class RemovalListener(SolidityListener):
    def __init__(self, nodes_to_remove):
        super().__init__()
        self.removals = []
        self.nodes_to_remove = nodes_to_remove

    def enterFunctionDefinition(self, ctx):
        func_name = ctx.children[0].getText()  # Extracting the function name from the correct position
        func_name = re.sub(r'^function\s*', '', func_name)  # Remove the 'function' prefix using regex
        if func_name in self.nodes_to_remove:
            self.removals.append((ctx.start.start, ctx.stop.stop))
    
    def enterModifierDefinition(self, ctx):
        mod_name = ctx.children[1].getText()  # Extracting the modifier name from the correct position
        if mod_name in self.nodes_to_remove:
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterContractDefinition(self, ctx):
        contract_name = ctx.identifier().getText()
        if contract_name in self.nodes_to_remove:
            self.removals.append((ctx.start.start, ctx.stop.stop))

class OutcomeCache:
    def __init__(self):
        self.tail = {}  # Points to outcome of tail
        self.result = None  # Result so far

    def add(self, c, result):
        """Add (C, RESULT) to the cache. C must be a list of scalars."""
        cs = c[:]
        cs.sort()
        p = self
        for start in range(len(c)):
            if c[start] not in p.tail:
                p.tail[c[start]] = OutcomeCache()
            p = p.tail[c[start]]
        p.result = result

    def lookup(self, c):
        """Return RESULT if (C, RESULT) is in the cache; None otherwise."""
        p = self
        for start in range(len(c)):
            if c[start] not in p.tail:
                return None
            p = p.tail[c[start]]
        return p.result

    def lookup_superset(self, c, start=0):
        """Return RESULT if there is some (C', RESULT) in the cache with
        C' being a superset of C or equal to C. Otherwise, return None."""
        if start >= len(c):
            if self.result:
                return self.result
            elif self.tail != {}:
                superset = self.tail[next(iter(self.tail))]
                return superset.lookup_superset(c, start + 1)
            else:
                return None
        if c[start] in self.tail:
            return self.tail[c[start]].lookup_superset(c, start + 1)
        return None

    def lookup_subset(self, c):
        """Return RESULT if there is some (C', RESULT) in the cache with
        C' being a subset of C or equal to C. Otherwise, return None."""
        p = self
        for start in range(len(c)):
            if c[start] in p.tail:
                p = p.tail[c[start]]
        return p.result

class DeltaDebugger:
    PASS = "PASS"
    FAIL = "FAIL"
    UNRESOLVED = "UNRESOLVED"
    ADD = "ADD"
    REMOVE = "REMOVE"
    
    def __init__(self):
        self.outcome_cache = OutcomeCache()
        self.verbose = 1
        self.cache_outcomes = 1

    def run_slither_analysis(self, file_path):
        command = ["slither", file_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            return result.stderr
        except subprocess.CalledProcessError as e:
            print("Slither analysis failed.")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Return Code: {e.returncode}")
            print(f"Error Output: {e.stderr}")
            return None

    def parse_slither_findings(self, slither_output, consider_findings):
        findings = {}
        for key in consider_findings.keys():
            pattern = re.compile(re.escape(key))
            findings_count = sum(1 for _ in pattern.findall(slither_output))
            if findings_count > 0:
                findings[key] = findings_count
        return findings

    def compare_slither_outputs(self, original_findings, modified_findings, consider_findings):
        for finding, threshold in consider_findings.items():
            original_count = original_findings.get(finding, 0)
            modified_count = modified_findings.get(finding, 0)
            if original_count != modified_count or original_count > threshold or modified_count > threshold:
                return False
        return True

    def remove_with_antlr(self, source_code, nodes_to_remove):
        lexer = SolidityLexer(InputStream(source_code))
        stream = CommonTokenStream(lexer)
        parser = SolidityParser(stream)
        tree = parser.sourceUnit()

        listener = RemovalListener(nodes_to_remove)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        # Remove code blocks in reverse order to avoid shifting indices
        for start, stop in sorted(listener.removals, reverse=True):
            source_code = source_code[:start] + source_code[stop+1:]

        # Additional step to remove leftover newlines and spaces
        source_code = re.sub(r'\n\s*\n', '\n', source_code).strip()

        # Ensure the source code is still syntactically correct
        try:
            lexer = SolidityLexer(InputStream(source_code))
            stream = CommonTokenStream(lexer)
            parser = SolidityParser(stream)
            parser.sourceUnit()
            # If parsing is successful, return the modified source code
            print("Validation of modified Solidity code successful.")
            return source_code
        except Exception as e:
            print(f"Validation failed after modification: {e}")
            return None

    def process_node(self, graph, node, sol_file_path, original_findings, processed_nodes):
        if node in processed_nodes:
            return False

        with open(sol_file_path, 'r') as file:
            original_content = file.read()

        modified_content = original_content
        processed_nodes.add(node)  # Mark node as processed

        for outbound in graph[node]['outbound']:
            if outbound == 'None':
                continue

            if outbound not in processed_nodes:
                processed_nodes.add(outbound)
                modified_content = self.remove_with_antlr(modified_content, {outbound})

            if graph[outbound]['inbound'] and graph[outbound]['inbound'] != ['None']:
                for inbound in graph[outbound]['inbound']:
                    if inbound not in processed_nodes and inbound != 'None':
                        processed_nodes.add(inbound)
                        modified_content = self.remove_with_antlr(modified_content, {inbound})

        if node not in processed_nodes and node != 'None':
            processed_nodes.add(node)
            modified_content = self.remove_with_antlr(modified_content, {node})

        temp_file_path = "temp_sol_file.sol"
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(modified_content)

        modified_slither_output = self.run_slither_analysis(temp_file_path)
        if modified_slither_output:
            modified_findings = self.parse_slither_findings(modified_slither_output, consider_findings)
            if self.compare_slither_outputs(original_findings, modified_findings, consider_findings):
                with open(sol_file_path, 'w') as file:
                    file.write(modified_content)
                os.remove(temp_file_path)  # Clean up the temporary file
                return True

        os.remove(temp_file_path)  # Clean up the temporary file
        return False

    def process_nodes(self, nodes, graph, sol_file_path, original_findings, processed_nodes):
        any_processed = False
        for node in nodes:
            result = self.process_node(graph, node, sol_file_path, original_findings, processed_nodes)
            if result:
                any_processed = True
        return any_processed

    def split(self, c, n):
        subsets = []
        start = 0
        for i in range(n):
            subset = c[start:int(start + (len(c) - start) / (n - i))]
            subsets.append(subset)
            start = start + len(subset)
        return subsets

    def delta_debugging(self, nodes, graph, sol_file_path, original_findings, processed_nodes):
        n = 2
        while len(nodes) >= 2:
            subsets = self.split(nodes, n)
            print(f"Delta Debugging: Processing subsets {subsets}")
            for subset in subsets:
                if not subset:
                    continue
                result = self.process_nodes(subset, graph, sol_file_path, original_findings, processed_nodes)
                if result:
                    nodes = subset
                    break
            else:
                if n >= len(nodes):
                    break
                n = min(len(nodes), n * 2)
        return nodes

    def remove_isolated_nodes(self, graph, sol_file_path, original_findings, processed_nodes):
        isolated_nodes = [node for node in graph if not graph[node]['inbound'] and not graph[node]['outbound']]
        any_processed = False

        for node in isolated_nodes:
            if node in processed_nodes:
                continue
            with open(sol_file_path, 'r') as file:
                original_content = file.read()

            modified_content = self.remove_with_antlr(original_content, {node})

            temp_file_path = "temp_sol_file.sol"
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write(modified_content)

            modified_slither_output = self.run_slither_analysis(temp_file_path)
            if modified_slither_output:
                modified_findings = self.parse_slither_findings(modified_slither_output, consider_findings)
                if self.compare_slither_outputs(original_findings, modified_findings, consider_findings):
                    with open(sol_file_path, 'w') as file:
                        file.write(modified_content)
                    any_processed = True
                    processed_nodes.add(node)  # Mark node as processed
                    del graph[node]  # Remove the node from the graph
            os.remove(temp_file_path)  # Clean up the temporary file
        return any_processed

def parse_nodes(file_path):
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

    debugger = DeltaDebugger()

    original_slither_output = debugger.run_slither_analysis(sol_file_path)
    original_findings = debugger.parse_slither_findings(original_slither_output, consider_findings) if original_slither_output else {}

    processed_nodes = set()

    grouped_nodes = {k: list(v) for k, v in groupby(
        sorted(graph.keys(), key=lambda x: len(graph[x]['inbound']) if graph[x]['inbound'] else 0),
        key=lambda x: len(graph[x]['inbound']) if graph[x]['inbound'] else 0
    )}

    # Process isolated nodes first
    isolated_nodes_processed = debugger.remove_isolated_nodes(graph, sol_file_path, original_findings, processed_nodes)
    if isolated_nodes_processed:
        print("Isolated nodes processed and removed successfully.")

    # Process remaining nodes
    for inbound_count in sorted(grouped_nodes.keys()):
        nodes_to_process = grouped_nodes[inbound_count]
        if nodes_to_process:
            all_nodes_processed = debugger.delta_debugging(nodes_to_process, graph, sol_file_path, original_findings, processed_nodes)
            print(f"All nodes processed in current group through delta debugging: {all_nodes_processed}")

if __name__ == "__main__":
    main()

