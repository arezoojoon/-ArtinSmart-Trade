#!/usr/bin/env python
"""Simple troubleshooting script"""

import subprocess
import sys

def run_ssh(cmd):
    """Run SSH command"""
    full_cmd = [
        'ssh',
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'ConnectTimeout=10',
        'root@72.62.93.118',
        cmd
    ]
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=15)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {e}"

print("\n" + "="*70)
print("🔍 TROUBLESHOOTING")
print("="*70)

print("\n1️⃣ PM2 Status:")
print(run_ssh("pm2 status"))

print("\n2️⃣ Recent Logs:")
print(run_ssh("pm2 logs fmcg-platform --lines 50 --nostream | tail -20"))

print("\n3️⃣ Port 3000:")
print(run_ssh("netstat -tlnp 2>/dev/null | grep 3000"))

print("\n4️⃣ Error Check:")
print(run_ssh("pm2 logs fmcg-platform --err --lines 20 --nostream"))

print("\n5️⃣ Process Check:")
print(run_ssh("ps aux | grep npm | grep -v grep"))

print("\n" + "="*70 + "\n")
