from antlr_ast.ast import (
    BaseNode as AstNode,
    parse as parse_ast,
    process_tree,
    BaseNodeTransformer,
)
from antlr_ast.inputstream import CaseTransformInputStream
from Solidity import grammar


class ExpressionStatement(AstNode):
    _fields = ['expression', ';']

    def get_source_code(self, node):
        return node.get_text()


class FunctionDefinition(AstNode):
    _fields = ['functionDescriptor', 'parameterList', 'modifierList', 'returnParameters', ';', 'block']

    def get_source_code(self, node):
        text = f"function {node.functionDescriptor.identifier.get_text()} ("
        for i, parameter in enumerate(node.parameterList.parameter):
            text += f"{parameter.typeName.get_text()} {parameter.identifier.get_text()}"
            if i < len(node.parameterList.parameter) - 1:
                text += ", "
            else:
                text += ")"
        # TODO: block visitor
        text += f" {node.modifierList.get_text()} {node.returnParameters.get_text()}"  # modify for more return parameters


class Block(AstNode):
    _fields = ['{', 'statement', '}', ';']

    def get_source_code(self, node):
        return node.get_text()


class Transformer(BaseNodeTransformer):
    def visit_ExpressionStatement(self, node):
        return node

    def visit_FunctionDefinition(self, node):
        return node

    def visit_Block(self, node):
        return node



def parse(text, start="sourceUnit", transformer=None, **kwargs):
    antlr_tree = parse_ast(
        grammar, text, start, transform=CaseTransformInputStream.LOWER, **kwargs
    )
    simple_tree = process_tree(antlr_tree, transformer_cls=transformer)

    return simple_tree


def get_children(tree):
    pass


if __name__ == "__main__":
    file = open("../Solidity/smart1/ext_changed.sol")
    code = file.read()
    file.close()
    ast_tree = parse(code, transformer=Transformer)
    get_children(ast_tree)
    # print(ast_tree)
    # print(ast_tree.get_text())
