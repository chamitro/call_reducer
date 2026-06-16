import traceback
from abc import abstractmethod
from typing import Any

import networkx as nx

from reducer import parsers


def remove_empty_lines(source_code):
    lines = source_code.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    return "\n".join(non_empty_lines)


class ASTRemoval(parsers.TreeTraversal):
    def __init__(self, content: str, graph: nx.DiGraph) -> None:
        self.content = content
        self.graph = graph
        self.removals: list[tuple[int, int]] = []
        self.replacements: list[dict[str, Any]] = []

    @abstractmethod
    def remove_nodes(self, nodes_to_remove: set, mode: str) -> str:
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

    def remove_nodes(self, nodes_to_remove: set, mode: str) -> str:
        """
        Removes nodes from Solidity source code.
        
        Args:
            nodes_to_remove: Set of nodes to be removed
            mode: Strategy for handling nodes (currently 'removal' is the primary mode for Solidity)
        
        Returns:
            Modified source code as a string with nodes removed
        """
        if mode not in ["removal"]:
            raise ValueError(f"Unknown mode: {mode}. Must be 'removal'")
        
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
        modified_code = tree.root_node.text
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
        return updated_tree.root_node.text.decode("utf-8")


class CDeclarationRemoval(ASTRemoval):
    LANGUAGE = "c"

    def __init__(self, content, graph):
        super().__init__(content, graph)
        self.removed_nodes = []
        self.removed_declarations = []
        self.goto_statements = []
        self.replaced_assignment_declarations = []
        self.removed_nodes_with_types = {}
        self.constant_values = {
            'int': '0xDEADBEEF',
            'short': '0xDEAD',
            'long': '0xDEADBEEFDEADBEEF',
            'long long': '0xDEADBEEFDEADBEEF',
            'unsigned int': '0xDEADBEEFU',
            'unsigned short': '0xDEADU',
            'unsigned long': '0xDEADBEEFDEADBEEFUL',
            'unsigned long long': '0xDEADBEEFDEADBEEFULL',

            'char': "'X'",
            'unsigned char': "'X'",
            'signed char': "'X'",

            'float': '0xDEADBEEF',
            'double': '0xDEADBEEFDEADBEEF',
            'long double': '0xDEADBEEFDEADBEEF',

            'bool': 'false',
            '_Bool': 'false',

            'void*': 'NULL',
            None: 'NULL',
            'None': 'NULL',
            'void': 'NULL',
            'char*': 'NULL',
            'int*': 'NULL',
            'float*': 'NULL',
            'double*': 'NULL',

            'size_t': '0xDEADBEEF',
            'ssize_t': '0xDEADBEEF',
            'int8_t': '0xDE',
            'uint8_t': '0xDEU',
            'int16_t': '0xDEAD',
            'uint16_t': '0xDEADU',
            'int32_t': '0xDEADBEEF',
            'uint32_t': '0xDEADBEEFU',
            'int64_t': '0xDEADBEEFDEADBEEF',
            'uint64_t': '0xDEADBEEFDEADBEEFULL',

            'struct': '{}',

            'array': 'array[31000]',
}

    def visit_default(self, node):
        pass

    def exit_default(self, node):
        pass

    def get_node_visitor(self, node):
        visitors = {
            "function_definition": self.visit_function_definition,
            "expression_statement": self.visit_expression_statement,
            "call_expression": self.visit_call_expression,
            "goto_statement": self.visit_goto_statement,
            "labeled_statement": self.visit_labeled_statement,
            "declaration": self.visit_declaration,
            "if_statement": self.visit_if_statement,
            "for_statement": self.visit_for_statement,
            "struct_specifier": self.visit_struct_specifier,
            "identifier": self.visit_identifier,
        }
        if self.mode in ["replacement", "combination"]:
            visitors.update({
                "return_statement": self.visit_return_statement,
            })
        return visitors.get(node.type, self.visit_default)

    def get_node_exit(self, node):
        exit_funcs = {
        }
        return exit_funcs.get(node.type, self.exit_default)

    def _add_to_removed_nodes(self, node):
        if node is not None and node not in self.removed_nodes:
            self.removed_nodes.append(node)

    def _add_to_removed_declarations(self, declaration_name):
        if declaration_name not in self.removed_declarations:
            self.removed_declarations.append(declaration_name)

    def _add_declaration_to_removed_declarations(self, declaration_node):
        for declaration_child in declaration_node.children:
            if declaration_child.type == "identifier":
                decl_name = declaration_child.text.decode("utf-8")
                self._add_to_removed_declarations(decl_name)
            elif declaration_child.type in ["init_declarator", "array_declarator"]:
                self._add_declaration_to_removed_declarations(declaration_child)

    def _find_specific_parent_node(self, node, parent_node_type):
        if node is None:
            return
        if node.type == parent_node_type:
            return node
        else:
            return self._find_specific_parent_node(node.parent, parent_node_type)

    def _has_parent_node(self, node, parent_node):
        current = node.parent
        while current is not None:
            if current == parent_node:
                return True
            current = current.parent
        return False

    def _handle_function_definition_removal(self, child, node, node_type):
        child_name = child.text.decode("utf-8")
        if child_name not in self.removed_nodes_with_types:
            self.removed_nodes_with_types[child_name] = node_type
        if child_name in self.removed_declarations:
            return self._add_to_removed_nodes(node)
        for removal_node in self.functions_to_remove:
            if (removal_node.name == child_name
                and node not in self.removed_nodes):
                if child_name == "main":
                    # keep main function but remove code
                    for main_child in node.children:
                        if main_child.type == "compound_statement":
                            for main_code in main_child.children:
                                if main_code.type not in ["{", "}"]:
                                    self._add_to_removed_nodes(main_code)
                else:
                    return self._add_to_removed_nodes(node)

    def _get_node_type(self, child):
        if child.type in ["primitive_type", "sized_type_specifier"]:
            return child.text.decode("utf-8")
        if child.type == "struct_specifier":
            return "struct"
        return None

    def visit_function_definition(self, node):
        """Collects function definition nodes to be removed."""
        node_type = None
        for child in node.children:
            if not node_type:
                node_type = self._get_node_type(child)
            if child.type == "function_declarator":
                for child_child in child.children:
                    if child_child.type == "identifier":
                        return self._handle_function_definition_removal(child_child, node, node_type)
                    elif child_child.type == "parenthesized_declarator":
                        for child_child_child in child_child.children:
                            if child_child_child.type == "identifier":
                                return self._handle_function_definition_removal(child_child_child, node, node_type)

    def _find_expression_statement_removal_parent_node(self, node):
        removal_parent_node = self._find_specific_parent_node(node, "expression_statement")
        if removal_parent_node:
            return removal_parent_node

        removal_parent_node = self._find_specific_parent_node(node, "declaration")
        if removal_parent_node:
            self._add_declaration_to_removed_declarations(removal_parent_node)
            return removal_parent_node

        for parent_type in ["if_statement", "for_statement"]:
            removal_parent_node = self._find_specific_parent_node(node, parent_type)
            if removal_parent_node:
                return removal_parent_node

        return None

    def _handle_call_expression_argument_list(self, child, node, node_type):
        for child_child in child.children:
            if child_child.type == "identifier":
                variable_name = child_child.text.decode("utf-8")
                if variable_name in self.removed_declarations:
                    if self.mode == "replacement":
                        return self.replaced_assignment_declarations.append(
                            (node, self.removed_nodes_with_types[variable_name], None)
                        )
                    else:
                        removal_parent_node = self._find_expression_statement_removal_parent_node(node)
                        return self._add_to_removed_nodes(removal_parent_node)

    def _handle_call_expression_identifier(self, child, node, node_type):
        call_name = child.text.decode("utf-8")
        for removal_node in self.functions_to_remove:
            if removal_node.name == call_name:
                if self.mode == "replacement":
                    return self.replaced_assignment_declarations.append(
                        (node, {"function": call_name}, None)
                    )
                removal_parent_node = self._find_expression_statement_removal_parent_node(node)
                return self._add_to_removed_nodes(removal_parent_node)

    def visit_call_expression(self, node):
        """Identifies and handles method/function calls that use removed functions or variables."""
        # call_expression uses variable from removed declaration in argument list
        for child in node.children:
            if child.type == "argument_list":
                self._handle_call_expression_argument_list(child, node, None)
            # call_expression uses removed function
            if child.type == "identifier":
                self._handle_call_expression_identifier(child, node, None)


    def _handle_expression_statement_identifier(self, child, node, node_type):
        child_name = child.text.decode("utf-8")
        if child_name not in self.removed_nodes_with_types:
            self.removed_nodes_with_types[child_name] = node_type
        if (
            child_name in self.removed_declarations
            and node not in self.removed_nodes
        ):
            if self.mode == "replacement":
                return self.replaced_assignment_declarations.append(
                    (node, self.removed_nodes_with_types[child_name], ";")
                )
            else:
                return self._add_to_removed_nodes(node)
        for removal_node in self.functions_to_remove:
            if (
                removal_node.name == child_name
                and node not in self.removed_nodes
            ):
                if self.mode == "replacement":
                    return self.replaced_assignment_declarations.append(
                        (node, self.removed_nodes_with_types[child_name], ";")
                    )
                else:
                    return self._add_to_removed_nodes(node)

    def visit_expression_statement(self, node):
        """Identifies expression statements that use removed declarations and marks them for removal or replacement."""
        for child in node.children:
            if child.type in ["call_expression", "assignment_expression", "update_expression"]:
                for child_child in child.children:
                    if child_child.type == "identifier":
                        self._handle_expression_statement_identifier(child_child, node, None)
                    elif child_child.type in ["field_expression", "subscript_expression"]:
                        for child_child_child in child_child.children:
                            if child_child_child.type == "identifier":
                                self._handle_expression_statement_identifier(child_child_child, node, None)

    def visit_goto_statement(self, node):
        """Collects goto statements for later analysis of associated labels."""
        if node not in self.goto_statements:
            self.goto_statements.append(node)

    def _handle_go_to_labeled_statement(self, node):
        if node.parent is None:
            return self._add_to_removed_nodes(node)
        if len(node.parent.children) <= 3:
            self._add_to_removed_nodes(node.parent)
        else:
            self._add_to_removed_nodes(node)

    def visit_labeled_statement(self, node):
        """Handles labeled statements and removes associated goto statements if labels are removed."""
        for removal_node in self.removed_nodes:
            if not self._has_parent_node(node, removal_node):
                continue
            for child in node.children:
                if child.type != "statement_identifier":
                    continue
                child_name = child.text.decode("utf-8")
                if child_name in self.removed_nodes:
                    continue
                for goto_statement in self.goto_statements:
                    for goto_child in goto_statement.children:
                        goto_child_name = goto_child.text.decode("utf-8")
                        if goto_child.type == "statement_identifier":
                            if child_name == goto_child_name:
                                self._handle_go_to_labeled_statement(
                                    goto_statement
                                )
                return

    def _add_declaration_to_removal_nodes(self, node, child_name, node_type):
        for removal_node in self.global_variables_to_remove:
            if removal_node.name == child_name:
                self._add_to_removed_nodes(node)
                self._add_to_removed_declarations(child_name)
                if child_name not in self.removed_nodes_with_types:
                    self.removed_nodes_with_types[child_name] = node_type
                removal_parent_node = self._find_specific_parent_node(node, "if_statement")
                if not removal_parent_node:
                    removal_parent_node = self._find_specific_parent_node(node, "for_statement")
                self._add_to_removed_nodes(removal_parent_node)
                return

    def _handle_declaration_init_declarator(self, child, node, node_type):
        for i, child_child in enumerate(child.children):
            if child_child.type == "=":
                previous_node_child = child_child
            if child_child.type == "identifier":
                child_name = child_child.text.decode("utf-8")
                if i < 2:
                    self._add_declaration_to_removal_nodes(node, child_name, node_type)
                elif self.mode == "replacement" and child_name in self.removed_declarations:
                    self.replaced_assignment_declarations.append(
                        (node, node_type, previous_node_child)
                    )
            if child_child.type == "array_declarator":
                return self._handle_declaration_init_declarator(child_child, node, node_type)

    def _handle_declaration_array_declarator(self, child, node, node_type):
        for child_child in child.children:
            if child_child.type == "identifier":
                child_name = child_child.text.decode("utf-8")
                self._add_declaration_to_removal_nodes(node, child_name, node_type)

    def _handle_declaration_function_declarator(self, child, node, node_type):
        for child_child in child.children:
            if child_child.type == "identifier":
                child_name = child_child.text.decode("utf-8")
                for removal_node in self.functions_to_remove:
                    if removal_node.name == child_name:
                        self._add_to_removed_nodes(node)

    def _handle_declaration_identifier(self, child, node, node_type):
        child_name = child.text.decode("utf-8")
        self._add_declaration_to_removal_nodes(node, child_name, node_type)

    def visit_declaration(self, node):
        """Processes variable and function declarations, marking them for removal if they match."""
        node_type = None
        for child in node.children:
            if not node_type:
                node_type = self._get_node_type(child)
            if child.type == "identifier":
                return self._handle_declaration_identifier(child, node, node_type)
            elif child.type == "init_declarator":
                return self._handle_declaration_init_declarator(child, node, node_type)
            elif child.type == "array_declarator":
                return self._handle_declaration_array_declarator(child, node, node_type)
            elif child.type == "function_declarator":
                return self._handle_declaration_function_declarator(child, node, node_type)

    def visit_if_statement(self, node):
        """Marks if statements for removal if they use removed variables or are in removal list."""
        for removal_node in self.if_statements_to_remove:
            _, line_num = removal_node.name.split("_")
            if str(node.start_point[0]) == line_num:
                return self._add_to_removed_nodes(node)
        for child in node.children:
            if child.type == "parenthesized_expression":
                for child_child in child.children:
                    if child_child.type == "identifier":
                        if child_child.text.decode("utf-8") in self.removed_declarations:
                            return self._add_to_removed_nodes(node)

    def visit_for_statement(self, node):
        """Marks for loops for removal if they use removed variables or are in removal list."""
        for removal_node in self.for_statements_to_remove:
            _, line_num = removal_node.name.split("_")
            if str(node.start_point[0]) == line_num:
                return self._add_to_removed_nodes(node)
        for child in node.children:
            if child.type in ["call_expression", "assignment_expression", "update_expression"]:
                for child_child in child.children:
                    if child_child.type == "identifier":
                        if child_child.text.decode("utf-8") in self.removed_declarations:
                            self._add_to_removed_nodes(node)
                        return

    def visit_return_statement(self, node):
        """Handles return statements in replacement mode when they contain removed variables."""
        for i, child in enumerate(node.children):
            if child.type == "return":
                previous_node_child = child
            if child.type == "identifier":
                child_name = child.text.decode("utf-8")
                if child_name in self.removed_declarations:
                    self.replaced_assignment_declarations.append(
                        (node, self.removed_nodes_with_types[child_name], previous_node_child)
                    )

    def visit_identifier(self, node):
        """Identifies and handles identifier uses of removed declarations in different contexts."""
        node_text = node.text.decode("utf-8")
        if node_text in self.removed_declarations:
            parent_node = self._find_specific_parent_node(node, "if_statement")
            if parent_node is not None:
                if self._find_specific_parent_node(node, "compound_statement") is None:
                    return self._add_to_removed_nodes(parent_node)
            parent_node = self._find_specific_parent_node(node, "for_statement")
            if parent_node is not None:
                if self._find_specific_parent_node(node, "compound_statement") is None:
                    return self._add_to_removed_nodes(parent_node)
        if self.mode == "removal":
            return

        if node_text in self.removed_declarations:
            if node_text in self.removed_nodes_with_types:
                for replaced_node, _, _ in self.replaced_assignment_declarations:
                    if self._has_parent_node(node, replaced_node):
                        return
                self.replaced_assignment_declarations.append(
                    (node, self.removed_nodes_with_types[node.text.decode("utf-8")], None)
                )

    def _handle_struct_declaration(self, child, node, node_type):
        if node_type == "parameter_declaration":
            return
        declaration_removal_types = [
            "init_declarator", "pointer_declarator", "array_declarator"
        ]
        for child in node.children:
            if child.type == "identifier":
                self._add_to_removed_declarations(child.text.decode("utf-8"))
                if self.mode == "replacement":
                    return
                else:
                    return self._add_to_removed_nodes(node)
            if child.type in declaration_removal_types:
                for child_child in child.children:
                    if child_child.type == "identifier":
                        self._add_to_removed_declarations(child_child.text.decode("utf-8"))
                        if self.mode != "replacement":
                            return self._add_to_removed_nodes(node)
                    if child_child.type == "array_declarator":
                        for child_child_child in child_child.children:
                            if child_child_child.type == "identifier":
                                self._add_to_removed_declarations(child_child_child.text.decode("utf-8"))
                                if self.mode != "replacement":
                                    return self._add_to_removed_nodes(node)
                                break
                    if child_child.type == "=":
                        previous_node_child = child_child
                        return self.replaced_assignment_declarations.append(
                            (node, "struct", previous_node_child)
                        )

    def visit_struct_specifier(self, node):
        """Processes struct specifiers and removes struct declarations or their fields as needed."""
        for child in node.children:
            if child.type == "type_identifier":
                struct_name = child.text.decode("utf-8")
                removal_struct = False
                for removal_node in self.structs_to_remove:
                    if removal_node.name == struct_name:
                        if len(node.children) < 3:
                            node_type = node.parent.type
                            return self._handle_struct_declaration(node, node.parent, node_type)
                        removal_struct = True
                if not removal_struct:
                    return
            if child.type == "field_declaration_list":
                for struct_fields in child.children:
                    for struct_field in struct_fields.children:
                        if struct_field.type not in ["{", "}"]:
                            self._add_to_removed_nodes(struct_field)

    def replace_assignment_declarations(self, edits):
        for node, node_type, previous_node_child in self.replaced_assignment_declarations:
            if isinstance(node_type, dict):
                node_type = self.removed_nodes_with_types[node_type["function"]]
            overlapping_removal = False
            for removal_node in self.removed_nodes:
                if self._has_parent_node(node, removal_node):
                    overlapping_removal = True
                    break

            if overlapping_removal:
                continue
            if previous_node_child:
                constant_value = f" {self.constant_values[node_type]};".encode("utf-8")
                if previous_node_child == ";":
                    new_end_byte = node.start_byte
                    new_end_byte_with_constant = node.start_byte + len(constant_value)
                    new_end_point = node.start_point
                    new_end_point_with_constant = (node.start_point[0],
                                                node.start_point[1]
                                                + len(constant_value.decode("utf-8")))
                else:
                    new_end_byte = previous_node_child.end_byte
                    new_end_byte_with_constant = previous_node_child.end_byte + len(constant_value)
                    new_end_point = previous_node_child.end_point
                    new_end_point_with_constant = (node.end_point[0],
                                                previous_node_child.end_point[1]
                                                + len(constant_value.decode("utf-8")))
            else:
                # When the replaced declaration is an identifier
                constant_value = f"{self.constant_values[node_type]}".encode("utf-8")
                new_end_byte = node.start_byte
                new_end_byte_with_constant = node.start_byte + len(constant_value)
                new_end_point = node.start_point
                new_end_point_with_constant = (node.start_point[0],
                                            node.start_point[1]
                                            + len(constant_value.decode("utf-8")))
            edits.append({
                "start_byte": node.start_byte,
                "old_end_byte": node.end_byte,
                "new_end_byte": new_end_byte,
                "new_end_byte_with_constant": new_end_byte_with_constant,
                "start_point": node.start_point,
                "old_end_point": node.end_point,
                "new_end_point": new_end_point,
                "new_end_point_with_constant": new_end_point_with_constant,
                "new_text": constant_value
            })


    def remove_nodes(self, nodes_to_remove: set, mode: str) -> str:
        """
        Main entry point for node removal with support for three modes.
        
        Args:
            nodes_to_remove: Set of nodes to be removed
            mode: Strategy for handling nodes - 'removal', 'replacement', or 'combination'
                - 'removal': Simply removes the identified nodes
                - 'replacement': Replaces nodes with constant values based on their type
                - 'combination': Iterates between replacement and removal until fixed point
        
        Returns:
            Modified source code as a string with nodes removed or replaced
        """
        if mode not in ["removal", "replacement", "combination"]:
            raise ValueError(
                f"Unknown mode: {mode}. Must be 'removal', 'replacement', or "
                f"'combination'."
            )
        
        sorted_nodes: list[Any] = sorted([node for node in nodes_to_remove],
                                          key=lambda x: x.name)
        self.mode = mode
        parser = parsers.get_parser(self.LANGUAGE)
        tree = parser.parse(self.content.encode("utf-8"))

        self.functions_to_remove: list[Any] = [node for node in sorted_nodes if node.node_type == "function"]
        self.global_variables_to_remove: list[Any] = [node for node in sorted_nodes if node.node_type == "global_variable"]
        self.structs_to_remove: list[Any] = [node for node in sorted_nodes if node.node_type == "struct"]
        self.if_statements_to_remove: list[Any] = [node for node in sorted_nodes if node.node_type == "if_statement"]
        self.for_statements_to_remove: list[Any] = [node for node in sorted_nodes if node.node_type == "for_statement"]

        try:
            self.traverse_node(tree.root_node)
        except Exception as e:
            print("Modification exception")
            print(traceback.format_exc())
            raise e
        self.removed_nodes.sort(key=lambda node: node.end_byte, reverse=True)

        edits = []
        modified_code = tree.root_node.text
        visited_nodes = [False] * len(self.removed_nodes)
        for i, removed_node in enumerate(self.removed_nodes):
            if visited_nodes[i]:
                continue
            visited_nodes[i] = True

            overlapping_nodes = [removed_node]

            for j in range(i + 1, len(self.removed_nodes)):
                other_node = self.removed_nodes[j]
                if (other_node.start_byte <= removed_node.end_byte and
                    other_node.end_byte >= removed_node.start_byte):
                    visited_nodes[j] = True
                    overlapping_nodes.append(other_node)
                elif other_node.start_byte > removed_node.end_byte:
                    break

            start_byte = min(node.start_byte for node in overlapping_nodes)
            end_byte = max(node.end_byte for node in overlapping_nodes)
            start_point = min(node.start_point for node in overlapping_nodes)
            end_point = max(node.end_point for node in overlapping_nodes)
            edits.append({
                "start_byte": start_byte,
                "old_end_byte": end_byte,
                "new_end_byte": start_byte,
                "start_point": start_point,
                "old_end_point": end_point,
                "new_end_point": start_point,
            })
        if mode in ["replacement", "combination"]:
            self.replace_assignment_declarations(edits)
            edits.sort(key=lambda edit: edit["start_byte"], reverse=True)
        for edit in edits:
            # Apply the edit to the tree
            if "new_text" in edit and mode in ["replacement", "combination"]:
                tree.edit(
                    start_byte=edit["start_byte"],
                    old_end_byte=edit["old_end_byte"],
                    new_end_byte=edit["new_end_byte_with_constant"],
                    start_point=edit["start_point"],
                    old_end_point=edit["old_end_point"],
                    new_end_point=edit["new_end_point_with_constant"],
                )
                # Update the source code
                modified_code = (
                    modified_code[: edit["start_byte"]] +
                    modified_code[edit["start_byte"]:edit["new_end_byte"]] +
                    edit["new_text"] +
                    modified_code[edit["old_end_byte"]:]
                )
            else:
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
        return remove_empty_lines(updated_tree.root_node.text.decode("utf-8"))


