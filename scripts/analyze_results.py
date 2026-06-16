#!/usr/bin/env python3
import argparse
import json
import os
import sys

from scythe import parsers

LANGUAGES = {
    "sol": ("solidity", {"comment"}),
    "java": ("java", {"line_comment", "block_comment"}),
    "c": ("c", {"comment"}),
}

METHODS = {
    "perses": ("minimized_perses", "perses"),
    "scythe": ("minimized_scythe", "scythe"),
    "scythe-perses": ("minimized_scythe_perses", "scythe_perses"),
}


def count_tokens(path, lang_key, comment_types):
    with open(path, "rb") as f:
        tree = parsers.PARSERS[lang_key].parse(f.read())
    tokens = 0
    stack = [tree.root_node]
    while stack:
        node = stack.pop()
        if node.children:
            stack.extend(node.children)
        elif node.type not in comment_types:
            tokens += 1
    return tokens


def read_times(time_file):
    times = {}
    if not os.path.isfile(time_file):
        return times
    with open(time_file) as f:
        for line in f:
            line = line.strip()
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            try:
                times[key.strip()] = int(value)
            except ValueError:
                try:
                    times[key.strip()] = float(value)
                except ValueError:
                    pass
    return times


def analyze_benchmark(bench_dir):
    for ext, (lang_key, comment_types) in LANGUAGES.items():
        original = os.path.join(bench_dir, f"original.{ext}")
        if os.path.isfile(original):
            break
    else:
        return None
    entry = {"original": {"tokens": count_tokens(original, lang_key, comment_types)}}
    times = read_times(os.path.join(bench_dir, "time"))
    for method, (stem, time_key) in METHODS.items():
        reduced = os.path.join(bench_dir, f"{stem}.{ext}")
        if not os.path.isfile(reduced):
            continue
        result = {"tokens": count_tokens(reduced, lang_key, comment_types)}
        if time_key in times:
            result["time"] = times[time_key]
        entry[method] = result
    return entry


def analyze(output_dir):
    results = {}
    for name in sorted(os.listdir(output_dir)):
        bench_dir = os.path.join(output_dir, name)
        if not os.path.isdir(bench_dir):
            continue
        entry = analyze_benchmark(bench_dir)
        if entry is not None:
            results[name] = entry
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", nargs="?", default="output",
                        help="run_solidity_benchmarks.sh output directory")
    parser.add_argument("-o", "--output", help="write JSON here (default: stdout)")
    args = parser.parse_args()

    if not os.path.isdir(args.output_dir):
        sys.exit(f"Error: output directory '{args.output_dir}' not found")

    results = analyze(args.output_dir)
    payload = json.dumps(results, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(payload + "\n")
        print(f"Wrote {len(results)} benchmark(s) to {args.output}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
