import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def check_logs():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # Get last 50 error lines
        cmd = "pm2 logs fmcg-platform --err --lines 50 --nostream"
        print(f"Running: {cmd}")
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode('utf-8', errors='replace')
        print(output)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    check_logs()
