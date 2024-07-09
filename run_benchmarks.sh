#!/bin/bash

# Base directory
BASE_DIR="Solidity"
SKIP_PERSEUS=false

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --skip-perses) SKIP_PERSEUS=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Output CSV file
CSV_FILE="$BASE_DIR/greduce_results.csv"
echo "Directory,Initial_Tokens,Initial_Functions,Initial_Contracts_Libraries_Interfaces,Greduce_Tokens,Greduce_Functions,Greduce_Contracts_Libraries_Interfaces,Greduce_Time_s,Perses_Tokens_Solidity2,Perses_Functions_Solidity2,Perses_Contracts_Libraries_Interfaces_Solidity2,Perses_Time_s_Solidity2,Perses_Tokens_Solidity,Perses_Functions_Solidity,Perses_Contracts_Libraries_Interfaces_Solidity,Perses_Time_s_Solidity" > "$CSV_FILE"

# Function to count the number of functions in a Solidity file
count_functions() {
    local FILE=$1
    grep -c 'function ' "$FILE" 2>/dev/null || echo "0"
}

# Function to count the number of tokens in a Solidity file
count_tokens() {
    local FILE=$1
    wc -w < "$FILE" 2>/dev/null || echo "0"
}

# Function to count the number of contracts, libraries, and interfaces in a Solidity file
count_contracts_libraries_interfaces() {
    local FILE=$1
    grep -E 'contract |library |interface ' "$FILE" 2>/dev/null | wc -l || echo "0"
}

# Function to find the most recent perses_result_* directory
find_most_recent_perses_result() {
    local DIR=$1
    find "$DIR" -type d -name 'perses_result_*' | sort -t '_' -k 3 -n | tail -1
}

# Function to measure execution time of a command in seconds
measure_time() {
    local START=$(date +%s)
    "$@"
    local END=$(date +%s)
    local DURATION=$((END - START))
    echo "$DURATION" # Return duration in seconds
}

# Function to write results to CSV
write_to_csv() {
    local DIR=$1
    local INITIAL_TOKENS=$2
    local INITIAL_FUNCTIONS=$3
    local INITIAL_CLI=$4
    local GRECUCE_TOKENS=$5
    local GRECUCE_FUNCTIONS=$6
    local GRECUCE_CLI=$7
    local GRECUCE_TIME=$8
    local PERSES_TOKENS2=$9
    local PERSES_FUNCTIONS2=${10}
    local PERSES_CLI2=${11}
    local PERSES_TIME2=${12}
    local PERSES_TOKENS=${13}
    local PERSES_FUNCTIONS=${14}
    local PERSES_CLI=${15}
    local PERSES_TIME=${16}
    echo "$DIR,$INITIAL_TOKENS,$INITIAL_FUNCTIONS,$INITIAL_CLI,$GRECUCE_TOKENS,$GRECUCE_FUNCTIONS,$GRECUCE_CLI,$GRECUCE_TIME,$PERSES_TOKENS2,$PERSES_FUNCTIONS2,$PERSES_CLI2,$PERSES_TIME2,$PERSES_TOKENS,$PERSES_FUNCTIONS,$PERSES_CLI,$PERSES_TIME" >> "$CSV_FILE"
}

