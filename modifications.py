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
            "modifier_definition": self.visit_modifier_definition,
            "struct_definition": self.visit_struct_definition,
            "variable_declaration": self.visit_variable_declaration,
            "state_variable_declaration": self.visit_state_variable_declaration,
            "event_definition": self.visit_event_definition,
        }
        return visitors.get(node.type, self.visit_default)

    def get_node_exit(self, node):
        exit_funcs = {}
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

    def remove_nodes(self, nodes_to_remove: set):
        parser = parsers.get_parser(self.LANGUAGE)
        tree = parser.parse(self.content.encode("utf-8"))

        # Identify all relevant nodes
        self.traverse_node(tree.root_node)
        nodes_to_remove = {
            DeclarationNode(node.children[1].text.decode("utf-8"), node.type, None)
            for node in self.removed_nodes
        }

        # Remove the identified nodes
        self.removed_nodes.sort(key=lambda node: node.start_byte, reverse=True)
        edits = []
        modified_code = tree.text
        for removed_node in self.removed_nodes:
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
}

if __name__ == "__main__":
    file_name = "ext_changed.sol"
    from reducer import utils
    content = utils.read_file(file_name)
    modifier = SolidityDeclarationRemoval(content, nx.DiGraph())

    # Automatically remove all relevant nodes
    updated_code = modifier.remove_nodes(set())
    print("Updated code:")  # Debug log
    print(updated_code)

    # Write back the updated code to the file
    utils.update_file(file_name, updated_code)

