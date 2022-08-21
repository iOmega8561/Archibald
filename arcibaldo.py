#!/usr/bin/python3
import utils.configs as configs
import utils.methods as methods
import utils.formats as formats

def main():
	#Prepare greeting text
	prompt = f"{formats.msgStr} Arcibaldo utility for Arch Linux, select a profile:\n"
	
	#Format-add every profile name and target to greetings
	for i, p in enumerate(configs.profiles):
		prompt += formats.selStr.format(i + 1, p.name, p.type)
	prompt += f"{formats.bold}User input:{formats.endc} "

	#Repeat input until a valid one is given
	index = methods.integerget(prompt, f"{formats.warnStr} Input not a number, retry.") - 1
	while index < 0 or index >= len(configs.profiles):
		print(f"{formats.warnStr} Not in range, try again.")
		index = methods.integerget(prompt, f"{formats.warnStr} Input not a number, retry.") - 1

	selection = configs.profiles[index]
	print(f"{formats.msgStr} Selected profile is {selection.name} ({selection.type})")
	
	#Try to find user defined driver name inside lspci output
	print(f"{formats.warnStr} Searching for any known graphics device...")
	pcidevices = methods.subprocess_easy("lspci")
	for device in configs.drivers:
		#Repeat match for every user defined driver group
		match = [f"VGA compatible controller: {device}", f"Display controller: {device}"]
		if any(x in pcidevices.stdout.rstrip("\n") for x in match):
			#If is found, add packages to profile.pkgs
			print(f"{formats.succStr} Found {device} device!")
			selection.pkgs += configs.drivers[device]

	#Packages installation
	print(f"{formats.warnStr} Please wait while PacMan installs packages...")
	methods.pacman_install(selection.pkgs, f"{formats.succStr} Successfully installed all packages!", f"{formats.errStr} PacMan encountered errors, check pacman.log")
	
	#Config files creation
	print(f"{formats.warnStr} Deploying configuration files...")
	for i, f in enumerate(configs.files):
		methods.makefile(f.path, f.name, f.text, f"{formats.errStr} Could not open {f.path}{f.name}.")
	
	#Arcibaldo runs with root privileges, so files in home will have rw protection
	methods.subprocess_easy(["chown", "-R", f"{methods.logname()}", f"/home/{methods.logname()}"])

	#Setting user groups one by one
	print(f"{formats.warnStr} Settings user groups...")
	for i in selection.groups:
		methods.subprocess_easy(["usermod", "-aG", f"{methods.logname()}"] + i)

	#Enabling systemd units all at one (systemctl supports it)
	print(f"{formats.warnStr} Enabling systemd units...")
	methods.subprocess_easy(["systemctl", "enable"] + selection.units)

if not methods.subprocess_watch("whoami", "root", "compare"):
	#Exit if not executing with sudo
	print(f"{formats.errStr} Arcibaldo needs {formats.uline}high{formats.endc} privileges.")
elif methods.subprocess_watch("logname", "root", "compare"):
	#Exit if logged in as the root use (/home/root does not exist)
	print(f"{formats.errStr} Executing logged as root is not supported.")
elif not methods.subprocess_watch(["cat", "/etc/os-release"], "Arch Linux", "find"):
	#Exit if system is not Arch Linux (pacman is used)
	print(f"{formats.errStr} This is not Arch Linux.")
else:
	#Run main logic
	main()