# Loop through each subdirectory in the base directory
for DIR in "$BASE_DIR"/smart*; do
    # Check if the directory exists
    if [ -d "$DIR" ]; then
        # Define the file paths
        EXT_CHANGED="$DIR/ext_changed.sol"
        INITIAL_EXT_CHANGED="$DIR/initial_ext_changed.sol"
        DELETE_COMMENTS_SCRIPT="delete_comments.py"
        VERSION_FILE="$DIR/version"
        PROPERTY_FILE="$DIR/property"
        SOLIDITY2_SCRIPT="$DIR/solidity2.sh"
        SOLIDITY_SCRIPT="$DIR/solidity.sh"

        # Step 1: Store a copy of initial_ext_changed.sol
        cp "$INITIAL_EXT_CHANGED" "$EXT_CHANGED"
        
        # Count initial metrics
        FUNCTIONS_INITIAL=$(count_functions "$INITIAL_EXT_CHANGED")
        TOKENS_INITIAL=$(count_tokens "$INITIAL_EXT_CHANGED")
        CLI_INITIAL=$(count_contracts_libraries_interfaces "$INITIAL_EXT_CHANGED")

        # Step 2: Run the delete_comments.py script
        TIME_DELETE_COMMENTS=$(measure_time python3 "$DELETE_COMMENTS_SCRIPT" "$EXT_CHANGED")

        # Step 3: Run the solc-select command
        TIME_SOLC_SELECT=$(measure_time solc-select use "$(cat "$VERSION_FILE")")

        # Step 4: Run the greduce command
        GRECUCE_TIME_OUTPUT=$(measure_time greduce --consider "$(cat "$PROPERTY_FILE")" --source-file "$EXT_CHANGED")
        GRECUCE_TIME=$(echo "$GRECUCE_TIME_OUTPUT" | grep -oP 'Execution time: \K[\d.]+')

        # Count metrics after greduce
        FUNCTIONS_AFTER_GRECUCE=$(count_functions "$EXT_CHANGED")
        TOKENS_AFTER_GRECUCE=$(count_tokens "$EXT_CHANGED")
        CLI_AFTER_GRECUCE=$(count_contracts_libraries_interfaces "$EXT_CHANGED")

        # Step 5: Run the perses_deploy.jar with solidity2.sh
        TIME_PERSES_SOLIDITY2_OUTPUT=$(measure_time java -jar perses_deploy.jar --test-script "$SOLIDITY2_SCRIPT" --input-file "$EXT_CHANGED")
        PERSES_TIME2=$TIME_PERSES_SOLIDITY2_OUTPUT
        PERSRES_DIR_STEP5=$(find_most_recent_perses_result "$DIR")
        if [ -d "$PERSRES_DIR_STEP5" ]; then

            EXT_CHANGED_STEP5="$PERSRES_DIR_STEP5/ext_changed.sol"
            if [ -f "$EXT_CHANGED_STEP5" ]; then
                FUNCTIONS_AFTER_PERSES_SOLIDITY2=$(count_functions "$EXT_CHANGED_STEP5")
                TOKENS_AFTER_PERSES_SOLIDITY2=$(count_tokens "$EXT_CHANGED_STEP5")
                CLI_AFTER_PERSES_SOLIDITY2=$(count_contracts_libraries_interfaces "$EXT_CHANGED_STEP5")
            else
                FUNCTIONS_AFTER_PERSES_SOLIDITY2="N/A"
                TOKENS_AFTER_PERSES_SOLIDITY2="N/A"
                CLI_AFTER_PERSES_SOLIDITY2="N/A"
            fi
        else
            FUNCTIONS_AFTER_PERSES_SOLIDITY2="N/A"
            TOKENS_AFTER_PERSES_SOLIDITY2="N/A"
            CLI_AFTER_PERSES_SOLIDITY2="N/A"
            PERSES_TIME2="N/A"
        fi

        # Step 6: Optionally run the perses_deploy.jar with solidity.sh
        if [ "$SKIP_PERSEUS" = false ]; then
            TIME_PERSES_SOLIDITY_OUTPUT=$(measure_time java -jar perses_deploy.jar --test-script "$SOLIDITY_SCRIPT" --input-file "$INITIAL_EXT_CHANGED")
            
            # Extract the relevant execution time from perses_deploy output
            PERSES_TIME=$TIME_PERSES_SOLIDITY_OUTPUT

            # Find the most recent perses_result_* directory after step 6
            PERSRES_DIR_STEP6=$(find_most_recent_perses_result "$DIR")
            if [ -d "$PERSRES_DIR_STEP6" ]; then
                INITIAL_EXT_CHANGED_STEP6="$PERSRES_DIR_STEP6/initial_ext_changed.sol"
                if [ -f "$INITIAL_EXT_CHANGED_STEP6" ]; then
                    FUNCTIONS_AFTER_PERSES_SOLIDITY=$(count_functions "$INITIAL_EXT_CHANGED_STEP6")
                    TOKENS_AFTER_PERSES_SOLIDITY=$(count_tokens "$INITIAL_EXT_CHANGED_STEP6")
                    CLI_AFTER_PERSES_SOLIDITY=$(count_contracts_libraries_interfaces "$INITIAL_EXT_CHANGED_STEP6")
                else
                    FUNCTIONS_AFTER_PERSES_SOLIDITY="N/A"
                    TOKENS_AFTER_PERSES_SOLIDITY="N/A"
                    CLI_AFTER_PERSES_SOLIDITY="N/A"
                fi
            else
                FUNCTIONS_AFTER_PERSES_SOLIDITY="N/A"
                TOKENS_AFTER_PERSES_SOLIDITY="N/A"
                CLI_AFTER_PERSES_SOLIDITY="N/A"
            fi
        else
            FUNCTIONS_AFTER_PERSES_SOLIDITY="N/A"
            TOKENS_AFTER_PERSES_SOLIDITY="N/A"
            CLI_AFTER_PERSES_SOLIDITY="N/A"
        fi

        # Write all results to CSV
        write_to_csv "$DIR" "$TOKENS_INITIAL" "$FUNCTIONS_INITIAL" "$CLI_INITIAL" "$TOKENS_AFTER_GRECUCE" "$FUNCTIONS_AFTER_GRECUCE" "$CLI_AFTER_GRECUCE" "$GRECUCE_TIME" "$TOKENS_AFTER_PERSES_SOLIDITY2" "$FUNCTIONS_AFTER_PERSES_SOLIDITY2" "$CLI_AFTER_PERSES_SOLIDITY2" "$PERSES_TIME2" "$TOKENS_AFTER_PERSES_SOLIDITY" "$FUNCTIONS_AFTER_PERSES_SOLIDITY" "$CLI_AFTER_PERSES_SOLIDITY" "$PERSES_TIME"

    else
        echo "Directory $DIR does not exist or is not a directory."
    fi
done

