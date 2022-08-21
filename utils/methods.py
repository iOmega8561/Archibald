import subprocess

def logname():
	proc = subprocess_easy("logname")
	return proc.stdout.rstrip("\n")

def integer_get(prompt, errStr):
	while True:
		try:
			i = int(input(prompt))
			return i
		except ValueError:
			print(errStr)

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
