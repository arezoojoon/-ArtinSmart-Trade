import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def debug_install():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        print("--- Running NPM Install (Capturing Stderr) ---")
        # Ensure directory exists (it should, but just in case)
        client.exec_command("mkdir -p /root/fmcg-platform")
        
        # Run install and redirect stderr to stdout to catch errors
        cmd = "cd /root/fmcg-platform && npm install next@14.2.3 2>&1"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # Read all output
        output = stdout.read().decode()
        print(output)
        
        print("Exit Code:", stdout.channel.recv_exit_status())
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    debug_install()
