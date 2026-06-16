import warnings
from abc import ABC, abstractmethod

from tree_sitter import Language, Parser, Query, QueryCursor  # type: ignore
import tree_sitter_c  # type: ignore
import tree_sitter_java  # type: ignore
import tree_sitter_solidity  # type: ignore

from scythe import utils


def _load_language(grammar_module) -> Language:
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", message="int argument support is deprecated"
        )
        return Language(grammar_module.language())


class _Query:

    __slots__ = ("_query",)

    def __init__(self, query: Query):
        self._query = query

    def captures(self, node):
        captures_by_name = QueryCursor(self._query).captures(node)
        pairs = [
            (n, name)
            for name, nodes in captures_by_name.items()
            for n in nodes
        ]
        pairs.sort(key=lambda item: (item[0].start_byte, item[0].end_byte))
        return pairs

    def matches(self, node):
        return QueryCursor(self._query).matches(node)


class _LanguageHandle:

    def __init__(self, language: Language):
        self.language = language
        self._query_cache: dict[str, Query] = {}

    def query(self, source: str) -> _Query:
        compiled = self._query_cache.get(source)
        if compiled is None:
            compiled = Query(self.language, source)
            self._query_cache[source] = compiled
        return _Query(compiled)


SOLIDITY_LANGUAGE = _LanguageHandle(_load_language(tree_sitter_solidity))
SOLIDITY_PARSER = Parser(SOLIDITY_LANGUAGE.language)

C_LANGUAGE = _LanguageHandle(_load_language(tree_sitter_c))
C_PARSER = Parser(C_LANGUAGE.language)

JAVA_LANGUAGE = _LanguageHandle(_load_language(tree_sitter_java))
JAVA_PARSER = Parser(JAVA_LANGUAGE.language)


PARSERS = {
    "solidity": SOLIDITY_PARSER,
    "c": C_PARSER,
    "java": JAVA_PARSER,
}


class TreeTraversal(ABC):
    @abstractmethod
    def get_node_visitor(self, node):
        pass

    @abstractmethod
    def get_node_exit(self, node):
        pass

    def traverse_node(self, node):
        visitor = self.get_node_visitor(node)
        visitor(node)

        for child in node.children:
            self.traverse_node(child)
        exit_node = self.get_node_exit(node)
        exit_node(node)


def get_parser(language: str):
    parser = PARSERS.get(language)
    if parser is None:
        raise Exception(f"Parser for language '{language}' was not found")
    return parser


def parse(file_name: str, language: str):
    parser = get_parser(language)
    file_content = utils.read_file(file_name).encode("utf-8")
    tree = parser.parse(file_content)
    return tree


def declaration_name(node):
    name_node = node.child_by_field_name("name")
    if name_node is None:
        for child in node.children:
            if child.type == "identifier":
                name_node = child
                break
    return name_node.text.decode("utf-8") if name_node is not None else None


def parameter_signature(function_node):
    signature = []
    for child in function_node.children:
        if child.type == "parameter":
            type_node = child.child_by_field_name("type") or (
                child.children[0] if child.children else None
            )
            signature.append(
                type_node.text.decode("utf-8") if type_node is not None else ""
            )
    return tuple(signature)


def type_reference_names(declaration_node):
    names = set()
    for child in declaration_node.children:
        if child.type != "type_name":
            continue
        stack = [child]
        while stack:
            n = stack.pop()
            if n.type in ("user_defined_type", "type_identifier", "identifier"):
                names.add(n.text.decode("utf-8"))
            stack.extend(n.children)
    return names
