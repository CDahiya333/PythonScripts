#!/bin/zsh

# Set up error handling
set -e

# Script directory
SCRIPT_DIR="/Users/chiragdahiya/Desktop/PythonScripts"
VENV_PATH="$SCRIPT_DIR/.venv"

# Ensure we're in the right directory
cd "$SCRIPT_DIR"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Run the Python script
python "$SCRIPT_DIR/organize.py"

# Deactivate virtual environment
deactivate
