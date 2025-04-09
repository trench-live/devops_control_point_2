import os
import sys
import re
from datetime import datetime
from typing import Optional, Tuple
from config import VERSION_FILE, VERSION_LOG_FILE

class VersionManager:
    """Class for version management with validation and logging"""

    # Regular expression for version format validation (X.Y.Z)
    VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

    @staticmethod
    def ensure_directory_exists(filepath: str) -> None:
        """Creates directory for file if it doesn't exist"""
        dir_path = os.path.dirname(filepath)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    @classmethod
    def read_version(cls) -> Optional[str]:
        """Reads current version from file"""
        try:
            if os.path.exists(VERSION_FILE):
                with open(VERSION_FILE, "r", encoding="utf-8") as f:
                    version = f.read().strip()
                    if cls.validate_version(version):
                        return version
            return None
        except IOError as e:
            print(f"Error reading {VERSION_FILE}: {e}", file=sys.stderr)
            return None

    @classmethod
    def write_version(cls, version: str) -> None:
        """Writes new version to file"""
        try:
            cls.ensure_directory_exists(VERSION_FILE)
            with open(VERSION_FILE, "w", encoding="utf-8") as f:
                f.write(version)
        except IOError as e:
            print(f"Error writing to {VERSION_FILE}: {e}", file=sys.stderr)
            raise

    @classmethod
    def log_version_change(cls, old_ver: str, new_ver: str, update_type: str) -> None:
        """Logs version change"""
        try:
            cls.ensure_directory_exists(VERSION_LOG_FILE)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = (
                f"[{timestamp}] {update_type.upper()} update: "
                f"{old_ver} -> {new_ver}\n"
            )
            with open(VERSION_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except IOError as e:
            print(f"Error writing to {VERSION_LOG_FILE}: {e}", file=sys.stderr)
            raise

    @classmethod
    def validate_version(cls, version: str) -> bool:
        """Validates version format"""
        return bool(cls.VERSION_PATTERN.fullmatch(version))

    @classmethod
    def increment_version(cls, version: str, increment_type: str) -> str:
        """
        Increments version according to SemVer:
        - major: X+1.0.0
        - minor: X.Y+1.0
        - patch: X.Y.Z+1
        """
        match = cls.VERSION_PATTERN.match(version)
        if not match:
            raise ValueError(f"Invalid version format: {version}")

        major, minor, patch = map(int, match.groups())

        if increment_type == "major":
            major += 1
            minor = patch = 0
        elif increment_type == "minor":
            minor += 1
            patch = 0
        elif increment_type == "patch":
            patch += 1

        return f"{major}.{minor}.{patch}"

def parse_arguments() -> Tuple[str, Optional[str]]:
    """Parses command line arguments"""
    if len(sys.argv) < 2:
        return "get", None  # Default mode - get version

    cmd = sys.argv[1].lower()
    if cmd not in {"major", "minor", "patch", "get"}:
        print("Usage: version.py [major|minor|patch|get]", file=sys.stderr)
        sys.exit(1)

    return cmd, None

def initialize_version_file() -> str:
    """Initializes version file if it doesn't exist"""
    if not os.path.exists(VERSION_FILE):
        initial_version = "1.0.0"
        VersionManager.write_version(initial_version)
        return initial_version
    return None

def main() -> None:
    """Main execution flow"""
    command, _ = parse_arguments()

    # Initialization on first run
    initialize_version_file()

    # Get current version
    current_version = VersionManager.read_version()
    if not current_version:
        print("Error: Failed to read version", file=sys.stderr)
        sys.exit(1)

    # Version retrieval mode
    if command == "get":
        print(current_version)
        return

    # Version increment
    try:
        new_version = VersionManager.increment_version(current_version, command)
        VersionManager.write_version(new_version)
        VersionManager.log_version_change(current_version, new_version, command)

        # Output for CI/CD (only version number)
        print(new_version)

    except ValueError as e:
        print(f"Version error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()