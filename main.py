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
	print(f"{formats.msgStr} Selected profile is {selection.name} ({selection.type})\n")
	
	if methods.subprocess_watch("lspci", ["VGA?NVIDIA", "Display controller?NVIDIA"], "find"):
		print(f"{format.succStr} Found Nvidia graphics controller/VGA!")
	
	print(f"{formats.msgStr} Using PacMan to setup your profile...")
	print(f"{formats.warnStr} PacMan will log itself to pacman.log")
	
	methods.pacman_install(selection.pkgs, f"{formats.errStr} PacMan encountered errors, check pacman.log")

if not methods.subprocess_watch("whoami", "root", "compare"):
	print(f"{formats.errStr} Arcibaldo needs {formats.uline}high{formats.endc} privileges.")
elif methods.subprocess_watch("logname", "root", "compare"):
	print(f"{formats.errStr} Executing logged as root is not supported.")
elif not methods.subprocess_watch(["cat", "/etc/os-release"], "Arch Linux", "find"):
	print(f"{formats.errStr} This is not Arch Linux.")
else:
	main()
