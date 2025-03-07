#!/usr/bin/env python3
import subprocess
import sys

GOOGLE_DNS = "8.8.8.8 8.8.4.4"


def get_connections():
    result = subprocess.run(["nmcli", "connection", "show"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    connections = []

    # Skip the header line (e.g., 'NAME  UUID  TYPE  DEVICE')
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        # Parse from the right side to accommodate names with spaces
        parts = line.rsplit(None, 3)
        # We expect 4 fields: NAME, UUID, TYPE, DEVICE
        if len(parts) < 4:
            continue
        name, uuid, typ, dev = parts
        # Only pick WiFi or Ethernet with a valid device
        if typ in ["wifi", "ethernet"] and dev != "--":
            connections.append(name)
    return connections


def set_dns(connection, dns, auto_dns):
    subprocess.run(["nmcli", "connection", "modify", connection, "ipv4.dns", dns])
    subprocess.run(["nmcli", "connection", "modify", connection, "ipv4.ignore-auto-dns", auto_dns])
    subprocess.run(["nmcli", "connection", "down", connection])
    subprocess.run(["nmcli", "connection", "up", connection])


def toggle_dns():
    connections = get_connections()
    if not connections:
        print("No active WiFi or Ethernet connections found.")
        return

    # Check DNS on the first connection to decide which mode we are in
    current_dns = subprocess.run(
        ["nmcli", "connection", "show", connections[0]],
        capture_output=True,
        text=True,
    ).stdout

    if GOOGLE_DNS in current_dns:
        print("Switching to automatic DNS...")
        for conn in connections:
            set_dns(conn, "", "no")
    else:
        print("Switching to Google DNS...")
        for conn in connections:
            set_dns(conn, GOOGLE_DNS, "yes")


if __name__ == "__main__":
    if subprocess.run(["which", "nmcli"], capture_output=True).returncode != 0:
        print("This script requires nmcli (NetworkManager). Please install it first.")
        sys.exit(1)
    toggle_dns()

