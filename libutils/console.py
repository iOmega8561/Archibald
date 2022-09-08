__formats = {

	"msg": "\033[1mMessage:\033[0m {text}",
	"err": "\033[91mError:\033[0m {text}",
	"wrn": "\033[91mWarning:\033[0m {text}",
	"exc": "\033[93mExeclog:\033[0m {text}",
	"suc": "\033[92mSuccess:\033[0m {text}",
	"nof": "{text}"

}

class NotALogLevel(Exception):
	pass

class ValueOutOfRange(Exception):
	pass

def log(text: str, level: str = "msg"):

	if level in __formats:
		print(__formats[level].format(text = text))
	else:
		raise NotALogLevel("Invalid log level")

def intGet(low: int = None, high: int = None, prompt: str = None):

	# Repeat until a valid input is given
	while True:
		try:

			# Take raw input and convert to int
			i = int(input(prompt if prompt else ""))

			if (low and i < low) or (high and i > high):
				raise ValueOutOfRange

			# Return if all's good
			return i

		# Except value error if raw is not base 10
		except ValueError:

			# Print error and continue
			log("Input not a number, try again.", "wrn")
		
		# Except out of range if not in given range
		except ValueOutOfRange:
			
			# Print error and continue
			log("Input out of range, try again.", "wrn")