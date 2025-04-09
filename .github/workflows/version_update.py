import os
import sys
from datetime import datetime


def read_version():
    if os.path.exists("version"):
        with open("version", "r") as f:
            return f.read().strip()
    else:
        return None


def write_version(version):
    with open("version", "w") as f:
        f.write(version)


def log(old_version, new_version, update_type):
    with open("version_log", "a") as log_file:
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
        log_message = f"[{new_version}] <- [{old_version}][{timestamp}] {update_type} update\n"
        log_file.write(log_message)


def increment_version(version, update_type):
    major, minor, patch = map(int, version.split('.'))

    match update_type:
        case "major":
            major += 1
            minor = 0
            patch = 0
        case "minor":
            minor += 1
            patch = 0
        case "patch":
            patch += 1

    return f"{major}.{minor}.{patch}"


def main():
    if not os.path.exists("version"):
        write_version("1.0.0")

    old_version = read_version()
    if old_version is None:
        print("Cannot read current version")
        return

    version_parts = old_version.split(".")
    if len(version_parts) != 3 or not all(part.isdigit() for part in version_parts):
        print("Unknown version format. Format major.minor.patch expected")
        return

    if len(sys.argv) != 3 or sys.argv[1] not in ["major", "minor", "patch"]:
        print("Error: argument expected (major/minor/patch)")
        return

    update_type = sys.argv[1]
    file_path = sys.argv[2]

    new_version = increment_version(old_version, update_type)

    write_version(new_version)

    log(old_version, new_version, update_type)

    print(f"Updated version from {old_version} to {new_version}.")


if __name__ == "__main__":
    main()