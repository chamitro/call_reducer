#!/bin/bash

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

# Function to extract token counts from perses output
extract_perses_tokens() {
    local output="$1"
    # Initial token count: look for "started at" line with #tokens=
    local initial=$(echo "$output" | grep -oP "started at.*?#tokens=\K\d+" | head -1 || echo "N/A")
    # Final token count: look for the final summary line "Reduction ratio is X/Y"
    local final=$(echo "$output" | grep -oP "Reduction ratio is \K\d+(?=/\d+)" | tail -1 || echo "N/A")
    # If no summary found, try to get from fixpoint iterations
    if [ "$final" = "N/A" ]; then
        final=$(echo "$output" | grep -oP "#Tokens=\K\d+" | tail -1 || echo "N/A")
    fi
    # If still not found, try the ratio format
    if [ "$final" = "N/A" ]; then
        final=$(echo "$output" | grep -oP "ratio=\K\d+(?=/\d+)" | tail -1 || echo "N/A")
    fi
    echo "$initial,$final"
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
    sudo rm small.o

    echo "[$(date)] Running greduce --mode $mode for $folder"

    # Get initial line count before greduce
    local initial_line_count=$(count_lines "./$BASE_DIR/$folder/small.c")

    local start_time=$(date +%s)
    local output=$(greduce --source-file "./$BASE_DIR/$folder/small.c" \
                                --script "./$BASE_DIR/$folder/test_r.sh" \
                                --language c \
                                --mode "$mode" 2>&1)
    local exit_code=$?
    local end_time=$(date +%s)
    local exec_time=$((end_time - start_time))

    # Count lines after reduction
    local final_line_count=$(count_lines "./$BASE_DIR/$folder/small.c")

    # Determine status
    local status="success"
    if [ $exit_code -ne 0 ]; then
        status="failed"
    fi

    # Log greduce result with initial and final line counts
    log_result "$folder" "greduce_$mode" "$exec_time" "$initial_line_count" "$final_line_count" "N/A" "N/A" "$status"

    # Run perses on the reduced file
    run_perses_on_reduced "$folder" "$mode"

    # Restore file after both scripts complete
    echo "[$(date)] Restoring small.c for $folder"
    git restore "./$BASE_DIR/$folder/small.c"

    return $exit_code
}

# Function to run perses on the reduced file
run_perses_on_reduced() {
    local folder="$1"
    local mode="$2"

    echo "[$(date)] Running perses on $mode reduced file for $folder"

    # Check if the reduced file exists
    if [ ! -f "./$BASE_DIR/$folder/small.c" ]; then
        echo "[$(date)] Warning: small.c not found for $folder, skipping perses"
        log_result "$folder" "perses_after_$mode" "0" "N/A" "N/A" "N/A" "N/A" "skipped_no_input"
        return 1
    fi

    # Get initial line count
    local initial_line_count=$(count_lines "$FULL_PATH/$BASE_DIR/$folder/small.c")

    local start_time=$(date +%s)
#    echo "sudo java -jar perses_deploy.jar --test-script '${FULL_PATH}/${BASE_DIR}/${folder}/test_r.sh' --input-file '${FULL_PATH}/${BASE_DIR}/${folder}/small.c' -o . 2>&1"
    local output=$(sudo java -jar perses_deploy.jar \
                              --test-script "$FULL_PATH/$BASE_DIR/$folder/test_r.sh" \
                              --input-file "$FULL_PATH/$BASE_DIR/$folder/small.c" \
                              -o . 2>&1)
    local exit_code=$?
    local end_time=$(date +%s)
    local exec_time=$((end_time - start_time))

    # Extract token counts
    local tokens=$(extract_perses_tokens "$output")
    local initial_tokens=$(echo "$tokens" | cut -d',' -f1)
    local final_tokens=$(echo "$tokens" | cut -d',' -f2)

    # Count lines after perses reduction (if output file exists)
    local final_line_count="N/A"
    if [ -f "./temp_query_reduction_output.c" ]; then
        final_line_count=$(count_lines "./temp_query_reduction_output.c")
    elif [ -f "$FULL_PATH/$BASE_DIR/$folder/small.c" ]; then
        # Perses might modify the file in place
        final_line_count=$(count_lines "$FULL_PATH/$BASE_DIR/$folder/small.c")
    fi

    # Determine status
    local status="success"
    if [ $exit_code -ne 0 ]; then
        status="failed"
    fi

    # Log result with mode context
    log_result "$folder" "perses_after_$mode" "$exec_time" "$initial_line_count" "$final_line_count" "$initial_tokens" "$final_tokens" "$status"

    return $exit_code
}

