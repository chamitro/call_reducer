#!/bin/bash

# Configuration
CSV_FILE="command_results.csv"
COMMAND_TO_TIME="your-command-here"  # Replace with your actual command
CHECK_COMMAND="your-check-command"   # Replace with your verification command

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Main function
main() {
    log "Script started"
    
    # Get sudo access upfront
    sudo -v
    if [ $? -ne 0 ]; then
        log "Failed to get sudo access. Exiting."
        exit 1
    fi
    
    # Keep sudo alive in background
    while true; do
        sudo -n true
        sleep 50
        kill -0 "$$" 2>/dev/null || exit
    done &
    
    # Create CSV file with headers if it doesn't exist
    if [ ! -f "$CSV_FILE" ]; then
        echo "Timestamp,Command,Execution_Time_Seconds,Status" > "$CSV_FILE"
        log "Created CSV file: $CSV_FILE"
    fi
    
    # Record start time
    START_TIME=$(date +%s.%N)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    log "Executing command: $COMMAND_TO_TIME"
    
    # Run the command and capture execution time
    eval "$COMMAND_TO_TIME"
    COMMAND_EXIT_CODE=$?
    
    # Calculate execution time
    END_TIME=$(date +%s.%N)
    EXECUTION_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    
    log "Command completed in ${EXECUTION_TIME}s with exit code $COMMAND_EXIT_CODE"
    
    # Run the check command
    log "Running check command: $CHECK_COMMAND"
    eval "$CHECK_COMMAND"
    CHECK_EXIT_CODE=$?
    
    # Determine status based on check command exit code
    if [ $CHECK_EXIT_CODE -eq 0 ]; then
        STATUS="error reproduced"
    elif [ $CHECK_EXIT_CODE -eq 1 ]; then
        STATUS="could not reproduce"
    else
        STATUS="unexpected exit code: $CHECK_EXIT_CODE"
    fi
    
    log "Check command result: $STATUS"
    
    # Write to CSV
    echo "\"$TIMESTAMP\",\"$COMMAND_TO_TIME\",$EXECUTION_TIME,\"$STATUS\"" >> "$CSV_FILE"
    
    log "Results written to $CSV_FILE"
    log "Script completed"
}

# Run main function in background if --background flag is provided
if [ "$1" == "--background" ]; then
    # Run in background and redirect output to log file
    LOG_FILE="script_output.log"
    nohup bash -c "$(declare -f main); $(declare -f log); main" > "$LOG_FILE" 2>&1 &
    echo "Script running in background. PID: $!"
    echo "Check $LOG_FILE for output"
else
    # Run in foreground
    main
fi#!/bin/bash

# Configuration
CSV_FILE="command_results.csv"
COMMAND_TO_TIME="your-command-here"  # Replace with your actual command
CHECK_COMMAND="your-check-command"   # Replace with your verification command

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Main function
main() {
    log "Script started"
    
    # Get sudo access upfront
    sudo -v
    if [ $? -ne 0 ]; then
        log "Failed to get sudo access. Exiting."
        exit 1
    fi
    
    # Keep sudo alive in background
    while true; do
        sudo -n true
        sleep 50
        kill -0 "$$" 2>/dev/null || exit
    done &
    
    # Create CSV file with headers if it doesn't exist
    if [ ! -f "$CSV_FILE" ]; then
        echo "Timestamp,Command,Execution_Time_Seconds,Status" > "$CSV_FILE"
        log "Created CSV file: $CSV_FILE"
    fi
    
    # Record start time
    START_TIME=$(date +%s.%N)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    log "Executing command: $COMMAND_TO_TIME"
    
    # Run the command and capture execution time
    eval "$COMMAND_TO_TIME"
    COMMAND_EXIT_CODE=$?
    
    # Calculate execution time
    END_TIME=$(date +%s.%N)
    EXECUTION_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    
    log "Command completed in ${EXECUTION_TIME}s with exit code $COMMAND_EXIT_CODE"
    
    # Run the check command
    log "Running check command: $CHECK_COMMAND"
    eval "$CHECK_COMMAND"
    CHECK_EXIT_CODE=$?
    
    # Determine status based on check command exit code
    if [ $CHECK_EXIT_CODE -eq 0 ]; then
        STATUS="error reproduced"
    elif [ $CHECK_EXIT_CODE -eq 1 ]; then
        STATUS="could not reproduce"
    else
        STATUS="unexpected exit code: $CHECK_EXIT_CODE"
    fi
    
    log "Check command result: $STATUS"
    
    # Write to CSV
    echo "\"$TIMESTAMP\",\"$COMMAND_TO_TIME\",$EXECUTION_TIME,\"$STATUS\"" >> "$CSV_FILE"
    
    log "Results written to $CSV_FILE"
    log "Script completed"
}

