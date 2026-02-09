import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def find_next_bin():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        print("--- Listing .bin ---")
        cmd = "ls -l /root/fmcg-platform/node_modules/.bin/"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("--- Searching for next executable ---")
        cmd = "find /root/fmcg-platform/node_modules/next -name next"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    find_next_bin()
