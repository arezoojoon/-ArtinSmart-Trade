import os
import glob

OUTPUT_DIR = r"C:\Users\arezo\.gemini\antigravity\brain\235f53ed-497a-4503-8117-74606d5a14f4"
TARGET_NAME = "golden_demo_final.webm"

def rename_latest():
    files = glob.glob(os.path.join(OUTPUT_DIR, "*.webm"))
    if not files:
        print("No .webm files found.")
        return

    # Sort by modification time
    latest_file = max(files, key=os.path.getmtime)
    print(f"Latest file: {latest_file}")
    
    target_path = os.path.join(OUTPUT_DIR, TARGET_NAME)
    
    # Check if latest IS the target (idempotency)
    if os.path.basename(latest_file) == TARGET_NAME:
        print("Latest file is already named correctly.")
        return

    # Delete target if exists (to overwrite)
    if os.path.exists(target_path):
        os.remove(target_path)
    
    os.rename(latest_file, target_path)
    print(f"Renamed to {target_path}")

if __name__ == "__main__":
    rename_latest()
