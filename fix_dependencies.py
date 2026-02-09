import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def fix_deps():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("Installing 'pg' and 'stripe'...")
        # Installing pg, @types/pg and ensuring stripe is there
        cmd = "cd /root/fmcg-platform && npm install pg @types/pg stripe --legacy-peer-deps"
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        while not stdout.channel.exit_status_ready():
             if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode('utf-8', errors='replace'), end='')
        
        if stdout.channel.recv_exit_status() != 0:
             print("❌ NPM Install Failed")
             print(stderr.read().decode())
        else:
             print("\n✅ Dependencies Installed.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    fix_deps()
