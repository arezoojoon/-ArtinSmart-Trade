import os
import shutil

BASE_DIR = r"I:\AI WhatsApp Sales & Lead Intelligence Platform for FMCG\src\app"
SRC = os.path.join(BASE_DIR, "admin")
DEST_PARENT = os.path.join(BASE_DIR, "(dashboard)")
DEST = os.path.join(DEST_PARENT, "admin")

def integrate_admin():
    # 1. Move Admin Dir
    if os.path.exists(SRC):
        if not os.path.exists(DEST_PARENT):
            os.makedirs(DEST_PARENT)
        
        # If dest exists, merge
        if os.path.exists(DEST):
            print(f"Merging {SRC} -> {DEST}")
            for item in os.listdir(SRC):
                s = os.path.join(SRC, item)
                d = os.path.join(DEST, item)
                if os.path.exists(d):
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                        shutil.rmtree(s)
                    else:
                        os.remove(d) # Overwrite
                        shutil.move(s, d)
                else:
                    shutil.move(s, d)
            os.rmdir(SRC)
        else:
            print(f"Moving {SRC} -> {DEST}")
            shutil.move(SRC, DEST)
    else:
        print(f"Source {SRC} not found (maybe already moved?)")

    # 2. Delete Admin Layout
    layout_file = os.path.join(DEST, "layout.tsx")
    if os.path.exists(layout_file):
        os.remove(layout_file)
        print(f"Deleted custom admin layout: {layout_file}")

    print("Admin Integration Complete (Local)")

if __name__ == "__main__":
    integrate_admin()
