import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def install_deps():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        # Use python3 -m pip to guarantee the same interpreter
        cmd = "python3 -m pip install fastapi uvicorn selenium webdriver-manager beautifulsoup4 requests"
        print(f"Executing: {cmd}")
        
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # Stream output
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                 print(stdout.channel.recv(1024).decode(), end="")
        
        err = stderr.read().decode()
        if err:
            print(f"\nSTDERR: {err}")
            
        print("\n✅ Dependencies Installed.")
        
        # Restart PM2
        print("Restarting PM2 Service...")
        client.exec_command("pm2 restart fmcg-backend")
        time.sleep(2)
        
        client.close()
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    install_deps()
