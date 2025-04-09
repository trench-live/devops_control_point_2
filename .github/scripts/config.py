import os

# Пути относительно корня репозитория
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERSION_FILE = os.path.join(REPO_ROOT, "version_info", "version")
VERSION_LOG_FILE = os.path.join(REPO_ROOT, "version_info", "version_log")