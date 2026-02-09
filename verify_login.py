import paramiko
import time

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

def verify_login():
    print(f"Connecting to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        # Check standard port 3000
        cmd = "curl -I http://localhost:3000/login"
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        print("--- OUTPUT ---")
        print(output)
        if error:
            print("--- ERROR STREAM (May contain progress details) ---")
            print(error)
            
        client.close()
        
    except Exception as e:
        print(f"SSH Error: {e}")

if __name__ == "__main__":
    verify_login()
