import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

FILES = [
    (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\insights\page.tsx", "/root/fmcg-platform/src/app/insights/page.tsx"),
    (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\follow-up\page.tsx", "/root/fmcg-platform/src/app/follow-up/page.tsx"),
    (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\(dashboard)\marketplace\page.tsx", "/root/fmcg-platform/src/app/(dashboard)/marketplace/page.tsx"),
]

def deploy_ui_fixes():
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
        
        print("Rebuilding UI...")
        stdin, stdout, stderr = client.exec_command("cd /root/fmcg-platform && npm run build && pm2 restart fmcg-platform")
        
        # Stream Output
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
        
        print("\nDeployment Complete.")
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    deploy_ui_fixes()
