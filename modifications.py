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

    @classmethod
    def setup_parse_tree(cls, source_code: str):
        """Parses the source code and returns the Tree-sitter syntax tree."""
        parser = parsers.get_parser(cls.LANGUAGE)
        return parser.parse(source_code.encode("utf-8"))


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

    def remove_nodes(self, nodes_to_remove: set):
        parser = parsers.get_parser(self.LANGUAGE)
        tree = parser.parse(self.content.encode("utf-8"))

        # Identify all function nodes
        self.traverse_node(tree.root_node)
        nodes_to_remove = {DeclarationNode(node.children[1].text.decode("utf-8"), "function", None) for node in self.removed_nodes}

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
        print(updated_tree)
        return updated_tree.text.decode("utf-8")
        


AST_REMOVALS = {
    "solidity": SolidityDeclarationRemoval,
}

if __name__ == "__main__":
    file_name = "ext_changed.sol"
    from reducer import utils
    content = utils.read_file(file_name)

    # Parse the source code to create a syntax tree
    syntax_tree = SolidityDeclarationRemoval.setup_parse_tree(content)

    # Create an instance of the removal class
    modifier = SolidityDeclarationRemoval(content, nx.DiGraph())

    # Automatically remove all functions
    updated_code = modifier.remove_nodes(set())
    print("Updated code:")  # Debug log
    print(updated_code)

    # Write back the updated code to the file
    utils.update_file(file_name, updated_code)

