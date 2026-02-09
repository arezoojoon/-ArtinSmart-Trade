import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def deploy_startup_script():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        # Create startup.sh
        script_content = """#!/bin/bash
cd /root/fmcg-platform
./node_modules/.bin/next start
"""
        print("Creating startup.sh...")
        cmd = f"echo '{script_content}' > /root/fmcg-platform/startup.sh && chmod +x /root/fmcg-platform/startup.sh"
        client.exec_command(cmd)
        
        # Update PM2 to use startup.sh
        print("Updating PM2...")
        client.exec_command("pm2 delete fmcg-platform")
        time.sleep(2)
        cmd = "pm2 start /root/fmcg-platform/startup.sh --name 'fmcg-platform'"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        
        print("Saving PM2...")
        client.exec_command("pm2 save")
        
        print("Waiting for boot (5s)...")
        time.sleep(5)
        
        print("Checking Bin existence...")
        stdin, stdout, stderr = client.exec_command("ls -l /root/fmcg-platform/node_modules/.bin/next")
        print(stdout.read().decode())
        print(stderr.read().decode())

        print("Checking Logs...")
        stdin, stdout, stderr = client.exec_command("pm2 logs fmcg-platform --lines 20 --nostream")
        print(stdout.read().decode())

        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    deploy_startup_script()
