#!/usr/bin/env python
"""Robust troubleshooting with better error handling"""

import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def safe_exec(ssh, cmd, timeout=20):
    """Execute command safely"""
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        return (out + err)[:1000]
    except Exception as e:
        return f"Error: {str(e)[:100]}"

def main():
    print("\n" + "="*70)
    print("🚨 TROUBLESHOOTING DEPLOYMENT ISSUE")
    print("="*70)
    
    try:
        print("⏳ Connecting to server...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)
        print("✅ Connected!")
        
        print("\n1️⃣ PM2 Status:")
        out = safe_exec(ssh, "pm2 status")
        print(out)
        
        print("\n2️⃣ Error Logs (last 30 lines):")
        out = safe_exec(ssh, "pm2 logs fmcg-platform --err --lines 30 --nostream 2>&1 | tail -20")
        print(out)
        
        print("\n3️⃣ Check if .next exists:")
        out = safe_exec(ssh, "ls -la /root/fmcg-platform/.next 2>&1 | head -5")
        print(out)
        
        print("\n4️⃣ Check package.json start script:")
        out = safe_exec(ssh, "grep -A 2 '\"start\"' /root/fmcg-platform/package.json")
        print(out)
        
        print("\n5️⃣ Try restarting with verbose output:")
        print("Stopping old process...")
        safe_exec(ssh, "pm2 stop fmcg-platform", timeout=10)
        time.sleep(2)
        
        print("Starting with npm start...")
        out = safe_exec(ssh, "cd /root/fmcg-platform && pm2 start npm --name fmcg-platform -- start", timeout=10)
        print(out)
        
        time.sleep(3)
        
        print("\n6️⃣ Check new status:")
        out = safe_exec(ssh, "pm2 status | grep fmcg")
        print(out)
        
        print("\n7️⃣ Check port 3000:")
        out = safe_exec(ssh, "curl -s http://localhost:3000 | head -c 100")
        print(out if out else "❌ No response on port 3000")
        
        ssh.close()
        
        print("\n" + "="*70)
        print("✅ Check complete. Review output above for errors.")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
