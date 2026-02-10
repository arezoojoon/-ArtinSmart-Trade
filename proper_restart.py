#!/usr/bin/env python
import paramiko, subprocess, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("72.62.93.118", username="root", password="9xLe/wDR#fh-6,&?6v)P")

print("Step 1: Kill everything on port 3000")
stdin, stdout, _ = ssh.exec_command("fuser -k 3000/tcp 2>/dev/null ; sleep 2", timeout=10)
stdout.read()

print("Step 2: Start server")
stdin, stdout, _ = ssh.exec_command("cd /root/fmcg-platform && npm start &", timeout=10)
stdout.read()

print("Step 3: Wait for server...")
for i in range(20):
    time.sleep(1)
    stdin, stdout, _ = ssh.exec_command("netstat -tlnp 2>/dev/null | grep 3000 | grep LISTEN", timeout=5)
    if stdout.read():
        print(f"✅ Server ready after {i+1} seconds")
        break
    print(f"  Waiting... {i+1}s")

print("\nStep 4: Test login page")
time.sleep(2)
stdin, stdout, _ = ssh.exec_command("timeout 5 curl -s http://localhost:3000/login | grep -c '<input type=\"email\"'", timeout=15)
count = stdout.read().decode().strip()

if count and int(count) > 0:
    print(f"✅✅✅ SUCCESS! Found email input field")
else:
    print("❌ Still not working")
    stdin, stdout, _ = ssh.exec_command("curl -s http://localhost:3000/login | head -100", timeout=15)
    html = stdout.read().decode()
    if "Hello World" in html or "Debug" in html:
        print("Still debug page")
    else:
        print("First 100 chars:", html[:100])

ssh.close()
