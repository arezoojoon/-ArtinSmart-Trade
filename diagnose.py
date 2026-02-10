#!/usr/bin/env python
"""Troubleshooting script to diagnose deployment issues"""

import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def diagnose():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)
    
    print("\n" + "="*70)
    print("🔍 DIAGNOSTIC REPORT")
    print("="*70)
    
    # 1. Check PM2 status
    print("\n1️⃣ PM2 Status:")
    stdin, stdout, stderr = ssh.exec_command("pm2 status")
    print(stdout.read().decode())
    
    # 2. Check PM2 logs (error output)
    print("\n2️⃣ PM2 Logs (Last 30 lines):")
    stdin, stdout, stderr = ssh.exec_command("pm2 logs fmcg-platform --lines 30 --nostream 2>&1")
    logs = stdout.read().decode()
    print(logs[-1500:] if len(logs) > 1500 else logs)
    
    # 3. Check if port 3000 is listening
    print("\n3️⃣ Port 3000 Status:")
    stdin, stdout, stderr = ssh.exec_command("netstat -tlnp 2>/dev/null | grep 3000")
    out = stdout.read().decode()
    print(out if out else "❌ Port 3000 is NOT listening")
    
    # 4. Check Node process
    print("\n4️⃣ Node Process Info:")
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep 'node\\|npm' | grep -v grep")
    print(stdout.read().decode())
    
    # 5. Check .env file
    print("\n5️⃣ Environment Variables (.env check):")
    stdin, stdout, stderr = ssh.exec_command("head -5 /root/fmcg-platform/.env 2>/dev/null || echo 'No .env found'")
    print(stdout.read().decode())
    
    # 6. Check file permissions
    print("\n6️⃣ File Permissions:")
    stdin, stdout, stderr = ssh.exec_command("ls -la /root/fmcg-platform/ | head -10")
    print(stdout.read().decode())
    
    # 7. Try to start the app manually
    print("\n7️⃣ Attempting manual start (10 second output):")
    stdin, stdout, stderr = ssh.exec_command("cd /root/fmcg-platform && timeout 10 npm start 2>&1 || true")
    out = stdout.read().decode()
    print(out[-1000:] if len(out) > 1000 else out)
    
    ssh.close()
    
    print("\n" + "="*70)
    print("📋 RECOMMENDATIONS:")
    print("="*70)
    print("""
1. Check if .env file exists and has required variables
2. Verify NODE_ENV is set to 'production'
3. Check if 'npm start' runs successfully
4. Look for specific error messages in logs
5. Ensure /root/.next directory exists
6. Verify NEXT_PUBLIC_API_URL is correct
7. Check NGINX configuration if using reverse proxy
    """)

if __name__ == "__main__":
    diagnose()
