from functions import console, linux

def __fatal(msg: str):

	console.log(f"{msg}", "wrn")
	return False

def __parse_pci(gfxd):
	
	to_install = []

	# Try to find known pci devs from lspci
	console.log("Parsing pci devices.", "exc")
	pcidevs = linux.lspci()

	for device in gfxd:

		# Repeat match for every user defined driver group
		match = [f"VGA compatible controller: {device}", f"Display controller: {device}", f"3D controller: {device}"]
		if any(x in pcidevs for x in match):

			# If is found, add packages to profile.pkgs
			console.log(f"Found {device} device!", "suc")
			to_install += gfxd[device]

	return to_install

def __apply(profile, user: str):
	
	console.log(f"Resolving profile {profile.name}", "wrn")

	if profile.gfxd and not profile.pkgs:

		profile.pkgs = __parse_pci(profile.gfxd)

	elif profile.gfxd:
		
		profile.pkgs += __parse_pci(profile.gfxd)

	if profile.pkgs:
		
		console.log("Installing packages (may take some time).", "exc")

		if not linux.pacman.S(profile.pkgs):
			return __fatal("Could not install packages")

	if profile.files:

		console.log("Creating configuration files.", "exc")

		for f in profile.files:
			linux.tee(f.path, f.name, f.text)

	if profile.groups:

		console.log("Setting user groups.", "exc")

		if not linux.usermod.aG(profile.groups, user):
			return __fatal("Could not set user groups")

	if profile.units:
		
		console.log("Enabling systemd units.", "exc")

		if not linux.systemctl.enable(profile.units):
			return __fatal("Could not enable systemd units")
	
	if profile.shell:

		console.log("Changing user shell.", "exc")

		if not linux.chsh(profile.shell, user):
			return __fatal("Could not change shell.")
	
	if profile.flatpaks:

		console.log("Installing flatpaks.", "exc")

		if not linux.flatpak.install(profile.flatpaks):
			return __fatal("Could not install flatpaks.")
	
	if profile.aur and user != "root":

		console.log("Installing paru and AUR packages.", "exc")

		if not linux.paru.setup():
			return __fatal("Could not install paru.")
		
		elif not linux.paru.S(profile.aur):
			return __fatal("Could not install aur packages.")

	if profile.bash:
		
		console.log("Custom shell commands.", "exc")
		
		for command in profile.bash:
			linux.bash_c(command)
	
	return True

__resolved = []

def resolve(p_dict: dict, index: int, user: str = linux.whoami()):
	
	# Get indexed keys list
	indexed = list(p_dict.keys())
	
	# Get key from caller index
	key = indexed[index]

	# Iter profile dependencies list
	for dep in p_dict[key].deps if p_dict[key].deps else []:

		# Check dependency exists and not duplicate
		if p_dict[dep] and dep not in __resolved:

			# If yes, resolve it's dependencies
			if not resolve(p_dict, indexed.index(dep), user):
				return False
			
			# Append dependency as resolved
			__resolved.append(dep)
		
		elif dep not in __resolved:

			# If does not exist, exit
			console.log(f"Missing dep. {dep} required by {key}", "wrn")
			return False

	# Apply desired profile
	if not __apply(p_dict[key], user):
		return False
	
	# Append profile to resolved
	__resolved.append(key)

	return True