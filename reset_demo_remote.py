import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def reset_remote():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False, timeout=10)
        print("Connected.")
        
        # Execute the reset script properly
        cmd = "python3 /root/fmcg-platform/force_reset_demo_user.py"
        print(f"Running: {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # Wait for completion
        exit_status = stdout.channel.recv_exit_status()
        
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("STDOUT:", out)
        print("STDERR:", err)
        
        if exit_status == 0:
            print("RESET SUCCESSFUL")
        else:
            print("RESET FAILED")
            
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    reset_remote()
