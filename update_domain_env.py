import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

REMOTE_SCRIPT = """
import os

ENV_PATH = "/root/fmcg-platform/.env"
NEW_URL = "https://trade.artinsmartagent.com"

print(f"Reading {ENV_PATH}...")
with open(ENV_PATH, "r") as f:
    lines = f.readlines()

new_lines = []
found = False
for line in lines:
    if line.startswith("NEXT_PUBLIC_APP_URL="):
        new_lines.append(f"NEXT_PUBLIC_APP_URL={NEW_URL}\\n")
        found = True
    else:
        new_lines.append(line)

if not found:
    new_lines.append(f"NEXT_PUBLIC_APP_URL={NEW_URL}\\n")

print(f"Updating NEXT_PUBLIC_APP_URL to {NEW_URL}...")
with open(ENV_PATH, "w") as f:
    f.writelines(new_lines)

print("Environment Updated.")
"""

def update_domain():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        sftp = client.open_sftp()
        with sftp.file("/tmp/update_env_domain.py", "w") as f:
            f.write(REMOTE_SCRIPT)
        sftp.close()
        
        print("Executing Update Script...")
        stdin, stdout, stderr = client.exec_command("python3 /tmp/update_env_domain.py")
        print(stdout.read().decode())
        
        print("Rebuilding Application to Bake in ENV...")
        stdin, stdout, stderr = client.exec_command("cd /root/fmcg-platform && npm run build && pm2 restart fmcg-platform")
        
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
        
        print("\nDomain Switch Complete.")
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    update_domain()
