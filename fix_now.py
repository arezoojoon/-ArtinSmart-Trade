#!/usr/bin/env python
import paramiko, time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD)

def run(cmd):
    stdin, stdout, _ = ssh.exec_command(cmd, timeout=30)
    return stdout.read().decode()[:500]

print("1. Clearing cache...")
print(run("cd /root/fmcg-platform && rm -rf .next .turbo"))

print("\n2. Building...")
print(run("cd /root/fmcg-platform && npm run build 2>&1 | tail -10"))

print("\n3. Starting...")
print(run("cd /root/fmcg-platform && pm2 start 'npm start' --name fmcg-platform 2>&1"))

time.sleep(5)

print("\n4. Check...")
print(run("curl -s http://localhost:3000/login | grep -o '<input' | wc -l"))

ssh.close()
