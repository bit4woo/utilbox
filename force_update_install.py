import subprocess

import pip

try:
    subprocess.run("python3.8 -m pip install --force-reinstall git+https://github.com/bit4woo/utilbox.git", shell=True)
except:
    try:
        subprocess.run("python3.8 -m pip uninstall utilbox", shell=True)
    except:
        pip.main(["uninstall", "-y", "utilbox"])  # Use -y flag to automatically confirm uninstallation

    try:
        subprocess.run("python3.8 -m pip install git+https://github.com/bit4woo/utilbox.git", shell=True)
    except:
        pip.main(["install", "git+https://github.com/bit4woo/utilbox.git"])
