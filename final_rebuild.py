#!/usr/bin/env python
import paramiko, time, subprocess

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD)

def run(cmd):
    stdin, stdout, _ = ssh.exec_command(cmd, timeout=600)
    try:
        return stdout.read(4096).decode('utf-8', errors='ignore')
    except:
        return ""

print("Cleaning and rebuilding...")
run("cd /root/fmcg-platform && rm -rf .next .turbo node_modules/.cache")
run("cd /root/fmcg-platform && npm run build")

print("Killing old process...")
run("pkill -f 'npm start' || true")
time.sleep(2)

print("Starting fresh...")
result = run("cd /root/fmcg-platform && nohup npm start > /tmp/app.log 2>&1 &")
print(result[:200] if result else "Background process started")

time.sleep(8)

print("Testing...")
result = run("curl -s http://localhost:3000/login | grep -E '<input|<button|<form' | head -3")
if result:
    print("✅ Login form found!")
    print(result)
else:
    print("Check logs:")
    result = run("tail -20 /tmp/app.log")
    print(result)

ssh.close()
