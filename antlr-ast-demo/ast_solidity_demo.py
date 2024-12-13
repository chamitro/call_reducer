import ast
import json

from antlr4.InputStream import InputStream
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from antlr4.tree.Tree import TerminalNodeImpl
from antlr_ast.ast import (
    BaseNode as AstNode,
    AliasNode,
    parse as parse_ast,
    process_tree,
    BaseNodeTransformer, Terminal,
)
from antlr_ast.inputstream import CaseTransformInputStream
from antlr_ast.marshalling import AstEncoder, get_decoder

from Solidity import grammar

rewriter = None


class ExpressionStatement(AstNode):
    _fields_spec = ['expression', ';']


class Expression(AstNode):
    _strict = True
    _fields_spec = [
        'expression', '(', ')', '++', '--', 'new', 'typeName', '[', ']',
        '.', 'identifier', '{', 'nameValueList', '}', '(', 'functionCallArguments',
        '+', '-', 'delete', '!', '~', '<assoc=right>', '**', '*', '/', '%', '<<',
        '>>', '&', '^', '|', '<', '>', '<=', '>=', '==', '!=', '&&', '||', '?', '=',
        '|=', '^=', '&=', '<<=', '>>=', '+=', '-=', '*=', '/=', '%=',
        'primaryExpression', ';'
]
#
#
#
# class FunctionDefinition(AliasNode):
#     _fields_spec = ['functionDescriptor', 'parameterList', 'modifierList', 'returnParameters', ';', 'block']
#     _strict = True

# class Block(AstNode):
#     _fields = ['{', 'statement', '}', ';']
#
#     def get_source_code(self, node):
#         return node.get_text()
#
#
# class FunctionCall(AstNode):
#     _fields = ["expression", "(", "functionCallArguments", ')' ';']
#
#
# class Identifier(AstNode):
#     _fields = ["(",'from', 'calldata', 'receive', 'callback', 'revert', 'error', 'address', 'GlobalKeyword', 'ConstructorKeyword', 'PayableKeyword', 'LeaveKeyword', 'Identifier', ')', ';']
#
#
class ExpressionList(AliasNode):
    _fields = ["expression", "(", ',', "expression", ")", "*", ";"]


def is_new_transformation(interval, transformation):
    for transformation_interval in transformation.keys():
        if transformation_interval[0] <= interval[0] and interval[1] <= transformation_interval[1]:
            return False
    return True

class Transformer(BaseNodeTransformer):
    transformations = {}
    def visit_FunctionCallArguments(self, node):
        return node

    def visit_Expression(self, node):
        # global rewriter
        if search_identifier_in_node(node=node, identifier="require"):
            return node
        identifier = search_identifier_in_node(node=node, identifier="mint")
        if identifier:
            parent = node._ctx.parentCtx
            if parent:
                if is_new_transformation((node._ctx.start.start, node._ctx.stop.stop), self.transformations):
                    self.transformations[(node._ctx.start.start, node._ctx.stop.stop)] = "true"
                    index = parent.children.index(node._ctx)
                    new_node = parse('true', "assemblyLiteral", Transformer)
                    parent.children.remove(node._ctx)
                    parent.children.insert(index, new_node)
                # rewriter.delete(from_idx=node._ctx.start.tokenIndex, to_idx=node._ctx.stop.tokenIndex, program_name=TokenStreamRewriter.DEFAULT_PROGRAM_NAME)
                # rewriter.insertAfter(parent.children[index - 1].getSymbol().tokenIndex, new_node.getText())
            # return parse('', "expression", Transformer)
            # return None
        return node
    #
    def visit_ExpressionList(self, node):
        identifier = search_identifier_in_node(node=node, identifier="mint")
        if identifier:
            parent = node._ctx.parentCtx
            if parent:
                if is_new_transformation((node._ctx.start.start, node._ctx.stop.stop), self.transformations):
                    self.transformations[(node._ctx.start.start, node._ctx.stop.stop)] = "true"
                    index = parent.children.index(node._ctx)
                    new_node = parse('true', "assemblyLiteral", Transformer)
                    parent.children.remove(node._ctx)
                    parent.children.insert(index, new_node)
        return node
    # def visit_ContractPart(self, node):
    #     if node.functionDefinition:
    #         if hasattr(node.functionDefinition.functionDescriptor.identifier, "Identifier"):
    #             if node.functionDefinition.functionDescriptor.identifier.Identifier == "mint":
    #                 print(node.get_text())
    #                 breakpoint()
    #                 return parse('', "contractPart", Transformer)
    #     return node

    def visit_FunctionDefinition(self, node):
        # global rewriter
        if hasattr(node.functionDescriptor.identifier, "Identifier"):
            if node.functionDescriptor.identifier.Identifier == "mint":
                parent = node._ctx.parentCtx
                if parent:
                    if is_new_transformation((node._ctx.start.start, node._ctx.stop.stop), self.transformations):
                        parent.children.remove(node._ctx)
                        self.transformations[(node._ctx.start.start, node._ctx.stop.stop)] = ""
                    # rewriter.delete(from_idx=node._ctx.start.tokenIndex, to_idx=node._ctx.stop.tokenIndex, program_name=TokenStreamRewriter.DEFAULT_PROGRAM_NAME)
                # return None
                # return parse('', "functionDefinition", Transformer)
        return node

    # @staticmethod
    # def visit_Block(node):
    #     return node
    #
    # @staticmethod
    # def visit_FunctionCall(node):
    #     return node
    #
    # @staticmethod
    # def visit_Identifier(node):
    #     return node


