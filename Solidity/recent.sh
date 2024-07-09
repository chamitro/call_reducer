#!/bin/bash

# Check if a directory argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <base_directory>"
    exit 1
fi

# Base directory to search in
BASE_DIR="$1"

# Check if the provided argument is a directory
if [ ! -d "$BASE_DIR" ]; then
    echo "Error: '$BASE_DIR' is not a valid directory."
    exit 1
fi

# Find the most recent directory created within the base directory's subdirectories
most_recent_dir=$(find "$BASE_DIR" -mindepth 1 -maxdepth 1 -type d -exec stat -c "%Y %n" {} \; | sort -nr | head -n 1 | awk '{print $2}')

if [ -n "$most_recent_dir" ]; then
    echo "Most recent directory created among subdirectories of '$BASE_DIR': $most_recent_dir"
else
    echo "No subdirectories found in '$BASE_DIR'."
fi

