import subprocess, os

class usermod:

    # sudo usermod -aG groups user
    def aG(groups: list, user: str):

        try:

            # Invoke subprocess
            subprocess.run(
			    ["sudo", "usermod", "-aG", ",".join(map(str, groups)), user],
			    stdout = open("archibald.log", "a"),
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
			    stdout = open("archibald.log", "a"),
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
			    stdout = open("archibald.log", "a"),
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
			    stdout = open("archibald.log", "a"),
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
			    stdout = open("archibald.log", "a"),
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
                stdout = open("archibald.log", "a"),
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
			    stdout = open("archibald.log", "a"),
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
            stdout = open("archibald.log", "a"),
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
            stdout = open("archibald.log", "a"),
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
            stdout = open("archibald.log", "a"),
            stderr = subprocess.STDOUT,
            check  = True,
            text   = True
        )

        # Return true if shell exists
        return True
    except subprocess.CalledProcessError:
        
        # Return false if not
        return False