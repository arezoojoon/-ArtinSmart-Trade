import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def deploy_ui_polish():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        sftp = ssh.open_sftp()
        
        # Files to upload
        files = [
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\page.tsx", "/root/fmcg-platform/src/app/page.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\public\favicon.png", "/root/fmcg-platform/public/favicon.png"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\public\favicon.png", "/root/fmcg-platform/public/favicon.ico"), # Copy to ico as well
        ]
        
        for local, remote in files:
            if os.path.exists(local):
                print(f"Uploading {os.path.basename(local)}...")
                sftp.put(local, remote)
            else:
                print(f"❌ Missing local file: {local}")
        
        sftp.close()
        
        # Build & Restart
        # Since we changed page.tsx (JS code), we must rebuild.
        # Favicon is static, but page.tsx requires build.
        print("Rebuilding and Restarting...")
        cmd = "cd /root/fmcg-platform && npm run build && pm2 restart fmcg-platform"
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Stream output
        while not stdout.channel.exit_status_ready():
             if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode('utf-8', errors='replace'), end='')
                
        if stdout.channel.recv_exit_status() != 0:
             print("❌ Build Failed")
             print(stderr.read().decode())
        
        print("\n✅ UI Polish Deployed.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_ui_polish()
