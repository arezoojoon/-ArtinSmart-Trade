#!/usr/bin/env python
"""Check what's actually being served at /login"""

import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)

print("Checking /login response:\n")
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:3000/login | head -50")
out = stdout.read().decode('utf-8', errors='replace')
print(out)

print("\n\nChecking for debug files:")
stdin, stdout, stderr = ssh.exec_command("find /root/fmcg-platform -name '*debug*' -o -name '*hello*' 2>/dev/null")
print(stdout.read().decode())

print("\nChecking startup.sh:")
stdin, stdout, stderr = ssh.exec_command("cat /root/fmcg-platform/startup.sh 2>/dev/null || echo 'No startup.sh'")
print(stdout.read().decode())

ssh.close()
