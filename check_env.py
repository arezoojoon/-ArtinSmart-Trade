import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def check_env():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(HOST, username=USER, password=PASSWORD)
        stdin, stdout, stderr = ssh.exec_command("grep 'NEXT_PUBLIC_SUPABASE_ANON_KEY' /root/fmcg-platform/.env /root/fmcg-platform/.env.local 2>/dev/null")
        output = stdout.read().decode().strip()
        print(f"Env Check Result:\n{output}")
        if "placeholder" in output or not output:
             print("❌ INVALID KEY FOUND (or missing)")
        else:
             print("✅ Valid Key Pattern Found")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    check_env()
