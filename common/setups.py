from common import methods, structures
from userconf import packages

def zram(ramsize: str = "ram / 2"):
	
	# Try to install zram-generator
	methods.subprocessEz(
		command = ["pacman", "-S", "--noconfirm", "zram-generator"], 
		errmsg = "Unexpected error installing zram-generator.")
		
	# Write zram config to /etc/systemd
	file = methods.makefile(
			name = "zram-generator.conf",
			path = "/etc/systemd",
			errmsg = "Could not open /etc/systemd/zram-generator.conf.")

	file.write(f"[zram0]\nzram-size = {ramsize}")

	# Reload units
	methods.subprocessEz(
		command = ["systemctl", "daemon-reload"])

def aur(user: str):

	# Try to remove pre-existent trash
	methods.subprocessEz(
		command = ["rm", "-fr", "paru"], cwd = f"/home/{user}")

	# Try git clone paru repository
	methods.subprocessEz(
		command = ["git", "clone", "https://aur.archlinux.org/paru"],
		user = user,
		cwd = f"/home/{user}",
		errmsg = "Git encountered an unexpected error.")

	# Try to install dependencies, compile and install paru
	methods.subprocessEz(command = ["makepkg", "-si", "--noconfirm", "--needed"],
		user = user,
		logfile = True,
		cwd = f"/home/{user}/paru",
		errmsg = "Could not install paru, check log files.")
		
	# Try to remove leftover trash
	methods.subprocessEz(
		command = ["rm", "-fr", "paru"], 
		cwd = f"/home/{user}")

def profile(profile: structures.profile , user: str):

	# Check if profile demands video drivers
	if profile.drivers != False:

		# Try to find known graphics cards from lspci
		methods.log("Searching for any known graphics device...", "wrn")
		lspci = methods.subprocessEz(command = ["lspci"])
		for device in packages.drivers:

			# Repeat match for every user defined driver group
			match = [f"VGA compatible controller: {device}", f"Display controller: {device}"]
			if any(x in lspci.stdout for x in match):

				# If is found, add packages to profile.pkgs
				methods.log(f"Found {device} device!", "suc")
				profile.pkgs += packages.drivers[device]

	if len(profile.pkgs) > 0:

		methods.log("Packages installation may take some time!", "wrn")

		# Call pacman to install packages
		methods.subprocessEz(
			command = ["pacman", "-S", "--needed", "--noconfirm"] + profile.pkgs,
			logfile = True, 
			succmsg = "Successfully installed all packages!", 
			errmsg = "Unexpected error, check pacman log file")

	if profile.files != None:

		methods.log("Creating configuration files...", "exc")

		# Config files creation
		for i, f in enumerate(profile.files):

			file = methods.makefile(
				name = f.name, 
				path = f.path.format(home = f"/home/{user}"),
				errmsg = f"Could not open {f.path}{f.name}.")

			file.write(f.text)
	
		# Archibald runs as root, home located files will be owned by root, let's fix that
		methods.subprocessEz(command = ["chown", "-R", user, f"/home/{user}"])

	if profile.groups != None:

		# Setting user groups one by one
		for i in profile.groups:
			methods.subprocessEz(command = ["usermod", "-aG", i, user])

	# Check if profile demands systemd enable
	if profile.units != None:

		# Try enable all at once
		methods.subprocessEz(
			command = ["systemctl", "enable"] + profile.units,
			logfile = True,
			errmsg = "Unexpected error, check systemctl log file")
	
	# Check if profile demands a chsh
	if profile.shell != None:

		# Try changing user shell
		methods.subprocessEz(
			command = ["chsh", "-s", profile.shell, user],
			errmsg = f"Unexpected error changing shell to {profile.shell}.")