#!/bin/bash

# Pull the latest changes from the remote repository
git pull

# Set PYTHONPATH and run the Python script
export PYTHONPATH=$(pwd)
python scripts/python/get_training_profile_data.py

# Get the current timestamp
current_timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# Add all changes to the staging area
git add .

# Commit changes with a dynamic message
commit_message="JF: Retraining $current_timestamp"
git commit -m "$commit_message"

# Push changes to the current branch
git push
