import paramiko

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def check_logs():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        
        # Read PM2 Logs
        stdin, stdout, stderr = client.exec_command("pm2 logs fmcg-backend --lines 50 --nostream")
        
        # Decode safely
        logs = stdout.read().decode('utf-8', errors='ignore')
        err_logs = stderr.read().decode('utf-8', errors='ignore')
        
        print("\n--- STDOUT ---")
        print(logs)
        print("\n--- STDERR ---")
        print(err_logs)
        
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    check_logs()
