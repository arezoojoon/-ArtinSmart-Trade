import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def probe_routes():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        routes = ["/", "/register", "/login"]
        for route in routes:
            cmd = f"curl -I http://localhost:3000{route}"
            print(f"--- Probing {route} ---")
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode())
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    probe_routes()
