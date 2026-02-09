import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

BASE_LOCAL = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG"
BASE_REMOTE = "/root/fmcg-platform"

FILES_TO_UPLOAD = [
    ("package.json", "package.json"),
]

def deploy_deps():
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
            local_path = os.path.normpath(local_path)
            
            print(f"Uploading {os.path.basename(local_path)}...")
            sftp.put(local_path, remote_path)
            
        sftp.close()
        
        # Install Dependencies, Build and Restart
        print("Triggering npm install, Build & Restart...")
        cmd = "cd /root/fmcg-platform && npm install && npm run build && pm2 restart fmcg-platform"
        
        # We need a long timeout for npm install
        stdin, stdout, stderr = client.exec_command(cmd, timeout=600)
        
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
            if stderr.channel.recv_ready():
                 print(stderr.channel.recv(1024).decode(), end="")
        
        print("\n✅ Dependency Fix Deployed.")
        client.close()
        
    except Exception as e:
        print(f"Deployment Error: {e}")

if __name__ == "__main__":
    deploy_deps()
