class profile:
	def __init__(self, name: str, type: str, drivers: bool = False, pkgs: list = [], units: list = None, groups: list = None, shell: str = None, flatpaks: list = None, bashcmd: list = None, files: list = None, aur: bool = False):
		self.name 	  = name
		self.type 	  = type
		self.drivers  = drivers
		self.pkgs 	  = pkgs
		self.units 	  = units
		self.groups   = groups
		self.files 	  = files
		self.shell 	  = shell
		self.flatpaks = flatpaks
		self.bashcmd  = bashcmd
		self.aur	  = aur

class file:
	def __init__(self, name: str, path: str, text: str):
		self.name = name
		self.path = path
		self.text = text

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