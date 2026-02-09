import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def diagnose():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        commands = [
            "ls -F /etc/nginx/sites-enabled/",
            "cat /etc/nginx/sites-enabled/*",
            "pm2 list",
            "netstat -tulnp | grep node",
            "ls -la /root/fmcg-platform/.next/server/pages" 
        ]
        
        for cmd in commands:
            print(f"\n--- Running: {cmd} ---")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err: print(f"STDERR: {err}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    diagnose()
