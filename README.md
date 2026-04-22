Homelab Morning Report
Automated infrastructure monitoring for a self-hosted homelab. Queries the Proxmox and TrueNAS APIs, displays a live status dashboard, and posts a unified daily report to Discord every morning via cron.
What it does
Runs every morning at 8am and posts a single Discord message with the health status of your entire homelab including Proxmox node stats, all VMs and LXC containers, TrueNAS pool health, scrub status, and per-drive SMART data. Green alert if everything is healthy, red alert if anything needs attention.
Project Structure
├── proxmox.py            Proxmox API module
├── truenas.py            TrueNAS API module
├── morning-report.py     Unified report — imports both modules
├── proxmox-status.py     Standalone Proxmox dashboard
├── .proxmox.env          Proxmox credentials (not committed)
└── .truenas.env          TrueNAS credentials (not committed)
Requirements
python3
pip3 install python-dotenv requests
jq (for bash scripts)
Setup
Clone the repo and create your .env files:
bashgit clone https://github.com/yourusername/homelab-monitor
cd homelab-monitor
touch .proxmox.env .truenas.env
chmod 600 .proxmox.env .truenas.env
Add your credentials to .proxmox.env:
bashPROXMOX_IP="your-proxmox-ip"
PROXMOX_USER="root@pam"
PROXMOX_PASSWORD="your-password"
DISCORD_WEBHOOK="your-webhook-url"
Add your credentials to .truenas.env:
bashTRUENAS_IP="your-truenas-ip"
TRUENAS_KEY="your-api-key"
Running manually
bashpython3 morning-report.py
Scheduling with cron
bashcrontab -e
Add this line:
bash0 8 * * * python3 ~/python-scripts/morning-report.py >> ~/python-scripts/morning-report.log 2>&1
Discord Output
✅ HOMELAB STATUS

Proxmox
Node: proxmox | online
CPU: 2.2% | RAM: 40.9GB / 330.6GB | Uptime: 67d
VMs Running: 5 | LXCs Running: 1

TrueNAS
Pool: Dataset | ONLINE
Healthy: True | Scrub: FINISHED | Errors: 0
Drives: sda: SUCCESS | sdb: SUCCESS
Security Notes
Never commit your .env files. Both are listed in .gitignore by default. API keys and passwords should never appear in your code or commit history.
Built With
Python 3, Bash, Proxmox VE REST API, TrueNAS Scale REST API, Discord Webhooks