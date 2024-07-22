from typing import NamedTuple, List, Any
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



class DeclarationNode(NamedTuple):
    name: str
    node_type: str
    parent: Any

    def __hash__(self):
        return hash((self.name, self.node_type, self.parent))

    def __str__(self):
        node_name = f"{self.node_type}[{self.name}]"
        if self.parent is not None:
            return f"{str(self.parent)}.{node_name}"
        else:
            return node_name

    __repr__ = __str__

class CGraphBuilder(CListener):
    def __init__(self):
        super().__init__()
        self.graph = nx.DiGraph()
        self.declaration_stack = []
        self.current_function = None
        self.typedefs = set()  # Track typedef names to prevent duplications

    def peek_declaration(self):
        if not self.declaration_stack:
            return None
        return self.declaration_stack[-1]

    def push_declaration(self, node):
        self.declaration_stack.append(node)

    def pop_declaration(self):
        if not self.declaration_stack:
            return None
        return self.declaration_stack.pop()

    def enterFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        func_name = ctx.declarator().getText().split('(')[0]  # Extract function name only
        parent_node = self.peek_declaration()
        func_node = DeclarationNode(func_name, "function", parent_node)
        self.graph.add_node(func_node)
        self.push_declaration(func_node)
        self.current_function = func_node  # Set the current function context
        if parent_node is not None:
            self.graph.add_edge(parent_node, func_node, label="def")

    def exitFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        self.pop_declaration()
        self.current_function = None  # Clear current function context

    def get_base_name(self, name):
        # Regular expression to match 'bla[...]'
        match = re.match(r'([a-zA-Z_]\w*)\[\d*\]', name)
        if match:
            return match.group(1)
        return name
        
    def enterDeclaration(self, ctx: CParser.DeclarationContext):
        """
        Handles both variable declarations and static assertions.
        Differentiates between typedef and variable declarations.
        """
        # Check if the declaration is a typedef
        is_typedef = any(
            specifier.getText() == 'typedef'
            for specifier in ctx.declarationSpecifiers().declarationSpecifier()
        )

        init_declarator_list = ctx.initDeclaratorList()
        if not init_declarator_list:
            return

        if is_typedef:
            # Handle typedefs
            for init_declarator in init_declarator_list.initDeclarator():
                declarator = init_declarator.declarator()
                if declarator:
                    typedef_name = declarator.getText()
                    if typedef_name not in self.typedefs:
                        typedef_node = DeclarationNode(typedef_name, "typedef", self.peek_declaration())
                        self.graph.add_node(typedef_node)
                        self.typedefs.add(typedef_name)  # Track typedef names
                        if self.peek_declaration() is not None:
                            self.graph.add_edge(self.peek_declaration(), typedef_node, label="def")
        else:
            # Handle variables, excluding function arguments
            for init_declarator in init_declarator_list.initDeclarator():
                declarator = init_declarator.declarator()
                if declarator:
                    var_name2 = declarator.getText()
                    var_name = self.get_base_name(var_name2)
                    # Check if the variable is a function argument
                    # Function arguments will not be handled here, only local variables
                    if self.current_function and not self._is_function_argument(declarator):
                        var_node = DeclarationNode(var_name, "var", self.current_function)
                        self.graph.add_node(var_node)
                        if self.current_function is not None:
                            self.graph.add_edge(self.current_function, var_node, label="def")
                        else:
                            # If no current function context, use the top of the stack (global scope)
                            parent_node = self.peek_declaration()
                            if parent_node is not None:
                                self.graph.add_edge(parent_node, var_node, label="def")

    def _is_function_argument(self, declarator):
        """
        Checks if the declarator represents a function argument.
        This is a placeholder and needs actual logic based on the parse tree structure.
        """
        # Actual implementation to check if the variable is a function argument
        # This is just an example; adjust it based on the CParser's API and context
        return False

    def enterStructOrUnionSpecifier(self, ctx: CParser.StructOrUnionSpecifierContext):
        struct_or_union_type = ctx.structOrUnion().getText()  # "struct" or "union"

        if ctx.Identifier():
            struct_name = ctx.Identifier().getText()
            print(f"Struct or Union detected: {struct_or_union_type} {struct_name}")  # Debugging print statement
        
            parent_node = self.peek_declaration()
            # Create a new DeclarationNode for the struct/union with the given name
            struct_node = DeclarationNode(struct_name, "struct", parent_node)
            self.graph.add_node(struct_node)
            if parent_node is not None:
                self.graph.add_edge(parent_node, struct_node, label="def")

    def enterTypeSpecifier(self, ctx: CParser.TypeSpecifierContext):
        # Handles custom variable types
        if ctx.typedefName():
            typedef_name = ctx.typedefName().Identifier().getText()
            if typedef_name not in self.typedefs:
                typedef_node = DeclarationNode(typedef_name, "var", self.peek_declaration())
                self.graph.add_node(typedef_node)
                self.typedefs.add(typedef_name)  # Track typedef names
                if self.peek_declaration() is not None:
                    self.graph.add_edge(self.peek_declaration(), typedef_node, label="def")

    @staticmethod
    def build_graph(source_code: str) -> nx.DiGraph:
        lexer = CLexer(InputStream(source_code))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        tree = parser.compilationUnit()

        listener = CGraphBuilder()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener.graph


