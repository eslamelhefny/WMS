#!/usr/bin/env bash
set -euo pipefail
APP_DIR=/opt/andalusia
BACKUP_DIR="$APP_DIR/backups"
mkdir -p "$BACKUP_DIR"
STAMP=$(date +%Y%m%d_%H%M%S)
tar -C "$APP_DIR" -czf "$BACKUP_DIR/andalusia_data_$STAMP.tar.gz" data
find "$BACKUP_DIR" -type f -name 'andalusia_data_*.tar.gz' -mtime +14 -delete
printf '%s\n' "$BACKUP_DIR/andalusia_data_$STAMP.tar.gz"
