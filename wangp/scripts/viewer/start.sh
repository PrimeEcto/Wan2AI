#!/bin/bash
# Start Wan2AI Image Gallery Server
# Usage: start.sh --gallery-dir /path/to/images [--port PORT] [--open]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GALLERY_DIR=""
PORT=0
HOST="127.0.0.1"
OPEN_BROWSER=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --gallery-dir) GALLERY_DIR="$2"; shift 2 ;;
    --port) PORT="$2"; shift 2 ;;
    --host) HOST="$2"; shift 2 ;;
    --open) OPEN_BROWSER=true; shift ;;
    *) shift ;;
  esac
done

if [ -z "$GALLERY_DIR" ]; then
  echo '{"error": "--gallery-dir is required"}' >&2
  exit 1
fi

mkdir -p "$GALLERY_DIR"

# Start server in background
python3 "$SCRIPT_DIR/server.py" --gallery-dir "$GALLERY_DIR" --port "$PORT" --host "$HOST" &
SERVER_PID=$!

# Wait for server to output its info
sleep 1

# Read server info
STATE_DIR="$GALLERY_DIR/../.viewer-state"
if [ -f "$STATE_DIR/server-info" ]; then
  URL=$(python3 -c "import json; print(json.load(open('$STATE_DIR/server-info'))['url'])")

  if [ "$OPEN_BROWSER" = true ]; then
    if command -v xdg-open &>/dev/null; then
      xdg-open "$URL" &>/dev/null &
    elif command -v open &>/dev/null; then
      open "$URL" &>/dev/null &
    fi
  fi

  cat "$STATE_DIR/server-info"
else
  echo '{"error": "Server failed to start"}' >&2
  exit 1
fi
