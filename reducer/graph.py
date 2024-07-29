from typing import List, Optional, Any
import re

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
import networkx as nx

import matplotlib.pyplot as plt

from reducer import utils

from reducer.grammars.solidity.SolidityLexer import SolidityLexer
from reducer.grammars.solidity.SolidityParser import SolidityParser
from reducer.grammars.solidity.SolidityListener import SolidityListener

from reducer.grammars.c.CLexer import CLexer
from reducer.grammars.c.CParser import CParser
from reducer.grammars.c.CListener import CListener

class ASTNode:
    def __init__(self, name: str, node_type: str, parent: Optional['ASTNode'] = None):
        self.name = name
        self.node_type = node_type
        self.children: List['ASTNode'] = []
        self.parent = parent

    def __str__(self):
        return f"{self.node_type}({self.name})"

    __repr__ = __str__

class ASTNode:
    def __init__(self, name: str, node_type: str, parent: Optional['ASTNode'] = None):
        self.name = name
        self.node_type = node_type
        self.children: List['ASTNode'] = []
        self.parent = parent

    def __str__(self):
        return f"{self.node_type}({self.name})"

    __repr__ = __str__

class CGraphBuilder(CListener):
    def __init__(self):
        super().__init__()
        self.ast_root = None
        self.current_node = None
        self.typedefs = set()  # Track typedef names to prevent duplications

    def enterFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        func_name = ctx.declarator().getText().split('(')[0]
        func_node = ASTNode(func_name, "function", self.current_node)
        if self.current_node is None:
            self.ast_root = func_node
        else:
            self.current_node.children.append(func_node)
        self.current_node = func_node

    def exitFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        self.current_node = self.current_node.parent if self.current_node else None

    def enterDeclaration(self, ctx: CParser.DeclarationContext):
        is_typedef = any(specifier.getText() == 'typedef' for specifier in ctx.declarationSpecifiers().declarationSpecifier())
        init_declarator_list = ctx.initDeclaratorList()
        if not init_declarator_list:
            return

        init_declarators = init_declarator_list.initDeclarator() if isinstance(init_declarator_list.initDeclarator(), list) else [init_declarator_list.initDeclarator()]

        for init_declarator in init_declarators:
            declarator = init_declarator.declarator()
            if declarator:
                var_name = declarator.getText()
                # Check if it's a function declaration (without definition)
                if '(' in var_name and ')' in var_name:
                    func_name = var_name.split('(')[0]
                    func_node = ASTNode(func_name, "function", self.current_node)
                    if self.current_node is None:
                        self.ast_root = func_node
                    else:
                        self.current_node.children.append(func_node)
                else:
                    var_node = ASTNode(var_name, "typedef" if is_typedef else "var", self.current_node)
                    if self.current_node:
                        self.current_node.children.append(var_node)

    def enterStructOrUnionSpecifier(self, ctx: CParser.StructOrUnionSpecifierContext):
        struct_or_union_type = ctx.structOrUnion().getText()
        struct_name = ctx.Identifier().getText() if ctx.Identifier() else ""
        struct_node = ASTNode(struct_name, struct_or_union_type, self.current_node)
        if self.current_node:
            self.current_node.children.append(struct_node)
        self.current_node = struct_node

    def exitStructOrUnionSpecifier(self, ctx: CParser.StructOrUnionSpecifierContext):
        self.current_node = self.current_node.parent if self.current_node else None

    @staticmethod
    def build_ast(source_code: str) -> ASTNode:
        lexer = CLexer(InputStream(source_code))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        tree = parser.compilationUnit()
        listener = CGraphBuilder()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener.ast_root

#class SolidityGraphBuilder(SolidityListener):
#    def __init__(self):
#        super().__init__()
#        self.graph = nx.DiGraph()
#        self.function_counter = 0
#        self.state_variable_counter = 0
#        self.local_variable_counter = 0
#        self.declaration_stack: List[DeclarationNode] = []
#        self.contracts: dict = {}

#    def peek_declaration(self):
#        if not self.declaration_stack:
#            return None
#        return self.declaration_stack[-1]

#    def push_declaration(self, node: DeclarationNode):
#        self.declaration_stack.append(node)

#    def pop_declaration(self):
#        if not self.declaration_stack:
#            return None
#        node = self.declaration_stack[-1]
#        self.declaration_stack = self.declaration_stack[:-1]
#        return node

#    def enterContractDefinition(self, ctx: SolidityParser.ContractDefinitionContext):
#        contract_name = ctx.getChild(1).getText()
#        contract_node = DeclarationNode(contract_name, "contract", None)
#        self.graph.add_node(contract_node)
#        self.push_declaration(contract_node)
#        self.contracts[contract_node.name] = contract_node

#        # Handle multiple inheritance specifiers
#        if ctx.inheritanceSpecifier():
#            inheritance_specifiers = ctx.inheritanceSpecifier()
#            for spec in inheritance_specifiers:
#                parent_contract_name = spec.userDefinedTypeName().getText()
#                if parent_contract_name != contract_name:
#                    parent_node = self.contracts[parent_contract_name]
#                    self.graph.add_edge(parent_node, contract_node,
#                                        label="inherits")

#    def exitContractDefinition(self, ctx):
#        self.pop_declaration()

