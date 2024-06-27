import re
from antlr4 import *
from SolidityLexer import SolidityLexer
from SolidityParser import SolidityParser
from SolidityListener import SolidityListener
import networkx as nx
import matplotlib.pyplot as plt

class SolidityGraphListener(SolidityListener):
    def __init__(self):
        super().__init__()
        self.graph = nx.DiGraph()
        self.contract_counter = 0
        self.function_counter = 0
        self.state_variable_counter = 0
        self.local_variable_counter = 0
        self.current_contract = None
        self.current_function = None

    def enterContractDefinition(self, ctx: SolidityParser.ContractDefinitionContext):
        contract_name = ctx.getChild(1).getText()
        self.graph.add_node(contract_name, label='contract')
        self.current_contract = contract_name
        self.contract_counter += 1

        # Handle multiple inheritance specifiers
        if ctx.inheritanceSpecifier():
            inheritance_specifiers = ctx.inheritanceSpecifier()
            for spec in inheritance_specifiers:
                parent_contract_name = spec.userDefinedTypeName().getText()
                if parent_contract_name != self.current_contract:
                    self.add_inherits_edge(parent_contract_name)

    def add_inherits_edge(self, parent_contract_name):
        if not self.graph.has_edge(self.current_contract, parent_contract_name):
            self.graph.add_edge(self.current_contract, parent_contract_name, label='inherits')

    def enterFunctionDefinition(self, ctx: SolidityParser.FunctionDefinitionContext):
        functions_name = ctx.getChild(0).getText()
        function_name = functions_name.replace("function", "").strip()
        unique_function_name = f"{self.current_contract}.{function_name}"
        self.graph.add_node(unique_function_name, label='function')
        self.graph.add_edge(self.current_contract, unique_function_name, label='defines_function')
        self.current_function = unique_function_name
        self.function_counter += 1

    def enterEventDefinition(self, ctx: SolidityParser.EventDefinitionContext):
        event_name = ctx.identifier().getText()
        self.graph.add_node(event_name, label='event')
        self.graph.add_edge(self.current_contract, event_name, label='defines_event')

    def enterEmitStatement(self, ctx: SolidityParser.EmitStatementContext):
        emit_statement = ctx.functionCall().getText()
        unique_emit_statement = f"{self.current_function}.{emit_statement}"
        self.graph.add_node(unique_emit_statement, label='emit')
        self.graph.add_edge(self.current_function, unique_emit_statement, label='defines_emit')

    def enterStructDefinition(self, ctx: SolidityParser.StructDefinitionContext):
        struct_name = ctx.identifier().getText()
        self.graph.add_node(struct_name, label='struct')
        self.graph.add_edge(self.current_contract, struct_name, label='defines_struct')

        # Handle struct members
        member_declarations = ctx.variableDeclaration()
        for member_decl in member_declarations:
            member_name = member_decl.identifier().getText()
            unique_member_name = f"{struct_name}.{member_name}"
            self.graph.add_node(unique_member_name, label='struct_member')
            self.graph.add_edge(struct_name, unique_member_name, label='defines_struct_member')

    def enterStateVariableDeclaration(self, ctx: SolidityParser.StateVariableDeclarationContext):
        identifier_token = ctx.identifier()
        var_name = identifier_token.getText()
        self.graph.add_node(var_name, label='state_variable')
        self.graph.add_edge(self.current_contract, var_name, label='defines_state_variable')
        self.state_variable_counter += 1

    def enterVariableDeclaration(self, ctx: SolidityParser.VariableDeclarationContext):
        if self.current_function:
            # Check if the variable declaration is directly nested within a struct
            parent_ctx = ctx.parentCtx
            if isinstance(parent_ctx, SolidityParser.StructDefinitionContext):
                # If parent context is StructDefinitionContext, skip adding as local_variable
                return
        
            local_var_name = ctx.getChild(1).getText()
            unique_local_var_name = f"{self.current_function}.{local_var_name}"
            self.graph.add_node(unique_local_var_name, label='local_variable')
            self.graph.add_edge(self.current_function, unique_local_var_name, label='defines_local_variable')
            self.local_variable_counter += 1


def build_graph_from_file(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()

    lexer = SolidityLexer(InputStream(source_code))
    stream = CommonTokenStream(lexer)
    parser = SolidityParser(stream)
    tree = parser.sourceUnit()

    listener = SolidityGraphListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    return listener.graph

if __name__ == '__main__':
    file_path = 'ext_changed.sol'
    graph = build_graph_from_file(file_path)
    
    # Print nodes with specific labels
    def print_nodes_with_label(graph, label):
        nodes = [node for node, data in graph.nodes(data=True) if data['label'] == label]
        print(f"Nodes with label '{label}':")
        print(nodes)
        print()

    def print_edges_with_label(graph):
        edges = graph.edges(data=True)
        print("Edges with labels:")
        for edge in edges:
            source = edge[0]
            target = edge[1]
            label = edge[2]['label']
            print(f"({source}) -> ({target}): {label}")
        print()

    print_nodes_with_label(graph, 'contract')
    print_nodes_with_label(graph, 'function')
    print_nodes_with_label(graph, 'event')
    print_nodes_with_label(graph, 'emit')
    print_nodes_with_label(graph, 'struct')
    print_nodes_with_label(graph, 'struct_member')
    print_nodes_with_label(graph, 'state_variable')
    print_nodes_with_label(graph, 'local_variable')
    
    # Print edges with labels
    print_edges_with_label(graph)
    
    # Draw and display the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)  # Positions for all nodes

    # Nodes
    node_labels = {node: node for node in graph.nodes()}
    node_colors = {'contract': 'lightblue', 'function': 'lightgreen', 'event': 'lightcoral',
                   'emit': 'lightyellow', 'struct': 'lightgrey', 'struct_member': 'lightgrey',
                   'state_variable': 'lightpink', 'local_variable': 'lightsalmon'}
    node_shapes = {'contract': 'o', 'function': 'o', 'event': 'o',
                   'emit': 'o', 'struct': 's', 'struct_member': 'o',
                   'state_variable': 'o', 'local_variable': 'o'}
    
    for label in node_colors:
        nx.draw_networkx_nodes(graph, pos, nodelist=[node for node, data in graph.nodes(data=True) if data['label'] == label],
                               node_color=node_colors[label], node_shape=node_shapes[label], label=label, node_size=500)

    # Edges
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), arrows=True)

    # Labels
    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=8, font_color='black')

    # Edge labels
    edge_labels = {(edge[0], edge[1]): edge[2]['label'] for edge in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red', font_size=4)

    plt.title('Solidity Contract Dependency Graph')
    plt.legend()
    plt.axis('off')
    plt.show()

