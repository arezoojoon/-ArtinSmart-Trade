import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def deploy_fix():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        # Upload the server-side fix script
        sftp = client.open_sftp()
        local_script = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\server_fix_auth.py"
        remote_script = "/root/fmcg-platform/server_fix_auth.py"
        
        print("Uploading fix script...")
        sftp.put(local_script, remote_script)
        sftp.close()
        
        # Run the fix script
        print("Executing fix on server...")
        stdin, stdout, stderr = client.exec_command("python3 /root/fmcg-platform/server_fix_auth.py")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # Rebuild and Restart
        print("Triggering Rebuild (This fixes the Client Bundle)...")
        # We use 'npm run build' to regenerate static assets with the new hardcoded keys
        cmd = "cd /root/fmcg-platform && npm run build && pm2 restart fmcg-platform"
        
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # Stream build output
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
                 
        print("\n✅ Auth Fix Deployed & Service Restarted.")
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    deploy_fix()
