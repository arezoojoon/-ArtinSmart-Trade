import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def check_pm2():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        print("--- PM2 List ---")
        stdin, stdout, stderr = client.exec_command("pm2 list")
        print(stdout.read().decode())
        
        print("--- PM2 Logs (Last 50 lines) ---")
        stdin, stdout, stderr = client.exec_command("pm2 logs fmcg-platform --lines 50 --nostream")
        print(stdout.read().decode())
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    check_pm2()
