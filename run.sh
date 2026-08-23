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
python3 server.py
