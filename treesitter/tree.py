from tree_sitter import Language, Parser
import os

# Step 1: Build the tree-sitter language library for C if not already built

# The path to the shared library file for tree-sitter languages
LIBRARY_PATH = "./tree-sitter-languages.so"

# Path to the C grammar repository
#C_GRAMMAR_REPO = "https://github.com/tree-sitter/tree-sitter-c.git"
C_LANGUAGE_DIR = "./tree-sitter-c"

if not os.path.exists(LIBRARY_PATH):
    # Clone the tree-sitter C grammar if it doesn't exist
    if not os.path.exists(C_LANGUAGE_DIR):
        os.system(f"git clone {C_GRAMMAR_REPO} {C_LANGUAGE_DIR}")

    # Build the shared library
    Language.build_library(
        LIBRARY_PATH,
        [C_LANGUAGE_DIR]
    )

# Step 2: Load the C language into tree-sitter
C_LANGUAGE = Language(LIBRARY_PATH, "c")

# Step 3: Create the parser and set the language
parser = Parser()
parser.set_language(C_LANGUAGE)

# Step 4: Function to parse C code and generate the AST
def parse_c_code(code):
    tree = parser.parse(code.encode("utf-8"))
    return tree

# Step 5: Function to print the AST recursively
def print_ast(node, source_code, indent=0):
    """Recursively print the AST with indentation."""
    node_type = node.type
    start_byte = node.start_byte
    end_byte = node.end_byte
    start_point = node.start_point
    end_point = node.end_point

    code_snippet = source_code[start_byte:end_byte]
    indent_str = "  " * indent

    print(f"{indent_str}({node_type} [Line {start_point[0] + 1}:{start_point[1] + 1} - Line {end_point[0] + 1}:{end_point[1] + 1}] Code: \"{code_snippet}\")")

    for child in node.children:
        print_ast(child, source_code, indent + 1)

if __name__ == "__main__":
    # Read C code from a file
    file_path = "example.c"
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        exit(1)

    with open(file_path, "r") as file:
        c_code = file.read()

    # Parse the C code
    tree = parse_c_code(c_code)

    # Print the AST
    print("Abstract Syntax Tree:")
    print_ast(tree.root_node, c_code)

