import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def diagnose_inst():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        print("--- Disk Usage ---")
        client.exec_command("df -h", get_pty=True)[1].read() # Printing output below
        stdin, stdout, stderr = client.exec_command("df -h")
        print(stdout.read().decode())
        
        print("--- Node Modules Root ---")
        stdin, stdout, stderr = client.exec_command("ls -ld /root/fmcg-platform/node_modules")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("--- Next Package Dir ---")
        stdin, stdout, stderr = client.exec_command("ls -ld /root/fmcg-platform/node_modules/next")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("--- Trying explicit install with logging ---")
        # Try installing just next with verbose logging
        cmd = "cd /root/fmcg-platform && npm install next@14.2.3 --no-audit --foreground-scripts --verbose"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # Read stream
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 data = stdout.channel.recv(1024).decode()
                 # print(data, end="") # Too much output
        
        print("Exit Code:", stdout.channel.recv_exit_status())
        
        print("--- Check Bin Again ---")
        stdin, stdout, stderr = client.exec_command("ls -l /root/fmcg-platform/node_modules/.bin/next")
        print(stdout.read().decode())
        print(stderr.read().decode())

        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    diagnose_inst()
