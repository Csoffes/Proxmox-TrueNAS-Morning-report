#!/usr/bin/env python3
# morning-report.py
# Unified homelab morning report — posts to Discord

import os
import socket
import requests
from datetime import datetime
from dotenv import load_dotenv
import proxmox
import truenas

load_dotenv(os.path.expanduser('~/python-scripts/.proxmox.env'))
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

def send_discord(message, color):
    requests.post(
        DISCORD_WEBHOOK,
        json={
            "embeds": [{
                "title": "🖥️ Homelab Morning Report",
                "description": message,
                "color": color,
                "footer": {
                    "text": f"{socket.gethostname()} — {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                }
            }]
        }
    )


# -------------FETCH DATA   ----------------------------

print("Fetching Proxmox status....")
px = proxmox.get_status()

print("Fetching TrueNAS Status")
tn = truenas.get_status()

#-----------------BUILD MESSAGE--------------------------------
running_vms  = len([v for v in px['vms']  if v['status'] == 'running'])
running_lxcs = len([l for l in px['lxcs'] if l['status'] == 'running'])

all_clear = tn['healthy'] and tn['scrub_errors'] == 0
drive_status = " | ".join([f"{d['name']}: {d['status']}" for d in tn['drives']])

status_icon = "✅" if all_clear else "⚠️"

message = f"""
**{status_icon} HOMELAB STATUS**

**Proxmox**
Node: {px['node']} | {px['status']}
CPU: {px['cpu']}% | RAM: {px['mem_used']}GB / {px['mem_total']}GB | Uptime: {px['uptime']}d
VMs Running: {running_vms} | LXCs Running: {running_lxcs}

**TrueNAS**
Pool: {tn['pool_name']} | {tn['pool_status']}
Healthy: {tn['healthy']} | Scrub: {tn['scrub_state']} | Errors: {tn['scrub_errors']}
Drives: {drive_status}
"""

color = 65280 if all_clear else 16711680

# ── OUTPUT ────────────────────────────────────────────
print(message)
send_discord(message, color)
print("Discord alert sent!")