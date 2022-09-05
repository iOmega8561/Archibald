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