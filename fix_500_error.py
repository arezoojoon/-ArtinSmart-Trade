import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def fix_500():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        commands = [
            "cd /root/fmcg-platform && rm -rf .next", # Clean cache
            "cd /root/fmcg-platform && npm run build", # Rebuild
            "pm2 restart fmcg-platform --update-env", # Restart with env update
            "curl -I http://localhost:3000" # Verify locally
        ]
        
        for cmd in commands:
            print(f"\n--- Executing: {cmd} ---")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            
            # Stream output
            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    print(stdout.channel.recv(1024).decode('utf-8', errors='replace'), end='')
            
            if stdout.channel.recv_exit_status() != 0:
                 print(f"❌ Command failed: {cmd}")
                 print(stderr.read().decode())
                 
        print("\n✅ Fix Sequence Complete")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    fix_500()
