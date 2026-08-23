#!/bin/sh
cd "$(dirname "$0")"

if [ ! -f "venv/bin/activate" ]; then
  rm -rf venv
  if ! python3 -m venv venv 2>/dev/null; then
    echo "python3-venv is missing, installing it..."
    PYVER=$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')
    apt-get update -y
    apt-get install -y python3-venv "python${PYVER}-venv" 2>/dev/null \
      || apt-get install -y python3-venv \
      || apt-get install -y "python${PYVER}-venv"
    python3 -m venv venv
  fi
fi

. venv/bin/activate

pip install -r requirements.txt

PORT="${ANDALUSIA_PORT:-8765}"
if [ "${ANDALUSIA_HOST:-127.0.0.1}" = "0.0.0.0" ]; then
  PUBLIC_IP=$(curl -s -4 ifconfig.me 2>/dev/null)
  if [ -n "$PUBLIC_IP" ]; then
    echo "Working URL: http://${PUBLIC_IP}:${PORT}"
  else
    echo "Working URL: http://<your-server-ip>:${PORT}  (could not auto-detect public IP)"
  fi
else
  echo "Working URL: http://127.0.0.1:${PORT}"
fi

python3 server.py
