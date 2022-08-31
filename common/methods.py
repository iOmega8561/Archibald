import subprocess, os

global username

def log(text: str, type: str = "msg"):

	logtypes = {

		"msg": "\033[1mMessage:\033[0m {text}",
		"err": "\033[91mError:\033[0m {text}",
		"wrn": "\033[91mWarning:\033[0m {text}",
		"exc": "\033[93mExecuting:\033[0m {text}",
		"suc": "\033[92mSuccess:\033[0m {text}",
		"nof": "{text}"

	}

	if type in logtypes:
		print(logtypes[type].format(text = text))

	else:
		log("Invalid log type.", "err")

def intGet(prompt: str):

	# Repeat until a valid input is given
	while True:
		try:

			# Take raw input and convert to int
			i = int(input(prompt))

			# Return if all's good
			return i

		# Except value error if raw is not base 10
		except ValueError:

			# Print error but NOT raise
			log("Input not a number, retry.", "wrn")

def linuxFile(path: str, name: str, text: str):
	
	cmd = []

	# Check {home} placeholder presence
	if "{home}" in path:

		# Format with $HOME and log without sudo
		path  = path.format(home = os.environ.get("HOME"))

	else:
		
		# Add sudo to cmd and log with sudo
		cmd   = ["sudo"]

	# Make parent folders if non existent
	subprocessRun(cmd + ["mkdir", "-p", path])

	# Run Popen to get stdin attached
	tee = subprocess.Popen(
		cmd    + ["tee", f"{path}/{name}"], 
		stdin  = subprocess.PIPE, 
		stdout = subprocess.DEVNULL,
    	stderr = subprocess.STDOUT
	)

	# Write to stdin and close pipe
	tee.stdin.write(str.encode(text))
	tee.stdin.close()

def subprocessRun(cmd: list, logs: bool = False, cwd: str = None, succ: str = None, err: str = None):
	stdout = subprocess.PIPE

	# Check if logfile is required
	if logs:

		# Display execution log
		log(" ".join(map(str, cmd[0:5])), "exc")

		# Output will be redirected on logfile
		stdout = open("archibald.log", "a")

	# Check if Working Dir has been passed
	if cwd == None:

		# If not, use current dir
		cwd = os.getcwd()

	try:

		# Call subprocess.run with requested cmd
		process = subprocess.run(
			cmd,
			stdout = stdout,
			stderr = subprocess.STDOUT,
			cwd    = cwd,
			check  = True,
			text   = True
		)

		# Print success if present
		if succ != None:
			log(succ, "suc")

		# Always return process object
		return process

	# Except error if occurs
	except subprocess.CalledProcessError:

		# Print error if given
		if err != None:
			log(err, "err")
		
		# Then raise
		raise

	except FileNotFoundError:

		# File not found error
		log("Executable not found.", "err")

		# Then raise
		raise

if __name__ == "common.methods":

	# Get whoami output when imported
	whoami = subprocess.run(
		["whoami"],
		stdout = subprocess.PIPE,
		text   = True
	)

	# Tranfsorm to single line
	username = whoami.stdout.rstrip("\n")