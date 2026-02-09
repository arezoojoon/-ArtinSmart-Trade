import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def check_status_short():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("--- PM2 Status ---")
        stdin, stdout, stderr = ssh.exec_command("pm2 status")
        print(stdout.read().decode())
        
        print("--- Last 20 Log Lines ---")
        stdin, stdout, stderr = ssh.exec_command("pm2 logs fmcg-platform --lines 20 --nostream")
        print(stdout.read().decode())
        
        print("--- HTTP Check ---")
        stdin, stdout, stderr = ssh.exec_command("curl -I http://localhost:3000")
        print(stdout.read().decode())
        print(stderr.read().decode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    check_status_short()
