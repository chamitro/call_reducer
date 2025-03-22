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
        self.removed_declarations = []

    def visit_default(self, node):
        pass

    def exit_default(self, node):
        pass

    def get_node_visitor(self, node):
        visitors = {
            "function_definition": self.visit_function_definition,
            "expression_statement": self.visit_expression_statement,
            "call_expression": self.visit_call_expression,
        }
        return visitors.get(node.type, self.visit_default)

    def get_node_exit(self, node):
        exit_funcs = {
        }
        return exit_funcs.get(node.type, self.exit_default)

    def add_expression_to_removal_nodes(self, child, node):
        child_name = child.text.decode("utf-8")
        if (child_name in self.removed_declarations
            and node not in self.removed_nodes):
            self.removed_nodes.append(node)
        for removal_node in self.nodes_to_remove:
            if (removal_node.name == child_name
                and removal_node.node_type == "function"
                and node not in self.removed_nodes):
                self.removed_nodes.append(node)

    def add_declaration_to_removed_declarations(self, declaration_node):
        for declaration_child in declaration_node.children:
            if declaration_child.type == "identifier":
                self.removed_declarations.append(declaration_child.text.decode("utf-8"))
            elif declaration_child.type == "init_declarator":
                self.add_declaration_to_removed_declarations(declaration_child)

    def find_specific_parent_node(self, node, parent_node):
        if node is None:
            return
        if node.type == parent_node:
            return node
        else:
            return self.find_specific_parent_node(node.parent, parent_node)

    def visit_function_definition(self, node):
        for child in node.children:
            if child.type == "function_declarator":
                for child_child in child.children:
                    if child_child.type == "identifier":
                        self.add_expression_to_removal_nodes(child_child, node)
                        return
                    elif child_child.type == "parenthesized_declarator":
                        for child_child_child in child_child.children:
                            if child_child_child.type == "identifier":
                                self.add_expression_to_removal_nodes(child_child_child, node)
                                return

    def visit_call_expression(self, node):
        remove_node = False
        #  call_expression uses variable from removed declaration in argument list
        for child in node.children:
            if child.type == "argument_list":
                for child_child in child.children:
                    if child_child.type == "identifier":
                        variable_name = child_child.text.decode("utf-8")
                        if variable_name in self.removed_declarations:
                            remove_node = True
            # call_expression uses removed function
            if child.type == "identifier":
                call_name = child.text.decode("utf-8")
                for removal_node in self.nodes_to_remove:
                    if (removal_node.name == call_name
                        and removal_node.node_type == "function"):
                        remove_node = True
        if remove_node:
            removal_parent_node = self.find_specific_parent_node(node, "expression_statement")
            if not removal_parent_node:
                removal_parent_node = self.find_specific_parent_node(node, "declaration")
                if removal_parent_node:
                    self.add_declaration_to_removed_declarations(removal_parent_node)
            if not removal_parent_node:
                removal_parent_node = self.find_specific_parent_node(node, "if_statement")
            if not removal_parent_node:
                removal_parent_node = self.find_specific_parent_node(node, "for_statement")
            if not removal_parent_node:
                breakpoint()
            self.removed_nodes.append(removal_parent_node)
        return

    def visit_expression_statement(self, node):
        for child in node.children:
            if child.type in ["call_expression", "assignment_expression"]:
                for child_child in child.children:
                    if child_child.type == "identifier":
                        self.add_expression_to_removal_nodes(child_child, node)

    def remove_nodes(self, nodes_to_remove: set):
        parser = parsers.get_parser(self.LANGUAGE)
        tree = parser.parse(self.content.encode("utf-8"))
        self.nodes_to_remove = nodes_to_remove
        self.traverse_node(tree.root_node)

        self.removed_nodes = list(set(self.removed_nodes))
        self.removed_nodes.sort(key=lambda node: node.start_byte, reverse=True)

        edits = []
        modified_code = tree.text
        visited_nodes = [False] * len(self.removed_nodes)
        for i, removed_node in enumerate(self.removed_nodes):
            if visited_nodes[i]:
                continue

            # Group of overlapping/contained nodes
            overlapping_nodes = [removed_node]

            for j in range(i + 1, len(self.removed_nodes)):
                other_node = self.removed_nodes[j]
                # Check for containment or overlap
                if (other_node.start_byte <= removed_node.end_byte and
                    other_node.end_byte >= removed_node.start_byte):
                    visited_nodes[j] = True
                    overlapping_nodes.append(other_node)
                elif other_node.start_byte > removed_node.end_byte:
                    break  # Since nodes are sorted, no further overlaps are possible

            # Create a single edit for the merged overlapping nodes
            start_byte = min(node.start_byte for node in overlapping_nodes)
            end_byte = max(node.end_byte for node in overlapping_nodes)
            edits.append({
                "start_byte": start_byte,
                "old_end_byte": end_byte,
                "new_end_byte": start_byte,
                "start_point": overlapping_nodes[0].start_point,
                "old_end_point": overlapping_nodes[-1].end_point,
                "new_end_point": overlapping_nodes[0].start_point,
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
    file_name = "./C/gcc-59903/small.c"
    from reducer import utils
    content = utils.read_file(file_name)
    modifier = CDeclarationRemoval(content, nx.DiGraph())
    updated_tree = modifier.remove_nodes(
        {DeclarationNode("safe_lshift_func_int16_t_s_s", "function", None)})
    with open("test_c_file.c", "w") as f:
        f.write(updated_tree)
    # print(updated_tree)
