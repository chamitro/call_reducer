from abc import abstractmethod

import networkx as nx
from reducer import parsers
from reducer.graph import DeclarationNode


class ASTRemoval(parsers.TreeTraversal):
    def __init__(self, content, graph: nx.DiGraph):
        self.content = content
        self.graph = graph
        self.removals = []
        self.replacements = []

    @abstractmethod
    def remove_nodes(self, nodes_to_remove: set) -> str:
        pass


class SolidityDeclarationRemoval(ASTRemoval):
    LANGUAGE = "solidity"

    def __init__(self, content, graph):
        super().__init__(content, graph)
        self.removed_nodes = []

    def visit_default(self, node):
        pass

    def exit_default(self, node):
        pass

    def get_node_visitor(self, node):
        visitors = {
            "function_definition": self.visit_function_definition,
            "call_expression": self.visit_call_expression,
            "modifier_definition": self.visit_modifier_definition,
            "struct_definition": self.visit_struct_definition,
            "variable_declaration": self.visit_variable_declaration,
            "state_variable_declaration": self.visit_state_variable_declaration,
            "event_definition": self.visit_event_definition,
        }
        return visitors.get(node.type, self.visit_default)

    def get_node_exit(self, node):
        exit_funcs = {
        }
        return exit_funcs.get(node.type, self.exit_default)

    def visit_function_definition(self, node):
        """Collects function nodes to be removed."""
        function_name = node.children[1].text.decode("utf-8")
        print(f"Identified function for removal: {function_name}")  # Debug log
        self.removed_nodes.append(node)

    def visit_modifier_definition(self, node):
        """Collects modifier nodes to be removed."""
        modifier_name = node.children[1].text.decode("utf-8")
        print(f"Identified modifier for removal: {modifier_name}")  # Debug log
        self.removed_nodes.append(node)

    def visit_struct_definition(self, node):
        """Collects struct nodes to be removed."""
        struct_name = node.children[1].text.decode("utf-8")
        print(f"Identified struct for removal: {struct_name}")  # Debug log
        self.removed_nodes.append(node)

    def visit_variable_declaration(self, node):
        """Collects variable declaration nodes to be removed."""
        variable_name = node.children[1].text.decode("utf-8")
        print(f"Identified variable for removal: {variable_name}")  # Debug log
        self.removed_nodes.append(node)

    def visit_state_variable_declaration(self, node):
        """Collects state variable nodes to be removed."""
        state_variable_name = node.children[1].text.decode("utf-8")
        print(f"Identified state variable for removal: {state_variable_name}")  # Debug log
        self.removed_nodes.append(node)

    def visit_event_definition(self, node):
        """Collects event nodes to be removed."""
        event_name = node.children[1].text.decode("utf-8")
        print(f"Identified event for removal: {event_name}")  # Debug log
        self.removed_nodes.append(node)

    def visit_function_definition(self, node):
        function_name = node.children[1].text.decode("utf-8")
        if any((node.name == function_name and node.node_type == "function")
               for node in self.nodes_to_remove):
            self.removed_nodes.append(node)

    def visit_call_expression(self, node):
        child = node.children[0]
        assert child.type == "expression"
        match child.children[0].type:
            case "member_expression":
                call_name = child.children[0].children[-1].text.decode("utf-8")
            case "identifier":
                call_name = child.children[0].text.decode("utf-8")
            case _:
                raise Exception("Unknown node")
        if any(node.name == call_name for node in self.nodes_to_remove):
            self.removed_nodes.append(node)
            current_node = node
            while True:
                match current_node.type:
                    case "assignment_expression":
                        self.removed_nodes.remove(node)
                        self.removed_nodes.append(current_node)
                        break
                    case "function_body":
                        break
                    case None:
                        break
                    case _:
                        current_node = current_node.parent

    def remove_nodes(self, nodes_to_remove: set):
        parser = parsers.get_parser(self.LANGUAGE)
        tree = parser.parse(self.content.encode("utf-8"))
        self.nodes_to_remove = nodes_to_remove
        self.traverse_node(tree.root_node)
        definitions = {
            node for node in self.removed_nodes
            if node.type in ["function_definition"]
        }
        self.removed_nodes.sort(key=lambda node: node.start_byte, reverse=True)
        edits = []
        modified_code = tree.text
        for removed_node in self.removed_nodes:
            if removed_node.type != "function_definition":
                if any(removed_node.start_byte > n.start_byte and removed_node.end_byte < n.end_byte for n in definitions):
                    continue
            if removed_node.type == "assignment_expression":
                edits.append({
                    "start_byte": removed_node.start_byte,
                    "old_end_byte": removed_node.end_byte,
                    "new_end_byte": removed_node.children[0].end_byte,
                    "start_point": removed_node.start_point,
                    "old_end_point": removed_node.end_point,
                    "new_end_point": removed_node.children[0].end_point,
                })
            else:
                edits.append({
                    "start_byte": removed_node.start_byte,
                    "old_end_byte": removed_node.end_byte,
                    "new_end_byte": removed_node.start_byte,  # Remove content
                    "start_point": removed_node.start_point,
                    "old_end_point": removed_node.end_point,
                    "new_end_point": removed_node.start_point,
                })

        for edit in edits:
            # Apply the edit to the tree
            tree.edit(
                start_byte=edit["start_byte"],
                old_end_byte=edit["old_end_byte"],
                new_end_byte=edit["new_end_byte"],
                start_point=edit["start_point"],
                old_end_point=edit["old_end_point"],
                new_end_point=edit["new_end_point"],
            )
            # Update the source code
            modified_code = (
                modified_code[: edit["start_byte"]] +
                modified_code[edit["start_byte"]:edit["new_end_byte"]] +
                modified_code[edit["old_end_byte"]:]
            )
        parser = parsers.get_parser(self.LANGUAGE)
        updated_tree = parser.parse(modified_code, tree)
        return updated_tree.text.decode("utf-8")


