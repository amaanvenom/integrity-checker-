import os
import json
import hashlib
from config.config import HASH_DB_FILE

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"[ERROR] Hashing failed for {file_path}: {e}")
        return None

def load_hashes():
    if not os.path.exists(HASH_DB_FILE):
        return {}
    with open(HASH_DB_FILE, "r") as f:
        return json.load(f)

def save_hashes(hashes):
    with open(HASH_DB_FILE, "w") as f:
        json.dump(hashes, f, indent=4)
