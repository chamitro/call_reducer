#!/bin/bash

# EXAMPLE RUN: ./reduce_analysis.sh BFS_TOP_DOWN 'is never used and should be removed=5'

# Function to count and print the number of tokens in a Solidity file
count_tokens() {
    local file_path=$1
    echo "Counting tokens in the file $file_path..."
    # Count the tokens by splitting on spaces, newlines, and special characters
    local token_count=$(grep -o -E '\w+|[{}()<>!=,;]' "$file_path" | wc -l)
    echo "Number of tokens: $token_count"
    echo "TOKENS: $token_count" >> reduction_results
    echo "" >> reduction_results  # Add a new line for readability
}

# Function to calculate the checksum of a file
file_checksum() {
    local file_path=$1
    sha256sum "$file_path" | awk '{ print $1 }'
}

# Function to time a command and output the time taken
time_command() {
    local command=$1
    local label=$2

    local start_time=$(date +%s)
    eval "$command"
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    echo "$label: $duration seconds"
    echo "$label: $duration seconds" >> reduction_results
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <method> <consider_option>"
    exit 1
fi

# Assign arguments to variables
METHOD=$1
CONSIDER_OPTION=$2

# Start the total timer
TOTAL_START_TIME=$(date +%s)

# Initialize iteration counter
iteration=0

echo "Method: $METHOD" >> reduction_results
echo "Method: $METHOD"

echo "" >> reduction_results  # Add a new line for readability

# Loop for a fixed number of iterations (2 iterations)
for ((iteration=1; iteration<=3; iteration++)); do
    echo "Iteration: $iteration" >> reduction_results
    echo "Iteration: $iteration"
    echo "" >> reduction_results  # Add a new line for readability
    python3 delete_comments.py
    # Calculate the checksum before running the commands
    CHECKSUM_BEFORE=$(file_checksum "./ext_changed.sol")
    # Execute the commands based on the first argument
    case $METHOD in
        BFS_TOP_DOWN)
            python3 nodes.py
            time_command "python3 top_down_bfs.py --consider \"$CONSIDER_OPTION\"" "TOP_DOWN BFS_TIME"
            time_command "python3 var_mod_ANTLR.py ./ext_changed.sol --consider \"$CONSIDER_OPTION\"" "STATEMENTS REDUCTION TIME"
            ;;
        BFS_DOWN_TOP)
            python3 nodes.py
            time_command "python3 down_top_bfs.py --consider \"$CONSIDER_OPTION\"" "DOWN_TOP_BFS TIME"
            time_command "python3 var_mod_ANTLR.py ./ext_changed.sol --consider \"$CONSIDER_OPTION\"" "STATEMENTS REDUCTION TIME"
            time_command "python3 unused_var.py ./ext_changed.sol --consider \"$CONSIDER_OPTION\"" "UNUSED CODE REDUCTION TIME"
            ;;
        HDD)
            python3 nodes.py
            time_command "python3 hdd_final.py --consider \"$CONSIDER_OPTION\"" "HDD TIME"
            time_command "python3 var_mod_ANTLR.py ./ext_changed.sol --consider \"$CONSIDER_OPTION\"" "STATEMENTS REDUCTION TIME"
            time_command "python3 unused_var.py ./ext_changed.sol --consider \"$CONSIDER_OPTION\"" "UNUSED CODE REDUCTION TIME"
            ;;
        *)
            echo "Invalid method. Valid options are: BFS_TOP_DOWN, BFS_DOWN_TOP, HDD"
            exit 1
            ;;
    esac

    # Calculate the checksum after running the commands
    CHECKSUM_AFTER=$(file_checksum "./ext_changed.sol")

    # Compare the checksums
    if [ "$CHECKSUM_BEFORE" == "$CHECKSUM_AFTER" ]; then
        # If the checksums are the same, exit the loop
        break
    fi
done

time_command "python3 unused_var.py ./ext_changed.sol --consider \"$CONSIDER_OPTION\"" "UNUSED CODE REDUCTION TIME"
# End the total timer
TOTAL_END_TIME=$(date +%s)
TOTAL_EXECUTION_TIME=$((TOTAL_END_TIME - TOTAL_START_TIME))

# Write the total execution time to the results file
echo "Script executed successfully." >> reduction_results
echo "TOTAL TIME: $TOTAL_EXECUTION_TIME seconds" >> reduction_results

echo "Script executed successfully."
echo "TOTAL TIME: $TOTAL_EXECUTION_TIME seconds"

# Count and print the number of tokens in the Solidity file
count_tokens "./ext_changed.sol"

