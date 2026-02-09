import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"
LOCAL_FILE = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\components\Layout\Sidebar.tsx"
REMOTE_FILE = "/root/fmcg-platform/src/components/Layout/Sidebar.tsx"

def deploy():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        sftp = client.open_sftp()
        sftp.put(LOCAL_FILE, REMOTE_FILE)
        print(f"Uploaded {LOCAL_FILE} to {REMOTE_FILE}")
        sftp.close()
        
        # Trigger Rebuild (Hot Reload might work if dev server, but this is prod)
        # Production build requires rebuild.
        print("Triggering Install & Rebuild...")
        # Installing psycopg2-binary for the promotion script + building frontend
        stdin, stdout, stderr = client.exec_command("pip install psycopg2-binary && cd /root/fmcg-platform && npm run build && pm2 restart fmcg-platform")
        
        # Stream output to avoid hanging if buffer fills, but wait for exit
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")
        
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    deploy()
