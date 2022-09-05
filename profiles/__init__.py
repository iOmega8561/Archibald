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

def pAdd(profile: pClass):
	if not "pList" in globals():
		global pList 
		pList = []
	
	ln = len(pList)

	if ln == 0:
		pList.insert(ln, profile)
		return
	
	pList.insert(ln+1, profile)

import profiles.gnome
import profiles.plasma
import profiles.cockpit
import profiles.custom