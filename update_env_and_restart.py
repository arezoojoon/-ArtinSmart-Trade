import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def update_env_and_restart():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        sftp = ssh.open_sftp()
        
        # 1. Upload .env.local
        local_env = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\.env.local"
        remote_env = "/root/fmcg-platform/.env.local"
        
        if os.path.exists(local_env):
            print(f"Uploading .env.local to {remote_env}...")
            sftp.put(local_env, remote_env)
            
            # Also copy to .env just in case Next.js prioritizes one or the other behaving oddly in prod
            sftp.put(local_env, "/root/fmcg-platform/.env") 
        else:
            print(f"❌ Critical: Local .env.local not found at {local_env}")
            return
            
        sftp.close()
        
        # 2. Restart PM2 with update-env
        print("Restarting PM2 to apply env changes...")
        # We need to reload the env vars. --update-env is crucial.
        # Also rebuilding might be safer if env vars are baked in at build time (Next.js PUBLIC vars often are!)
        # YES: NEXT_PUBLIC_ variables are inlined at build time. WE MUST REBUILD.
        
        cmd = "cd /root/fmcg-platform && npm run build && pm2 restart fmcg-platform --update-env"
        print(f"Executing: {cmd} (This will take a minute)...")
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Stream output
        while not stdout.channel.exit_status_ready():
             if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode('utf-8', errors='replace'), end='')
        
        if stdout.channel.recv_exit_status() != 0:
             print("❌ Build/Restart Failed!")
             print(stderr.read().decode())
        else:
             print("\n✅ Environment updated and App Rebuilt/Restarted.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    update_env_and_restart()
