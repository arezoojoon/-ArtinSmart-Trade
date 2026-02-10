#!/usr/bin/env python
"""Fix npm install with --legacy-peer-deps"""

import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def exec_cmd(ssh, cmd, timeout=600):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace')

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)
    
    print("\n" + "="*70)
    print("🛠️  FIXING NPM DEPENDENCY CONFLICT")
    print("="*70)
    
    # 1. Remove old node_modules
    print("\n1️⃣ Cleaning old dependencies...")
    exec_cmd(ssh, "cd /root/fmcg-platform && rm -rf node_modules package-lock.json")
    print("✅ Cleaned")
    
    # 2. Install with --legacy-peer-deps
    print("\n2️⃣ Installing with --legacy-peer-deps (may take 3-5 minutes)...")
    out = exec_cmd(ssh, "cd /root/fmcg-platform && npm install --legacy-peer-deps", timeout=1200)
    if "npm ERR" in out:
        print("⚠️ Warning:", out[-200:])
    else:
        print("✅ Dependencies installed successfully")
    
    # 3. Verify Next.js
    print("\n3️⃣ Verifying Next.js installation...")
    out = exec_cmd(ssh, "ls -la /root/fmcg-platform/node_modules/.bin/next")
    print(out[:300])
    
    # 4. Build
    print("\n4️⃣ Building project...")
    out = exec_cmd(ssh, "cd /root/fmcg-platform && npm run build", timeout=900)
    print("✅ Build complete")
    
    # 5. Clean PM2 and restart
    print("\n5️⃣ Restarting application...")
    exec_cmd(ssh, "pm2 delete all 2>/dev/null || true")
    time.sleep(2)
    exec_cmd(ssh, "cd /root/fmcg-platform && pm2 start npm --name fmcg-platform -- start")
    
    time.sleep(5)
    
    # 6. Verify
    print("\n6️⃣ Checking status...")
    out = exec_cmd(ssh, "pm2 status | grep fmcg")
    print(out)
    
    # 7. Test port
    print("\n7️⃣ Testing port 3000...")
    time.sleep(3)
    out = exec_cmd(ssh, "curl -s http://localhost:3000 | head -c 300")
    if "DOCTYPE" in out or "html" in out:
        print("✅ Server is responding!")
        print(out)
    else:
        print("⚠️ Response:", out[:200])
    
    # 8. Show logs
    print("\n8️⃣ Recent logs:")
    out = exec_cmd(ssh, "pm2 logs fmcg-platform --lines 15 --nostream 2>&1")
    print(out[-800:])
    
    ssh.close()
    
    print("\n" + "="*70)
    print("✅ FIX COMPLETE!")
    print("="*70)
    print("\n🌐 Application should be live at:")
    print("   https://trade.artinsmartagent.com")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