# Function to run perses (legacy - kept for compatibility)
run_perses() {
    local folder="$1"

    echo "[$(date)] Running perses for $folder"

    local start_time=$(date +%s)
    local output=$(sudo java -jar perses_deploy.jar \
                              --test-script "$FULL_PATH/$BASE_DIR/$folder/test_r.sh" \
                              --input-file "$FULL_PATH/$BASE_DIR/$folder/small_c_removal_reduction.c" \
                              -o . 2>&1)
    local exit_code=$?
    local end_time=$(date +%s)
    local exec_time=$((end_time - start_time))

    # Extract token counts
    local tokens=$(extract_perses_tokens "$output")
    local initial_tokens=$(echo "$tokens" | cut -d',' -f1)
    local final_tokens=$(echo "$tokens" | cut -d',' -f2)

    # Count lines of input file
    local initial_line_count=$(count_lines "$FULL_PATH/$BASE_DIR/$folder/small_c_removal_reduction.c")
    local final_line_count="N/A"

    # Determine status
    local status="success"
    if [ $exit_code -ne 0 ]; then
        status="failed"
    fi

    # Log result
    log_result "$folder" "perses" "$exec_time" "$initial_line_count" "$final_line_count" "$initial_tokens" "$final_tokens" "$status"

    return $exit_code
}

# Function to run perses on original file before any greduce
run_perses_baseline() {
    local folder="$1"

    echo "[$(date)] Running baseline perses on original file for $folder"

    # Check if the file exists
    if [ ! -f "./$BASE_DIR/$folder/small.c" ]; then
        echo "[$(date)] Warning: small.c not found for $folder, skipping baseline perses"
        log_result "$folder" "perses_baseline" "0" "N/A" "N/A" "N/A" "N/A" "skipped_no_input"
        return 1
    fi

    # Get initial line count
    local initial_line_count=$(count_lines "$FULL_PATH/$BASE_DIR/$folder/small.c")

    local start_time=$(date +%s)
    local output=$(sudo java -jar perses_deploy.jar \
                              --test-script "$FULL_PATH/$BASE_DIR/$folder/test_r.sh" \
                              --input-file "$FULL_PATH/$BASE_DIR/$folder/small.c" \
                              -o . 2>&1)
    local exit_code=$?
    local end_time=$(date +%s)
    local exec_time=$((end_time - start_time))

    # Extract token counts
    local tokens=$(extract_perses_tokens "$output")
    local initial_tokens=$(echo "$tokens" | cut -d',' -f1)
    local final_tokens=$(echo "$tokens" | cut -d',' -f2)

    # Count lines after perses reduction
    local final_line_count="N/A"
    if [ -f "./temp_query_reduction_output.c" ]; then
        final_line_count=$(count_lines "./temp_query_reduction_output.c")
    elif [ -f "$FULL_PATH/$BASE_DIR/$folder/small.c" ]; then
        final_line_count=$(count_lines "$FULL_PATH/$BASE_DIR/$folder/small.c")
    fi

    # Determine status
    local status="success"
    if [ $exit_code -ne 0 ]; then
        status="failed"
    fi

    # Log baseline result
    log_result "$folder" "perses_baseline" "$exec_time" "$initial_line_count" "$final_line_count" "$initial_tokens" "$final_tokens" "$status"

    # Restore file after baseline perses
    echo "[$(date)] Restoring small.c after baseline perses for $folder"
    git restore "./$BASE_DIR/$folder/small.c"

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
    run_perses_baseline "$folder"

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
