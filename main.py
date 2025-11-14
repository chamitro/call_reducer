import argparse
import time
import resource
import sys

from reducer import utils, parsers
from reducer.dd import Interesting, perform_dd
from reducer.checker import BasicPropertyChecker
from reducer.graph import build_graph_from_file

resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)


#example Solidity:greduce --script solidity2.sh
#example C: greduce --source-file ./example.c --script ./cproperty.sh --language c

# Argument parsing
parser = argparse.ArgumentParser(
    description=('Modify Solidity files based on node removal and '
                 "Slither analysis, considering specified findings.")
)

parser.add_argument(
    "--language",
    default="solidity",
    choices=['solidity', 'c'],
    help="Select specific language (options: 'solidity', 'c')"
)

parser.add_argument(
    "--source-file",
    type=str,
    default="ext_changed.sol",
    help="Source file to minimize",
)

parser.add_argument(
    '--script',
    type=str,
    help='script to run"',
    default="./solidity2.sh"
)

parser.add_argument(
    "--mode",
    default="combination",
    choices=['removal', 'replacement', 'combination'],
    help="Select whether the removal of variables should follow a removal, "
         "replacement or a combination strategy"
)
args = parser.parse_args()


def main():
    start_time = time.time()
    file_path = args.source_file
    print(f"Using source file: {file_path}")

    graph = build_graph_from_file(file_path, args.language)
    print(f"Graph built from file: {file_path}")
    print(graph)

    print(args.script)
    print(file_path)
    prop_checker = BasicPropertyChecker(file_path, args.script)
    content = utils.read_file(file_path)

    interesting = Interesting(graph, content,
                              prop_checker, args.language, args.mode)
    passes = [
        # ["if_statement"]
        ["for_statement", "if_statement"],
        ["global_variable", "struct"],
        ["function"],
        ["for_statement", "if_statement"],

        # ["function", "global_variable],
        # ["contract"],
        # ["event", "state_var", "struct", "var"]
    ]
    for pass_ in passes:
        interesting.mode = pass_
        perform_dd(interesting, lambda n: n.node_type in pass_,
                   parallel=False)

    # passes = [
    #     ["function"],
    #     ["struct", "var"]
    # ]
    # for pass_ in passes:
    #     interesting.mode = pass_
    #     perform_dd(interesting, lambda n: n.node_type in pass_,
    #                parallel=True)

    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")


if __name__ == "__main__":
    main()