# Run main function in background if --background flag is provided
if [ "$1" == "--background" ]; then
    # Run in background and redirect output to log file
    LOG_FILE="script_output.log"
    nohup bash -c "$(declare -f main); $(declare -f log); main" > "$LOG_FILE" 2>&1 &
    echo "Script running in background. PID: $!"
    echo "Check $LOG_FILE for output"
else
    # Run in foreground
    main
fi#!/bin/bash

# Configuration
CSV_FILE="command_results.csv"
COMMAND_TO_TIME="your-command-here"  # Replace with your actual command
CHECK_COMMAND="your-check-command"   # Replace with your verification command

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Main function
main() {
    log "Script started"
    
    # Get sudo access upfront
    sudo -v
    if [ $? -ne 0 ]; then
        log "Failed to get sudo access. Exiting."
        exit 1
    fi
    
    # Keep sudo alive in background
    while true; do
        sudo -n true
        sleep 50
        kill -0 "$$" 2>/dev/null || exit
    done &
    
    # Create CSV file with headers if it doesn't exist
    if [ ! -f "$CSV_FILE" ]; then
        echo "Timestamp,Command,Execution_Time_Seconds,Status" > "$CSV_FILE"
        log "Created CSV file: $CSV_FILE"
    fi
    
    # Record start time
    START_TIME=$(date +%s.%N)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    log "Executing command: $COMMAND_TO_TIME"
    
    # Run the command and capture execution time
    eval "$COMMAND_TO_TIME"
    COMMAND_EXIT_CODE=$?
    
    # Calculate execution time
    END_TIME=$(date +%s.%N)
    EXECUTION_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    
    log "Command completed in ${EXECUTION_TIME}s with exit code $COMMAND_EXIT_CODE"
    
    # Run the check command
    log "Running check command: $CHECK_COMMAND"
    eval "$CHECK_COMMAND"
    CHECK_EXIT_CODE=$?
    
    # Determine status based on check command exit code
    if [ $CHECK_EXIT_CODE -eq 0 ]; then
        STATUS="error reproduced"
    elif [ $CHECK_EXIT_CODE -eq 1 ]; then
        STATUS="could not reproduce"
    else
        STATUS="unexpected exit code: $CHECK_EXIT_CODE"
    fi
    
    log "Check command result: $STATUS"
    
    # Write to CSV
    echo "\"$TIMESTAMP\",\"$COMMAND_TO_TIME\",$EXECUTION_TIME,\"$STATUS\"" >> "$CSV_FILE"
    
    log "Results written to $CSV_FILE"
    log "Script completed"
}

# Run main function in background if --background flag is provided
if [ "$1" == "--background" ]; then
    # Run in background and redirect output to log file
    LOG_FILE="script_output.log"
    nohup bash -c "$(declare -f main); $(declare -f log); main" > "$LOG_FILE" 2>&1 &
    echo "Script running in background. PID: $!"
    echo "Check $LOG_FILE for output"
else
    # Run in foreground
    main
fi#!/bin/bash

