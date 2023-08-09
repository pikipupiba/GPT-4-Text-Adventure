#!/bin/bash

# Update and install required packages
apt-get update
apt-get install -y git awscli jq

# Fetch the OPENAI_API_KEY from AWS Secrets Manager
SECRET_NAME="OPENAI_API_KEY"
REGION="us-east-1"
OPENAI_API_KEY=$(aws secretsmanager get-secret-value --secret-id "$SECRET_NAME" --region "$REGION" | jq -r '.SecretString')
# Export OPENAI_API_KEY as an environment variable (this will only set it for the duration of the script)
export OPENAI_API_KEY=$OPENAI_API_KEY
echo "export OPENAI_API_KEY=$OPENAI_API_KEY" >> /etc/environment


# Define the repo and directory
REPO_URL="https://github.com/pikipupiba/GPT-4-Text-Adventure.git"
CLONE_DIR="/home/ubuntu"
REPO_DIR="$CLONE_DIR/GPT-4-Text-Adventure"

# Check if directory exists
if [ -d "$CLONE_DIR" ]; then
    # If it exists, navigate to it and pull the latest changes
    cd "$CLONE_DIR" || exit
    git pull
else
    # If it doesn't exist, clone the repo
    git clone "$REPO_URL" "$CLONE_DIR"
    cd "$CLONE_DIR" || exit
fi

chmod +x "$REPO_DIR/build_and_run.sh"

# Navigate to the repo
cd "$REPO_DIR" || exit