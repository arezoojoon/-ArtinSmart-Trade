import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def debug_build():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        cmd = "cd /root/fmcg-platform && npm run build"
        print(f"Running: {cmd}")
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Capture all output
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        
        print("--- STDOUT ---")
        print(out)
        print("--- STDERR ---")
        print(err)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    debug_build()
