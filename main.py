import argparse
import time

from reducer import utils
from reducer.dd import Interesting, perform_dd
from reducer.checker import PROPERTY_CHECKERS
from reducer.graph import build_graph_from_file


# Argument parsing
parser = argparse.ArgumentParser(
    description=('Modify Solidity files based on node removal and '
                 "Slither analysis, considering specified findings.")
)
parser.add_argument(
    "--language",
    default="solidity",
    choices=['solidity'],
    help="Select specific language"
)
parser.add_argument(
    "--source-file",
    type=str,
    default="ext_changed.sol",
    help="Source file to minimize",
)
parser.add_argument(
    '--consider',
    type=str,
    help='Findings to consider in the format "finding=threshold"',
    default=""
)
args = parser.parse_args()


def main():
    # Convert consider string to a dictionary
    if args.consider:
        key, value = args.consider.split('=')
        patterns = {key: int(value)}
    else:
        patterns = {}

    start_time = time.time()
    file_path = args.source_file
    graph = build_graph_from_file(file_path, args.language)

    prop_checker = PROPERTY_CHECKERS[args.language](file_path, patterns,
                                                    "slither")
    original_content = utils.read_file(file_path)

    interesting = Interesting(graph, original_content,
                              prop_checker, args.language)
    passes = [
        ["function"], ["contract"],
        ["event", "state_var", "struct", "var"]
    ]
    for pass_ in passes:
        interesting.mode = pass_
        perform_dd(interesting, lambda n: n.node_type in pass_,
                   parallel=True)

    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")


if __name__ == "__main__":
    main()
