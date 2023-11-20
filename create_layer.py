import os
import shutil
import subprocess
import sys


if __name__ == "__main__":
    os.makedirs("build/python", exist_ok=True)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-t", "build/python"])
    os.chdir("build")
    shutil.make_archive("layer", format="zip", root_dir=".", base_dir="python")