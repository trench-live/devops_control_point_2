import os
import sys
from datetime import datetime

# Configure from env variables
VERSION_FILE = os.getenv('VERSION_FILE', '../version_info/version')
VERSION_LOG_FILE = os.getenv('VERSION_LOG_FILE', '../version_info/version_log')

def read_version():
    try:
        with open(VERSION_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Creating new version file at {VERSION_FILE}")
        with open(VERSION_FILE, 'w') as f:
            f.write("0.1.0")
        return "0.1.0"

def write_version(version):
    with open(VERSION_FILE, 'w') as f:
        f.write(version)

def log_version(old_ver, new_ver, update_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {old_ver} -> {new_ver} ({update_type})\n"
    with open(VERSION_LOG_FILE, 'a') as f:
        f.write(log_entry)

def bump_version(current, update_type):
    major, minor, patch = map(int, current.split('.'))
    if update_type == "minor":
        minor += 1
        patch = 0
    elif update_type == "patch":
        patch += 1
    return f"{major}.{minor}.{patch}"

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["minor", "patch"]:
        print("Usage: python version_updater.py [minor|patch]")
        sys.exit(1)

    update_type = sys.argv[1]
    current_version = read_version()
    new_version = bump_version(current_version, update_type)

    write_version(new_version)
    log_version(current_version, new_version, update_type)

    print(f"Version updated: {current_version} → {new_version}")
    print(f"::set-output name=NEW_VERSION::{new_version}")