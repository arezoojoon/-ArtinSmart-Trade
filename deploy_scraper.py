import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

FILE_LOCAL = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\backend\scraper_engine.py"
FILE_REMOTE = "/root/fmcg-platform/backend/scraper_engine.py"

def upload():
    print(f"Uploading {os.path.basename(FILE_LOCAL)} to {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASS, look_for_keys=False, allow_agent=False)
        sftp = client.open_sftp()
        sftp.put(FILE_LOCAL, FILE_REMOTE)
        sftp.close()
        client.close()
        print("✅ Upload Complete.")
    except Exception as e:
        print(f"❌ Upload Failed: {e}")

if __name__ == "__main__":
    upload()
