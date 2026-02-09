import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

# We will upload the hardened scraper_engine.py first
FILES = [
    (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\backend\scraper_engine.py", "/root/fmcg-platform/backend/scraper_engine.py"),
]

COMMANDS = [
    # 1. Kill any existing nohup python process to clean up
    "pkill -f 'python3 /root/fmcg-platform/backend/main.py' || true",
    
    # 2. Kill existing PM2 python process if any
    "pm2 delete fmcg-backend || true",

    # 3. Start with PM2 (Production Ready)
    # We use 'python3' as interpreter. 
    "cd /root/fmcg-platform/backend && pm2 start main.py --name fmcg-backend --interpreter python3",
    
    # 4. Save PM2 list so it restarts on reboot
    "pm2 save",
    
    # 5. Check status
    "pm2 status"
]

def fix_backend():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        # Upload File
        sftp = client.open_sftp()
        for local, remote in FILES:
            print(f"Uploading {os.path.basename(local)}...")
            sftp.put(local, remote)
        sftp.close()
        
        # Execute Commands
        for cmd in COMMANDS:
            print(f"Running: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            if out: print(out)
            if err: print(f"STDERR: {err}")
            time.sleep(1) # Breath
            
        client.close()
        print("\nBackend Service Fixed & Restarted via PM2.")
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    fix_backend()
