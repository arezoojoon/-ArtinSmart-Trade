#!/usr/bin/env python
"""Rebuild and clear Next.js cache to fix stale content"""

import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def exec_cmd(ssh, cmd, timeout=600):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)

print("\n" + "="*70)
print("🔧 CLEANING BUILD CACHE AND REBUILDING")
print("="*70)

# 1. Clear old build
print("\n1️⃣ Clearing .next directory...")
out = exec_cmd(ssh, "cd /root/fmcg-platform && rm -rf .next")
print("✅ Cleared")

# 2. Clear PM2
print("\n2️⃣ Stopping PM2...")
exec_cmd(ssh, "pm2 delete all 2>/dev/null || true")
time.sleep(2)

# 3. Fresh build
print("\n3️⃣ Building project (clean)...")
out = exec_cmd(ssh, "cd /root/fmcg-platform && npm run build", timeout=900)
if "error" in out.lower():
    print("⚠️ Build had issues:", out[-500:])
else:
    print("✅ Build complete")

# 4. Start
print("\n4️⃣ Starting application...")
out = exec_cmd(ssh, "cd /root/fmcg-platform && pm2 start npm --name fmcg-platform -- start")
print(out[:300])

time.sleep(5)

# 5. Test
print("\n5️⃣ Testing /login endpoint...")
out = exec_cmd(ssh, "curl -s http://localhost:3000/login | grep -o '<h1[^>]*>[^<]*</h1>' | head -5")
print("Response:", out)

# 6. Check for debug
print("\n6️⃣ Checking for debug text...")
out = exec_cmd(ssh, "curl -s http://localhost:3000/login | grep -i 'debug\\|hello world' && echo 'FOUND DEBUG!' || echo 'No debug found'")
print(out)

ssh.close()

print("\n" + "="*70)
print("✅ REBUILD COMPLETE")
print("="*70 + "\n")
