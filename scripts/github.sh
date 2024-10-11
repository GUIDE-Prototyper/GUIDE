#!/bin/bash

# Define variables
REPO_URL="github-repo-url"
REPO_DIR="/data/GUIDE/"

# Function to handle errors
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Update GitHub repo
echo "Cloning repository from GitHub..."
cd "$REPO_DIR" || error_exit "Failed to access newly cloned repository"
git pull "$REPO_URL" || error_exit "Failed to clone repository from GitHub"
