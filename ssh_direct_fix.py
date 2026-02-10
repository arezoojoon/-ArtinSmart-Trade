#!/usr/bin/env python3
"""Direct SSH fix using subprocess and known_hosts."""

import subprocess
import os
import time

def run_cmd(cmd):
    """Run command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

# First, add server to known_hosts
print("Adding server to known_hosts...")
run_cmd('echo "72.62.93.118 ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDa... (host key)" >> %USERPROFILE%\\.ssh\\known_hosts 2>nul')

# Create expect-like script using plink
cmd_sequence = """
cd /root/fmcg-platform
killall -9 node npm next-server 2>/dev/null
sleep 2
rm -rf .next .cache out
npm run build 2>&1 | tail -30
nohup npm start > server.log 2>&1 &
sleep 8
curl -s http://localhost:3000/login | grep -o "email" | head -1
"""

print("Creating SSH session...")
for line in cmd_sequence.strip().split('\n'):
    print(f"Executing: {line}")
    out, code = run_cmd(f'plink -pw 9xLe/wDR#fh-6,&?6v root@72.62.93.118 "{line}"')
    if out:
        print(f"  > {out[:100]}")
    time.sleep(0.5)
