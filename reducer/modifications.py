from abc import ABC, abstractmethod
import re

import networkx as nx
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from reducer.grammars.solidity.SolidityLexer import SolidityLexer
from reducer.grammars.solidity.SolidityParser import SolidityParser
from reducer.grammars.solidity.SolidityListener import SolidityListener

from reducer.grammars.c.CLexer import CLexer
from reducer.grammars.c.CParser import CParser
from reducer.grammars.c.CListener import CListener

class ASTRemoval(ABC):
    def __init__(self, tree, graph: nx.DiGraph):
        self.tree = tree
        self.graph = graph
        self.removals = []
        self.replacements = []

    @abstractmethod
    def remove_nodes(self, source_code: str, nodes_to_remove: set,
                     removed_nodes: set) -> str:
        pass

    @abstractmethod
    def setup_parse_tree(self, source_code: str):
        pass

class CDeclarationRemoval(CListener, ASTRemoval):
    def __init__(self, tree, graph):
        super().__init__(tree, graph)
    
    def remove_use_site(self, ctx):
        text = ctx.getText()
        print(self.nodes_to_remove)
        print(f"eimaste stin remove_use_site kai to text einai:", text)
        if any(node.name + "(" in text for node in self.nodes_to_remove):
            equal_sign_index = text.find('=')
            if equal_sign_index != -1:
                start = ctx.start.start + equal_sign_index + 1
                stop = ctx.stop.stop
                if (stop < ctx.stop.stop
                        and text[stop - ctx.start.start] == ';'):
                    stop += 1
                stop -= 1
                self.removals.append((start, stop))
            else:
                self.removals.append((ctx.start.start, ctx.stop.stop))
        for node in self.nodes_to_remove:
                # Create a regex pattern to match the node name as a whole word
                pattern = re.compile(r'\b' + re.escape(node.name) + r'\b')
                if pattern.search(text):
                    print(f"BIKAME, VRIKAME KAPOIO NODE NAME NA ADISTOIXEI STO TEXT:", text)
                    self.removals.append((ctx.start.start, ctx.stop.stop))
                    break

    def get_base_name(self, name):
        # Regular expression to match 'bla[...]'
        match = re.match(r'([a-zA-Z_]\w*)\[\d*\]', name)
        if match:
            return match.group(1)
        return name

    def enterFunctionDefinition(self, ctx):
        # Extract function name from declarator context
        function_name = ctx.declarator().directDeclarator().getText()
#        print(function_name)
        fun2 = function_name.split('(', 1)[0]
#        print(fun2)
        if any((node.name == fun2 and node.node_type == "function")
               for node in self.nodes_to_remove):
            print("BIKAME STO FUNCTION")
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterDeclaration(self, ctx: CParser.DeclarationContext):
    # Check if the declaration is a typedef
        is_typedef = False
        typedef_name = None

    # Check for typedef and process specifiers
        for specifier in ctx.declarationSpecifiers().declarationSpecifier():
            specifier_text = specifier.getText()
            print(f"Specifier: {specifier_text}")
            if specifier_text == 'typedef':
                print("BIKAME STIN TYPEDEFFFFFFFFFFFFFFFFFF")
                is_typedef = True
                print(is_typedef)
            if any((node.name == specifier_text and node.node_type == "var") for node in self.nodes_to_remove):
                is_typedef = True

        print(f"Context: {ctx.getText()}")
        print(f"DeclarationSpecifiers: {ctx.declarationSpecifiers().getText()}")
        print(f"InitDeclaratorList: {ctx.initDeclaratorList()}")

        init_declarator_list = ctx.initDeclaratorList()

        if not init_declarator_list and is_typedef:
            print("No InitDeclaratorList found, handling typedef without initDeclaratorList.")
            print(ctx.getText())
            self.removals.append((ctx.start.start, ctx.stop.stop + 1))
            # Handle typedef without initDeclaratorList (e.g., typedef struct { ... } Person;)
            # Extract the last identifier in the declaration specifiers as the typedef name
        
        if not init_declarator_list:
            print("No InitDeclaratorList found, returning.")
            return
        print(is_typedef)
        
        if is_typedef:
        # Handle typedefs
            print("EXOUME TYPEDEF")
            for init_declarator in init_declarator_list.initDeclarator():
                declarator = init_declarator.declarator()
                if declarator:
                    typedef_name = declarator.getText()
                    print(f"Typedef name: {typedef_name}")
                    if any((node.name == typedef_name and node.node_type == "typedef") for node in self.nodes_to_remove):
                        print(f"Removing typedef: {typedef_name}")
                        self.removals.append((ctx.start.start, ctx.stop.stop + 1))
        else:
        # Handle variables, excluding function arguments
            for init_declarator in init_declarator_list.initDeclarator():
                declarator = init_declarator.declarator()
                if declarator:
                    var_name = declarator.getText()

                # Check if the variable is a function argument
                if any((node.name == self.get_base_name(var_name) and node.node_type == "var") for node in self.nodes_to_remove):
                    print(f"Removing variable: {var_name}")
                    self.removals.append((ctx.start.start, ctx.stop.stop + 1))

    def enterStructOrUnionSpecifier(self, ctx):
        if ctx.Identifier():
            struct_name = ctx.Identifier().getText()
            if any((node.name == struct_name and node.node_type == "struct")
               for node in self.nodes_to_remove):
                self.removals.append((ctx.start.start, ctx.stop.stop+1))

    def enterExpressionStatement(
            self, ctx: CParser.ExpressionStatementContext):
