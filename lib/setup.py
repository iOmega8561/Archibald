from lib import console, linux

def __fatal():

	console.log("Something went wrong, check archibald.log.", "err")
	exit(1)

def __parse_pci(gfxd):
	
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
	return []

def __apply(profile, user: str):
	
	console.log(f"Resolving profile {profile.name}", "wrn")

	if profile.gfxd and not profile.pkgs:

		profile.pkgs = __parse_pci(profile.gfxd)

	elif profile.gfxd:
		
		profile.pkgs += __parse_pci(profile.gfxd)

	if profile.pkgs:
		
		console.log("Installing packages (may take some time).", "exc")

		if not linux.pacman.S(profile.pkgs):
			__fatal()

	if profile.files:

		console.log("Creating configuration files.", "exc")

		for f in profile.files:
			linux.tee(f.path, f.name, f.text)

	if profile.groups:

		console.log("Setting user groups.", "exc")

		if not linux.usermod.aG(profile.groups, user):
			__fatal()

	if profile.units:
		
		console.log("Enabling systend units.", "exc")

		if not linux.systemctl.enable(profile.units):
			__fatal()
	
	if profile.shell:

		console.log("Changing user shell.", "exc")

		if not linux.chsh(profile.shell, user):
			console.log("Could not change shell.", "wrn")
	
	if profile.flatpaks:

		console.log("Installing flatpaks.", "exc")

		if not linux.flatpak.install(profile.flatpaks):
			console.log("Could not install flatpaks.", "wrn")
	
	if profile.aur and user != "root":

		console.log("Installing paru and AUR packages.", "exc")

		if not linux.paru.setup():
			console.log("Could not install paru.", "wrn")
		
		elif not linux.paru.S(profile.aur):
			console.log("Could not install aur packages.", "wrn")

	if profile.bash:
		
		console.log("Custom shell commands.", "exc")
		
		for command in profile.bash:
			linux.bash_c(command)

__resolved = []

def resolve(p_dict: dict, index: int, user: str = linux.whoami()):
	
	# Get indexed keys list
	indexed = list(p_dict.keys())
	
	# Get key from caller index
	key = indexed[index]

	# Check if profile has dependencies
	if not p_dict[key].deps:

		# If not just apply profile and return
		__apply(p_dict[key], user)
		return

	# Iter profile dependencies list
	for dep in p_dict[key].deps:

		# Check dependency exists and not duplicate
		if p_dict[dep] and dep not in __resolved:

			# Append dependency as resolved
			__resolved.append(dep)

			# If yes, resolve it's dependencies
			resolve(p_dict, indexed.index(dep), user)
		
		elif dep in __resolved:

			# Just skip dependency
			continue

		else:

			# If does not exist, exit
			console.log(f"Missing dep. {dep} required by {key}", "wrn")
			__fatal()

	# Apply desired profile
	__apply(p_dict[key], user)
				