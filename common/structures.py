class profile:
	def __init__(self, name: str, type: str, drivers: bool = False, pkgs: list = [], units: list = None, groups: list = None, shell: str = None, files: list = None):
		self.name 	 = name
		self.type 	 = type
		self.drivers = drivers
		self.pkgs 	 = pkgs
		self.units 	 = units
		self.groups  = groups
		self.files 	 = files
		self.shell 	 = shell

class file:
	def __init__(self, name: str, path: str, text: str):
		self.name = name
		self.path = path
		self.text = text