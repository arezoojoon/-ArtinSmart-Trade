import os
import shutil

BASE_DIR = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app"
DASHBOARD_GROUP = os.path.join(BASE_DIR, "(dashboard)")

# Source Paths
SRC_MARKETPLACE = os.path.join(BASE_DIR, "marketplace")
SRC_KPI_DASHBOARD = os.path.join(BASE_DIR, "dashboard", "marketplace")

# Dest Paths
DEST_MARKETPLACE = os.path.join(DASHBOARD_GROUP, "marketplace")
DEST_KPI_DASHBOARD = os.path.join(DEST_MARKETPLACE, "dashboard")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created: {path}")

def move_contents(src, dest):
    if not os.path.exists(src):
        print(f"Skipping {src} (Not found)")
        return
    
    ensure_dir(dest)
    
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.exists(d):
            print(f"Warning: {d} already exists. Overwriting/Merging...")
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
                shutil.rmtree(s)
            else:
                shutil.copy2(s, d)
                os.remove(s)
        else:
            shutil.move(s, d)
            print(f"Moved: {item} -> {dest}")

def cleanup_empty(path):
    if os.path.exists(path) and not os.listdir(path):
        os.rmdir(path)
        print(f"Removed empty dir: {path}")

# 1. Move Browse Page (marketplace -> (dashboard)/marketplace)
print("--- Moving Browse Page ---")
move_contents(SRC_MARKETPLACE, DEST_MARKETPLACE)

# 2. Move KPI Dashboard (dashboard/marketplace -> (dashboard)/marketplace/dashboard)
print("--- Moving KPI Dashboard ---")
move_contents(SRC_KPI_DASHBOARD, DEST_KPI_DASHBOARD)

# 3. Cleanup
cleanup_empty(SRC_MARKETPLACE)
cleanup_empty(SRC_KPI_DASHBOARD)
# Also cleanup parent 'dashboard' if empty
cleanup_empty(os.path.join(BASE_DIR, "dashboard"))

print("Reorganization Complete!")
