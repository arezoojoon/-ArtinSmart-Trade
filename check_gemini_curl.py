import paramiko

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"
CMD = "curl -v 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro?key=AIzaSyCmxOmUH3gzrVScB78vXOTR-KKiMBdKo1c'"

def check_gemini():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        print("Connected.")
        
        stdin, stdout, stderr = client.exec_command(CMD)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_gemini()
