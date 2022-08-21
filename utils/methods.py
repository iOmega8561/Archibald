import subprocess, os

def logname():
	proc = subprocess_easy("logname")
	return proc.stdout.rstrip("\n")

def integerget(prompt, errStr):
	while True:
		try:
			i = int(input(prompt))
			return i
		except ValueError:
			print(errStr)

def makefile(path, name, text, errStr):
	try:
		os.makedirs(path, exist_ok=True)
		with open(f"{path}/{name}", "w") as file:
			file.write(text)
	except IOError or OSError:
		print(errStr)
		quit()

def subprocess_easy(command, filename = None):
	if filename != None:
		file = open(filename, "w")
		proc = subprocess.run(command,
			stdout = file,
			stderr = subprocess.STDOUT,
			check = True,
			text = True)
	else:
		proc = subprocess.run(command,
			stdout = subprocess.PIPE,
			stderr = subprocess.STDOUT,
			check = True,
			text = True)
	return proc

def subprocess_watch(command, match, mode):
	proc = subprocess_easy(command)
	clean = proc.stdout.rstrip("\n")
	
	if mode == "compare" and all(x in clean for x in match):
		return True
	elif mode == "find" and any(x in clean for x in match):
		return True
	else:
		return False

def pacman_install(packages, succStr, errStr = None):
	try:
		proc = subprocess_easy(["pacman", "-S", "--needed", "--noconfirm", "--quiet"] + packages, "pacman.log")
		print(succStr)
	except subprocess.CalledProcessError:
		print(errStr)
		quit()
