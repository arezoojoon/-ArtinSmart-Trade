import paramiko

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def get_logs():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        # Read n lines
        stdin, stdout, stderr = client.exec_command("pm2 logs fmcg-platform --lines 100 --nostream")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_logs()
