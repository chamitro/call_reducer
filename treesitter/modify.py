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
parser = Parser()
parser.set_language(C_LANGUAGE)


# Read C code from a file
file_path = "example.c"
if not os.path.exists(file_path):
    print(f"File {file_path} does not exist.")
    exit(1)

with open(file_path, "r") as file:
    code = file.read()

code = code.encode("utf-8")
# Parse the original code
tree = parser.parse(code)
# Step 3: Define the new source code (manual modification)
new_code = b"""
int main() {}
"""


def find_nodes_by_type(node, node_type, nodes):
    """Recursively find the first node of a specific type."""
    if node.type == node_type:
        nodes.append(node)
    for child in node.children:
        find_nodes_by_type(child, node_type, nodes)
    return None


return_nodes = []
find_nodes_by_type(tree.root_node, "return_statement", return_nodes)
return_nodes.sort(key=lambda node: node.start_byte, reverse=True)

# Track edits for all nodes
edits = []
for return_node in return_nodes:
    edits.append({
        "start_byte": return_node.start_byte,
        "old_end_byte": return_node.end_byte,
        "new_end_byte": return_node.start_byte,  # Remove content
        "start_point": return_node.start_point,
        "old_end_point": return_node.end_point,
        "new_end_point": return_node.start_point,
    })

# Apply edits to the tree and modify the source code
modified_code = code
for edit in edits:
    # Apply the edit to the tree
    tree.edit(
        start_byte=edit["start_byte"],
        old_end_byte=edit["old_end_byte"],
        new_end_byte=edit["new_end_byte"],
        start_point=edit["start_point"],
        old_end_point=edit["old_end_point"],
        new_end_point=edit["new_end_point"],
    )
    # Update the source code
    modified_code = (
        modified_code[: edit["start_byte"]] +
        b"" +
        modified_code[edit["old_end_byte"]:]
    )

updated_tree = parser.parse(modified_code, tree)
updated_code = updated_tree.text.decode("utf-8")

print("\nModified Code:")
print(updated_code)
