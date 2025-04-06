import os
import sys
import re
from datetime import datetime
from config import VERSION_FILE, VERSION_LOG_FILE

def read_version():
    try:
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, "r") as f:
                return f.read().strip()
        else:
            return None
    except IOError as e:
        print(f"Error reading {VERSION_FILE}: {e}")
        return None

def write_version(version):
    try:
        with open(VERSION_FILE, "w") as f:
            f.write(version)
    except IOError as e:
        print(f"Error writing to {VERSION_FILE}: {e}")
        raise

def write_log(old_version, new_version, update_type):
    try:
        with open(VERSION_LOG_FILE, "a") as log_file:
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
            log_message = f"[{timestamp}] {update_type} update: {old_version} -> {new_version}\n"
            log_file.write(log_message)
    except IOError as e:
        print(f"Error writing to {VERSION_LOG_FILE}: {e}")
        raise

def validate_version(version):
    pattern = r"^\d+\.\d+\.\d+$"
    return re.match(pattern, version) is not None

def increment_version(version, update_type):
    major, minor, patch = map(int, version.split('.'))

    if update_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif update_type == "minor":
        minor += 1
        patch = 0
    elif update_type == "patch":
        patch += 1

    return f"{major}.{minor}.{patch}"

def parse_args():
    if len(sys.argv) != 2 or sys.argv[1] not in ["major", "minor", "patch"]:
        print("Error: incorrect parameter (major, minor or patch).")
        sys.exit(1)
    return sys.argv[1]

def main():
    update_type = parse_args()

    if not os.path.exists(VERSION_FILE):
        print(f"File {VERSION_FILE} not found, creating new one with version 1.0.0.")
        write_version("1.0.0")

    current_version = read_version()
    if current_version is None:
        print("Error: couldn't read last version.")
        return

    if not validate_version(current_version):
        print(f"Wrong version format in file {VERSION_FILE}. Required format 0.0.0")
        return

    new_version = increment_version(current_version, update_type)
    write_version(new_version)
    write_log(current_version, new_version, update_type)

    print(f"Version updated from {current_version} to {new_version}.")

if __name__ == "__main__":
    main()