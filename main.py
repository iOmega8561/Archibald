#!/usr/bin/python3
from common import methods, setups
from userconf import profiles

from os import getlogin

def main():

	# Ensure this is running on Arch Linux
	with open("/etc/os-release", "r") as release:

		if not "Arch Linux" in release.read():

			# Exit if system is not Arch Linux (pacman is necessary)
			methods.log("This is not Arch Linux.", "err")
			exit(1)

	methods.log("Welcome to Archibald, select a profile:")
	
	# Build selection text
	selection = "(Press CTRL+C anytime to exit)\n"
	for i, p in enumerate(profiles.list):
		selection += f"{i+1}) {p.name} | Profile target: {p.type}\n"

	try:

		# intGet makes sure this is an integer input
		answer = methods.intGet(f"{selection}Answer: ")
		while answer <= 0 or answer > len(profiles.list):

			# Repeat input until a valid answer is given
			methods.log("Number out of range, try again.", "wrn")
			answer = methods.intGet(f"{selection}Answer: ", "Input not a number, retry.")

		# Configure selected profile
		setups.profile(profiles.list[answer - 1], getlogin())

		##############################################################################

		# Ask for zram
		methods.log("Do you wish to configure Zram?")
		answer = input("Answer: ")

		if any(x in answer for x in ["Y", "y", "Yes", "yes"]):

			methods.log("Enter desired zram size (0 for default).")
			answer = methods.intGet("Answer (MB): ")

			setups.zram(ram = answer)

		###############################################################################

		# Ask for aur helper
		methods.log("Do you wish to install an AUR helper?")
		answer = input("Answer: ")

		if any(x in answer for x in ["Y", "y", "Yes", "yes"]):
			setups.aur(getlogin())

		# Conclusion
		methods.log("All operations completed, please reboot!", "suc")

	except KeyboardInterrupt:

		# Just quit if ctrl+c
		methods.log("Detected keyboard interrupt, terminating.", "wrn")
		exit(1)

if __name__ == "__main__":
	main()