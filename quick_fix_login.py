#!/usr/bin/env python
"""Quick fix for login page"""

import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)

print("Rebuilding...")
stdin, stdout, stderr = ssh.exec_command("cd /root/fmcg-platform && rm -rf .next && npm run build 2>&1 | tail -20", timeout=900)
print(stdout.read().decode())

print("\nRestarting PM2...")
stdin, stdout, stderr = ssh.exec_command("pm2 delete all; sleep 2; cd /root/fmcg-platform && pm2 start npm --name fmcg-platform -- start", timeout=30)
print(stdout.read().decode())

import time
time.sleep(5)

print("\nChecking result...")
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:3000/login | grep -E '<input|<button' | head -3", timeout=10)
out = stdout.read().decode()
if out:
    print("✅ Login form elements found!")
    print(out)
else:
    print("Still showing debug...")
    stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:3000/login | grep -oP '<h[1-6][^>]*>\\K[^<]+'", timeout=10)
    print("Page content:", stdout.read().decode())

ssh.close()
