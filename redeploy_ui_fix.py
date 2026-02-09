import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def redeploy_ui_fix():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # 1. Check Remote .env
        print("\n--- Checking Remote .env ---")
        try:
             stdin, stdout, stderr = ssh.exec_command("cat /root/fmcg-platform/.env.local || cat /root/fmcg-platform/.env")
             env_content = stdout.read().decode().strip()
             print(f"Remote Env Content (First 100 chars): {env_content[:100]}...")
             if "placeholder" in env_content:
                 print("⚠️ WARNING: Remote .env seems to have placeholders!")
             else:
                 print("✅ Remote .env looks populated (not placeholder).")
        except Exception as e:
            print(f"Error reading env: {e}")

        sftp = ssh.open_sftp()
        
        # 2. Upload UI Fixes
        files = [
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\page.tsx", "/root/fmcg-platform/src/app/page.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\(auth)\register\page.tsx", "/root/fmcg-platform/src/app/(auth)/register/page.tsx"),
        ]
        
        for local, remote in files:
            if os.path.exists(local):
                print(f"Uploading {os.path.basename(local)}...")
                sftp.put(local, remote)
            else:
                print(f"❌ Missing local file: {local}")
        
        sftp.close()
        
        # 3. Rebuild & Restart
        print("\n--- Rebuilding and Restarting ---")
        commands = [
            "cd /root/fmcg-platform && npm run build",
            "pm2 restart fmcg-platform --update-env",
            "curl -I http://localhost:3000"
        ]
        
        for cmd in commands:
            print(f"Executing: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # Stream output
            while not stdout.channel.exit_status_ready():
                 if stdout.channel.recv_ready():
                    print(stdout.channel.recv(1024).decode('utf-8', errors='replace'), end='')
            
            if stdout.channel.recv_exit_status() != 0:
                 print(f"❌ Command failed: {cmd}")
                 print(stderr.read().decode())

        print("\n✅ UI Fixes Deployed.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    redeploy_ui_fix()
