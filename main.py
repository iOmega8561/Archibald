#!/usr/bin/python3
from common import formats, methods
from config import profiles

import setup

def main():

	# Check high privileges
	whoami = methods.subprocessEz(["whoami"])
	privileges = whoami.stdout.rstrip("\n")

	if privileges != "root":

		# Exit if not executing with sudo
		print(f"{formats.errStr} Archibald needs {formats.uline}high{formats.endc} privileges.")
		exit(1)

	# Ensure this is running on Arch Linux
	cat = methods.subprocessEz(["cat", "/etc/os-release"])
	release = cat.stdout

	if not "Arch Linux" in release:

		# Exit if system is not Arch Linux (pacman is necessary)
		print(f"{formats.errStr} This is not Arch Linux.")
		exit(1)

	# Ensure logged user is not root
	logname = methods.subprocessEz(["logname"])
	user = logname.stdout.rstrip("\n")

	if user == "root":

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
		setup.profile(profiles.list[answer - 1], user)

		##############################################################################

		# Ask for zram
		print(f"{formats.msgStr} Would you like Archibald to configure Zram? (Yes/No)")
		answer = input(f"{formats.bold}User input:{formats.endc} ")

		if any(x in answer for x in ["Y", "y", "Yes", "yes"]):
			setup.zram()

		###############################################################################

		# Ask for aur helper
		print(f"{formats.msgStr} Would you like Archibald to install an AUR helper? (Yes/No)")
		answer = input(f"{formats.bold}User input:{formats.endc} ")

		if any(x in answer for x in ["Y", "y", "Yes", "yes"]):
			setup.aur(user)

		# Conclusion
		print(f"{formats.succStr} Archibald has finished, please reboot!")

	except KeyboardInterrupt:

		# Just quit if ctrl+c
		print(f"\n{formats.warnStr} Detected keyboard interrupt, Archibald will terminate")
		exit(1)

if __name__ == "__main__":
	main()