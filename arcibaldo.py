#!/usr/bin/python3
import utils.configs as configs
import utils.methods as methods
import utils.formats as formats

def main():
	prompt = f"{formats.msgStr} Arcibaldo welcomes you, select a profile:\n"
	
	for i, p in enumerate(configs.profiles):
		prompt += formats.selStr.format(i + 1, p.name, p.type)
	prompt += f"{formats.bold}User input:{formats.endc} "

	index = methods.integer_get(prompt, f"{formats.warnStr} Input not a number, retry.") - 1
	while index < 0 or index >= len(configs.profiles):
		print(f"{formats.warnStr} Not in range, try again.")
		index = methods.integer_get(prompt, f"{formats.warnStr} Input not a number, retry.") - 1

	selection = configs.profiles[index]
	print(f"{formats.msgStr} Selected profile is {selection.name} ({selection.type})")
	
	print(f"{formats.warnStr} Searching for any known graphics device...")
	pcidevices = methods.subprocess_easy("lspci")
	for device in configs.drivers:
		match = [f"VGA compatible controller: {device}", f"Display controller: {device}"]
		if any(x in pcidevices.stdout.rstrip("\n") for x in match):
			print(f"{formats.succStr} Found {device} device!")
			selection.pkgs += configs.drivers[device]

	print(f"{formats.warnStr} Please wait while PacMan installs packages...")
	methods.pacman_install(selection.pkgs,
		f"{formats.succStr} Successfully installed all packages!",
		f"{formats.errStr} PacMan encountered errors, check pacman.log")
	
	print(f"{formats.warnStr} Deploying configuration files...")
	for i, f in enumerate(configs.files):
		try:
			print(f"{f.path}/{f.name}")
			file = open(f"{f.path}/{f.name}", "w")
			file.write(f.text)
		except IOError:
			print(f"{formats.errStr} Could not open {f.path}{f.name}, exiting...")
			quit()

if not methods.subprocess_watch("whoami", "root", "compare"):
	print(f"{formats.errStr} Arcibaldo needs {formats.uline}high{formats.endc} privileges.")
elif methods.subprocess_watch("logname", "root", "compare"):
	print(f"{formats.errStr} Executing logged as root is not supported.")
elif not methods.subprocess_watch(["cat", "/etc/os-release"], "Arch Linux", "find"):
	print(f"{formats.errStr} This is not Arch Linux.")
else:
	main()
