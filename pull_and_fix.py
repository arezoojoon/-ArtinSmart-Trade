#!/usr/bin/env python
"""Pull latest code and deploy"""

import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD)

print("Pulling latest code...")
stdin, stdout, _ = ssh.exec_command("cd /root/fmcg-platform && git pull 2>&1")
out = stdout.read().decode()[:300]
print(out)

print("\nRestarting...")
stdin, stdout, _ = ssh.exec_command("pm2 restart fmcg-platform 2>&1")
print(stdout.read().decode()[:300])

time.sleep(5)

print("\nChecking...")
stdin, stdout, _ = ssh.exec_command("curl -s http://localhost:3000/login | grep -c '<input'")
count = stdout.read().decode().strip()
print(f"Input fields found: {count}")

ssh.close()
