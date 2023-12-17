"""This module contains Linux distribution specific commands, wrapped as python procedures
   and classes to directly execute binaries and shell wrappers from Archibald
   
   PEP8 naming convention is ignored for class and function names in this file
   to keep conform with system executable names"""

import subprocess
import os
import json

libpath = os.path.abspath(os.path.dirname(__file__))
logpath = f"{libpath}/../logfiles"
os.makedirs(logpath, exist_ok=True)

class usermod:

    # sudo usermod -aG groups user
    @staticmethod
    def aG(groups: list, user: str):
        """Command: usermod -aG %s $USER"""

        try:

            with open(f"{logpath}/usermod.log", "a", encoding="utf-8") as log:

                # Invoke subprocess
                subprocess.run(
			        ["sudo", "usermod", "-aG", ",".join(map(str, groups)), user],
			        stdout = log,
		    	    stderr = subprocess.STDOUT,
			        check  = True,
			        text   = True
		        )

            # Return true for success
            return True
        except subprocess.CalledProcessError:

            # Return false for failure
            return False

class systemctl:

    # sudo systemctl enable units
    @staticmethod
    def enable(units: list):
        """Command: systemctl enable %s"""

        try:

            with open(f"{logpath}/systemctl.log", "a", encoding="utf-8") as log:

                # Invoke subprocess
                subprocess.run(
			        ["sudo", "systemctl", "enable"] + units,
			        stdout = log,
		    	    stderr = subprocess.STDOUT,
			        check  = True,
			        text   = True
		        )

            # Return true for success
            return True
        except subprocess.CalledProcessError:

            # Return false for failure
            return False

    # sudo systemctl enable units
    @staticmethod
    def start(units: list):
        """Command: systemctl start %s"""

        try:

            with open(f"{logpath}/systemctl.log", "a", encoding="utf-8") as log:

                # Invoke subprocess
                subprocess.run(
			        ["sudo", "systemctl", "start"] + units,
			        stdout = log,
		    	    stderr = subprocess.STDOUT,
			        check  = True,
			        text   = True
		        )

            # Return true for success
            return True
        except subprocess.CalledProcessError:

            # Return false for failure
            return False

    @staticmethod
    def daemon_reload():
        """Command: systemctl daemon-reload"""

        # Invoke subprocess
        subprocess.run(
		    ["sudo", "systemctl", "daemon-reload"],
		    check  = True
		)

class makepkg:
    """Executable: makepkg"""

    # makepkg -sir
    @staticmethod
    def sir(cwd: str = os.getcwd()):
        """Command: makepkg -sir %s --noconfirm --needed"""

        try:

            with open(f"{logpath}/makepkg.log", "a", encoding="utf-8") as log:

                # Invoke subprocess
                subprocess.run(
			        ["makepkg", "-sir", "--noconfirm", "--needed"],
			        stdout = log,
		    	    stderr = subprocess.STDOUT,
                    cwd    = cwd,
			        check  = True,
			        text   = True
		        )

            # Return true for success
            return True
        except subprocess.CalledProcessError:

            # Return false for failure
            return False

class pacman:
    """Executable: pacman"""

    # sudo pacman -S pkgs
    @staticmethod
    def S(pkgs: list):
        """Command: pacman -S %s --noconfirm --needed"""

        try:

            with open(f"{logpath}/pacman.log", "a", encoding="utf-8") as log:

                # Invoke subprocess
                subprocess.run(
			        ["sudo", "pacman", "-S", "--noconfirm", "--needed"] + pkgs,
			        stdout = log,
		    	    stderr = subprocess.STDOUT,
			        check  = True,
			        text   = True
		        )

            # Return true for success
            return True
        except subprocess.CalledProcessError:

            # Return false for failure
            return False

    # pacman -Qs pkgs
    @staticmethod
    def Qs(pkgs: list):
        """Command: pacman -Qs %s"""

        try:

            with open(f"{logpath}/pacman.log", "a", encoding="utf-8") as log:

                # Invoke subprocess
                subprocess.run(
                    ["pacman", "-Qs"] + pkgs,
                    stdout = log,
		    	    stderr = subprocess.STDOUT,
			        check  = True,
			        text   = True
                )

            # Return true for success
            return True
        except subprocess.CalledProcessError:

            # Return false for failure
            return False

class paru:
    """Executable: paru"""

    @staticmethod
    def setup():
        """Commands: pacman -Qs paru (to check if it's already there)
                     git clone https://aur.archlinux.org/paru (if it's not)
                     cd paru && makepkg -sir --needed --noconfirm (if it's not)"""

        if pacman.Qs(["paru"]):
            return True

        if not clone("https://aur.archlinux.org/paru") or not makepkg.sir("paru"):
            return False

        return True

    # sudo pacman -S pkgs
    @staticmethod
    def S(pkgs: list):
        """Command: paru -S %s --noconfirm"""

        try:

            with open(f"{logpath}/paru.log", "a", encoding="utf-8") as log:

                # Invoke subprocess
                subprocess.run(
			        ["paru", "-S", "--noconfirm"] + pkgs,
			        stdout = log,
		    	    stderr = subprocess.STDOUT,
			        check  = True,
			        text   = True
		        )

            # Return true for success
            return True
        except subprocess.CalledProcessError:

            # Return false for failure
            return False

