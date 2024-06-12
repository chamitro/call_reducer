import pydot

def parse_dot_file(dot_file_path):
    """
    Parses a DOT file and extracts nodes and edges, accounting for subgraphs.
    """
    try:
        graphs = pydot.graph_from_dot_file(dot_file_path)
        if not graphs:
            print(f"No graphs found in {dot_file_path}")
            return None

        graph = graphs[0]
        edges_map = {}

        # Function to recursively extract nodes and edges
        def extract_nodes_and_edges(subgraph, edges_map):
            for edge in subgraph.get_edges():
                src = edge.get_source().strip('"')
                dst = edge.get_destination().strip('"')

                if src not in edges_map:
                    edges_map[src] = {"outbound": set(), "inbound": set()}
                if dst not in edges_map:
                    edges_map[dst] = {"outbound": set(), "inbound": set()}

                edges_map[src]["outbound"].add(dst)
                edges_map[dst]["inbound"].add(src)

            for node in subgraph.get_nodes():
                node_id = node.get_name().strip('"')
                if node_id and node_id not in edges_map:
                    edges_map[node_id] = {"outbound": set(), "inbound": set()}

            # Recursively process subgraphs
            for s in subgraph.get_subgraphs():
                extract_nodes_and_edges(s, edges_map)

        # Start extraction from the top-level graph
        extract_nodes_and_edges(graph, edges_map)

        return edges_map
    except Exception as e:
        print(f"Failed to read or parse DOT file {dot_file_path}: {e}")
        return None

def print_edges(edges_map, output_file):
    """
    Writes each node along with its outbound and inbound edges to a file in the specified format.
    """
    if not edges_map:
        output_file.write("No edges to display.\n")
        return
    for node, edges in edges_map.items():
        display_node = node.split('_', 1)[-1] if '_' in node else node
        formatted_outbound = [n.split('_', 1)[-1] if '_' in n else n for n in edges['outbound']]
        formatted_inbound = [n.split('_', 1)[-1] if '_' in n else n for n in edges['inbound']]

        total_edges = len(formatted_outbound) + len(formatted_inbound)
        outbound = ', '.join(formatted_outbound) if formatted_outbound else 'None'
        inbound = ', '.join(formatted_inbound) if formatted_inbound else 'None'
        
        output_file.write(f"{display_node} has {total_edges} edges - Outbound to: [{outbound}] - Inbound from: [{inbound}]\n")

# Path to the DOT file
dot_file_path = './ext_changed.sol.all_contracts.call-graph.dot'
edges_map = parse_dot_file(dot_file_path)

# Open a file to store the results
with open('nodes.txt', 'w') as output_file:
    if edges_map:
        print_edges(edges_map, output_file)

