import paramiko
import os
import sys

HOSTNAME = '72.62.93.118'
USERNAME = 'root'
PASSWORD = '7P(Z+D0U?sqPE5ta4/Xx' # User provided password

REMOTE_PATH = '/var/www/fmcg'
LOCAL_PATH = os.getcwd()

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

def upload_files(sftp, local_dir, remote_dir):
    # Files/Dirs to upload
    to_upload = ['src', 'public', 'package.json', 'next.config.ts', 'tailwind.config.ts', 'tsconfig.json', '.env.local', 'postcss.config.mjs']
    
    for item in to_upload:
        local_item = os.path.join(local_dir, item)
        remote_item = f"{remote_dir}/{item}"
        
        if os.path.isfile(local_item):
            print(f"Uploading file: {item}")
            sftp.put(local_item, remote_item)
            if item == '.env.local':
                sftp.rename(remote_item, f"{remote_dir}/.env")
        
        elif os.path.isdir(local_item):
            print(f"Uploading directory: {item}")
            # Recursively upload directory
            for root, dirs, files in os.walk(local_item):
                for file in files:
                    local_path = os.path.join(root, file)
                    rel_path = os.path.relpath(local_path, local_dir)
                    remote_file_path = f"{remote_dir}/{rel_path}".replace('\\', '/')
                    
                    # Ensure remote dir exists
                    remote_file_dir = os.path.dirname(remote_file_path)
                    try:
                        sftp.stat(remote_file_dir)
                    except FileNotFoundError:
                        run_command(client, f"mkdir -p {remote_file_dir}")
                    
                    sftp.put(local_path, remote_file_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        PASSWORD = sys.argv[1]
    
    if not PASSWORD:
        print("Error: Password required.")
        sys.exit(1)

    print(f"Connecting to {HOSTNAME}...")
    client = create_ssh_client(HOSTNAME, USERNAME, PASSWORD)
    sftp = client.open_sftp()

    print("--- Preparing Remote Server ---")
    # Install Node.js 18+ if not exists
    run_command(client, "curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs")
    
    # Create directory
    run_command(client, f"mkdir -p {REMOTE_PATH}")
    
    # Clear old files (optional, but good for clean build)
    # run_command(client, f"rm -rf {REMOTE_PATH}/*") # Risky? Maybe just overwrite.

    print("--- Uploading Files ---")
    upload_files(sftp, LOCAL_PATH, REMOTE_PATH)

    print("--- Installing Dependencies on Server ---")
    run_command(client, f"cd {REMOTE_PATH} && npm install --legacy-peer-deps")

    print("--- Building Next.js App ---")
    run_command(client, f"cd {REMOTE_PATH} && npm run build")

    print("--- Staring Application with PM2 ---")
    # Check if pm2 installed
    run_command(client, "npm install -g pm2")
    run_command(client, f"cd {REMOTE_PATH} && pm2 delete fmcg || true")
    run_command(client, f"cd {REMOTE_PATH} && pm2 start npm --name 'fmcg' -- start -- -p 3000")
    run_command(client, "pm2 save")

    # Nginx Config Update (for Port 3000)
    nginx_config = """
server {
    listen 80;
    server_name fmcg.artinsmartagent.com;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl;
    server_name fmcg.artinsmartagent.com;
    ssl_certificate /etc/letsencrypt/live/fmcg.artinsmartagent.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/fmcg.artinsmartagent.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
"""
    # Write Nginx config
    with open('nginx_temp', 'w') as f:
        f.write(nginx_config)
    sftp.put('nginx_temp', '/etc/nginx/sites-available/fmcg.artinsmartagent.com')
    os.remove('nginx_temp')
    
    run_command(client, "ln -sf /etc/nginx/sites-available/fmcg.artinsmartagent.com /etc/nginx/sites-enabled/")
    run_command(client, "nginx -t && systemctl restart nginx")

    print("--- Deployment Complete! ---")
    client.close()
