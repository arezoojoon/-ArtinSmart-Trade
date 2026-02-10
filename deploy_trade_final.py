import paramiko
import os
import time

# Server Details
HOSTNAME = "72.62.93.118"
USERNAME = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"
REMOTE_DIR = "/root/fmcg-platform" # User specified directory
DOMAIN = "trade.artinsmartagent.com"

def deploy():
    print(f"🚀 Starting Deployment to {DOMAIN} ({HOSTNAME})...")
    
    try:
        # 1. Setup SSH Connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f"🔑 Connecting to {USERNAME}@{HOSTNAME}...")
        ssh.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
        sftp = ssh.open_sftp()
        print("✅ Connected via SSH")

        # 2. Check for SSL Certs
        print("🔍 Checking SSL Certificates...")
        stdin, stdout, stderr = ssh.exec_command(f"[ -f /etc/letsencrypt/live/{DOMAIN}/fullchain.pem ] && echo 'exists' || echo 'missing'")
        cert_status = stdout.read().decode().strip()
        
        if cert_status == 'missing':
            print(f"⚠️ SSL Certs missing for {DOMAIN}. Attempting to generate with Certbot...")
            # Ensure Certbot is installed
            ssh.exec_command("apt-get update && apt-get install -y certbot python3-certbot-nginx")
            
            # Check is Nginx is running, if so, we must ensure it doesn't block port 80 if we use standalone, 
            # OR use --nginx plugin. Assuming nginx is installed and running.
            # We try --nginx plugin first.
            cmd = f"certbot --nginx -d {DOMAIN} --non-interactive --agree-tos -m admin@artinsmartagent.com --redirect"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                print(f"❌ Certbot failed: {stderr.read().decode()}")
                # Fallback: Stop nginx, run standalone, start nginx
                print("🔄 Trying standalone mode...")
                ssh.exec_command("service nginx stop")
                ssh.exec_command(f"certbot certonly --standalone -d {DOMAIN} --non-interactive --agree-tos -m admin@artinsmartagent.com")
                ssh.exec_command("service nginx start")
            else:
                print("✅ Certbot succeeded.")
        else:
            print("✅ SSL Certs found.")

        # 3. Upload Nginx Config
        # We upload the local nginx_trade.conf to /etc/nginx/sites-available/trade
        # and link to sites-enabled.
        local_nginx = "nginx_trade.conf"
        remote_nginx = f"/etc/nginx/sites-available/{DOMAIN}"
        
        if os.path.exists(local_nginx):
            print(f"nginx config found: {local_nginx}")
            sftp.put(local_nginx, remote_nginx)
            
            # Link it
            ssh.exec_command(f"ln -sf {remote_nginx} /etc/nginx/sites-enabled/{DOMAIN}")
            
            # Remove default if exists (optional but recommended to avoid conflicts)
            # ssh.exec_command("rm /etc/nginx/sites-enabled/default")
            
            # Test & Reload
            stdin, stdout, stderr = ssh.exec_command("nginx -t")
            if stdout.channel.recv_exit_status() == 0:
                ssh.exec_command("nginx -s reload")
                print("✅ Nginx reloaded with new config.")
            else:
                print(f"⚠️ Nginx config test failed: {stderr.read().decode()}")

        # 4. Upload Application Code
        # We assume the directory structure is maintained.
        
        # Directories to create (ensure they exist)
        dirs_to_create = [
            "src/app/(auth)/login",
            "src/app/(auth)/register",
            "src/app/(dashboard)/dashboard",
            "src/app/(dashboard)/leads/hunter",
            "src/app/(dashboard)/products",
            "src/app/(dashboard)/whatsapp/simulator",
            "src/app/api/whatsapp",
             "src/lib", "src/components/Layout"
        ]
        
        for dir_path in dirs_to_create:
            # Use forward slashes for remote linux path
            remote_path = f"{REMOTE_DIR}/{dir_path}" 
            ssh.exec_command(f"mkdir -p {remote_path}")

        # Files to upload (Critical files)
        files_to_upload = [
            ("src/lib/gemini.ts", "src/lib/gemini.ts"),
            ("src/lib/marketplace.ts", "src/lib/marketplace.ts"),
            ("src/middleware.ts", "src/middleware.ts"), 
            ("src/app/api/chat/route.ts", "src/app/api/chat/route.ts"),
            ("src/app/api/whatsapp/route.ts", "src/app/api/whatsapp/route.ts"),
            ("src/app/(dashboard)/dashboard/page.tsx", "src/app/(dashboard)/dashboard/page.tsx"),
            ("src/app/(dashboard)/leads/hunter/page.tsx", "src/app/(dashboard)/leads/hunter/page.tsx"), 
            ("src/app/(dashboard)/whatsapp/page.tsx", "src/app/(dashboard)/whatsapp/page.tsx"),
            ("src/app/(dashboard)/whatsapp/simulator/page.tsx", "src/app/(dashboard)/whatsapp/simulator/page.tsx"),
            ("src/app/(dashboard)/layout.tsx", "src/app/(dashboard)/layout.tsx"),
            ("src/app/layout.tsx", "src/app/layout.tsx"),
            ("src/app/page.tsx", "src/app/page.tsx"), 
            ("src/components/Layout/MobileNav.tsx", "src/components/Layout/MobileNav.tsx"),
            ("src/components/Layout/Sidebar.tsx", "src/components/Layout/Sidebar.tsx"),
            ("src/app/(auth)/layout.tsx", "src/app/(auth)/layout.tsx"),
            ("src/app/(auth)/login/page.tsx", "src/app/(auth)/login/page.tsx"),
            ("src/app/(auth)/register/page.tsx", "src/app/(auth)/register/page.tsx"),
            ("public/manifest.json", "public/manifest.json"),
            ("package.json", "package.json"),
            ("next.config.js", "next.config.js") # Upload config too
        ]

        for local, remote in files_to_upload:
            local_path = os.path.join(os.getcwd(), local.replace('/', os.sep))
            remote_path = f"{REMOTE_DIR}/{remote}" # Linux path
            
            if os.path.exists(local_path):
                print(f"📤 Uploading {local}...")
                sftp.put(local_path, remote_path)
            else:
                print(f"⚠️ Local file missing: {local}")

        print("✅ Files uploaded.")
        sftp.close()

        # 5. Build and Restart App
        print("🔄 Building and Restarting Application...")
        
        # Determine PM2 process name (defaulting to previous 'fmcg-platform' or new 'trade-platform')
        # We'll check if 'fmcg-platform' exists, if so use it, else start new.
        
        commands = [
            f"cd {REMOTE_DIR}",
            "npm install",
            "npm run build",
            # Restart or Start if not running
            "pm2 restart fmcg-platform || pm2 start npm --name 'fmcg-platform' -- start"
        ]
        
        full_command = " && ".join(commands)
        # Using bash explicitly
        stdin, stdout, stderr = ssh.exec_command(full_command)
        
        print("--- Build Output ---")
        while True:
            line = stdout.readline()
            if not line: break
            print(line.strip())
        print("--- End Output ---")

        # Check PM2 status
        stdin, stdout, stderr = ssh.exec_command("pm2 list")
        print(stdout.read().decode())

        ssh.close()
        print(f"✅ Deployment Complete! Visit https://{DOMAIN}")

    except Exception as e:
        print(f"❌ Deployment Failed: {e}")

if __name__ == "__main__":
    deploy()
