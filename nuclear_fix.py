import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def nuclear_fix():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("1. Stopping & Deleting PM2...")
        ssh.exec_command("pm2 stop all")
        ssh.exec_command("pm2 delete all")
        time.sleep(2)
        
        print("2. Killing ALL Node processes...")
        ssh.exec_command("killall -9 node")
        ssh.exec_command("killall -9 next-server")
        time.sleep(2)
        
        print("3. Force killing port 3000...")
        ssh.exec_command("fuser -k 3000/tcp")
        time.sleep(2)
        
        print("4. Verifying Port 3000 is empty...")
        stdin, stdout, stderr = ssh.exec_command("lsof -t -i:3000")
        if stdout.read().strip():
            print("❌ Port 3000 STILL in use! Manual intervention required.")
            return
        else:
            print("✅ Port 3000 is CLEAN.")
            
        print("5. Starting Server FRESH...")
        cmd = "cd /root/fmcg-platform && pm2 start npm --name 'fmcg-platform' -- start"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        
        print("6. Saving PM2...")
        ssh.exec_command("pm2 save")
        
        print("7. Checking Logs for 10 seconds...")
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command("pm2 logs fmcg-platform --lines 20 --nostream")
        logs = stdout.read().decode()
        print(logs)
        
        if "EADDRINUSE" in logs:
            print("❌ FAILURE: EADDRINUSE Detected in new logs.")
        elif "Ready" in logs or "started" in logs:
            print("✅ SUCCESS: Server started correctly.")
        else:
            print("⚠️ WARNING: Check logs manually.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    nuclear_fix()