#    def enterFunctionDefinition(self, ctx: SolidityParser.FunctionDefinitionContext):
#        functions_name = ctx.getChild(0).getText()
#        function_name = functions_name.replace("function", "").strip()
#        parent_node = self.peek_declaration()
#        function_node = DeclarationNode(function_name, "function", parent_node)
#        self.graph.add_node(function_node)
#        self.push_declaration(function_node)
#        if parent_node is not None:
#            self.graph.add_edge(parent_node, function_node, label="def")

#    def exitFunctionDefinition(self, ctxt):
#        self.pop_declaration()

#    def enterModifierDefinition(self,
#                                ctx: SolidityParser.ModifierDefinitionContext):
#        function_name = ctx.getChild(1).getText()
#        parent_node = self.peek_declaration()
#        function_node = DeclarationNode(function_name, "function", parent_node)
#        self.graph.add_node(function_node)
#        self.push_declaration(function_node)
#        if parent_node is not None:
#            self.graph.add_edge(parent_node, function_node, label="def")

#    def exitModifierDefinition(self, ctx):
#        self.pop_declaration()

#    def enterEventDefinition(self, ctx: SolidityParser.EventDefinitionContext):
#        event_name = ctx.identifier().getText()
#        parent_node = self.peek_declaration()
#        event_node = DeclarationNode(event_name, "event", parent_node)
#        self.graph.add_node(event_node)
#        if parent_node is not None:
#            self.graph.add_edge(parent_node, event_node, label='def')

#    def enterStructDefinition(self, ctx: SolidityParser.StructDefinitionContext):
#        struct_name = ctx.identifier().getText()
#        parent_node = self.peek_declaration()
#        struct_node = DeclarationNode(struct_name, "struct", parent_node)
#        self.graph.add_node(struct_node)
#        self.push_declaration(struct_node)
#        if parent_node is not None:
#            self.graph.add_edge(parent_node, struct_node, label='def')

#    def exitStructDefinition(self, ctxt):
#        self.pop_declaration()

#    def enterStateVariableDeclaration(self, ctx: SolidityParser.StateVariableDeclarationContext):
#        identifier_token = ctx.identifier()
#        var_name = identifier_token.getText()
#        parent_node = self.peek_declaration()
#        var_node = DeclarationNode(var_name, "state_var", parent_node)
#        self.graph.add_node(var_node)
#        if parent_node is not None:
#            self.graph.add_edge(parent_node, var_node, label='def')

#    def enterVariableDeclaration(self, ctx: SolidityParser.VariableDeclarationContext):
#        local_var_name = ctx.getChild(1).getText()
#        parent_node = self.peek_declaration()
#        var_node = DeclarationNode(local_var_name, "var", parent_node)
#        self.graph.add_node(var_node)
#        if parent_node is not None:
#            self.graph.add_edge(parent_node, var_node, label='def')

#    @staticmethod
#    def build_graph(source_code: str) -> nx.DiGraph:
#        lexer = SolidityLexer(InputStream(source_code))
#        stream = CommonTokenStream(lexer)
#        parser = SolidityParser(stream)
#        tree = parser.sourceUnit()

#        listener = SolidityGraphBuilder()
#        walker = ParseTreeWalker()
#        walker.walk(listener, tree)
#        return listener.graph

GRAPH_BUILDERS = {
#    "solidity": SolidityGraphBuilder,
    "c": CGraphBuilder
}

def print_ast(node: ASTNode, indent: str = ""):
    print(f"{indent}{node}")
    for child in node.children:
        print_ast(child, indent + "  ")

def visualize_ast(ast_node: ASTNode, graph=None, parent=None):
    if graph is None:
        graph = nx.DiGraph()

    graph.add_node(ast_node.name)
    if parent:
        graph.add_edge(parent, ast_node.name)

    for child in ast_node.children:
        visualize_ast(child, graph, ast_node.name)
    
    return graph

def build_graph_from_file(file_path: str, language: str) -> nx.DiGraph:
    content = utils.read_file(file_path)
    if language == "c":
        ast = CGraphBuilder.build_ast(content)
        print_ast(ast)  # Print the AST
        return visualize_ast(ast)
    elif language == "solidity":
        ast = SolidityGraphBuilder.build_ast(content)
        print_ast(ast)  # Print the AST
        return visualize_ast(ast)

if __name__ == '__main__':
    file_path = 'ext_changed.sol'
    graph = build_graph_from_file(file_path)

    # Print nodes with specific labels
    def print_nodes_with_label(graph, label):
        nodes = [node for node in graph.nodes()
                 if node.node_type == label]
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
    print_nodes_with_label(graph, 'struct')
    print_nodes_with_label(graph, 'var')
    print_nodes_with_label(graph, 'state_var')

    # Print edges with labels
    print_edges_with_label(graph)

    # Draw and display the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)  # Positions for all nodes

    # Nodes
    node_labels = {node: node for node in graph.nodes()}
    node_colors = {'contract': 'lightblue', 'function': 'lightgreen', 'event': 'lightcoral',
                   'struct': 'lightgrey', 'var': 'yellow',
                   'state_var': 'lightpink'}
    node_shapes = {'contract': 'o', 'function': 'o', 'event': 'o',
                   'emit': 'o', 'struct': 's', 'var': 'o',
                   'state_var': 'o'}

    for label in node_colors:
        nx.draw_networkx_nodes(graph, pos, nodelist=[node for node in graph.nodes() if node.node_type == label],
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

