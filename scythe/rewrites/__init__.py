from scythe.rewrites.base import ASTRemoval, remove_empty_lines
from scythe.rewrites.solidity import SolidityDeclarationRemoval
from scythe.rewrites.c import CDeclarationRemoval
from scythe.rewrites.java import JavaDeclarationRemoval

AST_REMOVALS = {
    "solidity": SolidityDeclarationRemoval,
    "c": CDeclarationRemoval,
    "java": JavaDeclarationRemoval,
}

__all__ = [
    "ASTRemoval",
    "remove_empty_lines",
    "AST_REMOVALS",
    "SolidityDeclarationRemoval",
    "CDeclarationRemoval",
    "JavaDeclarationRemoval",
]
