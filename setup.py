from common import formats, datastores, methods
from config import packages

def zram(ramsize: str = "ram / 2"):
	
	# Try to install zram-generator
	methods.subprocessEz(command = ["pacman", "-S", "--noconfirm", "zram-generator"],
		errStr = f"{formats.errStr} Unexpected error installing zram-generator.")
		
	# Write zram config to /etc/systemd
	file = methods.makefile("/etc/systemd", "zram-generator.conf", 
		f"{formats.errStr} Could not open /etc/systemd/zram-generator.conf.")
	file.write(f"[zram0]\nzram-size = {ramsize}")

	# Reload units
	methods.subprocessEz(command = ["systemctl", "daemon-reload"])

def aur(user: str):

	# Try to remove pre-existent trash
	methods.subprocessEz(command = ["rm", "-fr", "paru"], cwd = f"/home/{user}")

	# Try git clone paru repository
	print(f"{formats.execStr} Performing git clone https://aur.archlinux.org/paru as {user}...")
	methods.subprocessEz(command = ["git", "clone", "https://aur.archlinux.org/paru"],
		user = user,
		cwd = f"/home/{user}",
		errStr = f"{formats.errStr} Git encountered an unexpected error.")

	# Try to install dependencies, compile and install paru
	print(f"{formats.execStr} Performing makepkg -si as {user}, expect sudo prompts...")
	methods.subprocessEz(command = ["makepkg", "-si", "--noconfirm", "--needed"],
		user = user,
		filespecs = ["logs", "makepkg.log"],
		cwd = f"/home/{user}/paru",
		errStr = f"{formats.errStr} Could not install paru, check log files.")
		
	# Try to remove leftover trash
	methods.subprocessEz(command = ["rm", "-fr", "paru"], cwd = f"/home/{user}")

def profile(profile: datastores.profile , user: str):

	# Check if profile demands video drivers
	if profile.drivers != False:

		# Try to find known graphics cards from lspci
		print(f"{formats.execStr} Searching for any known graphics device...")
		lspci = methods.subprocessEz(command = ["lspci"])
		for device in packages.drivers:

			# Repeat match for every user defined driver group
			match = [f"VGA compatible controller: {device}", f"Display controller: {device}"]
			if any(x in lspci.stdout for x in match):

				# If is found, add packages to profile.pkgs
				print(f"{formats.succStr} Found {device} device!")
				profile.pkgs += packages.drivers[device]

	if len(profile.pkgs) > 0:

		# Call pacman to install packages
		print(f"{formats.execStr} Please wait while Pacman installs packages...")
		methods.subprocessEz(command = ["pacman", "-S", "--needed", "--noconfirm"] + profile.pkgs,
			filespecs = ["logs", "pacman.log"], 
			succStr = f"{formats.succStr} Successfully installed all packages!", 
			errStr = f"{formats.errStr} Unexpected error, check pacman log file")

	if profile.files != None:

		# Config files creation
		print(f"{formats.execStr} Creating configuration files...")
		for i, f in enumerate(profile.files):
			file = methods.makefile(f.path.format(home = f"/home/{user}"), f.name, 
				f"{formats.errStr} Could not open {f.path}{f.name}.")
			file.write(f.text)
	
		# Archibald runs as root, home located files will be owned by root, let's fix that
		methods.subprocessEz(command = ["chown", "-R", user, f"/home/{user}"])

	if profile.groups != None:

		# Setting user groups one by one
		print(f"{formats.execStr} Settings user groups...")
		for i in profile.groups:
			methods.subprocessEz(command = ["usermod", "-aG", i, user])

	# Check if profile demands systemd enable
	if profile.units != None:

		# Try enable all at once
		print(f"{formats.execStr} Enabling system services...")
		methods.subprocessEz(command = ["systemctl", "enable"] + profile.units,
			filespecs = ["logs", "systemctl.log"],
			errStr = f"{formats.errStr} Unexpected error, check systemctl log file")
	
	# Check if profile demands a chsh
	if profile.shell != None:

		# Try changing user shell
		print(f"{formats.execStr} Changing user shell to {profile.shell}...")
		methods.subprocessEz(command = ["chsh", "-s", profile.shell, user],
			errStr = f"{formats.errStr} Unexpected error changing shell to {profile.shell}.")

if __name__ == "__main__":
	exit(1)