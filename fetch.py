import os
import subprocess

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
    return distro_name[0][len("DISTRIB_DESCRIPTON=\""):-1].strip()

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

def print_fetch():
    info = [
        ["user", get_user()],
        ["hostname", get_hostname()],
        ["distro", get_distroname()],
        ["uptime", get_uptime()],
        ["kernel", get_kernel()],
        ["host", get_host()],
        ["ram", get_ram()],
        ["terminal", get_terminal()],
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
