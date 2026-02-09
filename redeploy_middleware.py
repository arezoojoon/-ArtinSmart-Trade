import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def redeploy():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # Upload Middleware
        sftp = ssh.open_sftp()
        local_path = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\middleware.ts"
        remote_path = "/root/fmcg-platform/src/middleware.ts"
        print(f"Uploading {local_path} -> {remote_path}")
        sftp.put(local_path, remote_path)
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
                 
        print("\n✅ Middleware Redeployed")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    redeploy()
