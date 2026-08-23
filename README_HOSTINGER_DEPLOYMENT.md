# Hostinger VPS Deployment — Andalusia Academy Revision 20.1

## Important
This project is a Python application. Deploy the **full application on Hostinger VPS**, not ordinary Web/Cloud hosting.

The current prototype does **not** implement server-side user authentication. For Internet-facing testing, the supplied NGINX configuration enables HTTP Basic Authentication in front of the whole application. Do not remove it until proper server-side authentication/authorization is implemented.

## Recommended architecture
Internet → HTTPS/NGINX → Basic Auth → `127.0.0.1:8765` → Andalusia Python server → local `data/` (SQLite + JSON + XLSX)

The app server intentionally remains bound to `127.0.0.1`; NGINX is the only Internet-facing service.

## 1. Create the VPS
Use a Hostinger Linux VPS. Ubuntu 24.04 is a good choice for these scripts.

Allow inbound TCP ports 22, 80, and 443 in the VPS firewall.

## 2. Upload this folder to the VPS
Example from your computer:

```bash
scp -r Andalusia_Academy_Revision_20_1_Hostinger_VPS_Ready root@YOUR_VPS_IP:/root/
```

Or upload the ZIP, SSH to the VPS, then unzip it.

## 3. Install the application
SSH to the VPS and run:

```bash
cd /root/Andalusia_Academy_Revision_20_1_Hostinger_VPS_Ready
sudo bash deploy/install_hostinger.sh academy.example.com
```

Use the exact domain or subdomain that will host the app, for example `academy.yourdomain.com`.

The installer:
- installs Python, NGINX, and required tools
- copies the app to `/opt/andalusia`
- creates a Python virtual environment
- installs `openpyxl`
- creates a systemd service
- enables NGINX reverse proxying
- asks you to create a Basic Auth username/password
- preserves an existing `/opt/andalusia/data` directory on re-install

## 4. Point DNS to the VPS
Create an A record for your chosen host/domain pointing to the VPS IPv4 address. Wait for DNS propagation before SSL.

If using a subdomain such as `academy.example.com`, create an A record for `academy` pointing to the VPS IP.

## 5. Install SSL
After the domain resolves to the VPS:

```bash
cd /root/Andalusia_Academy_Revision_20_1_Hostinger_VPS_Ready
sudo bash deploy/install_ssl_hostinger.sh
```

Select the intended domain(s) when Certbot prompts you.

## 6. Verify

```bash
systemctl status andalusia --no-pager
systemctl status nginx --no-pager
curl -I http://127.0.0.1:8765/
journalctl -u andalusia -n 100 --no-pager
```

Then open `https://academy.example.com` and enter the NGINX Basic Auth credentials.

## 7. Backups
The application stores its persistent data under `/opt/andalusia/data`:
- SQLite database
- JSON snapshot
- Excel mirror

Create a manual backup:

```bash
sudo bash /opt/andalusia/deploy/backup_data.sh
```

If the deploy scripts were not copied into `/opt/andalusia`, run the included `deploy/backup_data.sh` from this package or copy it there.

For a daily 02:30 backup, edit root's crontab:

```bash
sudo crontab -e
```

Add:

```cron
30 2 * * * /root/Andalusia_Academy_Revision_20_1_Hostinger_VPS_Ready/deploy/backup_data.sh >/dev/null 2>&1
```

The script keeps 14 days of its own `andalusia_data_*.tar.gz` backups.

## 8. Update to a newer revision without deleting data
Upload/unzip the newer build, then run its update script:

```bash
cd /root/NEW_BUILD_FOLDER
sudo bash deploy/update_app.sh
```

The update script first backs up the existing data, then replaces the Python/static application code while preserving `/opt/andalusia/data`.

## Useful commands

```bash
sudo systemctl restart andalusia
sudo systemctl restart nginx
sudo journalctl -u andalusia -f
sudo nginx -t
```

## Production security note
NGINX Basic Auth is suitable as an additional access barrier for an internal pilot, but it is not a replacement for proper application authentication, user sessions, server-side RBAC, password policy, audit/security controls, and CSRF protection. Before broad production use, implement those controls in the backend.
