from common import methods, structures
from userconf import packages

def zram(ram: int):
	
	# Default if value is zero or minus
	if ram == 0 or ram < 0:
		ram = "min(ram / 2, 4096)"

	# Try to install zram-generator
	methods.subprocessRun(
		cmd  = ["sudo", "pacman", "-S", "--noconfirm", "zram-generator"],
		logs = True
	)
		
	# Write zram config to /etc/systemd
	methods.linuxFile(
		path = "/etc/systemd",
		name = "zram-generator.conf",
		text = f"[zram0]\nzram-size = {ram}"
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
		logs = True
	)

	# Try to install dependencies, compile and install paru
	methods.subprocessRun(
		cmd  = ["makepkg", "-si", "--noconfirm", "--needed"],
		logs = True,
		cwd  = "paru"
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
			logs = True
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
				logs = True
			)

	# Check if profile demands systemd enable
	if profile.units != None:

		# Try enable all at once
		methods.subprocessRun(
			cmd  = ["sudo", "systemctl", "enable"] + profile.units,
			logs = True
		)
	
	# Check if profile demands a chsh
	if profile.shell != None:

		# Try changing user shell
		methods.subprocessRun(
			cmd  = ["sudo", "chsh", "-s", profile.shell, user],
			logs = True
		)
	
	# Check if profile includes flatpaks
	if profile.flatpaks != None:

		# Install flatpak
		methods.subprocessRun(
			cmd  = ["sudo", "pacman", "-S", "--noconfirm", "flatpak"],
			logs = True
		)

		# Install requested flatpaks
		methods.subprocessRun(
			cmd  = ["flatpak", "install", "-y", "-v"] + profile.flatpaks,
			logs = True
		)
	
	# Check if profile include custom commands
	if profile.bashcmd != None:
		
		methods.log("Parsing custom bash commands...", "wrn")

		# Execute such commands one by one
		for command in profile.bashcmd:
			methods.subprocessRun(cmd  = ["bash", "-c", command])