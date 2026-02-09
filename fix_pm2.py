import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def fix_pm2():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        print("Deleting old PM2 process...")
        client.exec_command("pm2 delete fmcg-platform")
        time.sleep(2)
        
        print("Starting new PM2 process via NPM...")
        # Run from directory, executing 'npm start'
        cmd = "cd /root/fmcg-platform && pm2 start npm --name 'fmcg-platform' -- start"
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read().decode())
        
        print("Saving PM2 list...")
        client.exec_command("pm2 save")
        
        print("Waiting for boot (5s)...")
        time.sleep(5)
        
        print("Checking Logs...")
        stdin, stdout, stderr = client.exec_command("pm2 logs fmcg-platform --lines 20 --nostream")
        print(stdout.read().decode())
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    fix_pm2()
