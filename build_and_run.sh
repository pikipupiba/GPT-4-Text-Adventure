#!/bin/bash

# Function to stop the container
cleanup() {
  echo "Stopping container..."
  docker stop "$CONTAINER_NAME"
}

# Trap to call cleanup function on Ctrl+C
trap cleanup INT

print_help() {
  echo "Usage: $0 [OPTIONS]"
  echo "Build and run a Docker image."
  echo
  echo "  Option         Description                                  Default"
  echo "  -n, --name     Creates <name>_image and <name>_container.   ai-adventure-academy"
  echo "  -p, --port     Specify the port.                            7878"
  echo "  -s, --share    Enable Gradio share mode.                    Off"
  echo "  -h, --help     Show this help message and exit."
}

# Default image name
NAME="ai-adventure-academy"
SHARE_MODE=False
PORT=7878

# Parse command-line options
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
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

  # Run the container, mapping port 8000 inside the container to port 8000 on the host
  docker run \
    --name "$CONTAINER_NAME" \
    -it \
    -p "$PORT":"$PORT" \
    -e OPENAI_API_KEY \
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