class CDeclarationRemoval(ASTRemoval):
    LANGUAGE = "c"

    def __init__(self, content, graph):
        super().__init__(content, graph)
        self.removed_nodes = []

    def visit_default(self, node):
        pass

    def exit_default(self, node):
        pass

    def get_node_visitor(self, node):
        visitors = {
            "function_definition": self.visit_function_definition,
            "expression_statement": self.visit_expression_statement,
        }
        return visitors.get(node.type, self.visit_default)

    def get_node_exit(self, node):
        exit_funcs = {
        }
        return exit_funcs.get(node.type, self.exit_default)

    def visit_function_definition(self, node):
        function_name = node.children[1].children[0].text.decode("utf-8")
        if any((node.name == function_name and node.node_type == "function")
               for node in self.nodes_to_remove):
            self.removed_nodes.append(node)

    def visit_call_expression(self, node):
        child = node.children[0]
        call_name = child.text.decode("utf-8")
        if any(node.name == call_name for node in self.nodes_to_remove):
            self.removed_nodes.append(node)

    def visit_expression_statement(self, node):
        child = node.children[0]
        if child.type == "call_expression":
            call_name = child.children[0].text.decode("utf-8")
            if any(node.name == call_name for node in self.nodes_to_remove):
                self.removed_nodes.append(node)

    def remove_nodes(self, nodes_to_remove: set):
        parser = parsers.get_parser(self.LANGUAGE)
        tree = parser.parse(self.content.encode("utf-8"))
        self.nodes_to_remove = nodes_to_remove
        self.traverse_node(tree.root_node)
        definitions = {
            node for node in self.removed_nodes
            if node.type in ["function_definition"]
        }
        self.removed_nodes.sort(key=lambda node: node.start_byte, reverse=True)
        edits = []
        modified_code = tree.text
        for removed_node in self.removed_nodes:
            if removed_node.type != "function_definition":
                if any(removed_node.start_byte > n.start_byte and removed_node.end_byte < n.end_byte for n in definitions):
                    continue
            if removed_node.type == "assignment_expression":
                edits.append({
                    "start_byte": removed_node.start_byte,
                    "old_end_byte": removed_node.end_byte,
                    "new_end_byte": removed_node.children[0].end_byte,
                    "start_point": removed_node.start_point,
                    "old_end_point": removed_node.end_point,
                    "new_end_point": removed_node.children[0].end_point,
                })
            else:
                edits.append({
                    "start_byte": removed_node.start_byte,
                    "old_end_byte": removed_node.end_byte,
                    "new_end_byte": removed_node.start_byte,  # Remove content
                    "start_point": removed_node.start_point,
                    "old_end_point": removed_node.end_point,
                    "new_end_point": removed_node.start_point,
                })

        for edit in edits:
            # Apply the edit to the tree
            tree.edit(
                start_byte=edit["start_byte"],
                old_end_byte=edit["old_end_byte"],
                new_end_byte=edit["new_end_byte"],
                start_point=edit["start_point"],
                old_end_point=edit["old_end_point"],
                new_end_point=edit["new_end_point"],
            )
            # Update the source code
            modified_code = (
                modified_code[: edit["start_byte"]] +
                modified_code[edit["start_byte"]:edit["new_end_byte"]] +
                modified_code[edit["old_end_byte"]:]
            )
        parser = parsers.get_parser(self.LANGUAGE)
        updated_tree = parser.parse(modified_code, tree)
        return updated_tree.text.decode("utf-8")


AST_REMOVALS = {
    "solidity": SolidityDeclarationRemoval,
    "c": CDeclarationRemoval,
}

if __name__ == "__main__":
    file_name = "example.c"
    from reducer import utils
    content = utils.read_file(file_name)
    modifier = CDeclarationRemoval(content, nx.DiGraph())
    updated_tree = modifier.remove_nodes(
        {DeclarationNode("print_array", "function", None)})
    print(updated_tree)
