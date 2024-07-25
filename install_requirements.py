import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

requirements = [
    "gunicorn",
    "vercel",
    # Add other dependencies here
]

if sys.platform == "win32":
    requirements.append("pywin32==306")

for package in requirements:
    install(package)
