import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def fetch_logs():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        # Fetch last 200 lines of logs
        cmd = "pm2 logs fmcg-platform --lines 200 --nostream"
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        print("--- LOGS START ---")
        print(output)
        if error:
            print("--- STDERR ---")
            print(error)
        print("--- LOGS END ---")
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    fetch_logs()
