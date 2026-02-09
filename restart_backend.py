import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

COMMANDS = [
    "cd /root/fmcg-platform/backend",
    "pip3 install fastapi uvicorn selenium webdriver-manager beautifulsoup4 requests --break-system-packages",
    "pm2 delete fmcg-backend || true",
    "pm2 start main.py --name fmcg-backend --interpreter python3 --time",
    "pm2 save",
    "pm2 status"
]

def restart_backend():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected. Executing restart sequence...")
        
        full_cmd = " && ".join(COMMANDS)
        stdin, stdout, stderr = client.exec_command(full_cmd)
        
        # Stream output to avoid timeouts
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
        
        print("\n✅ Backend Restart Sequence Complete.")
        client.close()
    except Exception as e:
        print(f"❌ SSH Error: {e}")

if __name__ == "__main__":
    restart_backend()
