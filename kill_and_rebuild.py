#!/usr/bin/env python
import paramiko, time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD)

def run(cmd):
    stdin, stdout, _ = ssh.exec_command(cmd)
    return stdout.read(2048).decode('utf-8', errors='ignore')

print("Killing all Node processes...")
print(run("killall -9 node npm 2>/dev/null || true"))

time.sleep(2)

print("Rebuilding...")
print(run("cd /root/fmcg-platform && rm -rf .next && npm run build 2>&1 | tail -5"))

print("\nStarting app...")
print(run("cd /root/fmcg-platform && nohup npm start > /tmp/app.log 2>&1 &"))

time.sleep(10)

print("\nTesting login page...")
result = run("curl -s http://localhost:3000/login | grep '<input' | head -1")
if '<input' in result:
    print("✅ SUCCESS! Login form loaded!")
else:
    print("❌ Still showing debug. Logs:")
    print(run("tail -15 /tmp/app.log"))

ssh.close()
