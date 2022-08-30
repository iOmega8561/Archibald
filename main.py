#!/usr/bin/python3
from common import methods, setups
from userconf import profiles

def main():

	# Check sudo privileges
	whoami = methods.subprocessEz(["whoami"])
	privileges = whoami.stdout.rstrip("\n")

	if privileges != "root":

		# Exit if not executing with sudo
		methods.log("Archibald needs high privileges.", "err")
		exit(1)

	# Ensure this is running on Arch Linux
	cat = methods.subprocessEz(["cat", "/etc/os-release"])
	release = cat.stdout

	if not "Arch Linux" in release:

		# Exit if system is not Arch Linux (pacman is necessary)
		methods.log("This is not Arch Linux.", "err")
		exit(1)

	# Ensure logged user is not root
	logname = methods.subprocessEz(["logname"])
	user = logname.stdout.rstrip("\n")

	if user == "root":

		# Exit if logged in as the root use (/home/root does not exist)
		methods.log("Executing logged as root is not supported.", "err")
		exit(1)
	
	methods.log("Welcome to Archibald, select a profile:")
	
	# Build selection text
	selection = "(Press CTRL+C to exit)\n"
	for i, p in enumerate(profiles.list):
		selection += f"{i+1}) {p.name} | Profile target: {p.type}\n"

	try:

		# Integerget makes sure this is an integer input
		answer = methods.integerget(f"{selection}Answer: ", "Input not a number, retry.")
		while answer <= 0 or answer > len(profiles.list):

			# Repeat input until a valid answer is given
			methods.log("Number out of range, try again.", "wrn")
			answer = methods.integerget(f"{selection}Answer: ", "Input not a number, retry.")

		# Configure selected profile
		setups.profile(profiles.list[answer - 1], user)

		##############################################################################

		# Ask for zram
		methods.log("Would you like to configure Zram?")
		answer = input("Answer: ")

		if any(x in answer for x in ["Y", "y", "Yes", "yes"]):
			setups.zram()

		###############################################################################

		# Ask for aur helper
		methods.log("Would you like to install an AUR helper?")
		answer = input("Answer: ")

		if any(x in answer for x in ["Y", "y", "Yes", "yes"]):
			setups.aur(user)

		# Conclusion
		methods.log("All operations completed, please reboot!", "suc")

	except KeyboardInterrupt:

		# Just quit if ctrl+c
		methods.log("Detected keyboard interrupt, terminating.", "wrn")
		exit(1)

if __name__ == "__main__":
	main()