import paramiko
import os
import sys
import time

# Host Configuration
HOST = "72.62.93.118"
USER = "root"
PASS = "9xLe/wDR#fh-6,&?6v)P"

# Paths
LOCAL_BACKEND_DIR = os.path.join(os.getcwd(), 'backend')
REMOTE_BACKEND_DIR = "/root/fmcg-platform/backend"

def create_ssh_client(server, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=user, password=password)
    return client

def run_command(client, command):
    print(f"Running: {command}")
    stdin, stdout, stderr = client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print(stdout.read().decode())
    else:
        print("Error:", stderr.read().decode())
    return exit_status

def upload_dir(sftp, local_dir, remote_dir):
    # Ensure remote directory exists
    try:
        sftp.chdir(remote_dir)
    except IOError:
        print(f"Creating remote directory: {remote_dir}")
        sftp.mkdir(remote_dir)
        sftp.chdir(remote_dir)

    for item in os.listdir(local_dir):
        if item in ['__pycache__', '.venv', '.env', '.git', '.pytest_cache', 'tests', 'venv']:
            continue

        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"

        if os.path.isfile(local_path):
            print(f"Uploading file: {item}")
            sftp.put(local_path, remote_path)
            
        elif os.path.isdir(local_path):
            print(f"Uploading directory: {item}")
            upload_dir(sftp, local_path, remote_path)
            # Restore verify back to parent dir
            sftp.chdir(remote_dir)

def deploy():
    print(f"🚀 Starting Backend Deployment to {HOST}...")
    
    try:
        client = create_ssh_client(HOST, USER, PASS)
        sftp = client.open_sftp()
        
        print("--- Uploading Backend Files ---")
        upload_dir(sftp, LOCAL_BACKEND_DIR, REMOTE_BACKEND_DIR)
        
        print("--- Installing Dependencies ---")
        # Install python dependencies for backend
        run_command(client, f"cd {REMOTE_BACKEND_DIR} && pip install -r requirements.txt")
        
        print("--- Restarting Backend Service ---")
        # Restart PM2 service
        run_command(client, "pm2 restart fmcg-backend")
        
        print("--- Verifying Service Status ---")
        run_command(client, "pm2 show fmcg-backend")
        
        print("✅ Backend Deployment Complete!")
        client.close()
        
    except Exception as e:
        print(f"❌ Deployment Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    deploy()
