import networkx as nx
from typing import NamedTuple, List, Any, Optional

from reducer import parsers


class DeclarationNode(NamedTuple):
    name: str
    node_type: str
    parent: Any

    def __hash__(self) -> int:
        return hash((self.name, self.node_type, self.parent))

    def __str__(self) -> str:
        node_name = f"{self.node_type}[{self.name}]"
        if self.parent is not None:
            return f"{str(self.parent)}.{node_name}"
        else:
            return node_name

    def __repr__(self) -> str:
        return self.__str__()


class GraphBuilder(parsers.TreeTraversal):
    LANGUAGE: Optional[str] = None

    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        self.declaration_stack: List[DeclarationNode] = []

    def peek_declaration(self) -> Optional[DeclarationNode]:
        if not self.declaration_stack:
            return None
        return self.declaration_stack[-1]

    def push_declaration(self, node: DeclarationNode) -> None:
        self.declaration_stack.append(node)

    def pop_declaration(self) -> Optional[DeclarationNode]:
        if not self.declaration_stack:
            return None
        return self.declaration_stack.pop()

    def build_graph(self, source_file: str) -> nx.DiGraph:
        assert self.LANGUAGE is not None, "LANGUAGE must be set in subclasses"
        tree = parsers.parse(source_file, self.LANGUAGE)
        root_node = tree.root_node
        self.traverse_node(root_node)
        return self.graph


class SolidityGraphBuilder(GraphBuilder):
    LANGUAGE: str = "solidity"

    def __init__(self) -> None:
        super().__init__()
        self.function_counter = 0
        self.state_variable_counter = 0
        self.local_variable_counter = 0
        self.contracts: dict[str, DeclarationNode] = {}

    def visit_default(self, node):
        pass

    def exit_default(self, node):
        pass

    def visit_contract_declaration(self, node):
        contract_name = node.children[1].text.decode("utf-8")
        contract_node = DeclarationNode(contract_name, "contract", None)
        self.graph.add_node(contract_node)
        self.push_declaration(contract_node)
        self.contracts[contract_node.name] = contract_node

        for child in node.children:
            if child.type == "inheritance_specifier":
                parent_name = child.text.decode("utf-8")
                if parent_name != contract_name:
                    parent_node = self.contracts[parent_name]
                    self.graph.add_edge(parent_node, contract_node,
                                        label="inherits")

    def exit_contract_declaration(self, ctx):
        self.pop_declaration()

    def visit_function_definition(self, node):
        func_name = node.children[1].text.decode("utf-8")
        parent_node = self.peek_declaration()
        func_node = DeclarationNode(func_name, "function", parent_node)
        self.graph.add_node(func_node)
        self.push_declaration(func_node)
        self.current_function = func_node  # Set the current function context
        if parent_node is not None:
            self.graph.add_edge(parent_node, func_node, label="def")

    def exit_function_definition(self, node):
        self.pop_declaration()

    def visit_modifier_definition(self, node):
        # function_name = node.text.decode("utf-8")
        # parent_node = self.peek_declaration()
        # function_node = DeclarationNode(function_name, "function", parent_node)
        # self.graph.add_node(function_node)
        # self.push_declaration(function_node)
        # if parent_node is not None:
        #     self.graph.add_edge(parent_node, function_node, label="def")
        pass

    def exit_modifier_definition(self, node):
        # self.pop_declaration()
        pass

    def visit_event_definition(self, node):
        event_name = node.text.decode("utf-8")
        parent_node = self.peek_declaration()
        event_node = DeclarationNode(event_name, "event", parent_node)
        self.graph.add_node(event_node)
        if parent_node is not None:
            self.graph.add_edge(parent_node, event_node, label='def')

    def get_node_visitor(self, node):
        visitors = {
            "contract_declaration": self.visit_contract_declaration,
            "interface_declaration": self.visit_contract_declaration,
            "function_definition": self.visit_function_definition,
            "modifier_definition": self.visit_modifier_definition,
            "event_definition": self.visit_event_definition,
        }
        return visitors.get(node.type, self.visit_default)

    def get_node_exit(self, node):
        exit_funcs = {
            "contract_declaration": self.exit_contract_declaration,
            "interface_declaration": self.visit_contract_declaration,
            "function_definition": self.exit_function_definition,
            "modifier_definition": self.exit_modifier_definition,
        }
        return exit_funcs.get(node.type, self.exit_default)


