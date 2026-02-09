import paramiko

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def kill_node():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        print("Killing all node processes...")
        # Ignore errors if no process found
        ssh.exec_command("killall -9 node") 
        ssh.exec_command("killall -9 next-server")
        
        print("Restarting PM2...")
        # PM2 might have died if we killed its node process (PM2 runs on node)
        # So we might need to resurrect it or just start the app
        # But usually 'pm2 resurrect' or just starting the app works if PM2 is global
        # Let's try to start pm2 daemon if killed, then restart app
        
        # Check if pm2 is running
        stdin, stdout, stderr = ssh.exec_command("pm2 status")
        if stdout.channel.recv_exit_status() != 0:
             print("PM2 daemon killed. Restarting...")
             # This assumes pm2 is in path
        
        ssh.exec_command("pm2 restart fmcg-platform || pm2 start npm --name 'fmcg-platform' -- start")
        
        print("✅ Cleanup Complete.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    kill_node()
