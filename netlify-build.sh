#!/bin/bash

# Exit on error
set -e

# Print commands for debugging
set -x

# Create necessary directories
mkdir -p output
mkdir -p templates

# Install Python dependencies
pip install -r requirements.txt

# Print Python version
python --version

# Make sure directories exist
ls -la

echo "Build completed successfully"
