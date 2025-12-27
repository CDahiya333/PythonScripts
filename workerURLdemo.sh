#!/bin/bash



# Define the path where your script and venv live

BASE_DIR="/Users/chiragdahiya/Desktop/PythonScripts"



# Check for arguments

if [ "$#" -lt 2 ]; then

    echo "Usage: workerURL <URL> <DIRECTORY>"

    exit 1

fi



# Activate virtual environment

if [ -f "$BASE_DIR/.venv/bin/activate" ]; then

    source "$BASE_DIR/.venv/bin/activate"

else

    echo "Error: Virtual environment not found in $BASE_DIR/.venv"

    exit 1

fi



# Run the python script

python3 "$BASE_DIR/selenium_downloader.py" "$1" "$2"



# Clean up

deactivate%                                    
# Make sure to make the sh file executable `chmod +x workerURLdemo.sh`
# Additionally you can either directly export the variable to PATH which is easier to manage everything in one place but prone to errors if the file is modified
# Second approach it to create ~/bin folder and then moving your scripts there preventing any modifications to these scripts.