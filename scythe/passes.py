from dataclasses import dataclass
from typing import Callable, Optional, Tuple

BLOCK_MIN_BYTES = 40


def _big_block(n):
    return (n.args[1] - n.args[0]) >= BLOCK_MIN_BYTES


def _not_main(n):
    return n.name != "main"


def _not_placeholder(n):
    return n.name != "__A"


@dataclass(frozen=True)
class Pass:
    kinds: Tuple[str, ...]
    driver: str = "probe"
    mode: Optional[str] = None
    where: Optional[Callable] = None


@dataclass(frozen=True)
class Language:
    mode: str
    passes: Tuple[Pass, ...]


LANGUAGES = {
    "solidity": Language(mode="removal", passes=(
        Pass(("contract",), mode="flatten"),
        Pass(("function", "modifier", "event")),
        Pass(("contract", "struct")),
        Pass(("state_var",)),
        Pass(("contract", "struct")),
        Pass(("var",)),
    )),
    "c": Language(mode="replacement", passes=(
        Pass(("function",), where=_not_main),
        Pass(("global_variable",)),
        Pass(("struct",), driver="ddmin", where=_not_placeholder),
        Pass(("for_statement", "if_statement"), where=_big_block),
        Pass(("initializer",), where=_big_block),
        Pass(("expression",), where=_big_block),
    )),
    "java": Language(mode="replacement", passes=(
        Pass(("class",), driver="ddmin", mode="flatten"),
        Pass(("function",), driver="ddmin"),
        Pass(("field",), driver="ddmin"),
        Pass(("class",), driver="ddmin"),
        Pass(("local_variable",), driver="ddmin"),
    )),
}
