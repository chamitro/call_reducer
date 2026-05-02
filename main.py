import argparse
import time
import resource
import sys

from reducer import utils
from reducer.dd import Interesting, perform_dd
from reducer.checker import PROPERTY_CHECKERS
from reducer.graph import build_graph_from_file

resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)


#example Solidity: greduce --source-file ./Solidity/smart2/ext_changed.sol --script ./Solidity/smart2/solidity2.sh
#example C: greduce --source-file "./C/gcc-59903/small.c" --script "./C/gcc-59903/test_r.sh" --language c --mode "$mode"

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
    prop_checker = PROPERTY_CHECKERS[args.language](file_path, args.script)
    content = utils.read_file(file_path)

    interesting = Interesting(graph, content,
                              prop_checker, args.language, args.mode)

    passes = [
        ["function"],
        ["contract"],
        ["event", "state_var", "struct", "var"]
    ]
    parallel = True

    if args.language == "c":
        parallel = False
        passes = [
            ["for_statement", "if_statement"],
            ["global_variable", "struct"],
            ["function"],
            ["for_statement", "if_statement"],
        ]

    for pass_ in passes:
        interesting.mode = pass_
        perform_dd(interesting, lambda n: n.node_type in pass_,
                   parallel=parallel, language=args.language)


    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")


if __name__ == "__main__":
    main()
