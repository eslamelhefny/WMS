#!/usr/bin/env bash
set -euo pipefail
if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
  echo "Run as root: sudo bash deploy/update_app.sh"
  exit 1
fi
APP_DIR=/opt/andalusia
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
STAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$APP_DIR/backups"
tar -C "$APP_DIR" -czf "$APP_DIR/backups/data_$STAMP.tar.gz" data
systemctl stop andalusia
cp "$PROJECT_DIR/server.py" "$APP_DIR/server.py"
cp "$PROJECT_DIR/requirements.txt" "$APP_DIR/requirements.txt"
rm -rf "$APP_DIR/static"
cp -a "$PROJECT_DIR/static" "$APP_DIR/static"
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"
chown -R andalusia:andalusia "$APP_DIR"
systemctl start andalusia
sleep 2
curl -fsS http://127.0.0.1:8765/ >/dev/null
echo "Updated successfully. Data preserved. Backup: $APP_DIR/backups/data_$STAMP.tar.gz"
