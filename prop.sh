#!/bin/bash

# EXAMPLE: java -jar perses_deploy.jar --test-script solidity2.sh --input-file view_pure.sol

# Start time
start_time=$(date +%s)
source_file=$1

# Define patterns and their expected counts in an associative array
declare -A patterns=(
  ["internal compiler error"]=1
)

# Flag to track if all patterns match their expected counts
all_patterns_match=1

if [ -z $source_file ]; then
   source_file=small.c
fi

for pattern in "${!patterns[@]}"; do
  expected_count=${patterns[$pattern]}
  # Count occurrences of the pattern
  count=$(
sudo docker run -v $(pwd)/$source_file:/usr/gcc/small.c --rm theosotr/gcc-4.8.2 gcc -m64 -o t -O3 small.c 2>&1 > /dev/null | grep -o "$pattern" | wc -l | xargs)

  # Check if the pattern matches the expected count
  if [ "$count" -eq "$expected_count" ]; then
    echo "\"$pattern\" found exactly $expected_count times."
  else
    echo "\"$pattern\" expected to be found $expected_count times, but was found $count times."
    all_patterns_match=0
  fi
done

# Function to count the number of tokens in a Solidity file
count_tokens() {
    local file_path=$1
    local token_count=$(grep -o -E '\w+|[{}()<>!=,;]' "$file_path" | wc -l)
    echo "$token_count"
}

# Count the number of tokens in ext_changed.sol
token_count=$(count_tokens "$source_file")

# # Ensure reduction_results file exists
# if [ ! -f reduction_results ]; then
#     touch reduction_results
# fi
#
# # Debugging information to ensure file is being touched/created
# echo "Checking if reduction_results file exists and can be written to."
# ls -l reduction_results
#
# # Print results to the reduction_results file
# {
#     echo "PERSES:"
#     echo "TOTAL TIME: $total_time seconds"
#     echo "TOKENS: $token_count"
#     echo ""  # Add a new line for readability
# } >> reduction_results
#
# # Debugging information to check if the results are written to the file
# echo "Contents of reduction_results file after writing:"
# cat reduction_results

# Exit with code 0 if all patterns match their expected counts, else exit with code 1
if [ "$all_patterns_match" -eq 1 ]; then
  echo "All patterns match their expected counts."
  exit 0
else
  echo "One or more patterns do not match their expected counts."
  exit 1
fi

