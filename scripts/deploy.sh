#!/bin/bash

# Define variables
REPO_URL="github-repo-url"
REPO_DIR="/data/GUIDE/"
VENV_DIR="/data/venv-guide/"
GUNICORN_CONFIG="/data/GUIDE/gunicorn.conf.py"

# Function to handle errors
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Update GitHub repo
echo "Cloning repository from GitHub..."
cd "$REPO_DIR" || error_exit "Failed to access newly cloned repository"
git pull "$REPO_URL" || error_exit "Failed to clone repository from GitHub"


# Activate the virtual environment
echo "Activating virtual environment..."
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
else
    error_exit "Virtual environment not found"
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt || error_exit "Failed to install dependencies"

# Restart Gunicorn
echo "Restarting Gunicorn..."
pkill -f gunicorn
echo "Starting Gunicorn..."
gunicorn -c "$GUNICORN_CONFIG" quartapp.app:app --daemon || error_exit "Failed to start Gunicorn"