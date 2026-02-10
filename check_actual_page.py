#!/usr/bin/env python
import subprocess

# Use SSH key/paramiko with longer wait
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("Connecting...")
ssh.connect("72.62.93.118", username="root", password="9xLe/wDR#fh-6,&?6v)P", timeout=30)

print("Getting login page source...")
stdin, stdout, _ = ssh.exec_command("curl http://localhost:3000/login 2>/dev/null | grep -o '<h[1-6][^>]*>[^<]*</h' | head -5", timeout=10)

import time
time.sleep(2)

try:
    out = stdout.read(4096).decode()
    print("Page H tags:", out)
    
    if "Login Debug" in out or "Hello" in out:
        print("\n❌ Still showing debug page")
        print("\nChecking what build exists:")
        stdin2, stdout2, _ = ssh.exec_command("ls -la /root/fmcg-platform/.next/static/chunks/ 2>/dev/null | grep -i login | head -3", timeout=5)
        print(stdout2.read().decode())
    else:
        print("\n✅ Real page loaded!")
except Exception as e:
    print(f"Error: {e}")

ssh.close()
