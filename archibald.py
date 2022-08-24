#!/usr/bin/python3
from utilities import formats, classes, methods
from config import dicts, defaults

def processAskZram(ramsize: str = "ram / 2"):

	# Prompt user to let Archibald configure swap on zram
	print(f"{formats.msgStr} Would you like Archibald to enable swap on zram? (Yes/No)")
	feedback = input(f"{formats.bold}User input:{formats.endc} ")

	if any(x in feedback for x in ["Y", "y", "Yes", "yes"]):
		
		# Try to install zram-generator
		methods.subprocessEz(command = ["pacman", "-Sy", "--noconfirm", "zram-generator"],
			errStr = f"{formats.errStr} Unexpected error installing zram-generator.")
		
		# Write zram config to /etc/systemd
		file = methods.makefile("/etc/systemd", "zram-generator.conf", 
			f"{formats.errStr} Could not open /etc/systemd/zram-generator.conf.")
		file.write(f"[zram0]\nzram-size = {ramsize}")

		# Reload units
		methods.subprocessEz(command = ["systemctl", "daemon-reload"])
	else:

		# Just skip zram
		return 


def processAskAur(logname: str):

	# Prompt user to let Archibald install paru
	print(f"{formats.msgStr} Would you like Archibald to enable AUR? (Yes/No)")
	feedback = input(f"{formats.bold}User input:{formats.endc} ")
	if any(x in feedback for x in ["Y", "y", "Yes", "yes"]):

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
			errStr = f"{formats.errStr} Could not install paru, check logs.")
		
		# Try to remove leftover trash
		methods.subprocessEz(command = ["rm", "-fr", "paru"], cwd = f"/home/{logname}")
	else:

		# Just skip AUR
		return

def processProfile(selection: classes.profile , logname: str):

	# Prompt user his choice again
	print(f"{formats.msgStr} Selected profile is {selection.name} ({selection.type})")
	
	# Check if profile demands video drivers
	if selection.drivers != False:

		# Try to find known graphics cards from lspci
		print(f"{formats.execStr} Searching for any known graphics device...")
		lspci = methods.subprocessEz(command = ["lspci"])
		for device in dicts.drivers:

			# Repeat match for every user defined driver group
			match = [f"VGA compatible controller: {device}", f"Display controller: {device}"]
			if any(x in lspci.stdout for x in match):

				# If is found, add packages to profile.pkgs
				print(f"{formats.succStr} Found {device} device!")
				selection.pkgs += dicts.drivers[device]

	# Call pacman -Sy, if pkgs = [] just update databases
	print(f"{formats.execStr} Please wait while PacMan installs packages...")
	methods.subprocessEz(command = ["pacman", "-Sy", "--needed", "--noconfirm"] + selection.pkgs,
		filespecs = ["logs", "pacman.log"], 
		succStr = f"{formats.succStr} Successfully installed all packages!", 
		errStr = f"{formats.errStr} PacMan encountered errors, check logs")

	if selection.files != None:

		# Config files creation
		print(f"{formats.execStr} Deploying configuration files...")
		for i, f in enumerate(selection.files):
			file = methods.makefile(f.path, f.name, 
				f"{formats.errStr} Could not open {f.path}{f.name}.")
			file.write(f.text)
	
		# Archibald runs as root, home located files will be owned by root, let's fix that
		methods.subprocessEz(command = ["chown", "-R", logname, f"/home/{logname}"])

	if selection.groups != None:

		# Setting user groups one by one
		print(f"{formats.execStr} Settings user groups...")
		for i in selection.groups:
			methods.subprocessEz(command = ["usermod", "-aG", i, logname])

	# Check if profile demands systemd enable
	if selection.units != None:

		# Try enable all at once
		print(f"{formats.execStr} Enabling systemd units...")
		methods.subprocessEz(command = ["systemctl", "enable"] + selection.units,
			filespecs = ["logs", "systemctl.log"],
			errStr = f"{formats.errStr} Systemctl encountered errors, check logs")
	
	# Check if profile demands a chsh
	if selection.shell != None:

		# Try changing user shell
		print(f"{formats.execStr} Changing user shell to {selection.shell}...")
		methods.subprocessEz(command = ["chsh", "-s", selection.shell, logname],
			errStr = f"{formats.errStr} Error changing user shell to {selection.shell}.")

def main():

	# First checks to ensure everything's good
	if not methods.watchStdout(["whoami"], "root", 0):

		# Exit if not executing with sudo
		print(f"{formats.errStr} Archibald needs {formats.uline}high{formats.endc} privileges.")

	elif not methods.watchStdout(["cat", "/etc/os-release"], "Arch Linux", 1):

		# Exit if system is not Arch Linux (pacman is necessary)
		print(f"{formats.errStr} This is not Arch Linux.")

	# Use method to get clean output of logname command
	logname = methods.justLogname()
	
	if logname == "root":

		# Exit if logged in as the root use (/home/root does not exist)
		print(f"{formats.errStr} Executing logged as root is not supported.")
		quit()
	
	print(f"{formats.msgStr} Welcome to Archibald, your Arch configuration helper.")

	# Prepare selection text
	prompt = f"{formats.msgStr} Please select one the following profiles:\n"
	
	# Format-add every profile name and target to greetings
	for i, p in enumerate(defaults.profiles):
		prompt += formats.selStr.format(i + 1, p.name, p.type)
	prompt += f"{formats.bold}User input:{formats.endc} "

	try:

		# Print prompt text and get user input, must be integer
		index = methods.integerget(prompt, f"{formats.execStr} Input not a number, retry.")
		while index <= 0 or index > len(defaults.profiles):

			# Repeat input until a valid one is given
			print(f"{formats.execStr} Not in range, try again.")
			index = methods.integerget(prompt, f"{formats.execStr} Input not a number, retry.")

		processProfile(defaults.profiles[index - 1], logname)
		processAskZram(ramsize = "ram / 2")
		processAskAur(logname)

		# Conclusion
		print(f"{formats.succStr} Archibald has finished, please reboot!")

	except KeyboardInterrupt:

		# Just quit if interrupted
		print(f"\n{formats.warnStr} Detected keyboard interrupt, Archibald will terminate")
		quit()

if __name__ == "__main__":
	main()