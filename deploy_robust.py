import os
import shutil
import paramiko
import time
# from scp import SCPClient (Removed unused dependency)

# Configuration
HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P" # User provided
REMOTE_DIR = "/root/fmcg-platform"
BUILD_DIR = "_deploy_build"

def ignore_patterns(path, names):
    return [n for n in names if n in ['node_modules', '.next', '.git', '.vscode', '__pycache__', 'dist', 'build']]

def prepare_build():
    """Creates a clean build directory and structures it for deployment."""
    if os.path.exists(BUILD_DIR):
        print(f"🧹 Cleaning previous build: {BUILD_DIR}")
        try:
            shutil.rmtree(BUILD_DIR)
        except Exception as e:
            print(f"⚠️ Could not delete {BUILD_DIR}, trying to continue... {e}")

    print(f"📂 Copying project to {BUILD_DIR}...")
    try:
        shutil.copytree(".", BUILD_DIR, ignore=ignore_patterns)
    except Exception as e:
        print(f"❌ Copy failed: {e}")
        return False

    # RESTRUCTURE FOR PRODUCTION (Fixing the path issues)
    print("🔧 Restructuring files for Production...")
    
    # Define moves: Source in Build -> Dest in Build
    moves = [
        ("src/app/leads", "src/app/(dashboard)/leads"),
        ("src/app/whatsapp", "src/app/(dashboard)/whatsapp"),
        ("src/app/products", "src/app/(dashboard)/products"),
        ("src/app/broadcast", "src/app/(dashboard)/broadcast"),
        ("src/app/campaigns", "src/app/(dashboard)/campaigns"),
        ("src/app/analytics", "src/app/(dashboard)/analytics"),
        ("src/app/settings", "src/app/(dashboard)/settings"),
        ("src/app/admin", "src/app/(dashboard)/admin"),
    ]

    for src, dest in moves:
        full_src = os.path.join(BUILD_DIR, src)
        full_dest = os.path.join(BUILD_DIR, dest)
        
        if os.path.exists(full_src):
            if not os.path.exists(os.path.dirname(full_dest)):
                os.makedirs(os.path.dirname(full_dest))
            
            try:
                shutil.move(full_src, full_dest)
                print(f"✅ Moved {src} -> {dest}")
            except Exception as e:
                print(f"⚠️ Failed to move {src}: {e}")
        else:
            print(f"ℹ️ Source not found (might already be moved or missing): {src}")

    return True

def upload_and_deploy():
    """Uploads the structured build folder and triggers deployment."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"🚀 Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        # Upload using SFTP
        sftp = ssh.open_sftp()
        
        # Helper to upload directory recursively
        def upload_dir(local_path, remote_path):
            try:
                sftp.chdir(remote_path)
            except IOError:
                sftp.mkdir(remote_path)
                sftp.chdir(remote_path)
            
            for item in os.listdir(local_path):
                if item in ['node_modules', '.next', '.git']: continue
                
                l_item = os.path.join(local_path, item)
                r_item = f"{remote_path}/{item}"
                
                if os.path.isdir(l_item):
                    upload_dir(l_item, r_item)
                else:
                    print(f"📤 Uploading {item}...")
                    sftp.put(l_item, r_item)
                    
        print("📦 Uploading Build...")
        # Upload critical files first
        upload_dir(BUILD_DIR, REMOTE_DIR)
        
        print("✅ Upload Complete.")
        
        # Remote Commands
        commands = [
            f"cd {REMOTE_DIR} && npm install --legacy-peer-deps",
            f"cd {REMOTE_DIR} && npm install @supabase/auth-helpers-nextjs --legacy-peer-deps", # Ensure dependency exists
            f"cd {REMOTE_DIR} && npm run build",
            f"cd {REMOTE_DIR} && pm2 restart fmcg-platform || pm2 start npm --name 'fmcg-platform' -- start"
        ]
        
        for cmd in commands:
            print(f"🔄 Executing: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            
            # Stream output
            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    print(stdout.channel.recv(1024).decode('utf-8'), end='')
                if stderr.channel.recv_ready():
                    print(stderr.channel.recv(1024).decode('utf-8'), end='')
            
            if stdout.channel.recv_exit_status() != 0:
                print(f"❌ Command failed: {cmd}")
                # Don't exit, try to continue or check logs
        
        print("🎉 Deployment Pipeline Finished!")
        
    except Exception as e:
        print(f"❌ Deployment Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    if prepare_build():
        upload_and_deploy()
