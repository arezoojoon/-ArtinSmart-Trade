import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def force_kill():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("Checking port 3000 immediately...")
        stdin, stdout, stderr = ssh.exec_command("lsof -t -i:3000")
        pids = stdout.read().decode().strip().split('\n')
        
        if pids and pids[0]:
            print(f"⚠️ FOUND ZOMBIE PROCESSES: {pids}")
            for pid in pids:
                if pid:
                    print(f"🔥🔥 KILLING PID {pid} 🔥🔥")
                    ssh.exec_command(f"kill -9 {pid}")
        else:
            print("Port 3000 seems free (unexpected based on analysis).")

        print("Stopping PM2 to be safe...")
        ssh.exec_command("pm2 stop fmcg-platform")
        
        import time
        time.sleep(2)
        
        print("Double checking port 3000...")
        stdin, stdout, stderr = ssh.exec_command("lsof -t -i:3000")
        if stdout.read().strip():
             print("❌ Port 3000 STILL in use! Using fuser...")
             ssh.exec_command("fuser -k 3000/tcp")
        else:
             print("✅ Port 3000 is clean.")

        print("Starting Fresh via PM2...")
        cmd = "cd /root/fmcg-platform && pm2 restart fmcg-platform || pm2 start npm --name 'fmcg-platform' -- start"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("✅ Force Kill Sequence Complete.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    force_kill()
