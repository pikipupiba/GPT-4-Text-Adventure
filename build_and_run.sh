#!/bin/bash
# Troubleshooting:

# wsl create process not expected to return

# wsl --install Ubuntu
# exit
# wsl -s Ubuntu
# wsl -d Ubuntu
# exit
# turn off docker-desktop auto start
# restart computer
# launch docker-desktop

# Function to stop the container
cleanup() {
  echo "Saving data and stopping container..."
  docker stop "$CONTAINER_NAME"
  docker rm "$CONTAINER_NAME"
trap cleanup INT
}

print_help() {
  echo "Usage: $0 [OPTIONS]"
  echo "Build and run a Docker image."
  echo
  echo "  Option         Description                                  Default"
  echo "  -k, --name     OpenAI API key.                              $ + OPENAI_API_KEY"
  echo "  -n, --name     Creates <name>_image and <name>_container.   ai-adventure-academy"
  echo "  -p, --port     Specify the port.                            80"
  echo "  -s, --share    Enable Gradio share mode.                    Off"
  echo "  -h, --help     Show this help message and exit."
}

# Default image name
NAME="ai-adventure-academy"
SHARE_MODE=False
PORT=80

# Parse command-line options
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -k|--key)
      echo "OpenAI API key set"
      OPENAI_API_KEY="$2"
      shift
      shift
      ;;
    -a|--azure-key)
      echo "Azure OpenAI API key set"
      AZURE_OPENAI_API_KEY="$2"
      shift
      shift
      ;;
    -b|--azure-base)
      echo "Azure OpenAI API base set"
      AZURE_OPENAI_API_BASE="$2"
      shift
      shift
      ;;
    -n|--name)
      echo "Name set to $2"
      NAME="$2"
      shift
      shift
      ;;
    -p|--port)
      echo "Port set to $2"
      PORT="$2"
      shift
      shift
      ;;
    -s|--share)
      echo "Share mode enabled"
      SHARE_MODE=True
      shift
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "Unknown option: $key"
      exit 1
      ;;
  esac
done

IMAGE_NAME=${NAME}_image
CONTAINER_NAME=${NAME}_container

if docker build -t "$IMAGE_NAME" .; then
  echo "Image successfully built!"

  if docker inspect "$CONTAINER_NAME" &> /dev/null; then
    echo "Container $CONTAINER_NAME already exists. Saving data and stopping container..."
    docker stop "$CONTAINER_NAME"
    docker rm "$CONTAINER_NAME"
  else
    echo "Container $CONTAINER_NAME does not exist."
  fi

  echo "Running new container..."

  # Run the container, mapping port 8000 inside the container to port 8000 on the host
  # --mount type=bind,source=/home/ubuntu/game_data,target=/app/data/history \
  docker run \
    --name "$CONTAINER_NAME" \
    -p "$PORT":"$PORT" \
    -e OPENAI_API_KEY="$OPENAI_API_KEY" \
    -e AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" \
    -e AZURE_OPENAI_API_BASE="$AZURE_OPENAI_API_BASE" \
    -e GRADIO_SERVER_NAME="0.0.0.0" \
    -e GRADIO_SERVER_PORT="$PORT" \
    -e SHARE_MODE="$SHARE_MODE" \
    "$IMAGE_NAME"

  # Clean up container when script exits normally
  cleanup
else
  echo "Build failed. Exiting..."
  exit 1
fi
