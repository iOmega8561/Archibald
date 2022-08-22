class profile:
	def __init__(self, name, type, pkgs, units, groups, shell):
		self.name = name
		self.type = type
		self.pkgs = pkgs
		self.units = units
		self.groups = groups
		self.shell = shell

class file:
	def __init__(self, name, path, text):
		self.name = name
		self.path = path
		self.text = text
