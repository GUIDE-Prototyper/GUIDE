#!/bin/bash

# Define variables
VENV_DIR="/data/venv-guide/"
GUNICORN_CONFIG="/data/GUIDE/gunicorn.conf.py"

# Function to handle errors
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Activate the virtual environment
echo "Activating virtual environment..."
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
else
    error_exit "Virtual environment not found"
fi

# Restart Gunicorn
echo "Starting Gunicorn..."
gunicorn -c "$GUNICORN_CONFIG" quartapp.app:app || error_exit "Failed to start Gunicorn"