class SolidityGraphBuilder(SolidityListener):
    def __init__(self):
        super().__init__()
        self.graph = nx.DiGraph()
        self.function_counter = 0
        self.state_variable_counter = 0
        self.local_variable_counter = 0
        self.declaration_stack: List[DeclarationNode] = []
        self.contracts: dict = {}

    def peek_declaration(self):
        if not self.declaration_stack:
            return None
        return self.declaration_stack[-1]

    def push_declaration(self, node: DeclarationNode):
        self.declaration_stack.append(node)

    def pop_declaration(self):
        if not self.declaration_stack:
            return None
        node = self.declaration_stack[-1]
        self.declaration_stack = self.declaration_stack[:-1]
        return node

    def enterContractDefinition(self, ctx: SolidityParser.ContractDefinitionContext):
        contract_name = ctx.getChild(1).getText()
        contract_node = DeclarationNode(contract_name, "contract", None)
        self.graph.add_node(contract_node)
        self.push_declaration(contract_node)
        self.contracts[contract_node.name] = contract_node

        # Handle multiple inheritance specifiers
        if ctx.inheritanceSpecifier():
            inheritance_specifiers = ctx.inheritanceSpecifier()
            for spec in inheritance_specifiers:
                parent_contract_name = spec.userDefinedTypeName().getText()
                if parent_contract_name != contract_name:
                    parent_node = self.contracts[parent_contract_name]
                    self.graph.add_edge(parent_node, contract_node,
                                        label="inherits")

    def exitContractDefinition(self, ctx):
        self.pop_declaration()

    def enterFunctionDefinition(self, ctx: SolidityParser.FunctionDefinitionContext):
        functions_name = ctx.getChild(0).getText()
        function_name = functions_name.replace("function", "").strip()
        parent_node = self.peek_declaration()
        function_node = DeclarationNode(function_name, "function", parent_node)
        self.graph.add_node(function_node)
        self.push_declaration(function_node)
        if parent_node is not None:
            self.graph.add_edge(parent_node, function_node, label="def")

    def exitFunctionDefinition(self, ctxt):
        self.pop_declaration()

    def enterModifierDefinition(self,
                                ctx: SolidityParser.ModifierDefinitionContext):
        function_name = ctx.getChild(1).getText()
        parent_node = self.peek_declaration()
        function_node = DeclarationNode(function_name, "function", parent_node)
        self.graph.add_node(function_node)
        self.push_declaration(function_node)
        if parent_node is not None:
            self.graph.add_edge(parent_node, function_node, label="def")

    def exitModifierDefinition(self, ctx):
        self.pop_declaration()

    def enterEventDefinition(self, ctx: SolidityParser.EventDefinitionContext):
        event_name = ctx.identifier().getText()
        parent_node = self.peek_declaration()
        event_node = DeclarationNode(event_name, "event", parent_node)
        self.graph.add_node(event_node)
        if parent_node is not None:
            self.graph.add_edge(parent_node, event_node, label='def')

    def enterStructDefinition(self, ctx: SolidityParser.StructDefinitionContext):
        struct_name = ctx.identifier().getText()
        parent_node = self.peek_declaration()
        struct_node = DeclarationNode(struct_name, "struct", parent_node)
        self.graph.add_node(struct_node)
        self.push_declaration(struct_node)
        if parent_node is not None:
            self.graph.add_edge(parent_node, struct_node, label='def')

    def exitStructDefinition(self, ctxt):
        self.pop_declaration()

    def enterStateVariableDeclaration(self, ctx: SolidityParser.StateVariableDeclarationContext):
        identifier_token = ctx.identifier()
        var_name = identifier_token.getText()
        parent_node = self.peek_declaration()
        var_node = DeclarationNode(var_name, "state_var", parent_node)
        self.graph.add_node(var_node)
        if parent_node is not None:
            self.graph.add_edge(parent_node, var_node, label='def')

    def enterVariableDeclaration(self, ctx: SolidityParser.VariableDeclarationContext):
        local_var_name = ctx.getChild(1).getText()
        parent_node = self.peek_declaration()
        var_node = DeclarationNode(local_var_name, "var", parent_node)
        self.graph.add_node(var_node)
        if parent_node is not None:
            self.graph.add_edge(parent_node, var_node, label='def')

    @staticmethod
    def build_graph(source_code: str) -> nx.DiGraph:
        lexer = SolidityLexer(InputStream(source_code))
        stream = CommonTokenStream(lexer)
        parser = SolidityParser(stream)
        tree = parser.sourceUnit()

        listener = SolidityGraphBuilder()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener.graph

GRAPH_BUILDERS = {
    "solidity": SolidityGraphBuilder,
    "c": CGraphBuilder
}


def build_graph_from_file(file_path: str, language: str) -> nx.DiGraph:
    content = utils.read_file(file_path)
    cls = GRAPH_BUILDERS[language]
    return cls.build_graph(content)


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

