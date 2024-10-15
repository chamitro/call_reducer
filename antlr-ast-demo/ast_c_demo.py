from antlr_ast.ast import (
    BaseNode as AstNode,
    parse as parse_ast,
    process_tree,
    BaseNodeTransformer,
)
from antlr_ast.inputstream import CaseTransformInputStream
from C import grammar


class SubExpr(AstNode):
    _fields = ['expr->expression']


class BinaryExpr(AstNode):
    _fields = ['left', 'right', 'op']


class NotExpr(AstNode):
    _fields = ['NOT->op', 'expr']


class Transformer(BaseNodeTransformer):
    def visit_BinaryExpr(self, node):
        return BinaryExpr.from_spec(node)

    def visit_SubExpr(self, node):
        return SubExpr.from_spec(node)

    def visit_NotExpr(self, node):
        return NotExpr.from_spec(node)


def parse(text, start="declarationList", **kwargs):
    antlr_tree = parse_ast(
        grammar, text, start, transform=CaseTransformInputStream.LOWER, **kwargs
    )
    simple_tree = process_tree(antlr_tree, transformer_cls=Transformer)

    return simple_tree


if __name__ == "__main__":
    with open("../C/clang-22382/small.c", "r") as file:
        code = file.read()
    import time
    start_time = time.time()
    ast_tree = parse(code)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(ast_tree)
