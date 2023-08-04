#!/bin/bash

# Default image name
IMAGE_NAME="ai-adventure-academy"
SHARE_MODE=False
PORT=7878

# Parse command-line options
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -n|--name)
      echo "Image name set to $2"
      IMAGE_NAME="$2"
      shift
      shift
      ;;
    -p|--port)
      echo "Port set to $2"
      PORT="$2"
      shift
      shift
      ;;
    -s|--share-mode)
      echo "Share mode enabled"
      SHARE_MODE=True
      shift
      ;;
    *)
      echo "Unknown option: $key"
      exit 1
      ;;
  esac
done

if docker build -t "$IMAGE_NAME" .; then
  echo "Image successfully built!"

  # Run the container, mapping port 8000 inside the container to port 8000 on the host
  docker run \
    -it \
    -p "$PORT":"$PORT" \
    -e OPENAI_API_KEY \
    -e GRADIO_SERVER_NAME="0.0.0.0" \
    -e GRADIO_SERVER_PORT="$PORT" \
    -e SHARE_MODE="$SHARE_MODE" \
    "$IMAGE_NAME"
else
  echo "Build failed. Exiting..."
  exit 1
fi