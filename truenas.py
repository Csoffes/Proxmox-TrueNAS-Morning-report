
#!/usr/bin/env python3
# truenas.py
# TrueNAS api functions - import by other scripts

import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv(os.path.expanduser('~/scripts/.truenas.env'))

TRUENAS_IP = os.getenv('TRUENAS_IP')
TRUENAS_KEY = os.getenv('TRUENAS_KEY')

def api_call(endpoint):
    url = f"http://{TRUENAS_IP}/api/v2.0/{endpoint}"
    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {TRUENAS_KEY}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    return response.json()

def get_status():
    pool = api_call("pool")[0]
    smart = api_call("smart/test/results")

    drives = []
    for drive in smart:
        drives.append({
            "name": drive["name"],
            "model": drive["model"],
            "type": drive["type"],
            "status": drive["tests"][0]["status"],
            "verbose": drive["tests"][0]["status_verbose"]
        })

    return {
        "pool_name": pool["name"],
        "pool_status": pool["status"],
        "healthy": pool["healthy"],
        "scrub_state": pool["scan"]["state"],
        "scrub_errors": pool["scan"]["errors"],
        "drives": drives
    }