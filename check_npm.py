import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def check_npm():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        print("--- Package.json Scripts ---")
        cmd = "cat /root/fmcg-platform/package.json"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        
        print("--- Node Modules Bin ---")
        cmd = "ls -l /root/fmcg-platform/node_modules/.bin/next"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())

        print("--- NPM Install Log (Tail) ---")
        # We didn't save a log file, but let's check node version
        cmd = "node -v && npm -v"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    check_npm()
