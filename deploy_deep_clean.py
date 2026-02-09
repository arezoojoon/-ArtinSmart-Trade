import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def deploy_deep_clean():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        # Stop App
        print("Stopping App...")
        client.exec_command("pm2 stop fmcg-platform")
        
        # Delete artifacts
        print("Deleting .next and node_modules (This may take a moment)...")
        stdin, stdout, stderr = client.exec_command("cd /root/fmcg-platform && rm -rf .next node_modules package-lock.json")
        while not stdout.channel.exit_status_ready():
            time.sleep(1)
            
        print("Installing Dependencies...")
        stdin, stdout, stderr = client.exec_command("cd /root/fmcg-platform && npm install")
        
        # Stream output to avoid hanging
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
        
        print("\nBuilding App...")
        stdin, stdout, stderr = client.exec_command("cd /root/fmcg-platform && npm run build")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")

        print("\nRestarting App...")
        client.exec_command("pm2 restart fmcg-platform")
        
        print("\n✅ Deep Clean Completed.")
        client.close()
        
    except Exception as e:
        print(f"Deployment Error: {e}")

if __name__ == "__main__":
    deploy_deep_clean()
