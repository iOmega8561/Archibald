import subprocess, os, json

os.makedirs("logfiles", exist_ok=True)

class usermod:

    # sudo usermod -aG groups user
    def aG(groups: list, user: str):

        try:

            # Invoke subprocess
            subprocess.run(
			    ["sudo", "usermod", "-aG", ",".join(map(str, groups)), user],
			    stdout = open("logfiles/usermod.log", "a"),
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
    def enable(units: list):

        try:

            # Invoke subprocess
            subprocess.run(
			    ["sudo", "systemctl", "enable"] + units,
			    stdout = open("logfiles/systemctl.log", "a"),
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
    def start(units: list):

        try:

            # Invoke subprocess
            subprocess.run(
			    ["sudo", "systemctl", "start"] + units,
			    stdout = open("logfiles/systemctl.log", "a"),
		    	stderr = subprocess.STDOUT,
			    check  = True,
			    text   = True
		    )

            # Return true for success
            return True
        except subprocess.CalledProcessError:

            # Return false for failure
            return False
    
    def daemon_reload():

        # Invoke subprocess
        subprocess.run(
		    ["sudo", "systemctl", "daemon-reload"],
		    check  = True
		)

class makepkg:
    
    # makepkg -sir
    def sir(cwd: str = os.getcwd()):

        try:

            # Invoke subprocess
            subprocess.run(
			    ["makepkg", "-sir", "--noconfirm", "--needed"],
			    stdout = open("logfiles/makepkg.log", "a"),
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

    # sudo pacman -S pkgs
    def S(pkgs: list):
        
        try:

            # Invoke subprocess
            subprocess.run(
			    ["sudo", "pacman", "-S", "--noconfirm", "--needed"] + pkgs,
			    stdout = open("logfiles/pacman.log", "a"),
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
    def Qs(pkgs: list):

        try:

            # Invoke subprocess
            subprocess.run(
                ["pacman", "-Qs"] + pkgs,
                stdout = open("logfiles/pacman.log", "a"),
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

    def setup():
        if pacman.Qs(["paru"]):
            return True

        if not clone("https://aur.archlinux.org/paru") or not makepkg.sir("paru"):
            return False
        
        return True

    # sudo pacman -S pkgs
    def S(pkgs: list):
        try:

            # Invoke subprocess
            subprocess.run(
			    ["paru", "-S", "--noconfirm"] + pkgs,
			    stdout = open("logfiles/paru.log", "a"),
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

    # flatpak install flatpaks
    def install(flatpaks: list):
        
        # Check if flatpak is installed
        if not pacman.Qs(["flatpak"]):

            # Install if not
            pacman.S(["flatpak"])
        
        try:

            # Invoke subprocess
            subprocess.run(
			    ["flatpak", "install", "-y", "-v"] + flatpaks,
			    stdout = open("logfiles/flatpak.log", "a"),
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

    # Check if git is installed
    if not pacman.Qs(["git"]):

        # Install if not
        pacman.S(["git"])
    
    try:

        # Try git clone
        subprocess.run(
            ["git", "clone", url],
            stdout = open("logfiles/git.log", "a"),
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
    tee = subprocess.Popen(
	    cmd, 
		stdin  = subprocess.PIPE, 
		stdout = subprocess.DEVNULL,
    	stderr = subprocess.STDOUT
	)
    
    # Write bytes to stdin
    tee.stdin.write(str.encode(text))

    # Close stdin when finished
    tee.stdin.close()

def chsh(shell: str, user: str):

    try:
        
        # Call subprocess
        subprocess.run(
            ["sudo", "chsh", "-s", shell, user],
            stdout = open("logfiles/chsh.log", "a"),
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

    try:
        
        # Call subprocess
        subprocess.run(
            ["bash", "-c", command],
            stdout = open("logfiles/bash.log", "a"),
            stderr = subprocess.STDOUT,
            check  = True,
            text   = True
        )

        # Return true if shell exists
        return True
    except subprocess.CalledProcessError:
        
        # Return false if not
        return False