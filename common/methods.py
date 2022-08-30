import subprocess, os

def log(text: str, type: str = "msg"):

	types = {
		"msg": "\033[1mMessage:\033[0m {text}",
		"err": "\033[91mError:\033[0m {text}",
		"wrn": "\033[91mWarning:\033[0m {text}",
		"exc": "\033[93mExecuting:\033[0m {text}",
		"suc": "\033[92mSuccess:\033[0m {text}",
		"nof": "{text}"
	}

	if type in types:
		print(types[type].format(text = text))
	else:
		log("Invalid log type.", "err")

def integerget(prompt: str, wrnmsg: str = None):

	# Repeat until a valid input is given
	while True:
		try:

			# Take raw input and convert to int
			i = int(input(prompt))

			# Return if all's good
			return i

		# Except value error if raw is not base 10
		except ValueError:

			# Print error if given but NOT raise
			if wrnmsg != None:
				log(wrnmsg, "wrn")

def makefile(name: str, path: str):
	try:
		
		# Make parent folders if non existent
		os.makedirs(path, exist_ok=True)

		file = open(f"{path}/{name}", "w")
		return file

	# Except errors that could occur
	except IOError or OSError:

		log(f"Could not open {path}/{name}.")
		
		# Then raise
		raise

def subprocessEz(command: list, user: str = None, logfile: bool = False, cwd: str = None, succmsg: str = None, errmsg: str = None):

	log(" ".join(map(str, command[0:4])), "exc")

	# Check if logfile is required
	if logfile == False:

		# Output will be redirected on subprocess.PIPE
		redirect = subprocess.PIPE

	else:
		
		# Output will be redirected on file
		redirect = makefile(f"{command[0]}.log", "logs", errmsg)
	
	# Check if user has been passed
	if user != None:

		# If yes, then add runuser first to cmd
		command = ["runuser", "-u", user, "--"] + command

	# Check if Working Dir has been passed
	if cwd == None:

		# If not, use current dir
		cwd = os.getcwd()

	try:

		# Call subprocess.run with requested command
		process = subprocess.run(command,
			stdout = redirect,
			stderr = subprocess.STDOUT,
			cwd = cwd,
			check = True,
			text = True)

		# Print success if present
		if succmsg != None:
			log(succmsg, "suc")

		# Always return process object
		return process

	# Except error if occurs
	except subprocess.CalledProcessError:

		# Print error if given
		if errmsg != None:
			log(errmsg, "err")
		
		# Then raise
		raise

	except FileNotFoundError:

		# File not found error
		log("Executable not found.", "err")

		# Then raise
		raise