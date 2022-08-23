#!/usr/bin/python3
import utilities.configs as configs
import utilities.methods as methods
import utilities.formats as formats

def main(logname):
	# Prepare greeting text
	prompt = f"{formats.msgStr} Please select one the following profiles:\n"
	
	# Format-add every profile name and target to greetings
	for i, p in enumerate(configs.profiles):
		prompt += formats.selStr.format(i + 1, p.name, p.type)
	prompt += f"{formats.bold}User input:{formats.endc} "

	# Print prompt text and get user imput, must be integer
	try:
		index = methods.integerget(prompt, f"{formats.execStr} Input not a number, retry.") - 1
		while index < 0 or index >= len(configs.profiles):

			# Repeat input until a valid one is given
			print(f"{formats.execStr} Not in range, try again.")
			index = methods.integerget(prompt, f"{formats.execStr} Input not a number, retry.") - 1
	except KeyboardInterrupt:
		print(f"\n{formats.warnStr} Detected keyboard interrupt, Archibald will terminate")
		quit()

	# When success, save chosen profile inside selection and prompt user his choice again
	selection = configs.profiles[index]
	print(f"{formats.msgStr} Selected profile is {selection.name} ({selection.type})")
	
	# Try to find user defined driver name inside lspci output
	print(f"{formats.execStr} Searching for any known graphics device...")
	lspci = methods.subprocessEz(command = ["lspci"])
	for device in configs.drivers:

		# Repeat match for every user defined driver group
		match = [f"VGA compatible controller: {device}", f"Display controller: {device}"]
		if any(x in lspci.stdout.rstrip("\n") for x in match):

			# If is found, add packages to profile.pkgs
			print(f"{formats.succStr} Found {device} device!")
			selection.pkgs += configs.drivers[device]

	# Packages installation via pacman subprocess
	print(f"{formats.execStr} Please wait while PacMan installs packages...")
	methods.subprocessEz(command = ["pacman", "-S", "--needed", "--noconfirm"] + selection.pkgs,
		filespecs = ["logs", "pacman.log"], 
		succStr = f"{formats.succStr} Successfully installed all packages!", 
		errStr = f"{formats.errStr} PacMan encountered errors, check logs")
	
	# Config files creation
	print(f"{formats.execStr} Deploying configuration files...")
	for i, f in enumerate(selection.files):
		file = methods.makefile(f.path, f.name, f"{formats.errStr} Could not open {f.path}{f.name}.")
		file.write(f.text)
	
	# Archibald runs with root privileges, so files in home will have rw protection
	methods.subprocessEz(command = ["chown", "-R", f"{logname}", f"/home/{logname}"])

	# Setting user groups one by one
	print(f"{formats.execStr} Settings user groups...")
	for i in selection.groups:
		methods.subprocessEz(command = ["usermod", "-aG", f"{logname}"] + i)

	# Enabling systemd units all at one (systemctl supports multiple arguments)
	print(f"{formats.execStr} Enabling systemd units...")
	methods.subprocessEz(command = ["systemctl", "enable"] + selection.units,
		filespecs = ["logs", "systemctl.log"], 
		succStr = f"{formats.succStr} Successfully enabled systemd units!", 
		errStr = f"{formats.errStr} Systemctl encountered errors, check logs")
	
	# Check if profile demands a chsh
	if selection.shell != None:

		# Try changing user shell
		print(f"{formats.execStr} Changing user shell to {selection.shell}...")
		methods.subprocessEz(command = ["chsh", "-s", f"{selection.shell}", f"{logname}"],
			filespecs = ["logs", "chsh.log"], 
			errStr = f"{formats.errStr} Error changing user shell to {selection.shell}.")

	# Conclusion
	print(f"{formats.succStr} Archibald has finished, please reboot!")


# First checks to ensure everything's good
if not methods.watchStdout(["whoami"], "root", 0):

	# Exit if not executing with sudo
	print(f"{formats.errStr} Archibald needs {formats.uline}high{formats.endc} privileges.")

elif not methods.watchStdout(["cat", "/etc/os-release"], "Arch Linux", 1):

	# Exit if system is not Arch Linux (pacman is necessary)
	print(f"{formats.errStr} This is not Arch Linux.")

else:

	# Use method to get clean output of logname command
	logname = methods.justLogname()
	
	if logname == "root":

		# Exit if logged in as the root use (/home/root does not exist)
		print(f"{formats.errStr} Executing logged as root is not supported.")
		quit()
	
	print(f"{formats.msgStr} Welcome to Archibald, your Arch configuration helper.")
	# Run main logic
	main(logname)
