import os
import subprocess
import pyautogui

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

logo = """\
     ___
    (.· |
    (<> |
   / __  \\
  ( /  \\ /|
 _/\\ __)/_)
 \\/-____\\/
"""

def get_user():
    return os.environ["USER"]

def get_hostname():
    result = subprocess.run(['hostname'], stdout=subprocess.PIPE)
    return get_user() + "@" + result.stdout.decode("utf-8").strip()

def get_distroname():
    file = open("/etc/lsb-release", "r")
    lsb_release = file.read()

    distro_name = [line for line in lsb_release.splitlines() if line.startswith("DISTRIB_DESCRIPTION")]
    return distro_name[0][len("DISTRIB_DESCRIPTION=\""):-1].strip()

def get_uptime():
    result = subprocess.run(["uptime", "--pretty"], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip()

def get_kernel():
    result = subprocess.run(["uname", "-r"], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip()

def get_host():
    name = ""
    version = ""
    model = ""

    try:
        name_file = open("/sys/devices/virtual/dmi/id/product_name", "r")
        name = name_file.read().strip()
    except Exception:
        pass

    try:
        version_file = open("/sys/devices/virtual/dmi/id/product_version", "r")
        version = version_file.read().strip()
    except Exception:
        pass

    try:
        model_file = open("/sys/firmware/devicetree/base/model", "r")
        model = model_file.read().strip()
    except Exception:
        pass

    return name + " " + version + " " + model

def get_ram():
    result = subprocess.run(["free", "-h"], stdout=subprocess.PIPE)
    memline = result.stdout.decode("utf-8").splitlines()[2]
    elements = memline.split()
    total = elements[1]
    free = elements[2]

    return free + " / " + total

def get_terminal():
    return os.environ["TERM"]

def get_resolution():
    return pyautogui.size()

def get_cpu():
    command = "cat /proc/cpuinfo"
    all_info = subprocess.check_output(command, shell=True).decode().strip()
    for line in all_info.split("\n"):
        if "model name" in line:
            return line.split(":")[1].strip()

def get_gpu():
    result = subprocess.check_output("lspci", shell=True).decode()
    gpus = [line for line in result.split("\n") if "VGA compatible controller" in line or "3D controller" in line]
    return gpus[0].split(":")[-1].strip()

def print_fetch():
    info = [
        ["User:", get_user()],
        ["Hostname:", get_hostname()],
        ["Distro:", get_distroname()],
        ["Uptime:", get_uptime()],
        ["Kernel:", get_kernel()],
        ["Host:", get_host()],
        ["Ram:", get_ram()],
        ["Terminal:", get_terminal()],
        ["Resolution:", get_resolution()],
        ["Cpu:", get_cpu()],
        ["Gpu:", get_gpu()],
    ]

    for index, entry in enumerate(info):
        line = logo.splitlines()[index] if index < len(logo.splitlines()) else ""

        print("{3}{0:<12} {1} {2:<10} {3}{4}".format(
                                         line,
                                         bcolors.OKBLUE,
                                         entry[0],
                                         bcolors.WARNING,
                                         entry[1]))

print_fetch()
