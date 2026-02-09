import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

FILES = [
    (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\package.json", "/root/fmcg-platform/package.json"),
    (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\lib\gemini.ts", "/root/fmcg-platform/src/lib/gemini.ts"),
]

def deploy_and_update():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        sftp = client.open_sftp()
        for local, remote in FILES:
            print(f"Uploading {os.path.basename(local)}...")
            sftp.put(local, remote)
        sftp.close()
        
        print("Updating Dependencies (npm install)...")
        # Ensure we are in the right directory
        stdin, stdout, stderr = client.exec_command("cd /root/fmcg-platform && npm install")
        
        # Stream Output of Install
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
        
        print("\nRebuilding and Restarting...")
        stdin, stdout, stderr = client.exec_command("cd /root/fmcg-platform && npm run build && pm2 restart fmcg-platform")
        
         # Stream Output of Build
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
                 
        print("\nDeployment Complete.")
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    deploy_and_update()
