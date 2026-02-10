#!/usr/bin/env python
"""Debug npm install issue and fix it"""

import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def exec_cmd(ssh, cmd, show=True, timeout=300):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    full = out + err
    if show:
        print(full[-1000:] if len(full) > 1000 else full)
    return full

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)
    
    print("\n" + "="*70)
    print("🔍 DEBUGGING NPM INSTALL")
    print("="*70)
    
    # 1. Check npm and node versions
    print("\n1️⃣ Node & NPM versions:")
    exec_cmd(ssh, "node -v && npm -v")
    
    # 2. Check project directory
    print("\n2️⃣ Project contents:")
    exec_cmd(ssh, "ls -la /root/fmcg-platform/ | head -15")
    
    # 3. Check package.json
    print("\n3️⃣ Package.json exists:")
    exec_cmd(ssh, "[ -f /root/fmcg-platform/package.json ] && echo 'EXISTS' || echo 'MISSING'")
    
    # 4. Try npm install with verbose output
    print("\n4️⃣ Running npm install (verbose):")
    exec_cmd(ssh, "cd /root/fmcg-platform && npm install --verbose 2>&1 | tail -50", timeout=1200)
    
    # 5. Check if next package exists
    print("\n5️⃣ Checking for next package:")
    exec_cmd(ssh, "ls -la /root/fmcg-platform/node_modules/next/ 2>&1 | head -10")
    
    # 6. List some installed packages
    print("\n6️⃣ Installed packages:")
    exec_cmd(ssh, "ls /root/fmcg-platform/node_modules/ 2>&1 | grep -E 'next|react' | head -10")
    
    ssh.close()

if __name__ == "__main__":
    main()
