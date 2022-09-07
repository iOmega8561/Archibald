from lib import console, linux

def errEx():
	console.log("Something went wrong, check archibald.log.", "err")
	exit(1)

def parsePCI(gfxd):
	
	# Try to find known pci devs from lspci
	console.log("Parsing pci devices.", "exc")
	pcidevs = linux.lspci()

	for device in gfxd:

		# Repeat match for every user defined driver group
		match = [f"VGA compatible controller: {device}", f"Display controller: {device}"]
		if any(x in pcidevs for x in match):

			# If is found, add packages to profile.pkgs
			console.log(f"Found {device} device!", "suc")
			return gfxd[device]

def profile(profile, user: str):

	if profile.gfxd != None:

		if profile.pkgs != None:
			profile.pkgs = parsePCI(profile.gfxd)
		else:
			profile.pkgs += parsePCI(profile.gfxd)

	if profile.pkgs != None:
		
		console.log("Installing packages (may take some time).", "exc")

		if not linux.pacman.S(profile.pkgs):
			errEx()

	if profile.files != None:

		console.log("Creating configuration files.", "exc")

		for f in profile.files:
			linux.tee(f.path, f.name, f.text)

	if profile.groups != None:

		console.log("Setting user groups.", "exc")

		if not linux.usermod.aG(profile.groups, user):
			errEx()

	if profile.units != None:
		
		console.log("Enabling systend units.", "exc")

		if not linux.systemctl.enable(profile.units):
			errEx()
	
	if profile.shell != None:

		console.log("Changing user shell.", "exc")

		if not linux.chsh(profile.shell, user):
			console.log("Could not change shell.", "wrn")
	
	if profile.flatpaks != None:

		console.log("Installing flatpaks.", "exc")

		if not linux.flatpak.install(profile.flatpaks):
			console.log("Could not install flatpaks.", "wrn")
	
	if profile.aur != None and user != "root":

		console.log("Installing paru aur helper.", "exc")

		if linux.clone("https://aur.archlinux.org/paru"):

			if not linux.makepkg.sir("paru"):
				console.log("Could not install paru.", "wrn")
		else:
			console.log("Git could not resolve address.", "wrn")

	if profile.bashcmd != None:
		
		console.log("Custom shell commands.", "exc")
		
		for command in profile.bashcmd:
			linux.bash_c(command)


