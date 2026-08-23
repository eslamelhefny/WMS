#!/usr/bin/env bash
set -euo pipefail

if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
  echo "Run as root: sudo bash deploy/install_hostinger.sh your-domain.com"
  exit 1
fi

DOMAIN=${1:-}
if [[ -z "$DOMAIN" ]]; then
  echo "Usage: sudo bash deploy/install_hostinger.sh academy.example.com"
  exit 1
fi

APP_DIR=/opt/andalusia
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)

export DEBIAN_FRONTEND=noninteractive
apt update
apt install -y python3 python3-venv python3-pip nginx apache2-utils curl

if ! id andalusia >/dev/null 2>&1; then
  useradd --system --home "$APP_DIR" --shell /usr/sbin/nologin andalusia
fi

mkdir -p "$APP_DIR" "$APP_DIR/backups"
# First install: copy runtime files. If data already exists, preserve it.
cp "$PROJECT_DIR/server.py" "$APP_DIR/server.py"
cp "$PROJECT_DIR/requirements.txt" "$APP_DIR/requirements.txt"
rm -rf "$APP_DIR/static" "$APP_DIR/deploy"
cp -a "$PROJECT_DIR/static" "$APP_DIR/static"
cp -a "$PROJECT_DIR/deploy" "$APP_DIR/deploy"
if [[ ! -f "$APP_DIR/data/store.json" ]]; then
  cp -a "$PROJECT_DIR/data" "$APP_DIR/data"
else
  echo "Existing /opt/andalusia/data preserved."
fi

python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/pip" install --upgrade pip
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"

chown -R andalusia:andalusia "$APP_DIR"
chmod 750 "$APP_DIR" "$APP_DIR/data" "$APP_DIR/backups"
find "$APP_DIR/data" -type f -exec chmod 640 {} \;

cp "$PROJECT_DIR/deploy/andalusia.service.template" /etc/systemd/system/andalusia.service
systemctl daemon-reload
systemctl enable --now andalusia.service

sed "s/__DOMAIN__/$DOMAIN/g" "$PROJECT_DIR/deploy/nginx-private.conf.template" > /etc/nginx/sites-available/andalusia
ln -sf /etc/nginx/sites-available/andalusia /etc/nginx/sites-enabled/andalusia
rm -f /etc/nginx/sites-enabled/default

if [[ ! -f /etc/nginx/.andalusia_htpasswd ]]; then
  read -r -p "Basic Auth username [academyadmin]: " AUTH_USER
  AUTH_USER=${AUTH_USER:-academyadmin}
  echo "Create a strong password for $AUTH_USER:"
  htpasswd -c /etc/nginx/.andalusia_htpasswd "$AUTH_USER"
fi
chmod 640 /etc/nginx/.andalusia_htpasswd
chown root:www-data /etc/nginx/.andalusia_htpasswd

nginx -t
systemctl enable --now nginx
systemctl reload nginx

sleep 2
if curl -fsS http://127.0.0.1:8765/ >/dev/null; then
  echo "Backend health check: OK"
else
  echo "Backend health check FAILED. Run: journalctl -u andalusia -n 100 --no-pager"
  exit 1
fi

echo
echo "Installed successfully."
echo "Domain configured in NGINX: $DOMAIN"
echo "Next: point the domain A record to this VPS, then install SSL after DNS propagation."
echo "Service status: systemctl status andalusia"
echo "Logs: journalctl -u andalusia -f"
