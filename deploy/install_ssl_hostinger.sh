#!/usr/bin/env bash
set -euo pipefail
if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
  echo "Run as root: sudo bash deploy/install_ssl_hostinger.sh"
  exit 1
fi
apt update
apt install -y python3 python3-venv libaugeas0
rm -rf /opt/certbot
python3 -m venv /opt/certbot
/opt/certbot/bin/pip install --upgrade pip
/opt/certbot/bin/pip install certbot certbot-nginx
ln -sf /opt/certbot/bin/certbot /usr/bin/certbot
certbot --nginx
# Hostinger's recommended twice-daily renewal pattern.
grep -q '/opt/certbot/bin/python' /etc/crontab || echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" >> /etc/crontab
