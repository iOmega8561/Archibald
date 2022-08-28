#!/usr/bin/python3
from common import formats, datastores, methods
from config import packages, profiles

def main():

	# First checks to ensure everything's good
	if not methods.watchStdout(["whoami"], "root", 0):

		# Exit if not executing with sudo
		print(f"{formats.errStr} Archibald needs {formats.uline}high{formats.endc} privileges.")
		exit(1)

	elif not methods.watchStdout(["cat", "/etc/os-release"], "Arch Linux", 1):

		# Exit if system is not Arch Linux (pacman is necessary)
		print(f"{formats.errStr} This is not Arch Linux.")
		exit(1)

	# Use method to get clean output of logname command
	logname = methods.logname()
	
	if logname == "root":

		# Exit if logged in as the root use (/home/root does not exist)
		print(f"{formats.errStr} Executing logged as root is not supported.")
		exit(1)
	
	print(f"{formats.msgStr} Welcome to Archibald, your Arch configuration helper.")

	# Prepare selection text
	selection = f"{formats.msgStr} Please select one the following profiles:\n"
	
	# Format-add every profile name and target to greetings
	for i, p in enumerate(profiles.list):
		selection += formats.selStr.format(i + 1, p.name, p.type)
	selection += f"{formats.bold}User input:{formats.endc} "

	try:

		# Print prompt text and get user input, must be integer
		answer = methods.integerget(selection, f"{formats.execStr} Input not a number, retry.")
		while answer <= 0 or answer > len(profiles.list):

			# Repeat input until a valid answer is given
			print(f"{formats.execStr} Not in range, try again.")
			answer = methods.integerget(selection, f"{formats.execStr} Input not a number, retry.")

		# Configure selected profile
		profileSetup(profiles.list[answer - 1], logname)

		##############################################################################

		# Ask for zram
		print(f"{formats.msgStr} Would you like Archibald to configure Zram? (Yes/No)")
		answer = input(f"{formats.bold}User input:{formats.endc} ")

		if any(x in answer for x in ["Y", "y", "Yes", "yes"]):
			zramSetup()

		###############################################################################

		# Ask for aur helper
		print(f"{formats.msgStr} Would you like Archibald to install an AUR helper? (Yes/No)")
		answer = input(f"{formats.bold}User input:{formats.endc} ")

		if any(x in answer for x in ["Y", "y", "Yes", "yes"]):
			aurSetup(logname)

		# Conclusion
		print(f"{formats.succStr} Archibald has finished, please reboot!")

	except KeyboardInterrupt:

		# Just quit if ctrl+c
		print(f"\n{formats.warnStr} Detected keyboard interrupt, Archibald will terminate")
		exit(1)

if __name__ == "__main__":
	main()




































def zramSetup(ramsize: str = "ram / 2"):
	
	# Try to install zram-generator
	methods.subprocessEz(command = ["pacman", "-S", "--noconfirm", "zram-generator"],
		errStr = f"{formats.errStr} Unexpected error installing zram-generator.")
		
	# Write zram config to /etc/systemd
	file = methods.makefile("/etc/systemd", "zram-generator.conf", 
		f"{formats.errStr} Could not open /etc/systemd/zram-generator.conf.")
	file.write(f"[zram0]\nzram-size = {ramsize}")

	# Reload units
	methods.subprocessEz(command = ["systemctl", "daemon-reload"])

def aurSetup(logname: str):

	# Try to remove pre-existent trash
	methods.subprocessEz(command = ["rm", "-fr", "paru"], cwd = f"/home/{logname}")

	# Try git clone paru repository
	print(f"{formats.execStr} Performing git clone https://aur.archlinux.org/paru as {logname}...")
	methods.subprocessEz(command = ["git", "clone", "https://aur.archlinux.org/paru"],
		user = logname,
		cwd = f"/home/{logname}",
		errStr = f"{formats.errStr} Git encountered an unexpected error.")

	# Try to install dependencies, compile and install paru
	print(f"{formats.execStr} Performing makepkg -si as {logname}, expect sudo prompts...")
	methods.subprocessEz(command = ["makepkg", "-si", "--noconfirm", "--needed"],
		user = logname,
		filespecs = ["logs", "makepkg.log"],
		cwd = f"/home/{logname}/paru",
		errStr = f"{formats.errStr} Could not install paru, check log files.")
		
	# Try to remove leftover trash
	methods.subprocessEz(command = ["rm", "-fr", "paru"], cwd = f"/home/{logname}")

def profileSetup(profile: datastores.profile , logname: str):

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
			file = methods.makefile(f.path.format(home = f"/home/{logname}"), f.name, 
				f"{formats.errStr} Could not open {f.path}{f.name}.")
			file.write(f.text)
	
		# Archibald runs as root, home located files will be owned by root, let's fix that
		methods.subprocessEz(command = ["chown", "-R", logname, f"/home/{logname}"])

	if profile.groups != None:

		# Setting user groups one by one
		print(f"{formats.execStr} Settings user groups...")
		for i in profile.groups:
			methods.subprocessEz(command = ["usermod", "-aG", i, logname])

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
		methods.subprocessEz(command = ["chsh", "-s", profile.shell, logname],
			errStr = f"{formats.errStr} Unexpected error changing shell to {profile.shell}.")
