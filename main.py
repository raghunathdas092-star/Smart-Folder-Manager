import os
import shutil
import hashlib
from datetime import datetime
from config import SOURCE_FOLDER, FOLDERS

hashes = set()

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "activity_log.txt")

def file_hash(path):
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

with open(log_file, "a") as log:
    log.write(f"\n--- Run at {datetime.now()} ---\n")

    for file in os.listdir(SOURCE_FOLDER):
        file_path = os.path.join(SOURCE_FOLDER, file)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            file_md5 = file_hash(file_path)

            if file_md5 in hashes:
                log.write(f"Duplicate found: {file}\n")
                continue

            hashes.add(file_md5)

            if ext in FOLDERS:
                target = os.path.join(SOURCE_FOLDER, FOLDERS[ext])
                os.makedirs(target, exist_ok=True)

                shutil.move(file_path, os.path.join(target, file))
                log.write(f"Moved: {file} -> {FOLDERS[ext]}\n")

print("Files organized successfully.")
