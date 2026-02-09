import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def deploy_force_install():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        print("--- Installing Dependencies (Legacy Peer Deps) ---")
        cmd = "cd /root/fmcg-platform && npm install --legacy-peer-deps"
        stdin, stdout, stderr = client.exec_command(cmd)
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
        
        if stdout.channel.recv_exit_status() != 0:
            print("Install Failed!")
            print(stderr.read().decode())
            return

        print("\n--- Building App ---")
        cmd = "cd /root/fmcg-platform && npm run build"
        stdin, stdout, stderr = client.exec_command(cmd)
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
                 
        if stdout.channel.recv_exit_status() != 0:
            print("Build Failed!")
            print(stderr.read().decode())
            return
            
        print("\n--- Updating Startup Script ---")
        # Ensure startup.sh points to the now-existing binary
        script_content = """#!/bin/bash
cd /root/fmcg-platform
./node_modules/.bin/next start
"""
        cmd = f"echo '{script_content}' > /root/fmcg-platform/startup.sh && chmod +x /root/fmcg-platform/startup.sh"
        client.exec_command(cmd)

        print("--- Restarting PM2 ---")
        client.exec_command("pm2 restart fmcg-platform")
        time.sleep(5)
        
        print("--- Checking Logs ---")
        stdin, stdout, stderr = client.exec_command("pm2 logs fmcg-platform --lines 20 --nostream")
        print(stdout.read().decode())
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    deploy_force_install()
