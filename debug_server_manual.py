import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def debug_server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("Stopping PM2...")
        ssh.exec_command("pm2 stop fmcg-platform")
        
        print("Starting Server Manually (timeout 10s)...")
        # We run this and wait a bit to capture output
        cmd = "cd /root/fmcg-platform && npm start"
        
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
        
        # Read output line by line until timeout or finish
        try:
            for line in stdout:
                print(line.strip())
            for line in stderr:
                print("ERR: " + line.strip())
        except Exception:
            print("--- Timeout / End of Capture ---")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Restart PM2 to restore service (even if broken, better than stopped)
        print("Restarting PM2...")
        try:
            ssh.exec_command("pm2 restart fmcg-platform")
        except:
            pass
        ssh.close()

if __name__ == "__main__":
    debug_server()
