import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def check_status():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("--- PM2 Status ---")
        stdin, stdout, stderr = ssh.exec_command("pm2 status")
        print(stdout.read().decode())
        
        print("--- Port 3000 Status ---")
        stdin, stdout, stderr = ssh.exec_command("netstat -nlp | grep :3000")
        print(stdout.read().decode())
        
        print("--- Check HTTP ---")
        stdin, stdout, stderr = ssh.exec_command("curl -I http://localhost:3000")
        print(stdout.read().decode())
        print(stderr.read().decode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    check_status()