class flatpak:
    """Executable: flatpak"""

    # flatpak install flatpaks
    @staticmethod
    def install(flatpaks: list):
        """Commands: pacman -Qs flatpak (to check if it's already there)
                     pacman -S flatpak (if it's not)
                     flatpak install -y -v %s"""

        # Check if flatpak is installed
        if not pacman.Qs(["flatpak"]):

            # Install if not
            pacman.S(["flatpak"])

        try:

            with open(f"{logpath}/flatpak.log", "a", encoding="utf-8") as log:

                # Invoke subprocess
                subprocess.run(
			        ["flatpak", "install", "-y", "-v"] + flatpaks,
			        stdout = log,
		    	    stderr = subprocess.STDOUT,
			        check  = True,
			        text   = True
		        )

            # Return true for success
            return True
        except subprocess.CalledProcessError:

            # Return false for failure
            return False

def whoami():
    """Executable: whoami"""

    # Call subprocess
    whoami_proc = subprocess.run(
        ["whoami"],
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        check = True,
        text = True
    )

    # Return username
    return whoami_proc.stdout.rstrip("\n")

def mkdir(path: str):
    """Executable: mkdir"""

    # Check if it's a home path
    if "{home}" in path:
        homedir = os.environ.get("HOME")

        # If it is don't execute with sudo
        cmd = ["mkdir", "-p", path.format(home = homedir)]
    else:

        # If it's not, execute with sudo
        cmd = ["sudo", "mkdir", "-p", path]

    # Call subprocess
    subprocess.run(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        check = True,
        text = True
    )

def lsblk_json():
    """Executable: lsblk"""

    lsblk = subprocess.run(
        ["lsblk", "-J", "-fs", "--output=NAME,FSTYPE,UUID,MOUNTPOINTS"],
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        check  = True,
        text   = True
    )

    blockdevices = json.loads(lsblk.stdout)

    return blockdevices["blockdevices"]

def findmount(mountpoint: str):
    """This function returns the blockdevice
       that is mounted at the input mountpoint"""

    # Get block devices from lsblk
    blockdevices = lsblk_json()

    for device in blockdevices:

        # Check if mountpoint exists in device mountpoints
        if mountpoint in device["mountpoints"]:

            # If yes, return device
            return device

        # Check every device child if it has any
        for child in device["children"] if "children" in device.keys() else []:

            # Check if mountpoint exists
            if mountpoint in child["mountpoints"]:

                # Return child
                return child

def lspci():
    """Executable: lspci"""

    # Check if pciutils is installed
    if not pacman.Qs(["pciutils"]):

        # Install if not
        pacman.S(["pciutils"])

    # Get lspci subprocess
    lspci_proc = subprocess.run(
        ["lspci"],
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        check  = True,
        text   = True
    )

    # Return stripped output
    return lspci_proc.stdout.rstrip("\n")

def lsusb():
    """Executable: lsusb"""

    # Check if pciutils is installed
    if not pacman.Qs(["usbutils"]):

        # Install if not
        pacman.S(["usbutils"])

    # Get lspci subprocess
    lspci_proc = subprocess.run(
        ["lspci"],
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        check  = True,
        text   = True
    )

    # Return stripped output
    return lspci_proc.stdout.rstrip("\n")

def clone(url: str, cwd: str = os.getcwd()):
    """Executable: git
       Command: git clone %s"""

    # Check if git is installed
    if not pacman.Qs(["git"]):

        # Install if not
        pacman.S(["git"])

    try:

        with open(f"{logpath}/git.log", "a", encoding="utf-8") as log:

            # Try git clone
            subprocess.run(
                ["git", "clone", url],
                stdout = log,
                stderr = subprocess.STDOUT,
                cwd    = cwd,
                check  = True,
                text   = True
            )

        # Return true for success
        return True
    except subprocess.CalledProcessError:

        # False for failure
        return False

def tee(path: str, name: str, text: str):
    """Executable: tee"""

    mkdir(path = path)

    # Check if it's a home path
    if "{home}" in path:
        homedir = os.environ.get("HOME")

        # If it is don't execute with sudo
        cmd = ["tee", f"{path.format(home = homedir)}/{name}"]
    else:

        # If it's not, execute with sudo
        cmd = ["sudo", "tee", f"{path}/{name}"]

    # Use Popen for stdin
    __tee = subprocess.Popen(
	    cmd,
		stdin  = subprocess.PIPE,
		stdout = subprocess.DEVNULL,
    	stderr = subprocess.STDOUT
	)

    # Write bytes to stdin
    __tee.stdin.write(str.encode(text))

    # Close stdin when finished
    __tee.stdin.close()

def chsh(shell: str, user: str):
    """Executable: chsh
       Command: chsh -s %s $USER"""

    try:

        with open(f"{logpath}/chsh.log", "a", encoding="utf-8") as log:

            # Call subprocess
            subprocess.run(
                ["sudo", "chsh", "-s", shell, user],
                stdout = log,
                stderr = subprocess.STDOUT,
                check  = True,
                text   = True
            )

        # Return true if shell exists
        return True
    except subprocess.CalledProcessError:

        # Return false if not
        return False

def bash_c(command: str):
    """Executable: bash
       Command: bash -c %s"""

    try:

        with open(f"{logpath}/bash.log", "a", encoding="utf-8") as log:

            # Call subprocess
            subprocess.run(
                ["bash", "-c", command],
                stdout = log,
                stderr = subprocess.STDOUT,
                check  = True,
                text   = True
            )

        # Return true if shell exists
        return True
    except subprocess.CalledProcessError:

        # Return false if not
        return False
