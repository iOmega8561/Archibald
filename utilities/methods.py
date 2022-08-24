import subprocess, os

def justLogname():

	process = subprocess.run("logname",
			stdout = subprocess.PIPE,
			text = True)
	return process.stdout.rstrip("\n")

def integerget(prompt: str, errStr: str = None):

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
			if errStr != None:
				print(errStr)

def makefile(path: str, name: str, errStr: str = None):
	try:
		
		# Make parent folders if non existent
		os.makedirs(path, exist_ok=True)

		file = open(f"{path}/{name}", "w")
		return file

	# Except errors that could occur
	except IOError or OSError:
		
		# Print error string if given
		if errStr != None:
			print(errStr)
		
		# Then raise
		raise

def watchStdout(command: list, match: list, mode: int):

	# First get a process object, then clean stdout
	process = subprocessEz(command)
	cleanStdout = process.stdout.rstrip("\n")
	
	# Check wich comparison "mode" to use
	if mode == 0 and all(x in cleanStdout for x in match):

		# Return true if stdout is equal to match
		return True

	elif mode == 1 and any(x in cleanStdout for x in match):

		# Return true if math is contained in stdout
		return True

def subprocessEz(command: list, user: str = None, filespecs: list = None, cwd: str = None, succStr: str = None, errStr: str = None):

	# Check if user has been passed
	if user != None:

		# If yes, then add runuser first to cmd
		command = ["runuser", "-u", user, "--"] + command

	# Check if filespecs meets requirements
	if filespecs == None or len(filespecs) != 2:

		# Output will be redirected on subprocess.PIPE
		redirect = subprocess.PIPE

	else:
		
		# Output will be redirected on file
		redirect = makefile(filespecs[0], filespecs[1], errStr)
	
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
		if succStr != None:
			print(succStr)

		# Always return process object
		return process

	# Except error if occurs
	except subprocess.CalledProcessError:

		# Print error if given
		if errStr != None:
			print(errStr)
		
		# Then raise
		raise