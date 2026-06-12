import os
import subprocess
import time
import json
from datetime import datetime

class AutoUpdater:
    """
    安全自动升级系统（Git + start.sh 统一入口）
    """

    def __init__(self, repo_path="~/trading_bot"):
        self.repo_path = os.path.expanduser(repo_path)
        self.version_file = os.path.join(self.repo_path, "version.json")

    def get_current_version(self):
        if not os.path.exists(self.version_file):
            return "0.0.0"
        with open(self.version_file, "r") as f:
            return json.load(f).get("version", "0.0.0")

    def save_version(self, version):
        with open(self.version_file, "w") as f:
            json.dump({
                "version": version,
                "updated_at": str(datetime.now())
            }, f, indent=2)

    def pull_latest(self):
        print("[UPDATER] pulling latest code...")

        result = subprocess.run(
            ["git", "pull"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.returncode != 0:
            print("[UPDATER] git pull failed!")
            return False

        return True

    def restart(self):
        print("[UPDATER] restarting bot via start.sh...")

        os.chdir(self.repo_path)

        # 停掉旧进程
        os.system("pkill -f main.py")
        time.sleep(1)

        # 用统一入口启动
        os.system("nohup ./start.sh > logs/run.log 2>&1 &")

    def run(self):
        old_version = self.get_current_version()

        if self.pull_latest():
            new_version = str(int(time.time()))

            if new_version != old_version:
                print(f"[UPDATER] version changed: {old_version} → {new_version}")
                self.save_version(new_version)
                self.restart()
