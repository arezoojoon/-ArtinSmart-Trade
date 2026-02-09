import paramiko
import os

HOST = "72.62.93.118"
USER = "root"
PASSWORD = "9xLe/wDR#fh-6,&?6v)P"

def deploy_stripe():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, username=USER, password=PASSWORD)
        
        sftp = ssh.open_sftp()
        
        # Files to upload
        files = [
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\lib\stripe.ts", "/root/fmcg-platform/src/lib/stripe.ts"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\payment\page.tsx", "/root/fmcg-platform/src/app/payment/page.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\api\stripe\checkout\route.ts", "/root/fmcg-platform/src/app/api/stripe/checkout/route.ts"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\api\stripe\webhook\route.ts", "/root/fmcg-platform/src/app/api/stripe/webhook/route.ts"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\(auth)\register\page.tsx", "/root/fmcg-platform/src/app/(auth)/register/page.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\(auth)\login\page.tsx", "/root/fmcg-platform/src/app/(auth)/login/page.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app\(dashboard)\layout.tsx", "/root/fmcg-platform/src/app/(dashboard)/layout.tsx"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\lib\permissions.ts", "/root/fmcg-platform/src/lib/permissions.ts"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\lib\supabase\client.ts", "/root/fmcg-platform/src/lib/supabase/client.ts"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\middleware.ts", "/root/fmcg-platform/src/middleware.ts"),
            (r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\components\Layout\Sidebar.tsx", "/root/fmcg-platform/src/components/Layout/Sidebar.tsx"),
        ]
        
        # Create directories if they don't exist
        dirs = [
             "/root/fmcg-platform/src/app/payment",
             "/root/fmcg-platform/src/app/api/stripe",
             "/root/fmcg-platform/src/app/api/stripe/checkout",
             "/root/fmcg-platform/src/app/api/stripe/webhook",
             "/root/fmcg-platform/src/lib/supabase",
        ]
        
        for remote_dir in dirs:
            try:
                sftp.mkdir(remote_dir)
            except IOError:
                pass # Exists
        
        for local, remote in files:
            if os.path.exists(local):
                print(f"Uploading {os.path.basename(local)}...")
                sftp.put(local, remote)
            else:
                print(f"❌ Missing local file: {local}")
        
        sftp.close()
        
        # Rebuild & Restart
        print("Installing dependencies and Rebuilding...")
        cmd = "cd /root/fmcg-platform && npm install @supabase/ssr --legacy-peer-deps && npm run build && pm2 restart fmcg-platform"
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        # Stream output
        while not stdout.channel.exit_status_ready():
             if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode('utf-8', errors='replace'), end='')
                
        if stdout.channel.recv_exit_status() != 0:
             print("❌ Build Failed")
             print(stderr.read().decode())
        
        print("\n✅ Stripe Integration Deployed.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_stripe()
