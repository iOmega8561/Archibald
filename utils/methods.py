import subprocess, os

def logname():
	proc = subprocess_easy("logname")
	return proc.stdout.rstrip("\n")

def integerget(prompt, errStr = None):
	while True:
		try:
			i = int(input(prompt))
			return i
		except ValueError:
			if errStr != None:
				print(errStr)

def makefile(path, name, text, errStr = None):
	try:
		os.makedirs(path, exist_ok=True)
		with open(f"{path}/{name}", "w") as file:
			file.write(text)
	except IOError or OSError:
		if errStr != None:
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

def subprocess_try(command, file = None, succStr = None, errStr = None):
	try:
		proc = subprocess_easy(command, file)
		if succStr != None:
			print(succStr)
		return proc
	except subprocess.CalledProcessError:
		if errStr != None:
			print(errStr)
		quit()

def subprocess_watch(command, match, mode):
	proc = subprocess_try(command)
	clean = proc.stdout.rstrip("\n")
	
	if mode == "all" and all(x in clean for x in match):
		return True
	elif mode == "any" and any(x in clean for x in match):
		return True
	
	return False
