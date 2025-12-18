import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from hashing.final import calculate_hash, load_hashes, save_hashes
from telegram.telegram_alert import send_telegram_alert
from config.config import MONITOR_PATH

class IntegrityMonitorHandler(FileSystemEventHandler):
    def __init__(self):
        self.hashes = load_hashes()
        self.scan_initial_files()

    def scan_initial_files(self):
        print("[INFO] Performing initial file scan...")
        for root, _, files in os.walk(MONITOR_PATH):
            for f in files:
                full_path = os.path.join(root, f)
                if not os.path.isfile(full_path):
                    continue
                file_hash = calculate_hash(full_path)
                if file_hash:
                    self.hashes[full_path] = file_hash
        save_hashes(self.hashes)

    def on_created(self, event):
        if event.is_directory:
            return
        path = event.src_path
        file_hash = calculate_hash(path)
        if file_hash:
            self.hashes[path] = file_hash
            save_hashes(self.hashes)
            send_telegram_alert(path, "Created")
            print(f"[CREATED] {path}")

    def on_modified(self, event):
        if event.is_directory:
            return
        path = event.src_path
        new_hash = calculate_hash(path)
        if not new_hash:
            return
        old_hash = self.hashes.get(path)
        if old_hash != new_hash:
            self.hashes[path] = new_hash
            save_hashes(self.hashes)
            send_telegram_alert(path, "Modified")
            print(f"[MODIFIED] {path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        path = event.src_path
        if path in self.hashes:
            del self.hashes[path]
            save_hashes(self.hashes)
        send_telegram_alert(path, "Deleted")
        print(f"[DELETED] {path}")

def start_monitoring():
    event_handler = IntegrityMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=MONITOR_PATH, recursive=True)
    observer.start()
    print(f"[INFO] Monitoring started on {MONITOR_PATH}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()
