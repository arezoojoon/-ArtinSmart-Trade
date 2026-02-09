import paramiko
import os
import time

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

paramiko.util.log_to_file("paramiko_admin_integration.log")

def ensure_remote_dir(sftp, remote_directory):
    dirs = remote_directory.split('/')
    path = ""
    for dir in dirs:
        if not dir: continue
        path += "/" + dir
        try:
            sftp.stat(path)
        except IOError:
            print(f"Creating remote directory: {path}")
            sftp.mkdir(path)

def upload_recursive(sftp, local_dir, remote_dir):
    ensure_remote_dir(sftp, remote_dir)
    for item in os.listdir(local_dir):
        if item == ".DS_Store" or item == "__pycache__": continue
        local_path = os.path.join(local_dir, item)
        remote_path = remote_dir + "/" + item.replace("\\", "/")
        
        if os.path.isfile(local_path):
            print(f"Uploading {local_path} -> {remote_path}...")
            try:
                sftp.put(local_path, remote_path)
            except Exception as e:
                print(f"Failed to upload {item}: {e}")
        elif os.path.isdir(local_path):
            upload_recursive(sftp, local_path, remote_path)

def run_remote_command(ssh, command):
    print(f"Executing: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if exit_status != 0:
        print(f"Error: {error}")
    else:
        print(f"Output: {output}")
    return exit_status

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to {HOST}...")
    ssh.connect(HOST, username=USER, password=PASSWORD)
    sftp = ssh.open_sftp()

    # 1. Update Sidebar
    deploy_file_list = [
        ("src/components/Layout/Sidebar.tsx", "/root/fmcg-platform/src/components/Layout/Sidebar.tsx")
    ]
    for local, remote in deploy_file_list:
        ensure_remote_dir(sftp, os.path.dirname(remote))
        sftp.put(local, remote)
        print(f"Uploaded {local}")

    # 2. Upload Integrated Admin Folder
    local_admin = r"src/app/(dashboard)/admin" 
    remote_admin = "/root/fmcg-platform/src/app/(dashboard)/admin"
    
    print("Uploading Admin Directory...")
    if os.path.exists(local_admin):
        upload_recursive(sftp, local_admin, remote_admin)
    else:
        print(f"Error: Local path {local_admin} not found!")

    # 3. Cleanup Old Admin Folder (CRITICAL)
    print("Cleaning up old admin directory to prevent route conflicts...")
    run_remote_command(ssh, "rm -rf /root/fmcg-platform/src/app/admin")
    
    # 4. Remove Admin Layout (Sidebar component also if needed, but keeping it for now in case logic uses it, but layout file is gone)
    run_remote_command(ssh, "rm -f /root/fmcg-platform/src/app/(dashboard)/admin/layout.tsx")

    sftp.close()

    # Rebuild
    print("Triggering Rebuild...")
    run_remote_command(ssh, "cd /root/fmcg-platform && npm run build")
    
    print("Restarting PM2...")
    run_remote_command(ssh, "pm2 restart fmcg-platform")

    ssh.close()
    print("Admin Integration Deployed!")

except Exception as e:
    print(f"Connection Failed: {e}")
