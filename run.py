import subprocess
import sys

from download_models import download_models


def main():
    print("Checking models...")
    download_models()

    print("Starting Medical AI...")

    subprocess.run([
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--reload"
    ])


if __name__ == "__main__":
    main()