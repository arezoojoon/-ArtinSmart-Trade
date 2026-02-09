import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def force_install_next():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        print("Installing Next.js explicitly...")
        stdin, stdout, stderr = client.exec_command("cd /root/fmcg-platform && npm install next@14.2.3")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
        
        print("\nChecking bin...")
        stdin, stdout, stderr = client.exec_command("ls -l /root/fmcg-platform/node_modules/.bin/next")
        print(stdout.read().decode())
        
        print("Restarting PM2...")
        client.exec_command("pm2 restart fmcg-platform")
        time.sleep(5)
        
        print("Logs...")
        stdin, stdout, stderr = client.exec_command("pm2 logs fmcg-platform --lines 20 --nostream")
        print(stdout.read().decode())
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    force_install_next()
