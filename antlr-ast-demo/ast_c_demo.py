from antlr_ast.ast import (
    BaseNode as AstNode,
    parse as parse_ast,
    process_tree,
    BaseNodeTransformer, AliasNode,
)
from antlr_ast.inputstream import CaseTransformInputStream
from C import grammar


class SubExpr(AstNode):
    _fields = ['expression']


class BinaryExpr(AstNode):
    _fields = ['left', 'right', 'op']


class NotExpr(AstNode):
    _fields = ['NOT->op', 'expr']


class DeclarationList(AstNode):
    _fields = ["declaration"]


class Transformer(BaseNodeTransformer):
    # @staticmethod
    def visit_DeclarationList(self, node):
        breakpoint()
        return node.name_of_part

#     @staticmethod
    def visit_SubExpr(self, node):
        return node.name_of_part

#     @staticmethod
    def visit_NotExpr(self, node):
        return node.name_of_part

#     @staticmethod
    def visit_VariableDecl(self, node):
        return node.name_of_part

#     @staticmethod
    def visit_FunctionDecl(self, node):
        return node.name_of_part

#     @staticmethod
    def visit_IfStmt(self, node):
        return node.name_of_part

#     @staticmethod
    def visit_ParamDecl(self, node):
        return node.name_of_part

#     @staticmethod
    def visit_CompoundStmt(self, node):
        return node.name_of_part

#     @staticmethod
    def visit_ReturnStmt(self, node):
        return node.name_of_part


def parse(text, start="translationUnit", **kwargs):
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
    # print(ast_tree.get_text())
    # code_text = "\n".join([node.get_text() for node in ast_tree])
    # print(code_text)
