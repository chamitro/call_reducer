from typing import NamedTuple, List, Any

import networkx as nx

from reducer import parsers


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


class GraphBuilder(parsers.TreeTraversal):
    LANGUAGE = None

    def __init__(self):
        self.graph = nx.DiGraph()

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

    def build_graph(self, source_file: str) -> nx.DiGraph:
        tree = parsers.parse(source_file, self.LANGUAGE)
        root_node = tree.root_node
        self.traverse_node(root_node)
        return self.graph


class SolidityGraphBuilder(GraphBuilder):
    LANGUAGE = "solidity"

    def __init__(self):
        super().__init__()
        self.function_counter = 0
        self.state_variable_counter = 0
        self.local_variable_counter = 0
        self.declaration_stack: List[DeclarationNode] = []
        self.contracts: dict = {}

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


GRAPH_BUILDERS = {
    "solidity": SolidityGraphBuilder,
}


def get_graph_builder(language: str) -> GraphBuilder:
    builder = GRAPH_BUILDERS.get(language)
    if builder is None:
        raise Exception(
            f"Graph builder for language '{language}' was not found")
    return builder


def build_graph_from_file(file_path: str, language: str) -> nx.DiGraph:
    builder = get_graph_builder(language)
    return builder().build_graph(file_path)


if __name__ == '__main__':
    file_path = 'ext_changed.sol'
    builder = SolidityGraphBuilder()
    builder.build_graph(file_path)
