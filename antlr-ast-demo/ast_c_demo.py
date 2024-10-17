from antlr_ast.ast import (
    BaseNode as AstNode,
    parse as parse_ast,
    process_tree,
    BaseNodeTransformer,
)
from antlr_ast.inputstream import CaseTransformInputStream
from C import grammar
from antlr4.tree.Tree import TerminalNodeImpl


class SubExpr(AstNode):
    _fields = ['expr->expression']

    def to_code(self):
        pass


class BinaryExpr(AstNode):
    _fields = ['left', 'right', 'op']

    def to_code(self):
        pass


class NotExpr(AstNode):
    _fields = ['NOT->op', 'expr']

    def to_code(self):
        pass


class VariableDecl(AstNode):
    _fields = ['type', 'name', 'initializer']

    def to_code(self):
        pass


class FunctionDecl(AstNode):
    _fields = ['return_type', 'name', 'params', 'body', 'qualifiers']

    def to_code(self):
        pass


class IfStmt(AstNode):
    _fields = ['condition', 'then_branch', 'else_branch']

    def to_code(self):
        pass


class ParamDecl(AstNode):
    _fields = ['type', 'name']

    def to_code(self):
        pass


class CompoundStmt(AstNode):
    _fields = ['statements']

    def to_code(self):
        pass


class ReturnStmt(AstNode):
    _fields = ['expr']

    def to_code(self):
        pass


class Transformer(BaseNodeTransformer):
    def visit_BinaryExpr(self, node):
        return BinaryExpr.from_spec(node)

    def visit_SubExpr(self, node):
        return SubExpr.from_spec(node)

    def visit_NotExpr(self, node):
        return NotExpr.from_spec(node)

    def visit_VariableDecl(self, node):
        return VariableDecl.from_spec(node)

    def visit_FunctionDecl(self, node):
        return FunctionDecl.from_spec(node)

    def visit_IfStmt(self, node):
        return IfStmt.from_spec(node)

    def visit_ParamDecl(self, node):
        return ParamDecl.from_spec(node)

    def visit_CompoundStmt(self, node):
        return CompoundStmt.from_spec(node)

    def visit_ReturnStmt(self, node):
        return ReturnStmt.from_spec(node)


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
    t = ast_tree[0].get_text()
    code_text = "\n".join([node.get_text() for node in ast_tree])
    print(code_text)
