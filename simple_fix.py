#!/usr/bin/env python
import subprocess
import time

# Direct SSH command to fix
cmds = [
    "ssh -o StrictHostKeyChecking=no root@72.62.93.118 'killall -9 node npm 2>/dev/null || true'",
    "ssh -o StrictHostKeyChecking=no root@72.62.93.118 'sleep 3'",
    "ssh -o StrictHostKeyChecking=no root@72.62.93.118 'cd /root/fmcg-platform && rm -rf .next && npm run build'",
    "ssh -o StrictHostKeyChecking=no root@72.62.93.118 'cd /root/fmcg-platform && npm start &'",
    "ssh -o StrictHostKeyChecking=no root@72.62.93.118 'sleep 15'",
    "ssh -o StrictHostKeyChecking=no root@72.62.93.118 'curl -s http://localhost:3000/login | grep -c \"<input\" && echo \"✅ Fixed\" || echo \"Still broken\"'",
]

for i, cmd in enumerate(cmds, 1):
    print(f"\n{i}. Running: {cmd[:60]}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
    if result.stdout:
        print(result.stdout.strip()[-200:])
    if result.returncode != 0 and "error" in result.stderr.lower():
        print(f"Error: {result.stderr[:200]}")