class CGraphBuilder(GraphBuilder):
    LANGUAGE: str = "c"

    def __init__(self) -> None:
        super().__init__()
        self.function_counter = 0
        self.state_variable_counter = 0
        self.local_variable_counter = 0
        self.current_function: Optional[DeclarationNode] = None
        self.structs: dict[str, DeclarationNode] = {}
        self.declarations: dict[str, DeclarationNode] = {}

    def visit_default(self, node):
        pass

    def exit_default(self, node):
        pass

    def add_function_declaration_node(self, node):
        func_name = node.text.decode("utf-8")
        parent_node = self.peek_declaration()
        func_node = DeclarationNode(func_name, "function", parent_node)
        self.graph.add_node(func_node)
        self.push_declaration(func_node)
        self.declarations[func_name] = func_node
        self.current_function = func_node  # Set the current function context
        if parent_node is not None:
            self.graph.add_edge(parent_node, func_node, label="def")

    def visit_function_definition(self, node):
        for child in node.children:
            if child.type == "function_declarator":
                for child_child in child.children:
                    if child_child.type == "identifier":
                        self.add_function_declaration_node(child_child)
                        break
                    if child_child.type == "parenthesized_declarator":
                        for child_child_child in child_child.children:
                            if child_child_child.type == "identifier":
                                self.add_function_declaration_node(child_child_child)
                                break

    def exit_function_definition(self, node):
        self.pop_declaration()
        self.current_function = None  # Clear current function context

    def add_global_variable(self, var_name):
        if self.current_function:
            var_node = DeclarationNode(var_name, "global_variable", self.current_function)
            self.graph.add_node(var_node)
            self.declarations[var_name] = var_node
            self.push_declaration(var_node)
            if self.current_function is not None:
                self.graph.add_edge(self.current_function, var_node, label="var")
        else:
            # If no current function context, use the top of the stack (global scope)
            parent_node = self.peek_declaration()
            var_node = DeclarationNode(var_name, "global_variable", parent_node)
            self.graph.add_node(var_node)
            self.declarations[var_name] = var_node
            self.push_declaration(var_node)
            if parent_node is not None:
                self.graph.add_edge(parent_node, var_node, label="var")

    def visit_declaration(self, node):
        global_variable = False
        for child in node.children:
            if (
                child.type == "storage_class_specifier"
                and child.text.decode("utf-8") == "static"
            ):
                global_variable = True
                break
        if global_variable:
            for child in node.children:
                if child.type == "identifier":
                    var_name = child.text.decode("utf-8")
                    self.add_global_variable(var_name)
                elif child.type in [
                    "init_declarator", "array_declarator", "function_declarator"
                ]:
                    for child_child in child.children:
                        if child_child.type == "identifier":
                            var_name = child_child.text.decode("utf-8")
                            self.add_global_variable(var_name)

    def exit_declaration(self, node):
        pass

    def visit_for_statement(self, node):
        for_name = "for_" + str(node.start_point[0])
        for_node = DeclarationNode(for_name, "for_statement", None)
        self.graph.add_node(for_node)

    def exit_for_statement(self, node):
        pass

    def visit_if_statement(self, node):
        if_name = "if_" + str(node.start_point[0])
        if_node = DeclarationNode(if_name, "if_statement", None)
        self.graph.add_node(if_node)

    def exit_if_statement(self, node):
        pass

    def _handle_struct_declaration_parent(self, parent_node):
        for child in parent_node.children:
            if child.type == "identifier":
                return child.text.decode("utf-8")
            if child.type in ["init_declarator", "pointer_declarator", "array_declarator"]:
                for child_child in child.children:
                    if child_child.type == "identifier":
                        return child_child.text.decode("utf-8")

    def _handle_struct_parameter_declaration_parent(self, parent_node):
        function_declarator = parent_node.parent.parent
        for child in function_declarator.children:
            if child.type == "identifier":
                return child.text.decode("utf-8")

    def _handle_struct_function_definition_parent(self, parent_node):
        for child in parent_node.children:
            if child.type == "function_declarator":
                for child_child in child.children:
                    if child_child.type == "identifier":
                        return child_child.text.decode("utf-8")

    def visit_struct_specifier(self, node):
        parent_node = node.parent if len(node.children) < 3 else None
        for child in node.children:
            if child.type == "type_identifier":
                struct_name = child.text.decode("utf-8")
                struct_node = DeclarationNode(struct_name, "struct", None)
                if struct_name not in self.structs:
                    self.structs[struct_name] = struct_node
                    return self.graph.add_node(struct_node)
                if parent_node is not None:
                    declaration_name = None
                    if parent_node.type == "declaration":
                        declaration_name = self._handle_struct_declaration_parent(parent_node)
                    elif parent_node.type == "parameter_declaration":
                        declaration_name = self._handle_struct_parameter_declaration_parent(parent_node)
                    elif parent_node.type == "function_definition":
                        declaration_name = self._handle_struct_function_definition_parent(parent_node)
                    if declaration_name:
                        if self.declarations.get(declaration_name) is not None:
                            declaration = self.declarations.get(declaration_name)
                            self.graph.add_edge(struct_node, declaration, label="struct")
                    return

    def exit_struct_specifier(self, node):
        pass

    def get_node_visitor(self, node):
        visitors = {
            "function_definition": self.visit_function_definition,
            "declaration": self.visit_declaration,
            "struct_specifier": self.visit_struct_specifier,
            "for_statement": self.visit_for_statement,
            "if_statement": self.visit_if_statement,
        }
        return visitors.get(node.type, self.visit_default)

    def get_node_exit(self, node):
        exit_funcs = {
            "function_definition": self.exit_function_definition,
            "declaration": self.exit_declaration,
            "struct_specifier": self.exit_struct_specifier,
            "for_statement": self.exit_for_statement,
            "if_statement": self.exit_if_statement,
        }
        return exit_funcs.get(node.type, self.exit_default)


GRAPH_BUILDERS = {
    "solidity": SolidityGraphBuilder,
    "c": CGraphBuilder,
}


def get_graph_builder(language: str) -> type[GraphBuilder]:
    builder = GRAPH_BUILDERS.get(language)
    if builder is None:
        raise Exception(
            f"Graph builder for language '{language}' was not found")
    return builder


def build_graph_from_file(file_path: str, language: str) -> nx.DiGraph:
    builder = get_graph_builder(language)
    return builder().build_graph(file_path)


if __name__ == '__main__':
    file_path = './C/gcc-59903/small.c'
    builder = CGraphBuilder()
    graph = builder.build_graph(file_path)
    print(graph)

    # file_path = 'ext_changed.sol'
    # builder = SolidityGraphBuilder()
    # graph = builder.build_graph(file_path)
    # print(graph)

    import matplotlib.pyplot as plt  # type: ignore

    nx.draw(graph, with_labels=False, node_color='lightblue', edge_color='gray',
            node_size=2, font_size=5, font_weight='bold')

    # Display the plot
    plt.savefig("graph.png")
