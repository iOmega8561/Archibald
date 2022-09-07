#!/usr/bin/python3
from lib import console, linux, setup
from profiles import profiles_strap

def main():

	# Ensure this is running on Arch Linux
	with open("/etc/os-release", "r") as release:

		if not "Arch Linux" in release.read():

			# Exit if system is not Arch Linux
			console.log("This is not Arch Linux.", "err")
			exit(1)
	
	username, p_dict, index = linux.whoami(), profiles_strap(), 1

	console.log(f"Welcome {username}, select a profile:")
	
	for P in p_dict:
		console.log(f"{index}) {p_dict[P].name}", "nof")
		index += 1

	try:

		# intGet makes sure this is an integer input
		input = console.intGet(f"Answer: ")
		while input <= 0 or input > len(p_dict):

			# Repeat input until a valid answer is given
			console.log("Number out of range, try again.", "wrn")
			input = console.intGet(f"Answer: ")

		# Configure selected profile
		setup.resolve(p_dict, input-1, username)

		# Conclusion
		console.log("All operations completed, please reboot!", "suc")

	except KeyboardInterrupt:

		# Just quit if ctrl+c
		console.log("Detected keyboard interrupt, terminating.", "wrn")
		exit(1)

if __name__ == "__main__":
	main()