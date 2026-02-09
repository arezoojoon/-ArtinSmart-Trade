import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def read_pm2_logs():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # Read the last 100 lines of logs
        cmd = "pm2 logs --lines 100 --nostream"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        print(stdout.read().decode())
        print(stderr.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    read_pm2_logs()
