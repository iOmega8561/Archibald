class profile:

	class __file:

		def __init__(self,
					 origin: str,
					 name: 	 str, 
					 attr_l: list,
			):

			# Check if name is str and attr_l is list
			if type(name) is not str or type(attr_l) is not list:
				
				# If not throw exception
				raise ValueError(f'{origin} files attribute not valid')
			
			# Check if attr_l[0] is str
			if type(attr_l[0]) is not str or type(attr_l[1]) is not str:

				# If not throw exception
				raise ValueError(f'{origin} "{name}" file does not have valid path/text')
			
			self.name = name
			self.path = attr_l[0]
			self.text = attr_l[1]

	class __attr:
		
		def __init__(self,
				 _type:      type,
				 required:  bool = False,
				 default  		 = None
		):

			self._type    = _type
			self.required = required
			self.default  = default

	__attr_l = {
		"name":     __attr(str, required = True),
		"type":     __attr(str, required = True),
		"gfxd": 	__attr(dict),
		"pkgs":     __attr(list),
		"units":    __attr(list),
		"groups":   __attr(list),
		"shell":    __attr(str),
		"aur":      __attr(bool),
		"files":	__attr(dict),
		"flatpaks": __attr(list),
		"bashcmd":  __attr(list)
	}


	def __init__(self, obj):

		# Iterate attributes dictionary
		for attr in self.__attr_l:
			
			# Check if attribure is missing but it's required
			if not hasattr(obj, attr) and self.__attr_l[attr].required:
				
				# If yes, throw an exception
				raise ValueError(f'{obj.__name__} MUST have a valid "{attr}" attribute')
			
			# Check if attribure is missing but is not required
			elif not hasattr(obj, attr) and not self.__attr_l[attr].required:
				
				# If yes, set the default value
				setattr(self, attr, self.__attr_l[attr].default)
			
			# Check if attribure is of correct type class
			elif type(getattr(obj, attr)) is not self.__attr_l[attr]._type:

				# If yes, throw an exception
				raise ValueError(f'Attr "{attr}" of {obj.__name__} not a {self.__attr_l[attr]._type}')
			
			# Check if attribute name is "files"
			elif attr == "files":
				
				# Retrieve file dict and declare files attribute
				fdict, files = getattr(obj, "files"), []

				for f in fdict:

					# Create file object
					new = self.__file(obj.__name__, f, fdict[f])

					# Append obj to files
					files.append(new)

				# Set profile "files" attr as files list
				setattr(self, "files", files)

			# Attribute is ok
			else:

				# Just copy attribute value
				setattr(self, attr, getattr(obj, attr))

############################################

from os import listdir
from os.path import dirname

def parse(getlist: bool = False):

	profiles_store, name = {}, dirname(__file__)

	for f in listdir(name):

		# Skip if name starts with __
		if f[0:2] == "__":
			continue

		# Remove .py suffix
		f = f.removesuffix('.py')
		
		# Import to variable
		imp = __import__(f"profiles.{f}", fromlist=[""])

		# Strap profile
		profiles_store[f] = profile(imp)
	
	if getlist:
		return list(profiles_store.values())

	return profiles_store