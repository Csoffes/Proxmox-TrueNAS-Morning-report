#!/usr/bin/env python3
# proxmox.py
# Proxmox API functions — imported by other scripts

import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv(os.path.expanduser('~/python-scripts/.proxmox.env'))

PROXMOX_IP = os.getenv('PROXMOX_IP')
PROXMOX_USER = os.getenv('PROXMOX_USER')
PROXMOX_PASSWORD = os.getenv('PROXMOX_PASSWORD')

def get_auth_token():
    url = f"https://{PROXMOX_IP}:8006/api2/json/access/ticket"
    response = requests.post(
        url,
        data={"username": PROXMOX_USER, "password": PROXMOX_PASSWORD},
        verify=False
    )
    response.raise_for_status()
    data = response.json()
    return data["data"]["ticket"], data["data"]["CSRFPreventionToken"]

def get_status():
    ticket, csrf_token = get_auth_token()
    nodes = api_call("nodes", ticket, csrf_token)
    node_name = nodes[0]["node"]

    node = nodes[0]
    result = {
        "node": node["node"],
        "status": node["status"],
        "cpu": round(node["cpu"] * 100, 1),
        "mem_used": round(node["mem"] / 1024**3, 1),
        "mem_total": round(node["maxmem"] / 1024**3, 1),
        "uptime": round(node["uptime"] / 86400, 1),
        "vms": [],
        "lxcs": []
    }

    vms = api_call(f"nodes/{node_name}/qemu", ticket, csrf_token)
    for vm in vms:
        result["vms"].append({
            "name": vm["name"],
            "status": vm["status"],
            "cpu": round(vm.get("cpu", 0) * 100, 1),
            "mem": round(vm.get("mem", 0) / 1024**3, 1),
        })

    lxcs = api_call(f"nodes/{node_name}/lxc", ticket, csrf_token)
    for lxc in lxcs:
        result["lxcs"].append({
            "name": lxc["name"],
            "status": lxc["status"],
            "cpu": round(lxc.get("cpu", 0) * 100, 1),
            "mem": round(lxc.get("mem", 0) / 1024**3, 1),
        })

    return result

def api_call(endpoint, ticket, csrf_token):
    url = f"https://{PROXMOX_IP}:8006/api2/json/{endpoint}"
    response = requests.get(
        url,
        cookies={"PVEAuthCookie": ticket},
        headers={"CSRFPreventionToken": csrf_token},
        verify=False
    )
    response.raise_for_status()
    return response.json()["data"]