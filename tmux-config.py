
#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LAYOUT_FILE = SCRIPT_DIR / ".tmux_layout"
SESSION_NAME = "my_session"

if not LAYOUT_FILE.exists():
    print(f"Error: {LAYOUT_FILE} file not found in {SCRIPT_DIR}.")
    exit(1)

# Start new detached session
subprocess.run(["tmux", "new-session", "-d", "-s", SESSION_NAME])

with LAYOUT_FILE.open() as f:
    for line in f:
        idx, name, layout = line.strip().split(maxsplit=2)
        if idx == "0":
            subprocess.run(["tmux", "rename-window", "-t", f"{SESSION_NAME}:{idx}", name])
        else:
            subprocess.run(["tmux", "new-window", "-t", f"{SESSION_NAME}:{idx}", "-n", name])

        # Create the panes explicitly (you have 3 panes total, so we need to create 2 additional splits)
        subprocess.run(["tmux", "select-window", "-t", f"{SESSION_NAME}:{idx}"])
        subprocess.run(["tmux", "split-window", "-h", "-t", f"{SESSION_NAME}:{idx}"])
        subprocess.run(["tmux", "split-window", "-v", "-t", f"{SESSION_NAME}:{idx}.1"])

        # Now apply the saved layout
        subprocess.run(["tmux", "select-layout", "-t", f"{SESSION_NAME}:{idx}", layout])

# Finally, attach
subprocess.run(["tmux", "attach-session", "-t", SESSION_NAME])
