from common import methods, structures
from userconf import packages

def zram():
	
	# Try to install zram-generator
	methods.subprocessRun(
		cmd  = ["sudo", "pacman", "-S", "--noconfirm", "zram-generator"],
		logs = True,
		err  = "Unexpected error installing zram-generator."
	)
		
	# Write zram config to /etc/systemd
	methods.linuxFile(
		path = "/etc/systemd",
		name = "zram-generator.conf",
		text = "[zram0]\nzram-size = ram / 2"
	)

	# Reload units
	methods.subprocessRun(
		cmd  = ["sudo", "systemctl", "daemon-reload"],
		logs = True
	)

def aur(user: str):

	if user == "root":

		methods.log("Cannot run makepkg as root, skipping.", "err")
		return

	# Try git clone paru repository
	methods.subprocessRun(
		cmd  = ["git", "clone", "https://aur.archlinux.org/paru"],
		logs = True,
		err  = "Git encountered an unexpected error."
	)

	# Try to install dependencies, compile and install paru
	methods.subprocessRun(
		cmd  = ["makepkg", "-si", "--noconfirm", "--needed"],
		logs = True,
		cwd  = "paru",
		err  = "Could not install paru, check archibald.log"
	)

def profile(profile: structures.profile , user: str):

	# Check if profile demands video drivers
	if profile.drivers != False:

		# Try to find known graphics cards from lspci
		methods.log("Searching for any known graphics device...", "wrn")
		lspci = methods.subprocessRun(cmd = ["lspci"])
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
		methods.subprocessRun(
			cmd  = ["sudo", "pacman", "-S", "--needed", "--noconfirm"] + profile.pkgs,
			logs = True,
			succ = "Successfully installed all packages!", 
			err  = "Unexpected error, check archibald.log"
		)

	if profile.files != None:

		methods.log("Creating configuration files...", "wrn")

		# Config files creation
		for i, f in enumerate(profile.files):

			methods.linuxFile(
				path = f.path,
				name = f.name,
				text = f.text
			)

	if profile.groups != None:

		methods.log("Setting user groups...", "wrn")

		# Setting user groups one by one
		for i in profile.groups:
			methods.subprocessRun(
				cmd  = ["sudo", "usermod", "-aG", i, user],
				logs = True,
			)

	# Check if profile demands systemd enable
	if profile.units != None:

		# Try enable all at once
		methods.subprocessRun(
			cmd  = ["sudo", "systemctl", "enable"] + profile.units,
			logs = True,
			err  = "Unexpected error, check archibald.log"
		)
	
	# Check if profile demands a chsh
	if profile.shell != None:

		# Try changing user shell
		methods.subprocessRun(
			cmd  = ["sudo", "chsh", "-s", profile.shell, user],
			logs = True,
			err  = f"Unexpected error changing shell to {profile.shell}."
		)