class JavaDeclarationRemoval(ASTRemoval):
    LANGUAGE = "java"
    count = 0

    def __init__(self, content, graph):
        super().__init__(content, graph)
        self.removed_nodes = []
        self.parser = parsers.get_parser(self.LANGUAGE)
        self.tree = self.parser.parse(content.encode("utf-8"))
        self.constant_values = {
            "int": "42",
            "boolean": "true",
            "char": "'a'",
            "void": "",
            "Boolean": "true",
            "Integer": "42",
            "String": "\"\"",
            "Object": "null",
            "double": "0.0",
            "float": "0.0f",
            "Double": "0.0",
            "Float": "0.0f",
            "byte": "0",
            "Byte": "0",
            "short": "0",
            "Short": "0",
            "long": "0L",
            "Long": "0L",

        }

    def visit_default(self, node):
        pass

    def exit_default(self, node):
        pass

    def update_tree_incrementally(self, new_content):
        old_tree = self.tree
        self.content = new_content
        self.tree = self.parser.parse(
            new_content.encode("utf-8"),
            old_tree=old_tree
        )

    def delete_nodes(self, tree=None):
        if tree is None:
            tree = self.tree
        self.removed_nodes = self.filter_enclosing_nodes(self.removed_nodes)  # remove duplicates and nested nodes
        self.removed_nodes.sort(key=lambda node: node.start_byte, reverse=True)
        source_code = tree.root_node.text
        modified_code = bytearray(source_code)

        for node in self.removed_nodes:
            start = node.start_byte
            end = node.end_byte
            del modified_code[start:end]

        modified_content = modified_code.decode("utf-8")

        return modified_content

    def get_node_visitor(self, node):
        visitors = {
            "method_declaration": self.visit_function_definition,
            "call_expression": self.visit_call_expression,
        }
        return visitors.get(node.type, self.visit_default)

    def get_node_exit(self, node):
        exit_funcs = {
        }
        return exit_funcs.get(node.type, self.exit_default)

    def is_contained(self, inner, outer):
        return (outer.start_byte <= inner.start_byte and outer.end_byte >= inner.end_byte)

    def filter_enclosing_nodes(self, nodes):
        result = []
        for node in nodes:
            if not any(self.is_contained(node, other) and node != other for other in nodes):
                result.append(node)
        return result

    def break_inheritance(self, nodes_to_remove: set):
        """Removes inheritance declarations (superclass and super_interfaces) from classes being removed."""
        parser = parsers.get_parser(self.LANGUAGE)
        tree = parser.parse(self.content.encode("utf-8"))
        for node in nodes_to_remove:

            class_name = node.name

            query = parsers.JAVA_LANGUAGE.query(f"""
            (class_declaration
            name: (identifier) @class_name
            (#eq? @class_name "{class_name}")) @class
            """)

            captures = query.captures(tree.root_node)
            class_node = None
            for node, capture_name in captures:
                if capture_name == "class":
                    class_node = node
                    break

            if class_node is None:
                continue

            for child in class_node.children:
                if child.type == "superclass" or child.type == "super_interfaces":
                    self.removed_nodes.append(child)

            for child in class_node.children:
                if child.type != "class_body":
                    continue
                for member in child.children:
                    if member.type != "constructor_declaration":
                        continue
                    for ctor_child in member.children:
                        if ctor_child.type != "constructor_body":
                            continue
                        for statement in ctor_child.children:
                            if statement.type == "explicit_constructor_invocation":
                                ctor_field = statement.child_by_field_name("constructor")
                                if ctor_field and ctor_field.type == "super":
                                    self.removed_nodes.append(statement)

        result = self.delete_nodes(tree)

        return result

    def visit_super_calls(self, tree):
        """Handles super() constructor calls and removes their associated superclass inheritance."""
        query = parsers.JAVA_LANGUAGE.query("""
        (
        (explicit_constructor_invocation
            constructor: (super)
            arguments: (argument_list) @args) @super_ctor
        )
        """)
        capt = query.captures(tree.root_node)

        for node, _ in capt:
            current = node
            while current is not None and current.type != "class_declaration":
                current = current.parent
            if current is None:
                # \No class declaration found for super call
                continue
            for child in current.children:
                if child.type == "superclass" or child.type == "super_interfaces":
                    self.removed_nodes.append(child)
                    break

            self.removed_nodes.append(node)

    def visit_function_definition(self, node):
        """Collects method definition nodes to be removed."""
        function_name = None
        for n in node.children:
            if n.type == "identifier":
                function_name = n.text.decode("utf-8")
                break
        if any((node.name == function_name and node.node_type == "function")
               for node in self.nodes_to_remove):
            self.removed_nodes.append(node)

    def visit_call_expression(self, node):
        """Identifies and handles method calls that should be removed or replaced."""
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

    def remove_nodes(self, nodes_to_remove: set, mode: str = "removal") -> str:
        """
        Main entry point for node removal with support for three modes.
        
        Args:
            nodes_to_remove: Set of nodes to be removed
            mode: Strategy for handling nodes - 'removal' or 'replacement'
                - 'removal': Simply removes the identified nodes
                - 'replacement': Replaces nodes with constant values based on their type
                - 'combination': Iterates between replacement and removal until fixed point
        
        Returns:
            Modified source code as a string
        """
        if mode not in ["removal", "replacement"]:
            raise ValueError(
                f"Unknown mode: {mode}. Must be 'removal' or 'replacement'"
            )
    
        self.mode = mode
        
        if mode == "replacement":
            result = self.replace_nodes(nodes_to_remove)
        else:
            result = self.remove_nodes_(nodes_to_remove)

        return result

    def remove_local_variable(self, node_to_remove, tree):
        """Removes local variable declarations and all statements that use them."""
        name = node_to_remove.name
        decl_q = parsers.JAVA_LANGUAGE.query(f"""
        (local_variable_declaration
          declarator: (variable_declarator
            name: (identifier) @var_name 
            (#eq? @var_name "{name}")
          )
        ) @decl
        """)
        for n, cap in decl_q.captures(tree.root_node):
            if cap == "decl":
                self.removed_nodes.append(n)

        id_q = parsers.JAVA_LANGUAGE.query(f"""
        (identifier) @id (#eq? @id "{name}")
        """)
        for n, cap in id_q.captures(tree.root_node):
            if cap == "id":
                stmt = self.find_ancestor(n, 'statement')
                if stmt:
                    self.removed_nodes.append(stmt)

    def remove_class(self, node_to_remove, tree):
        """Removes a class or interface declaration and all usages of that type."""
        name = node_to_remove.name

        query = parsers.JAVA_LANGUAGE.query(f"""
        (class_declaration
            name: (identifier) @class_name
            (#eq? @class_name "{name}")) @class_node

        """)
        query2 = parsers.JAVA_LANGUAGE.query(f"""
                                      (interface_declaration
        name: (identifier) @interface_name
        (#eq? @interface_name "{name}")) @interface_node
         """)
        class_node = None
        for node, capture in query.captures(tree.root_node):
            if capture == "class_node":
                class_node = node
                break

        if class_node is None:
            for node, capture in query2.captures(tree.root_node):
                if capture == "interface_node":
                    class_node = node
                    break
        if class_node is None:
            return

        self.removed_nodes.append(class_node)

        usage_query = parsers.JAVA_LANGUAGE.query(f"""
        (object_creation_expression type: (type_identifier) @used_type
        (#eq? @used_type "{name}")) @expr

        (cast_expression type: (type_identifier) @used_type
        (#eq? @used_type "{name}")) @expr

        (local_variable_declaration
            type: (type_identifier) @used_type
            (#eq? @used_type "{name}")) @stmt

        (field_declaration
            type: (type_identifier) @used_type
            (#eq? @used_type "{name}")) @stmt
        """)
        for node, cap in usage_query.captures(tree.root_node):
            if cap in {"expr", "stmt"}:
                self.removed_nodes.append(node)

    def remove_function(self, node_to_remove, tree):
        """Removes a method definition and all invocations of that method."""
        name = node_to_remove.name
        method_query_str = f'''(method_declaration name: (identifier) @func_name (#eq? @func_name "{name}")) @method'''

        call_query_str = f'''(method_invocation name:(identifier) @call_name (#eq? @call_name "{name}")) @call'''

        method_query = parsers.JAVA_LANGUAGE.query(method_query_str)
        call_query = parsers.JAVA_LANGUAGE.query(call_query_str)

        for node, capture_name in method_query.captures(tree.root_node):
            if capture_name == "method":
                function_args = ""
                for child in node.children:
                    if child.type == "formal_parameters":
                        function_args = child.text.decode("utf-8")
                        break
                if function_args == node_to_remove.args:
                    self.removed_nodes.append(node)
        for node, capture_name in call_query.captures(tree.root_node):
            if capture_name == "call":
                current_node = node
                while current_node.parent is not None:
                    if current_node.type in {
                        "local_variable_declaration",
                        "assignment_expression",
                        "expression_statement",
                        "return_statement",
                        "field_declaration",

                    }:
                        self.removed_nodes.append(current_node)
                        break
                    current_node = current_node.parent
        for node, capture_name in call_query.captures(tree.root_node):
            if capture_name == "call":
                self.removed_nodes.append(node)

    def remove_constructor(self, node_to_remove, tree):
        """Removes a constructor declaration."""
        name = node_to_remove.name
        constructor_query_str = f'''(constructor_declaration name: (identifier) @ctor_name (#eq? @ctor_name "{name}")) @ctor'''
        constructor_query = parsers.JAVA_LANGUAGE.query(constructor_query_str)
        for node, capture_name in constructor_query.captures(tree.root_node):
            if capture_name == "ctor":
                self.removed_nodes.append(node)

    def remove_field(self, node_to_remove, tree):
        """Removes a field declaration and all statements that access it."""
        name = node_to_remove.name
        field_decl_query_str = f'''( (field_declaration declarator: (variable_declarator name: (identifier) @field_name value: (_) @field_value ) ) (#eq? @field_name "{name}") )'''

        field_access_query_str = f'''
        (expression_statement
            (assignment_expression
            left: (field_access
                    field: (identifier) @field_name
                    (#eq? @field_name "{name}")))) @stmt

        (expression_statement
            (field_access
            field: (identifier) @field_name
            (#eq? @field_name "{name}"))) @stmt

        (return_statement
            (field_access
            field: (identifier) @field_name
            (#eq? @field_name "{name}"))) @stmt'''

        access_query = parsers.JAVA_LANGUAGE.query(field_access_query_str)

        field_query = parsers.JAVA_LANGUAGE.query(field_decl_query_str)

        for node, capture_name in field_query.captures(tree.root_node):
            if capture_name == "field_value":
                self.removed_nodes.append(node)
                if node.prev_sibling is not None:
                    if node.prev_sibling.type == "=":
                        self.removed_nodes.append(node.prev_sibling)

        for node, capture_name in access_query.captures(tree.root_node):
            if capture_name == "stmt":
                self.removed_nodes.append(node)
        decl_query_str = f'''
            (field_declaration
            declarator: (variable_declarator
                name: (identifier) @field_name
                (#eq? @field_name "{name}")
            )
            ) @decl
            '''
        access_captures = access_query.captures(tree.root_node)
        decl_query = parsers.JAVA_LANGUAGE.query(decl_query_str)
        decl_captures = decl_query.captures(tree.root_node)

        if decl_captures and not access_captures:
            for node, capture_name in decl_captures:
                if capture_name == "decl":
                    self.removed_nodes.append(node)

    def remove_nodes_(self, nodes_to_remove: set):
        """Main removal logic that identifies and removes specific node types from the Java source."""
        self.removed_nodes = []
        self.count += 1
        parser = parsers.get_parser(self.LANGUAGE)
        tree = parser.parse(self.content.encode("utf-8"))
        self.nodes_to_remove = nodes_to_remove

        for node_to_remove in self.nodes_to_remove:
            node_type = node_to_remove.node_type
            match node_type:
                case "function":
                    self.remove_function(node_to_remove, tree)
                case "constructor":
                    self.remove_constructor(node_to_remove, tree)
                case "field":
                    self.remove_field(node_to_remove, tree)
                case "class":
                    self.remove_class(node_to_remove, tree)
                case "local_variable":
                    self.remove_local_variable(node_to_remove, tree)

        result = self.delete_nodes(tree)

        return result

    def find_ancestor(self, node, typ):
        cur = node.parent
        while cur:
            if cur.type == typ:
                return cur
            cur = cur.parent
        return None

    def node_in_subtree(self, target, root):
        if root is None:
            return False
        if target == root:
            return True
        for c in root.children:
            if self.node_in_subtree(target, c):
                return True
        return False

    def is_read_context(self, node):
        decl = self.find_ancestor(node, 'variable_declarator')
        if decl and decl.child_by_field_name('name') == node:
            return False

        param = self.find_ancestor(node, 'formal_parameter')
        if param and param.child_by_field_name('name') == node:
            return False

        assign = self.find_ancestor(node, 'assignment_expression')
        if assign:
            left = assign.child_by_field_name('left') or (assign.children[0] if assign.children else None)
            if left and self.node_in_subtree(node, left):
                return False

        return True

    def replace_field(self, node_to_replace, tree):
        """Finds field access nodes to replace with constant values in replacement mode."""
        name = node_to_replace.name
        access_query = parsers.JAVA_LANGUAGE.query(f'''
        ;; Initializers: int z = x; int y = this.x;
        (variable_declarator
            value: (identifier) @use
            (#eq? @use {name}))
        (variable_declarator
            value: (field_access
                    field: (identifier) @field_name
                    (#eq? @field_name {name})) @use)

        ;; RHS of assignments: z = x; z = this.x;
        (assignment_expression
            right: (identifier) @use
            (#eq? @use {name}))
        (assignment_expression
            right: (field_access
                    field: (identifier) @field_name
                    (#eq? @field_name {name})) @use)

        ;; Argument: approve(x); approve(this.x);
        (argument_list
            (identifier) @use
            (#eq? @use {name}))
        (argument_list
            (field_access
                    field: (identifier) @field_name
                    (#eq? @field_name {name})) @use)

        ;; Return: return x; return this.x;
        (return_statement
            (identifier) @use
            (#eq? @use {name}))
        (return_statement
            (field_access
                    field: (identifier) @field_name
                    (#eq? @field_name {name})) @use)

        ;; Binary expression: x + y, y + x, this.x + ... 
        (binary_expression
            left: (identifier) @use
            (#eq? @use {name}))
        (binary_expression
            right: (identifier) @use
            (#eq? @use {name}))
        (binary_expression
            left: (field_access
                    field: (identifier) @field_name
                    (#eq? @field_name {name})) @use)
        (binary_expression
            right: (field_access
                    field: (identifier) @field_name
                    (#eq? @field_name {name})) @use)
        ''')

        decl_query_str = f'''
            (field_declaration
            type: (_) @field_type
            declarator: (variable_declarator
                name: (identifier) @field_name
                (#eq? @field_name "{name}")
            )
            ) @decl
            '''

        query = parsers.JAVA_LANGUAGE.query(decl_query_str)
        captures = query.captures(tree.root_node)

        field_type = None
        source_code = tree.root_node.text
        code = bytearray(source_code)

        for node, cap in captures:
            text = code[node.start_byte:node.end_byte].decode()
            if cap == "field_name":
                field_name = text
            elif cap == "field_type":
                field_type = text

        query = access_query
        captures = query.captures(tree.root_node)  # capture access
        nodes_to_replace = []
        for node, cap_name in captures:
            if not self.is_read_context(node):  # make sure it's not LHS
                continue
            nodes_to_replace.append(node)

        result = (nodes_to_replace, field_type)

        return result

    def replace_function(self, node_to_replace, tree):
        """Finds method invocations to replace with constant return values in replacement mode."""
        name = node_to_replace.name
        source_code = tree.root_node.text

        decl_query_str = f'''
            (method_declaration type: (_) @return_type 
            name: (identifier) @func_name 
            parameters: (formal_parameters) @params 
            (#eq? @func_name {name} ))'''

        decl_query = parsers.JAVA_LANGUAGE.query(decl_query_str)
        rt = None
        for node, capture_name in decl_query.captures(tree.root_node):
            if capture_name == "return_type":
                rt = source_code[node.start_byte:node.end_byte].decode("utf-8").strip()

        call_query_str = f'''
        (
        (method_invocation
            name: (identifier) @call_name (#eq? @call_name "{name}")
            arguments: (argument_list) @args
        ) @call
        )
        '''

        call_query = parsers.JAVA_LANGUAGE.query(call_query_str)

        nodes_to_replace = []
        call_arg_types = {}
        for node, capture_name in call_query.captures(tree.root_node):
            if capture_name == "call":
                nodes_to_replace.append(node)
                arg_list_node = None
                for child in node.children:
                    if child.type == "argument_list":
                        arg_list_node = child
                        break
                if arg_list_node:
                    arg_types = self.extract_arg_types(
                        arg_list_node)  # tried handling overloading here, if failed, just boils down to return type
                    arg_types = arg_types if arg_types else rt
                else:
                    arg_types = rt
                call_arg_types[node] = arg_types

        result = (nodes_to_replace, rt)

        return result

    def replace_local_variable(self, node_to_replace, tree):
        """Finds read uses of local variables and returns them with their type for replacement mode."""
        name = node_to_replace.name
        decl_query = parsers.JAVA_LANGUAGE.query(f'''
        (local_variable_declaration
            type: (_) @var_type
            declarator: (variable_declarator
                name: (identifier) @var_name (#eq? @var_name "{name}")
            )
        )
        ''')
        var_type = None
        for n, cap in decl_query.captures(tree.root_node):
            if cap == "var_type":
                var_type = tree.root_node.text[n.start_byte:n.end_byte].decode("utf-8").strip()

        use_query = parsers.JAVA_LANGUAGE.query(f'''
        ;; initializer RHS: int x = a;
        (variable_declarator
            name: (_)
            value: (identifier) @use1 (#eq? @use1 "{name}")
        )
        ;; assignment RHS: x = a;
        (assignment_expression right: (identifier) @use2 (#eq? @use2 "{name}"))
        ;; return x;
        (return_statement (identifier) @use3 (#eq? @use3 "{name}"))
        ;; argument: foo(x)
        (argument_list (identifier) @use4 (#eq? @use4 "{name}"))
        ;; binary ops: x  y, y  x
        (binary_expression left: (identifier) @use5 (#eq? @use5 "{name}"))
        (binary_expression right: (identifier) @use6 (#eq? @use6 "{name}"))
        ''')

        to_replace = []
        for n, cap in use_query.captures(tree.root_node):
            if cap.startswith("use") and self.is_read_context(n):
                to_replace.append(n)

        result = to_replace, var_type

        return result

    def replace_nodes(self, nodes_to_remove: set):
        """Replaces nodes with appropriate constant values based on their type in replacement mode."""
        parser = parsers.get_parser(self.LANGUAGE)
        tree = parser.parse(self.content.encode("utf-8"))
        source_code = tree.root_node.text
        self.nodes_to_remove = nodes_to_remove
        nodes_to_replace = []
        mapping = dict()
        for node in self.nodes_to_remove:
            if node.node_type == 'field':
                fields_to_replace = self.replace_field(node, tree)
                nodes_to_replace.append(fields_to_replace)

            elif node.node_type == 'function':
                functions_to_replace = self.replace_function(node, tree)
                nodes_to_replace.append(functions_to_replace)
            elif node.node_type == 'local_variable':
                locals_to_replace = self.replace_local_variable(node, tree)
                nodes_to_replace.append(locals_to_replace)
        for arr, typ in nodes_to_replace:
            for n in arr:
                mapping[n] = typ
        nodes_to_replace = [n for n, _ in nodes_to_replace]
        nodes_to_replace = [item for sub in nodes_to_replace for item in sub]

        nodes_to_replace = sorted(set(nodes_to_replace), key=lambda n: n.start_byte, reverse=True)
        nodes_to_replace = self.filter_enclosing_nodes(nodes_to_replace)
        modified_code = bytearray(source_code)

        for node in nodes_to_replace:

            constant_value = self.constant_values.get(
                mapping.get(node, None), None
            )
            if constant_value is None:
                typ = mapping.get(node, None)
                if typ:
                    constant_value = f"({typ}) null"
            replacement_text = constant_value.encode("utf-8")
            start = node.start_byte
            end = node.end_byte
            modified_code[start:end] = replacement_text
        modified_code = modified_code.decode("utf-8")  # type: ignore[assignment]
        self.content = modified_code  # type: ignore[assignment]

        result = modified_code

        return result

    def extract_param_types(self, params_text):
        params_text = params_text.strip()
        if params_text.startswith("(") and params_text.endswith(")"):
            inner = params_text[1:-1].strip()
        else:
            inner = params_text
        if not inner:
            return tuple()
        params = [p.strip() for p in inner.split(",")]
        types = []
        for p in params:
            tokens = p.split()
            if tokens:
                types.append(tokens[0])
        return tuple(types)

    def get_literal_type(self, node):

        typemap = {
            "decimal_integer_literal": "int",
            "boolean_literal": "boolean",
            "character_literal": "char"
        }
        return typemap.get(node.type, None)

    def extract_arg_types(self, arg_list_node):

        arg_types = []
        for child in arg_list_node.children:
            t = self.get_literal_type(child)
            if t is not None:
                arg_types.append(t)
        return tuple(arg_types)


AST_REMOVALS = {
    "solidity": SolidityDeclarationRemoval,
    "c": CDeclarationRemoval,
    "java": JavaDeclarationRemoval,
}