# Configuration
CSV_FILE="command_results.csv"
COMMAND_TO_TIME="your-command-here"  # Replace with your actual command
CHECK_COMMAND="your-check-command"   # Replace with your verification command

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Main function
main() {
    log "Script started"
    
    # Get sudo access upfront
    sudo -v
    if [ $? -ne 0 ]; then
        log "Failed to get sudo access. Exiting."
        exit 1
    fi
    
    # Keep sudo alive in background
    while true; do
        sudo -n true
        sleep 50
        kill -0 "$$" 2>/dev/null || exit
    done &
    
    # Create CSV file with headers if it doesn't exist
    if [ ! -f "$CSV_FILE" ]; then
        echo "Timestamp,Command,Execution_Time_Seconds,Status" > "$CSV_FILE"
        log "Created CSV file: $CSV_FILE"
    fi
    
    # Record start time
    START_TIME=$(date +%s.%N)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    log "Executing command: $COMMAND_TO_TIME"
    
    # Run the command and capture execution time
    eval "$COMMAND_TO_TIME"
    COMMAND_EXIT_CODE=$?
    
    # Calculate execution time
    END_TIME=$(date +%s.%N)
    EXECUTION_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    
    log "Command completed in ${EXECUTION_TIME}s with exit code $COMMAND_EXIT_CODE"
    
    # Run the check command
    log "Running check command: $CHECK_COMMAND"
    eval "$CHECK_COMMAND"
    CHECK_EXIT_CODE=$?
    
    # Determine status based on check command exit code
    if [ $CHECK_EXIT_CODE -eq 0 ]; then
        STATUS="error reproduced"
    elif [ $CHECK_EXIT_CODE -eq 1 ]; then
        STATUS="could not reproduce"
    else
        STATUS="unexpected exit code: $CHECK_EXIT_CODE"
    fi
    
    log "Check command result: $STATUS"
    
    # Write to CSV
    echo "\"$TIMESTAMP\",\"$COMMAND_TO_TIME\",$EXECUTION_TIME,\"$STATUS\"" >> "$CSV_FILE"
    
    log "Results written to $CSV_FILE"
    log "Script completed"
}

# Run main function in background if --background flag is provided
if [ "$1" == "--background" ]; then
    # Run in background and redirect output to log file
    LOG_FILE="script_output.log"
    nohup bash -c "$(declare -f main); $(declare -f log); main" > "$LOG_FILE" 2>&1 &
    echo "Script running in background. PID: $!"
    echo "Check $LOG_FILE for output"
else
    # Run in foreground
    main
fi#!/bin/bash

# Configuration
CSV_FILE="command_results.csv"
COMMAND_TO_TIME="your-command-here"  # Replace with your actual command
CHECK_COMMAND="your-check-command"   # Replace with your verification command

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Main function
main() {
    log "Script started"
    
    # Get sudo access upfront
    sudo -v
    if [ $? -ne 0 ]; then
        log "Failed to get sudo access. Exiting."
        exit 1
    fi
    
    # Keep sudo alive in background
    while true; do
        sudo -n true
        sleep 50
        kill -0 "$$" 2>/dev/null || exit
    done &
    
    # Create CSV file with headers if it doesn't exist
    if [ ! -f "$CSV_FILE" ]; then
        echo "Timestamp,Command,Execution_Time_Seconds,Status" > "$CSV_FILE"
        log "Created CSV file: $CSV_FILE"
    fi
    
    # Record start time
    START_TIME=$(date +%s.%N)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    log "Executing command: $COMMAND_TO_TIME"
    
    # Run the command and capture execution time
    eval "$COMMAND_TO_TIME"
    COMMAND_EXIT_CODE=$?
    
    # Calculate execution time
    END_TIME=$(date +%s.%N)
    EXECUTION_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    
    log "Command completed in ${EXECUTION_TIME}s with exit code $COMMAND_EXIT_CODE"
    
    # Run the check command
    log "Running check command: $CHECK_COMMAND"
    eval "$CHECK_COMMAND"
    CHECK_EXIT_CODE=$?
    
    # Determine status based on check command exit code
    if [ $CHECK_EXIT_CODE -eq 0 ]; then
        STATUS="error reproduced"
    elif [ $CHECK_EXIT_CODE -eq 1 ]; then
        STATUS="could not reproduce"
    else
        STATUS="unexpected exit code: $CHECK_EXIT_CODE"
    fi
    
    log "Check command result: $STATUS"
    
    # Write to CSV
    echo "\"$TIMESTAMP\",\"$COMMAND_TO_TIME\",$EXECUTION_TIME,\"$STATUS\"" >> "$CSV_FILE"
    
    log "Results written to $CSV_FILE"
    log "Script completed"
}

# Run main function in background if --background flag is provided
if [ "$1" == "--background" ]; then
    # Run in background and redirect output to log file
    LOG_FILE="script_output.log"
    nohup bash -c "$(declare -f main); $(declare -f log); main" > "$LOG_FILE" 2>&1 &
    echo "Script running in background. PID: $!"
    echo "Check $LOG_FILE for output"
else
    # Run in foreground
    main
fi

