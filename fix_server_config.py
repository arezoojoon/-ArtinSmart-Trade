import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def fix_server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        commands = [
            "pm2 delete fmcg",  # Kill old process
            "pm2 stop fmcg-platform",
            "cd /root/fmcg-platform && pm2 start npm --name 'fmcg-platform' -- start -- -p 3000",
            "pm2 save",
            "service nginx restart",
            "netstat -tulnp | grep :3000" # Verify it's listening
        ]
        
        for cmd in commands:
            print(f"\n--- Executing: {cmd} ---")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        print("✅ Server Process Fixed on Port 3000")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    fix_server()
