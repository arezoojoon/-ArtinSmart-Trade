import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def install_ssr():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        cmd = "cd /root/fmcg-platform && npm install @supabase/ssr --legacy-peer-deps"
        print(f"Running: {cmd}")
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("✅ @supabase/ssr Installed")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    install_ssr()
