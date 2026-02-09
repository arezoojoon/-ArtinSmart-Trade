import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def hard_restart():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        commands = [
            "pm2 delete all",
            "fuser -k 3000/tcp", # Kill whatever is on port 3000
            "pkill -f next-server",
            "pm2 flush",
            "cd /root/fmcg-platform && pm2 start npm --name 'fmcg-platform' -- start -- -p 3000",
            "pm2 save",
            "sleep 5",
            "curl -I http://localhost:3000"
        ]
        
        for cmd in commands:
            print(f"\n--- Executing: {cmd} ---")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err: print(f"STDERR: {err}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    hard_restart()
