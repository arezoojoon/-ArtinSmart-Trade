#!/usr/bin/env python
"""
Deployment script for Artin Smart Trade to production server.
Handles git pull, npm install, build, and PM2 restart.
"""

import paramiko
import time
import sys

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"
PROJECT_DIR = "/root/fmcg-platform"
REPO_URL = "https://github.com/arezoojoon/-ArtinSmart-Trade.git"

def run_cmd(ssh, cmd, timeout=300, show_output=True):
    """Execute command and return output"""
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    
    if show_output:
        if out:
            print(f"✓ {out[:200]}...")
        if err and "warning" not in err.lower():
            print(f"⚠ {err[:200]}...")
    
    return out, err, stdout.channel.recv_exit_status()

def deploy():
    """Main deployment function"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"🚀 Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)
        print("✅ Connected!")
        
        # Step 1: Clone or pull repository
        print("\n📦 Step 1: Cloning/Updating repository...")
        out, err, code = run_cmd(ssh, f"if [ ! -d {PROJECT_DIR} ]; then git clone {REPO_URL} {PROJECT_DIR}; else cd {PROJECT_DIR} && git pull origin main; fi")
        
        # Step 2: Install dependencies
        print("\n📥 Step 2: Installing dependencies...")
        out, err, code = run_cmd(ssh, f"cd {PROJECT_DIR} && npm install", timeout=600)
        
        # Step 3: Build project
        print("\n🔨 Step 3: Building project...")
        out, err, code = run_cmd(ssh, f"cd {PROJECT_DIR} && npm run build", timeout=900)
        if code != 0:
            print(f"❌ Build failed!")
            print(err)
            return False
        
        # Step 4: Restart PM2
        print("\n🔄 Step 4: Restarting PM2 services...")
        out, err, code = run_cmd(ssh, "pm2 stop fmcg-platform 2>/dev/null || true")
        out, err, code = run_cmd(ssh, f"cd {PROJECT_DIR} && pm2 start npm --name fmcg-platform -- start")
        out, err, code = run_cmd(ssh, "pm2 save")
        
        # Step 5: Verify deployment
        print("\n✅ Step 5: Verifying deployment...")
        time.sleep(5)
        out, err, code = run_cmd(ssh, "pm2 status")
        print(out)
        
        # Step 6: Health check
        print("\n🏥 Step 6: Health check...")
        out, err, code = run_cmd(ssh, "curl -s http://localhost:3000/login | grep -q 'html' && echo 'Server is online' || echo 'Server not responding'")
        print(out)
        
        print("\n✅ Deployment complete!")
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False
    
    finally:
        ssh.close()

if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)
