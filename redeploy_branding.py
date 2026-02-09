import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def redeploy_branding():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # Upload Modified Files
        sftp = ssh.open_sftp()
        files = [
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\page.tsx", "/root/fmcg-platform/src/app/page.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\(auth)\login\page.tsx", "/root/fmcg-platform/src/app/(auth)/login/page.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\components\Layout\Sidebar.tsx", "/root/fmcg-platform/src/components/Layout/Sidebar.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\layout.tsx", "/root/fmcg-platform/src/app/layout.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\whatsapp\simulator\page.tsx", "/root/fmcg-platform/src/app/whatsapp/simulator/page.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\public\logo.png", "/root/fmcg-platform/public/logo.png")
        ]
        
        for local, remote in files:
            print(f"Uploading {os.path.basename(local)}...")
            sftp.put(local, remote)
            
        sftp.close()
        
        # Rebuild and Restart
        commands = [
            "cd /root/fmcg-platform && npm run build",
            "pm2 restart fmcg-platform --update-env",
            "curl -I http://localhost:3000"
        ]
        
        for cmd in commands:
            print(f"\n--- Executing: {cmd} ---")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            
            # Stream output
            while not stdout.channel.exit_status_ready():
                 if stdout.channel.recv_ready():
                    print(stdout.channel.recv(1024).decode('utf-8', errors='replace'), end='')
            
            if stdout.channel.recv_exit_status() != 0:
                 print(f"❌ Command failed: {cmd}")
                 print(stderr.read().decode())
                 
        print("\n✅ Rebranding Deployed")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    redeploy_branding()
