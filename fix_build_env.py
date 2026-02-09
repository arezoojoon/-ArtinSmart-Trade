import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def fix_build_env():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        print("--- Checking UI Components ---")
        # Check if directories/files exist
        cmd = "ls -R /root/fmcg-platform/src/components/ui"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("--- Checking TSConfig ---")
        cmd = "cat /root/fmcg-platform/tsconfig.json"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())

        print("--- Installing Missing Dependencies ---")
        # Installing pg, stripe, @stripe/stripe-js
        cmd = "cd /root/fmcg-platform && npm install pg @stripe/stripe-js stripe --legacy-peer-deps"
        stdin, stdout, stderr = client.exec_command(cmd)
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
        
        print("\nExit Code:", stdout.channel.recv_exit_status())
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    fix_build_env()