#        print(f"BIKAME SE EXPRESSSSSSSSSSSION",ctx.getText())
#        expr = ctx.getText()
#        if any((node.name in expr and node.node_type == "var")
#               for node in self.nodes_to_remove):
#                self.removals.append((ctx.start.start, ctx.stop.stop+1))
        print("EXPRESSIONS")
        self.remove_use_site(ctx)
    
#    def enterAssignmentExpression(self, ctx: CParser.AssignmentExpressionContext):
##        self.remove_use_site(ctx)
#        assignment = ctx.getText()
#        print(f"EIMASTE SE ASSIGMENT:", assignment)

#        # Get the base name of the assignment
##        assignment_base_name = self.get_base_name(assignment)
#        
#        # Check if the base name of the assignment matches any node to be removed
#        if any(self.get_base_name(node.name) in assignment and node.node_type == "var"
#               for node in self.nodes_to_remove):
#            print(f"THA KANOUME REMOVE TO ASSIGMENT", assignment)
#            self.removals.append((ctx.start.start, ctx.stop.stop))

    def remove_nodes(self, source_code, nodes_to_remove: set, removed_nodes: set):
        self.nodes_to_remove = nodes_to_remove
        print(f"EIMASTE STIN REMOVE NODES:",nodes_to_remove)
        self.removed_nodes = removed_nodes.union(nodes_to_remove)
        walker = ParseTreeWalker()
        walker.walk(self, self.tree)
        for start, stop in sorted(self.removals, reverse=True):
            print("BIKAME RE NA KANOUME TA REMOVALS")
            code_block = source_code[start:stop + 1]
            if any(node.name in code_block for node in self.nodes_to_remove):
                source_code = source_code[:start] + \
                    (len(code_block) * " ") + source_code[stop + 1:]
#            print(source_code)
        source_code = source_code.replace(r"/\s\s+/g", ' ')
        modified_source_code = re.sub(r'\n\s*\n', '\n\n', source_code)
#        print(modified_source_code)
        return modified_source_code

    @classmethod
    def setup_parse_tree(self, source_code: str):
        lexer = CLexer(InputStream(source_code))
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        return parser.compilationUnit()


class SolidityDeclarationRemoval(SolidityListener, ASTRemoval):
    def __init__(self, tree, graph):
        super().__init__(tree, graph)

    def remove_use_site(self, ctx):
        text = ctx.getText()
        if any(node.name + "(" in text for node in self.nodes_to_remove):
            equal_sign_index = text.find('=')
            if equal_sign_index != -1:
                start = ctx.start.start + equal_sign_index + 1
                stop = ctx.stop.stop
                if (stop < ctx.stop.stop
                        and text[stop - ctx.start.start] == ';'):
                    stop += 1
                stop -= 1
                self.removals.append((start, stop))
            else:
                self.removals.append((ctx.start.start, ctx.stop.stop))
        elif any(node.name in text for node in self.nodes_to_remove):
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterFunctionDefinition(self,
                                ctx: SolidityParser.FunctionDefinitionContext):
        functions_name = ctx.getChild(0).getText()
        function_name = functions_name.replace("function", "").strip()
        if any((node.name == function_name and node.node_type == "function")
               for node in self.nodes_to_remove):
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterModifierInvocation(self,
                                ctx: SolidityParser.ModifierInvocationContext):
        modifier_name = ctx.getChild(0).getText()
        if any((node.name == modifier_name and node.node_type == "function")
               for node in self.nodes_to_remove):
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterModifierDefinition(self,
                                ctx: SolidityParser.ModifierDefinitionContext):
        self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterStructDefinition(self,
                              ctx: SolidityParser.StructDefinitionContext):
        struct_name = ctx.getChild(1).getText()
        if any((node.name == struct_name and node.node_type == "struct")
               for node in self.nodes_to_remove):
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterEventDefinition(self, ctx: SolidityParser.EventDefinitionContext):
        event_name = ctx.getChild(1).getText()
        if any((node.name == event_name and node.node_type == "event")
               for node in self.nodes_to_remove):
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterEmitStatement(self, ctx: SolidityParser.EmitStatementContext):
        emit_name = ctx.getChild(1).getText()
        if any((node.name == emit_name and node.node_type == "event")
               for node in self.nodes_to_remove):
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterStateVariableDeclaration(
            self, ctx: SolidityParser.StateVariableDeclarationContext):
        variable_name = None
        for i in range(ctx.getChildCount()):
            if isinstance(ctx.getChild(i), SolidityParser.IdentifierContext):
                variable_name = ctx.getChild(i).getText()
                break

        if variable_name:
            if any((node.name == variable_name
                    and node.node_type == "state_var")
                   for node in self.nodes_to_remove):
