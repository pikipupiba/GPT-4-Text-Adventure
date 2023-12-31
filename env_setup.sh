#!/bin/bash

# Update and install required packages
yum update
yum install -y git awscli jq

# Fetch the OPENAI_API_KEY from AWS Secrets Manager
REGION="us-east-1"
OPENAI_API_KEY_SECRET=$(aws secretsmanager get-secret-value --secret-id "OPENAI_API_KEY" --region "$REGION" | jq -r '.SecretString')
OPENAI_API_KEY=$(echo "$OPENAI_API_KEY_SECRET" | jq -r '.OPENAI_API_KEY')
# Export OPENAI_API_KEY as an environment variable (this will only set it for the duration of the script)
export OPENAI_API_KEY="$OPENAI_API_KEY"
# Add OPENAI_API_KEY to /etc/environment so it persists after the script is done
echo "export OPENAI_API_KEY=$OPENAI_API_KEY" >> /etc/environment


# Define the repo and directory
REPO_URL="https://github.com/pikipupiba/GPT-4-Text-Adventure.git"
CLONE_DIR="/home/ubuntu/AI-Adventure-Academy"
REPO_DIR="$CLONE_DIR/GPT-4-Text-Adventure"

# Check if directory exists
if [ -d "$CLONE_DIR" ]; then
    # If it exists, navigate to it and pull the latest changes
    echo "Directory $CLONE_DIR exists, pulling latest changes for $REPO_URL"
    cd "$CLONE_DIR" || return
    sudo git reset --hard origin/master
    sudo git clean -fxd
    PULL_OUTPUT=$(sudo git pull)
    echo "$PULL_OUTPUT"
else
    # If it doesn't exist, clone the repo
    echo "Directory $CLONE_DIR does not exist, cloning $REPO_URL"
    sudo git clone "$REPO_URL" "$CLONE_DIR"
    cd "$CLONE_DIR" || return
    PULL_OUTPUT="New clone"
fi

sudo chmod +x "$REPO_DIR/build_and_run.sh"

# Navigate to the repo
cd "$REPO_DIR" || return

# Only run the script if the repo was not already up-to-date
if [[ ! "$PULL_OUTPUT" == *"Already up to date"* ]]; then
    sudo bash ./build_and_run.sh -k "$OPENAI_API_KEY"
fi
