import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def check_env():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("Reading .env file...")
        stdin, stdout, stderr = ssh.exec_command("cat /root/fmcg-platform/.env")
        env_content = stdout.read().decode()
        
        print("--- ENV CONTENT START ---")
        print(env_content)
        print("--- ENV CONTENT END ---")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    check_env()
