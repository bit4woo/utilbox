import subprocess
import pip

try:
    subprocess.run("python3.8 -m pip uninstall utilbox")
    subprocess.run("python3.8 -m pip install git+https://github.com/bit4woo/utilbox.git")
except:
    pip.main(["install", "git+https://github.com/bit4woo/utilbox.git"])
    pip.main(["uninstall", "-y", "utilbox"])  # Use -y flag to automatically confirm uninstallation
