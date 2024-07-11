import argparse
import time

import matplotlib.pyplot as plt
import networkx as nx

from reducer import utils
from reducer.dd import Interesting, perform_dd
from reducer.checker import PROPERTY_CHECKERS
from reducer.graph import build_graph_from_file


# Argument parsing
parser = argparse.ArgumentParser(
    description=('Modify Solidity files based on node removal and '
                 "Slither analysis, considering specified findings.")
)

parser.add_argument(
    "--language",
    default="solidity",
    choices=['solidity', 'c'],
    help="Select specific language (options: 'solidity', 'c')"
)

parser.add_argument(
    "--source-file",
    type=str,
    default="ext_changed.sol",
    help="Source file to minimize",
)
parser.add_argument(
    '--consider',
    type=str,
    help='Findings to consider in the format "finding=threshold"',
    default=""
)
parser.add_argument(
    '--script',
    type=str,
    help='script to run"',
    default="./solidity2.sh"
)
args = parser.parse_args()


def main():
    # Convert consider string to a dictionary
    if args.consider:
        key, value = args.consider.split('=')
        patterns = {key: int(value)}
    else:
        patterns = {}

    start_time = time.time()
    file_path = args.source_file
    print(f"Using source file: {file_path}")

    graph = build_graph_from_file(file_path, args.language)
    print(f"Graph built from file: {file_path}")
    print(graph)
    
#    def print_nodes_with_label(graph, label):
#        nodes = [node for node in graph.nodes()
#                 if node.node_type == label]
#        print(f"Nodes with label '{label}':")
#        print(nodes)
#        print()

#    def print_edges_with_label(graph):
#        edges = graph.edges(data=True)
#        print("Edges with labels:")
#        for edge in edges:
#            source = edge[0]
#            target = edge[1]
#            label = edge[2]['label']
#            print(f"({source}) -> ({target}): {label}")
#        print()

#    print_nodes_with_label(graph, 'function')
#    print_nodes_with_label(graph, 'var')
##    print_nodes_with_label(graph, 'typedef')
#    print_nodes_with_label(graph, 'struct')
#    
#    print_edges_with_label(graph)
#    
#    # Draw and display the graph
#    plt.figure(figsize=(12, 8))
#    pos = nx.spring_layout(graph, seed=42)  # Positions for all nodes

#    # Nodes
#    node_labels = {node: node for node in graph.nodes()}
#    node_colors = {'function': 'lightgreen', 'var': 'yellow', 'struct':'red'}
#    node_shapes = {'function': 'o', 'var': 'o', 'struct': 'o'}

#    for label in node_colors:
#        nx.draw_networkx_nodes(graph, pos, nodelist=[node for node in graph.nodes() if node.node_type == label],
#                               node_color=node_colors[label], node_shape=node_shapes[label], label=label, node_size=500)

#    # Edges
#    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), arrows=True)

#    # Labels
#    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=8, font_color='black')

#    # Edge labels
#    edge_labels = {(edge[0], edge[1]): edge[2]['label'] for edge in graph.edges(data=True)}
#    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red', font_size=4)

#    plt.title('C Dependency Graph')
#    plt.legend()
#    plt.axis('off')
#    plt.show()


    prop_checker = PROPERTY_CHECKERS[args.language](file_path, patterns,
                                                    "slither", args.script)
    original_content = utils.read_file(file_path)

    interesting = Interesting(graph, original_content,
                              prop_checker, args.language)
    passes = [
        ["function"], ["contract"],
        ["event", "state_var", "struct"]
    ]
    for pass_ in passes:
        interesting.mode = pass_
        perform_dd(interesting, lambda n: n.node_type in pass_,
                   parallel=True)

    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")


if __name__ == "__main__":
    main()