#                print(f"Marking state variable '{variable_name}' for removal.")
                self.removals.append((ctx.start.start, ctx.stop.stop))

    def enterSimpleStatement(self,
                             ctx: SolidityParser.ExpressionStatementContext):
        self.remove_use_site(ctx)

    def enterReturnStatement(self, ctx: SolidityParser.ReturnStatementContext):
        self.remove_use_site(ctx)

    def enterExpressionStatement(
            self, ctx: SolidityParser.ExpressionStatementContext):
        self.remove_use_site(ctx)

    def enterVariableDeclarationStatement(
            self, ctx: SolidityParser.VariableDeclarationStatementContext):
        self.remove_use_site(ctx)

    def enterContractDefinition(self,
                                ctx: SolidityParser.ContractDefinitionContext):
        # Find the identifier in the children
        identifier = None
        for i in range(ctx.getChildCount()):
            if isinstance(ctx.getChild(i), SolidityParser.IdentifierContext):
                identifier = ctx.getChild(i).getText()
                break

        if identifier is None:
            return

        if any((node.name == identifier and node.node_type == "contract")
               for node in self.nodes_to_remove):
            self.removals.append((ctx.start.start, ctx.stop.stop))

    def exitSourceUnit(self, ctx: SolidityParser.SourceUnitContext):
        sorted_nodes = list(nx.topological_sort(self.graph))
        for contract_node in [n for n in self.graph
                              if n.node_type == "contract" and
                              n not in self.nodes_to_remove]:
            parents = [
                p for p in list(nx.ancestors(self.graph, contract_node))
                if p not in self.removed_nodes
            ]
            sorted_parents = []
            if parents:
                for n in sorted_nodes:
                    if n not in parents:
                        continue
                    pred_nodes = set(nx.ancestors(self.graph, n))
                    sorted_parents.append(n)
                    for pred in pred_nodes:
                        if pred in sorted_parents:
                            sorted_parents.remove(pred)

            new_inheritance_specifiers = ", ".join(
                parent.name for parent in sorted_parents)
            self.replacements.append((contract_node.name,
                                      new_inheritance_specifiers))

    def remove_nodes(self, source_code, nodes_to_remove: set,
                     removed_nodes: set):
        self.nodes_to_remove = nodes_to_remove
        self.removed_nodes = removed_nodes.union(nodes_to_remove)
        walker = ParseTreeWalker()
        walker.walk(self, self.tree)
        for start, stop in sorted(self.removals, reverse=True):
            code_block = source_code[start:stop + 1]
            if any(node.name in code_block for node in self.nodes_to_remove):
                source_code = source_code[:start] + \
                    (len(code_block) * " ") + source_code[stop + 1:]

        for identifier, new_inheritance_specifiers in self.replacements:
            pattern = re.compile(rf"(\b{identifier}\b\s+is\s+)[^{{]*")
            replacement_text = (
                f"{identifier} is {new_inheritance_specifiers}"
                if new_inheritance_specifiers
                else f"{identifier}"
            )
            source_code = pattern.sub(replacement_text, source_code)
        source_code = source_code.replace(r"/\s\s+/g", ' ')
        modified_source_code = re.sub(r'\n\s*\n', '\n\n', source_code)
        return modified_source_code

    @classmethod
    def setup_parse_tree(self, source_code: str):
        lexer = SolidityLexer(InputStream(source_code))
        stream = CommonTokenStream(lexer)
        parser = SolidityParser(stream)
        return parser.sourceUnit()


AST_REMOVALS = {
    "solidity": SolidityDeclarationRemoval,
    "c": CDeclarationRemoval
}
