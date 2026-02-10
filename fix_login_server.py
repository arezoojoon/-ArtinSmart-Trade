#!/usr/bin/env python3
"""
Fix login page debug issue on production server.
Root cause: stale .next build cache.
Solution: clean rebuild with npm run build.
"""

import paramiko
import time
import sys

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v"
PORT = 22

def ssh_command(ssh_client, command, timeout=30):
    """Execute SSH command and return output."""
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command, timeout=timeout)
        output = stdout.read().decode('utf-8', errors='ignore')
        error = stderr.read().decode('utf-8', errors='ignore')
        exit_code = stdout.channel.recv_exit_status()
        return output, error, exit_code
    except Exception as e:
        return "", str(e), 1

try:
    print("Connecting to server...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=10, auth_timeout=10, look_for_keys=False, allow_agent=False)
    
    print("✓ Connected\n")
    
    print("1️⃣ Checking current processes...")
    out, err, code = ssh_command(ssh, "ps aux | grep -E 'node|npm' | grep -v grep")
    print(out[:200] if out else "No node/npm processes found")
    
    print("\n2️⃣ Killing processes...")
    ssh_command(ssh, "killall -9 node npm next-server 2>/dev/null; sleep 2")
    
    print("3️⃣ Removing .next build cache...")
    ssh_command(ssh, "rm -rf /root/fmcg-platform/.next /root/fmcg-platform/.cache /root/fmcg-platform/out")
    
    print("4️⃣ Building Next.js (this may take 2-3 minutes)...")
    out, err, code = ssh_command(ssh, "cd /root/fmcg-platform && npm run build 2>&1 | tail -20", timeout=300)
    if "error" in out.lower() or code != 0:
        print(f"⚠️  Build had issues:\n{out}")
    else:
        print("✓ Build completed successfully")
    
    print("\n5️⃣ Starting Next.js server...")
    ssh_command(ssh, "cd /root/fmcg-platform && nohup npm start > server.log 2>&1 &")
    
    print("6️⃣ Waiting for server to start...")
    time.sleep(8)
    
    print("7️⃣ Testing login page...")
    out, err, code = ssh_command(ssh, "curl -s http://localhost:3000/login 2>&1 | grep -o 'type=\"email\"\\|Login Debug' | head -1")
    
    if "email" in out:
        print("✅ SUCCESS! Login page now shows proper form with email input!")
    elif "Login Debug" in out:
        print("❌ Still showing debug page - may need more time")
    else:
        print(f"Response check: {out[:100] if out else 'No match found'}")
    
    print("\n8️⃣ Server status:")
    out, err, code = ssh_command(ssh, "ps aux | grep 'npm start' | grep -v grep")
    print(out if out else "Server process not found")
    
    print("\n9️⃣ Recent server logs:")
    out, err, code = ssh_command(ssh, "tail -15 /root/fmcg-platform/server.log 2>/dev/null")
    print(out if out else "No logs available yet")
    
    ssh.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
