from abc import abstractmethod

import networkx as nx

from reducer import parsers
from reducer.graph import DeclarationNode


def remove_empty_lines(source_code):
    lines = source_code.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    return "\n".join(non_empty_lines)


class ASTRemoval(parsers.TreeTraversal):
    def __init__(self, content, graph: nx.DiGraph):
        self.content = content
        self.graph = graph
        self.removals = []
        self.replacements = []

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

    def remove_nodes(self, nodes_to_remove: set, mode: str):
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
        self.goto_statements = []
        self.replaced_assignment_declarations = []
        self.removed_nodes_with_types = {}
        self.dummy_values = {
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
        }
        if self.mode in ["replacement", "combination"]:

            visitors.update({
                "return_statement": self.visit_return_statement,
                "identifier": self.visit_identifier,
            })
        return visitors.get(node.type, self.visit_default)

    def get_node_exit(self, node):
        exit_funcs = {
        }
        return exit_funcs.get(node.type, self.exit_default)

    def _add_declaration_to_removed_declarations(self, declaration_node):
        for declaration_child in declaration_node.children:
            if declaration_child.type == "identifier":
                decl_name = declaration_child.text.decode("utf-8")
                if decl_name not in self.removed_declarations:
                    self.removed_declarations.append(decl_name)
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
        if (
            child_name in self.removed_declarations
            and node not in self.removed_nodes
        ):
            return self.removed_nodes.append(node)
        for removal_node in self.nodes_to_remove:
            if (removal_node.name == child_name
                and removal_node.node_type == "function"
                and node not in self.removed_nodes):
                if child_name == "main":
                    # keep main function but remove code
                    for main_child in node.children:
                        if main_child.type == "compound_statement":
                            self.removed_nodes.extend(
                                [
                                    main_code for main_code in main_child.children
                                    if main_code.type not in ["{", "}"]
                                ]
                            )
                else:
                    return self.removed_nodes.append(node)

    def _get_node_type(self, child):
        if child.type in ["primitive_type", "sized_type_specifier"]:
            return child.text.decode("utf-8")
        if child.type == "struct_specifier":
            return "struct"
        return None

    def visit_function_definition(self, node):
        node_type = None
        for child in node.children:
            if not node_type:
                node_type = self._get_node_type(child)
            if child.type == "function_declarator":
                for child_child in child.children:
                    if child_child.type == "identifier":
                        self._handle_function_definition_removal(child_child, node, node_type)
                        return
                    elif child_child.type == "parenthesized_declarator":
                        for child_child_child in child_child.children:
                            if child_child_child.type == "identifier":
                                self._handle_function_definition_removal(child_child_child, node, node_type)
                                return

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
                        if removal_parent_node not in self.removed_nodes:
                            return self.removed_nodes.append(removal_parent_node)

    def _handle_call_expression_identifier(self, child, node, node_type):
        call_name = child.text.decode("utf-8")
        for removal_node in self.nodes_to_remove:
            if (
                removal_node.name == call_name
                and removal_node.node_type == "function"
            ):
                if self.mode == "replacement":
                    return self.replaced_assignment_declarations.append(
                        (node, {"function": call_name}, None)
                    )
                removal_parent_node = self._find_expression_statement_removal_parent_node(node)
                if removal_parent_node not in self.removed_nodes:
                    return self.removed_nodes.append(removal_parent_node)

    def visit_call_expression(self, node):
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
                return self.removed_nodes.append(node)
        for removal_node in self.nodes_to_remove:
            if (
                removal_node.name == child_name
                and removal_node.node_type == "function"
                and node not in self.removed_nodes
            ):
                if self.mode == "replacement":
                    return self.replaced_assignment_declarations.append(
                        (node, self.removed_nodes_with_types[child_name], ";")
                    )
                else:
                    return self.removed_nodes.append(node)

    def visit_expression_statement(self, node):
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
        if node not in self.goto_statements:
            self.goto_statements.append(node)

    def _handle_go_to_labeled_statement(self, node):
        if node.parent is None:
            self.removed_nodes.append(node)
            return
        if len(node.parent.children) <= 3:
            self.removed_nodes.append(node.parent)
        else:
            self.removed_nodes.append(node)

    def visit_labeled_statement(self, node):
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
        for removal_node in self.nodes_to_remove:
            if (
                removal_node.name == child_name
                and removal_node.node_type == "global_variable"
                and node not in self.removed_nodes
                and child_name not in self.removed_declarations
            ):
                self.removed_nodes.append(node)
                self.removed_declarations.append(child_name)
                if child_name not in self.removed_nodes_with_types:
                    self.removed_nodes_with_types[child_name] = node_type
                removal_parent_node = self._find_specific_parent_node(node, "if_statement")
                if not removal_parent_node:
                    removal_parent_node = self._find_specific_parent_node(node, "for_statement")
                if removal_parent_node and removal_parent_node not in self.removed_nodes:
                    self.removed_nodes.append(removal_parent_node)
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
                for removal_node in self.nodes_to_remove:
                    if (
                        removal_node.name == child_name
                        and removal_node.node_type == "function"
                        and node not in self.removed_nodes
                    ):
                        self.removed_nodes.append(node)

    def _handle_declaration_identifier(self, child, node, node_type):
        child_name = child.text.decode("utf-8")
        self._add_declaration_to_removal_nodes(node, child_name, node_type)

    def visit_declaration(self, node):
        node_type = None
        for child in node.children:
            if not node_type:
                node_type = self._get_node_type(child)
            if child.type == "identifier":
                self._handle_declaration_identifier(child, node, node_type)
                return
            elif child.type == "init_declarator":
                self._handle_declaration_init_declarator(child, node, node_type)
                return
            elif child.type == "array_declarator":
                self._handle_declaration_array_declarator(child, node, node_type)
                return
            elif child.type == "function_declarator":
                self._handle_declaration_function_declarator(child, node, node_type)
                return

    def visit_if_statement(self, node):
        for removal_node in self.nodes_to_remove:
            if removal_node.node_type == "if_statement":
                _, line_num = removal_node.name.split("_")
                if str(node.start_point[0]) == line_num:
                    self.removed_nodes.append(node)
                    return
        for child in node.children:
            if child.type == "parenthesized_expression":
                for child_child in child.children:
                    if child_child.type == "identifier":
                        if child_child.text.decode("utf-8") in self.removed_declarations:
                            self.removed_nodes.append(node)
                        return

    def visit_for_statement(self, node):
        for removal_node in self.nodes_to_remove:
            if removal_node.node_type == "for_statement":
                _, line_num = removal_node.name.split("_")
                if str(node.start_point[0]) == line_num:
                    self.removed_nodes.append(node)
                    return
        for child in node.children:
            if child.type in ["call_expression", "assignment_expression", "update_expression"]:
                for child_child in child.children:
                    if child_child.type == "identifier":
                        if child_child.text.decode("utf-8") in self.removed_declarations:
                            self.removed_nodes.append(node)
                        return

    def visit_return_statement(self, node):
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
        node_text = node.text.decode("utf-8")
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
                self.removed_declarations.append(child.text.decode("utf-8"))
                if self.mode == "replacement":
                    return
                else:
                    return self.removed_nodes.append(node)
            if child.type in declaration_removal_types:
                for child_child in child.children:
                    if child_child.type == "identifier":
                        self.removed_declarations.append(child_child.text.decode("utf-8"))
                        if self.mode != "replacement":
                            return self.removed_nodes.append(node)
                    if child_child.type == "array_declarator":
                        for child_child_child in child_child.children:
                            if child_child_child.type == "identifier":
                                self.removed_declarations.append(child_child_child.text.decode("utf-8"))
                                if self.mode != "replacement":
                                    return self.removed_nodes.append(node)
                                break
                    if child_child.type == "=":
                        previous_node_child = child_child
                        return self.replaced_assignment_declarations.append(
                            (node, "struct", previous_node_child)
                        )

    def visit_struct_specifier(self, node):
        for child in node.children:
            if child.type == "type_identifier":
                struct_name = child.text.decode("utf-8")
                removal_struct = False
                for removal_node in self.nodes_to_remove:
                    if (
                        removal_node.node_type == "struct"
                        and removal_node.name == struct_name
                    ):
                        if len(node.children) < 3:
                            node_type = node.parent.type
                            return self._handle_struct_declaration(node, node.parent, node_type)
                        removal_struct = True
                if not removal_struct:
                    return
            if child.type == "field_declaration_list":
                for struct_fields in child.children:
                    self.removed_nodes.extend(
                        [
                            struct_field for struct_field in struct_fields.children
                            if struct_field.type not in ["{", "}"]
                        ]
                    )

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
                dummy_value = f" {self.dummy_values[node_type]};".encode("utf-8")
                if previous_node_child == ";":
                    new_end_byte = node.start_byte
                    new_end_byte_with_dummy = node.start_byte + len(dummy_value)
                    new_end_point = node.start_point
                    new_end_point_with_dummy = (node.start_point[0],
                                                node.start_point[1]
                                                + len(dummy_value.decode("utf-8")))
                else:
                    new_end_byte = previous_node_child.end_byte
                    new_end_byte_with_dummy = previous_node_child.end_byte + len(dummy_value)
                    new_end_point = previous_node_child.end_point
                    new_end_point_with_dummy = (node.end_point[0],
                                                previous_node_child.end_point[1]
                                                + len(dummy_value.decode("utf-8")))
            else:
                # When the replaced declaration is an identifier
                dummy_value = f"{self.dummy_values[node_type]}".encode("utf-8")
                new_end_byte = node.start_byte
                new_end_byte_with_dummy = node.start_byte + len(dummy_value)
                new_end_point = node.start_point
                new_end_point_with_dummy = (node.start_point[0],
                                            node.start_point[1]
                                            + len(dummy_value.decode("utf-8")))
            edits.append({
                "start_byte": node.start_byte,
                "old_end_byte": node.end_byte,
                "new_end_byte": new_end_byte,
                "new_end_byte_with_dummy": new_end_byte_with_dummy,
                "start_point": node.start_point,
                "old_end_point": node.end_point,
                "new_end_point": new_end_point,
                "new_end_point_with_dummy": new_end_point_with_dummy,
                "new_text": dummy_value
            })


    def remove_nodes(self, nodes_to_remove: set, mode: str):
        self.mode = mode
        parser = parsers.get_parser(self.LANGUAGE)
        tree = parser.parse(self.content.encode("utf-8"))

        self.nodes_to_remove = nodes_to_remove
        self.traverse_node(tree.root_node)
        self.removed_nodes.sort(key=lambda node: node.end_byte, reverse=True)

        edits = []
        modified_code = tree.text
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
                    new_end_byte=edit["new_end_byte_with_dummy"],
                    start_point=edit["start_point"],
                    old_end_point=edit["old_end_point"],
                    new_end_point=edit["new_end_point_with_dummy"],
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
        return remove_empty_lines(updated_tree.text.decode("utf-8"))


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
        # {DeclarationNode("func_129", "function", None)}
        {DeclarationNode("g_3", "declaration", None)}, "combination"
    )
    with open("test_c_file.c", "w") as f:
        f.write(updated_tree)
    # print(updated_tree)
