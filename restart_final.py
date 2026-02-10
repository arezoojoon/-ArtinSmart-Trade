#!/usr/bin/env python
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("72.62.93.118", username="root", password="9xLe/wDR#fh-6,&?6v)P")

def run(cmd):
    stdin, stdout, _ = ssh.exec_command(cmd)
    return stdout.read(2048).decode()

print("Killing processes...")
print(run("kill -9 97238 89719 2>/dev/null || true"))

time.sleep(2)

print("\nVerifying port is free...")
print(run("netstat -tlnp 2>/dev/null | grep 3000 || echo 'Port 3000 is FREE'"))

print("\nStarting application...")
print(run("cd /root/fmcg-platform && nohup npm start > /tmp/app.log 2>&1 &"))

time.sleep(10)

print("\nTesting...")
out = run("curl -s http://localhost:3000/login | grep -E '<form|<input' | wc -l")
count = out.strip()
if int(count) > 0:
    print(f"✅ SUCCESS! Found {count} form elements")
else:
    print("Still has issues. Last log:")
    print(run("tail -10 /tmp/app.log"))

ssh.close()
