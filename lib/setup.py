from lib import linux, utils

def errEx():
	utils.log("Something went wrong, check archibald.log.", "err")
	exit(1)

def drivers(drv: dict):
	# Try to find known graphics cards from lspci
	utils.log("Searching graphics cards.", "exc")
	pcidevs = linux.lspci()
	for device in drv:

		# Repeat match for every user defined driver group
		match = [f"VGA compatible controller: {device}", f"Display controller: {device}"]
		if any(x in pcidevs for x in match):

			# If is found, add packages to profile.pkgs
			utils.log(f"Found {device} device!", "suc")
			return drv[device]
		
		return []

def setupZram():
	
	utils.log("Enter desired zram size (0 for default).")
	ram = utils.intGet("Answer (MB): ")

	# Default if value is zero or minus
	if ram == 0 or ram < 0:
		ram = "min(ram / 2, 4096)"

	linux.pacman.S(["zram-generator"])
	
	# Write zram config to /etc/systemd
	linux.tee(
		"/etc/systemd", 
		"zram-generator.conf", 
		f"[zram0]\nzram-size = {ram}"
	)

	# Reload units
	linux.systemctl.daemon_reload()

def profile(profile, user: str):

	if profile.drivers != None:

		profile.pkgs += drivers(profile.drivers)

	if len(profile.pkgs) > 0:

		utils.log("Installing packages (may take some time).", "exc")

		if not linux.pacman.S(profile.pkgs):
			errEx()

	if profile.files != None:

		utils.log("Creating configuration files.", "exc")

		for f in profile.files:
			linux.tee(f.path, f.name, f.text)

	if profile.groups != None:

		utils.log("Setting user groups.", "exc")

		if not linux.usermod.aG(profile.groups, user):
			errEx()

	if profile.units != None:
		
		utils.log("Enabling systend units.", "exc")

		if not linux.systemctl.enable(profile.units):
			errEx()
	
	if profile.shell != None:

		utils.log("Changing user shell.", "exc")

		if not linux.chsh(profile.shell, user):
			utils.log("Could not change shell.", "wrn")
	
	if profile.flatpaks != None:

		utils.log("Installing flatpaks.", "exc")

		if not linux.flatpak.install(profile.flatpaks):
			utils.log("Could not install flatpaks.", "wrn")
	
	if profile.aur and user != "root":

		utils.log("Installing paru aur helper.", "exc")

		if linux.clone("https://aur.archlinux.org/paru"):

			if not linux.makepkg.sir("paru"):
				utils.log("Could not install paru.", "wrn")
		else:
			utils.log("Git could not resolve address.", "wrn")

	if profile.bashcmd != None:
		
		utils.log("Custom shell commands.", "exc")
		
		for command in profile.bashcmd:
			linux.bash_c(command)


