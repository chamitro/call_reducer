#!/bin/bash

sudo -v

# Experiment Runner Script
# Runs reduction experiments and logs results

# Configuration
BASE_DIR="C"
LOG_FILE="c_benchmark_results.csv"
FULL_PATH=$(pwd)

# Initialize CSV with headers
echo "folder_name,script_type,execution_time_seconds,initial_line_count,final_line_count,initial_tokens,final_tokens,status,timestamp" > "$LOG_FILE"

# Function to count lines in a file
count_lines() {
    wc -l < "$1" | tr -d ' '
}

# Function to count tokens using clang
count_tokens_clang() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "N/A"
        return
    fi
    # Use clang to tokenize and count (excludes whitespace and comments)
    local token_count=$(gcc -E -P "$file" 2>/dev/null | tr -s '[:space:]' '\n' | grep -v '^$' | wc -l)
    echo "$token_count"
}

# Function to log result
log_result() {
    local folder="$1"
    local script_type="$2"
    local exec_time="$3"
    local initial_line_count="${4:-N/A}"
    local final_line_count="${5:-N/A}"
    local initial_tokens="${6:-N/A}"
    local final_tokens="${7:-N/A}"
    local status="$8"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "$folder,$script_type,$exec_time,$initial_line_count,$final_line_count,$initial_tokens,$final_tokens,$status,$timestamp" >> "$LOG_FILE"
}

# Function to run greduce with a specific mode
run_greduce() {
    local folder="$1"
    local mode="$2"
    sudo ./$BASE_DIR/$folder/test_r.sh $BASE_DIR/$folder/small.c
    sudo rm -f small.o

    echo "[$(date)] Running greduce --mode $mode for $folder"

    # Get initial counts before greduce
    local initial_line_count=$(count_lines "./$BASE_DIR/$folder/small.c")
    local initial_tokens=$(count_tokens_clang "./$BASE_DIR/$folder/small.c")

    local start_time=$(date +%s)
    nice -n 15 greduce --source-file "./$BASE_DIR/$folder/small.c" \
                                --script "./$BASE_DIR/$folder/test_r.sh" \
                                --language c \
                                --mode "$mode"
    local exit_code=$?
    local end_time=$(date +%s)
    local exec_time=$((end_time - start_time))

    # Count lines and tokens after reduction
    local final_line_count=$(count_lines "./$BASE_DIR/$folder/small.c")
    local final_tokens=$(count_tokens_clang "./$BASE_DIR/$folder/small.c")

    # Determine status
    local status="success"
    if [ $exit_code -ne 0 ]; then
        status="failed"
    fi

    # Log greduce result with initial and final counts
    log_result "$folder" "greduce_$mode" "$exec_time" "$initial_line_count" "$final_line_count" "$initial_tokens" "$final_tokens" "$status"

    # Run perses on the reduced file
    run_perses "$folder" "$mode"

    # Restore file after both scripts complete
    echo "[$(date)] Restoring small.c for $folder"
    git restore "./$BASE_DIR/$folder/small.c"
    sudo rm -f *.o

    return $exit_code
}

# Function to run perses
run_perses() {
    local folder="$1"
    local mode="$2"

    echo "[$(date)] Running perses on $mode file for $folder"

    # Check if the input file exists
    if [ ! -f "./$BASE_DIR/$folder/small.c" ]; then
        echo "[$(date)] Warning: small.c not found for $folder, skipping perses"
        return 1
    fi

    # Get initial counts before perses
    local initial_line_count=$(count_lines "$FULL_PATH/$BASE_DIR/$folder/small.c")
    local initial_tokens=$(count_tokens_clang "$FULL_PATH/$BASE_DIR/$folder/small.c")

    local start_time=$(date +%s)
    nice -n 19 sudo java -jar perses_deploy.jar \
                              --test-script "$FULL_PATH/$BASE_DIR/$folder/perses_r.sh" \
                              --input-file "$FULL_PATH/$BASE_DIR/$folder/small.c" \
                              -o ./perses_output
    local exit_code=$?
    local end_time=$(date +%s)
    local exec_time=$((end_time - start_time))

    # Count lines and tokens after perses reduction
    local final_line_count="N/A"
    local final_tokens="N/A"

    if [ -f "./perses_output/small.c" ]; then
        final_line_count=$(count_lines "./perses_output/small.c")
        final_tokens=$(count_tokens_clang "./perses_output/small.c")
    fi

    # Determine status
    local status="success"
    if [ $exit_code -ne 0 ]; then
        status="failed"
    fi

    # Log result with mode context
    log_result "$folder" "perses_after_$mode" "$exec_time" "$initial_line_count" "$final_line_count" "$initial_tokens" "$final_tokens" "$status"

    # Clean up perses output directory
    sudo rm -rf ./perses_output

    return $exit_code
}

# Function to process a single folder
process_folder() {
    local folder="$1"

    echo "=========================================="
    echo "[$(date)] Processing folder: $folder"
    echo "=========================================="

    # Check if test_r.sh exists
    if [ ! -f "./$BASE_DIR/$folder/test_r.sh" ]; then
        echo "[$(date)] Skipping $folder - test_r.sh not found"
        return
    fi

    # Check if small.c exists
    if [ ! -f "./$BASE_DIR/$folder/small.c" ]; then
        echo "[$(date)] Skipping $folder - small.c not found"
        return
    fi

    # Run baseline perses on original file first
    run_perses "$folder" "baseline"

    # Run greduce with removal mode, then perses, then restore
    run_greduce "$folder" "removal"

    # Run greduce with combination mode, then perses, then restore
    run_greduce "$folder" "combination"

    # Run greduce with replacement mode, then perses, then restore
    run_greduce "$folder" "replacement"

    echo "[$(date)] Completed processing $folder"
    echo ""
}

# Main execution
main() {
    echo "Starting experiment runner at $(date)"
    echo "Base directory: $BASE_DIR"
    echo "Full path: $FULL_PATH"
    echo "Results will be saved to: $LOG_FILE"
    echo ""

    # Check if base directory exists
    if [ ! -d "$BASE_DIR" ]; then
        echo "Error: Directory $BASE_DIR not found!"
        exit 1
    fi

    # Process each folder in C directory
    for folder in "$BASE_DIR"/*/ ; do
        sudo rm -f *.o
        sudo -v
        if [ -d "$folder" ]; then
            folder_name=$(basename "$folder")
            process_folder "$folder_name"
        fi
    done

    echo "=========================================="
    echo "All experiments completed at $(date)"
    echo "Results saved to: $LOG_FILE"
    echo "=========================================="
}

# Run main function
main "$@"