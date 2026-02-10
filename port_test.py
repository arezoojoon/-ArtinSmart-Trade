#!/usr/bin/env python
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("72.62.93.118", username="root", password="9xLe/wDR#fh-6,&?6v)P")

def run(cmd):
    stdin, stdout, _ = ssh.exec_command(cmd)
    return stdout.read(2048).decode()

print("Full cleanup...")
print(run("killall -9 node npm next-server 2>/dev/null || true"))
time.sleep(3)

print("Clean everything...")
print(run("rm -rf /tmp/app.log /root/.npm/_logs/*"))

print("Starting on port 3001 first...")
print(run("cd /root/fmcg-platform && PORT=3001 npm start > /tmp/test.log 2>&1 &"))

time.sleep(8)

print("Test port 3001...")
out = run("curl -s http://localhost:3001/login | grep -c '<input'")
print(f"Input fields on port 3001: {out.strip()}")

if int(out.strip()) > 0:
    print("✅ App works! Now switching to port 3000...")
    run("killall -9 node npm 2>/dev/null || true")
    time.sleep(2)
    run("cd /root/fmcg-platform && npm start > /tmp/app.log 2>&1 &")
    time.sleep(8)
    out = run("curl -s http://localhost:3000/login | grep -c '<input'")
    print(f"Input fields on port 3000: {out.strip()}")
else:
    print("App has render issue. Check:")
    print(run("tail /tmp/test.log"))

ssh.close()
