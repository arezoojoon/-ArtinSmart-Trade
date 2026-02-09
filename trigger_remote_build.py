import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def trigger_build():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD, timeout=10)
        
        print("🚀 Triggering Build & Restart...")
        # Combine commands to ensure sequence
        cmd = "cd /root/fmcg-platform && npm run build && pm2 restart fmcg-platform"
        print(f"Executing: {cmd}")
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Stream logs
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end='')
            time.sleep(1)
            
        exit_code = stdout.channel.recv_exit_status()
        if exit_code != 0:
            print(f"❌ Build Failed with Exit Code {exit_code}!")
            print(stderr.read().decode())
        else:
            print("\n✅ Build & Restart Success.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    trigger_build()