def parse(text, start="sourceUnit", transformer=None, **kwargs):
    # global rewriter
    antlr_tree = parse_ast(
        grammar, text, start, transform=CaseTransformInputStream.LOWER, **kwargs
    )
    token_stream = antlr_tree.parser.getTokenStream()
    # rewriter = TokenStreamRewriter(token_stream)
    simple_tree = process_tree(antlr_tree, transformer_cls=transformer)
    tree = simple_tree._ctx

    return tree


def search_identifier_in_node(node, identifier):
    if isinstance(node, str):
        return None
    if node.Identifier == identifier:
        return node
    else:
        for child in node.children:
            child_with_identifier = search_identifier_in_node(child, identifier)
            if child_with_identifier:
                return child_with_identifier


def remove_tree_nodes(tree, removal_nodes):
    if isinstance(tree, str):
        return
    if tree in removal_nodes:
        parent = tree.parentCtx
        if parent:
            parent.children.remove(tree)
    if hasattr(tree, "children") and  tree.children:
        for child in tree.children:
            remove_tree_nodes(child, removal_nodes)


# class TreeToStringVisitor:
#     def __init__(self):
#         self.output = ""
#
#     def visit(self, node):
#         if isinstance(node, TerminalNodeImpl):
#             # Leaf node (token), append its text
#             self.output += node.getText()
#         else:
#             # Non-leaf node, visit children
#             for child in node.children or []:
#                 self.visit(child)
#
#
# def get_char_stream_from_context(ctx):
#     # Use the visitor to traverse and get the modified text
#     visitor = TreeToStringVisitor()
#     visitor.visit(ctx)
#
#     modified_code = visitor.output
#     # Create a new CharStream from the modified text
#     return InputStream(modified_code)


def get_source_code_from_tree(tree, replacement_dict):
    result = []
    current_index = tree.start.start
    sorted_replacements = sorted(replacement_dict.items(), key=lambda x: x[0][0])
    for (start, end), replacement in sorted_replacements:
        result.append(tree.start.getInputStream().getText(current_index, start - 1))
        result.append(replacement)
        current_index = end + 1

    result.append(tree.start.getInputStream().getText(current_index, tree.stop.stop))

    return ''.join(result)

if __name__ == "__main__":
    # Removing the `mint` function and all it's references
    file = open("../Solidity/smart3/ext_changed.sol")
    code = file.read()
    file.close()
    transformer = Transformer
    ast_tree = parse(code, transformer=transformer)
    ast_tree_string = get_source_code_from_tree(ast_tree, transformer.transformations)
    print(ast_tree_string)
    # print(ast_tree.getText())
    # print(ast_tree.toString(grammar.SolidityParser.SolidityParser.ruleNames, ast_tree.stop.stop))
    # print(ast_tree.toStringTree(grammar.SolidityParser.SolidityParser.ruleNames))
    # print(ast_tree.start.getInputStream().getText(ast_tree.start.start, ast_tree.stop.stop))

    # char_stream = get_char_stream_from_context(ast_tree)
    # print(char_stream.getText(ast_tree.start.start, ast_tree.stop.stop))
    # node._ctx.toString(grammar.SolidityParser.SolidityParser.ruleNames, node._ctx.stop)
    #
    # RETRIEVE
    # CODE:
    # node._ctx.start.getInputStream().getText(node._ctx.start.start, node._ctx.stop.stop)