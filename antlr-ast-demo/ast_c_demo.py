import sys

from antlr4.CommonTokenStream import CommonTokenStream
from antlr_ast.ast import (
    BaseNode as AstNode,
    parse as parse_ast,
    process_tree,
    BaseNodeTransformer, AliasNode, BaseAstVisitor, LexerErrorListener, StrictErrorListener,
)
from antlr_ast.inputstream import CaseTransformInputStream
from C import grammar


def is_new_transformation(interval, transformation):
    for transformation_interval in transformation.keys():
        if transformation_interval[0] <= interval[0] and interval[1] <= transformation_interval[1]:
            return False
    return True


class Transformer(BaseNodeTransformer):
    transformations = {}
    def visit_FunctionDefinition(self, node):
        if hasattr(node.declarator.directDeclarator.directDeclarator, "Identifier"):
            if node.declarator.directDeclarator.directDeclarator.Identifier == "safe_sub_func_int16_t_s_s":
                print(node.get_text())
                parent = node._ctx.parentCtx
                if parent:
                    if is_new_transformation((node._ctx.start.start, node._ctx.stop.stop), self.transformations):
                        parent.children.remove(node._ctx)
                        self.transformations[(node._ctx.start.start, node._ctx.stop.stop)] = ""
            elif hasattr(node.declarator.directDeclarator.directDeclarator, "declarator") and hasattr(node.declarator.directDeclarator.directDeclarator.declarator, "directDeclarator"):
                if node.declarator.directDeclarator.directDeclarator.declarator.directDeclarator.Identifier == "safe_sub_func_int16_t_s_s":
                    parent = node._ctx.parentCtx
                    if parent:
                        if is_new_transformation((node._ctx.start.start, node._ctx.stop.stop), self.transformations):
                            parent.children.remove(node._ctx)
                            self.transformations[(node._ctx.start.start, node._ctx.stop.stop)] = ""
        return node
    #
    # def visit_Expression(self, node):
    #     if "safe_sub_func_int16_t_s_s" in node.get_text():
    #         identifier = search_identifier_in_node(node=node, identifier="safe_sub_func_int16_t_s_s")
    #         if identifier:
    #             parent = node._ctx.parentCtx
    #             if parent:
    #                 if is_new_transformation((node._ctx.start.start, node._ctx.stop.stop), self.transformations):
    #                     self.transformations[(node._ctx.start.start, node._ctx.stop.stop)] = "42"
    #                     index = parent.children.index(node._ctx)
    #                     new_node = parse('42', "primaryExpression", Transformer)
    #                     parent.children.remove(node._ctx)
    #                     parent.children.insert(index, new_node)
    #     return node

    def visit_AssignmentExpression(self, node):
        if "safe_sub_func_int16_t_s_s" in node.get_text():
            print(node.get_text())
            print(node.get_position())
            identifier = search_identifier_in_node(node=node, identifier="safe_sub_func_int16_t_s_s")
            if identifier:
                identifier = identifier._ctx.parentCtx
                parent = identifier.parentCtx
                if parent:
                    if is_new_transformation((identifier.start.start, identifier.stop.stop), self.transformations):
                        self.transformations[(identifier.start.start, identifier.stop.stop)] = "42"
                        index = parent.children.index(identifier)
                        new_node = parse('42', "primaryExpression", Transformer)
                        parent.children.remove(identifier)
                        parent.children.insert(index, new_node)
        return node


from functools import lru_cache
from typing import Tuple, Union, Callable

_parse_cache = {}

def parse_ast_cache(
    grammar,
    text: str,
    start: str,
    strict=False,
    transform: Union[str, Callable] = None,
    error_listener = None,
) :
    cache_key = (id(grammar), text, start, transform, strict)

    if cache_key in _parse_cache:
        return _parse_cache[cache_key]

    input_stream = CaseTransformInputStream(text, transform=transform)

    lexer = grammar.Lexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(LexerErrorListener())

    token_stream = CommonTokenStream(lexer)
    parser = grammar.Parser(token_stream)
    parser.buildParseTrees = True

    if strict:
        error_listener = StrictErrorListener()

    if error_listener is not None and error_listener is not True:
        parser.removeErrorListeners()
        if error_listener:
            parser.addErrorListener(error_listener)

    parse_tree = getattr(parser, start)()

    _parse_cache[cache_key] = parse_tree

    return parse_tree



def parse(text, start="compilationUnit", transformer=None, **kwargs):
    antlr_tree = parse_ast_cache(
        grammar, text, start, transform=CaseTransformInputStream.LOWER, **kwargs
    )
    print("initial parsing done")
    simple_tree = process_tree(antlr_tree, transformer_cls=transformer, simplify=False)

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
    # import cProfile, pstats, io
    # from pstats import SortKey

    # pr = cProfile.Profile()
    # pr.enable()
    sys.setrecursionlimit(6000)
    with open("../C/clang-22382/small.c", "r") as file:
        code = file.read()

    import time
    start_time = time.time()
    transformer = Transformer
    ast_tree = parse(code, transformer=transformer)
    ast_tree_string = get_source_code_from_tree(ast_tree, transformer.transformations)
    # print(ast_tree_string)
    print("--- %s seconds ---" % (time.time() - start_time))
    # pr.disable()
    # s = io.StringIO()
    # # ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.TIME, SortKey.CUMULATIVE)
    # ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.CUMULATIVE)
    # ps.print_stats()
    # print(s.getvalue())

    # print(ast_tree)
    # code_text = "\n".join([node.get_text() for node in ast_tree])
    # print(code_text)

    # tree = parse_ast(grammar, code, "expression")
    # field_tree = BaseAstVisitor().visit(tree)
    # alias_tree = AliasVisitor(Transformer()).visit(field_tree)
    #
    # import ast
    #
    # nodes = [el for el in ast.walk(field_tree)]
    # import json
    #
    # json_str = json.dumps(field_tree, default=lambda o: o.to_json())
    # print(json_str)