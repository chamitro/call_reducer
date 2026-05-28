#!/bin/bash

SRC="Java/final-jdk-source"
DEST="Java/final-jdk-modified"

# Delete everything from the destination directory
rm -rf "$DEST"/*

# Copy everything from the source to the destination, preserving structure
cp -a "$SRC"/. "$DEST"/