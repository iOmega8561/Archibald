class profile:
	def __init__(self, name: str, type: str, pkgs: list = [], units: list = [], groups: list = [], shell: str = None, files: list = []):
		self.name = name
		self.type = type
		self.pkgs = pkgs
		self.units = units
		self.groups = groups
		self.shell = shell
		self.files = files

class file:
	def __init__(self, name: str, path: str, text: str):
		self.name = name
		self.path = path
		self.text = text
