from slither import Slither

def get_inheritance_tree(file_path):
    # Initialize Slither
    slither = Slither(file_path)

    # Dictionary to hold the inheritance tree
    inheritance_tree = {}

    for contract in slither.contracts:
        # Get the contract name
        contract_name = contract.name
        # Get the parent contracts
        parents = [parent.name for parent in contract.inheritance]
        inheritance_tree[contract_name] = parents

    return inheritance_tree

def invert_inheritance_tree(inheritance_tree):
    # Dictionary to hold the inverted inheritance tree
    inverted_tree = {}

    for child, parents in inheritance_tree.items():
        for parent in parents:
            if parent != 'None':
                if parent not in inverted_tree:
                    inverted_tree[parent] = []
                inverted_tree[parent].append(child)
    
    # Ensure all contracts are in the inverted tree, even if they have no children
    all_contracts = set(inheritance_tree.keys())
    for parent in all_contracts:
        if parent not in inverted_tree:
            inverted_tree[parent] = []
    
    return inverted_tree

def save_inheritance_tree_to_file(inverted_tree, file_path):
    with open(file_path, 'w') as file:
        for parent, children in inverted_tree.items():
            if children:
                file.write(f"Parent Contract {parent} has children: {', '.join(children)}\n")
            else:
                file.write(f"Parent Contract {parent} has no children\n")

# Example usage
sol_file_path = 'ext_changed.sol'
output_file_path = 'inheritance.txt'

inheritance_tree = get_inheritance_tree(sol_file_path)
inverted_tree = invert_inheritance_tree(inheritance_tree)
save_inheritance_tree_to_file(inverted_tree, output_file_path)
