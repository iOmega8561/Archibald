class pClass:
	def __init__(self, name: str, type: str, drivers: dict = None, pkgs: list = [], aur: bool = False, units: list = None, groups: list = None, files: list = None, shell: str = None, flatpaks: list = None, bashcmd: list = None):
		self.name 	  = name
		self.type 	  = type
		self.drivers  = drivers
		self.pkgs 	  = pkgs
		self.aur	  = aur
		self.units 	  = units
		self.groups   = groups
		self.files 	  = files
		self.shell 	  = shell
		self.flatpaks = flatpaks
		self.bashcmd  = bashcmd

class fClass:
	def __init__(self, name: str, path: str, text: str):
		self.name = name
		self.path = path
		self.text = text

pList = []

def pAdd(profile: pClass):
    pList += profile

import profiles.gnome
import profiles.plasma
import profiles.cockpit
import profiles.custom