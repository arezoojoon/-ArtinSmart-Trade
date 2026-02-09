import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

BASE_LOCAL = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG"
BASE_REMOTE = "/root/fmcg-platform"

FILES_TO_UPLOAD = [
    ("src/app/(dashboard)/admin/users/page.tsx", "src/app/(dashboard)/admin/users/page.tsx"),
    ("src/app/(dashboard)/admin/tenants/page.tsx", "src/app/(dashboard)/admin/tenants/page.tsx"),
    ("src/app/(dashboard)/admin/health/page.tsx", "src/app/(dashboard)/admin/health/page.tsx"),
    ("src/app/(dashboard)/admin/settings/page.tsx", "src/app/(dashboard)/admin/settings/page.tsx"),
]

def deploy_final():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        sftp = client.open_sftp()
        
        for local_rel, remote_rel in FILES_TO_UPLOAD:
            local_path = os.path.join(BASE_LOCAL, local_rel)
            remote_path = f"{BASE_REMOTE}/{remote_rel}"
            
            # Ensure remote directory exists
            remote_dir = os.path.dirname(remote_path)
            # Check if dir exists via SFTP (stat)
            try:
                sftp.stat(remote_dir)
            except IOError:
                print(f"Creating remote directory: {remote_dir}")
                stdin, stdout, stderr = client.exec_command(f"mkdir -p '{remote_dir}'")
                exit_status = stdout.channel.recv_exit_status() # BLOCK until done
                if exit_status != 0:
                    print(f"Failed to create dir: {stderr.read().decode()}")
                    continue
            
            # Normalize local path for Windows
            local_path = os.path.normpath(local_path)
            
            print(f"Uploading {os.path.basename(local_path)}...")
            sftp.put(local_path, remote_path)
            
        sftp.close()
        
        # Build and Restart
        print("Triggering Build & Restart...")
        cmd = "cd /root/fmcg-platform && npm run build && pm2 restart fmcg-platform"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # Stream output
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
        
        print("\n✅ Final Deployment Complete.")
        client.close()
        
    except Exception as e:
        print(f"Deployment Error: {e}")

if __name__ == "__main__":
    deploy_final()
