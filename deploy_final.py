#!/usr/bin/env python
"""Deploy and fix login page on server"""
import paramiko
import time

HOST = "72.62.93.118"
USER = "root"  
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)

print("\n" + "="*70)
print("🚀 DEPLOYING TO SERVER")
print("="*70)

def run(cmd, desc="", timeout=120):
    print(f"\n{desc}")
    stdin, stdout, _ = ssh.exec_command(cmd, timeout=timeout)
    result = stdout.read().decode('utf-8', errors='ignore')
    return result

# 1. Kill existing process
run("killall -9 node npm 2>/dev/null || echo 'No process to kill'", "1️⃣ Killing old processes...")
time.sleep(2)

# 2. Clean build
run("cd /root/fmcg-platform && rm -rf .next .turbo", "2️⃣ Cleaning cache...")

# 3. Rebuild
output = run("cd /root/fmcg-platform && npm run build 2>&1 | tail -20", "3️⃣ Building...", timeout=600)
print(output[-500:] if len(output) > 500 else output)

# 4. Start server
run("cd /root/fmcg-platform && npm start > /tmp/server.log 2>&1 &", "4️⃣ Starting server...")

# 5. Wait for startup
print("\n5️⃣ Waiting for server to start...", end="", flush=True)
for i in range(30):
    time.sleep(1)
    stdin, stdout, _ = ssh.exec_command("curl -s http://localhost:3000/login > /dev/null 2>&1 && echo 'UP' || echo 'DOWN'", timeout=5)
    status = stdout.read().decode().strip()
    if status == "UP":
        print(f" ✅ Ready! ({i+1}s)")
        break
    print(".", end="", flush=True)

# 6. Test login page
time.sleep(2)
print("\n6️⃣ Testing login page...")
stdin, stdout, _ = ssh.exec_command("curl -s http://localhost:3000/login | grep -o '<input[^>]*type=\"email\"' | head -1", timeout=10)
result = stdout.read().decode().strip()

if 'type="email"' in result:
    print("✅ Email input found! Page works correctly!")
else:
    print("❌ Debug page still showing. Checking...")
    stdin, stdout, _ = ssh.exec_command("curl -s http://localhost:3000/login | grep -o '<h1[^>]*>[^<]*' | head -1", timeout=10)
    h1 = stdout.read().decode().strip()
    print(f"Page content: {h1}")

ssh.close()

print("\n" + "="*70)
print("✅ DEPLOYMENT COMPLETE")
print("="*70)
print("\n🌐 Visit: https://trade.artinsmartagent.com/login")
print("\n" + "="*70 + "\n")
