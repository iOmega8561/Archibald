from types import ModuleType
import os

class profile:

	class __file:

		def __init__(self, origin: str, name: str, attr_l: list):

			# Check if name is str and attr_l is list
			if type(name) is not str or type(attr_l) is not list:
				
				# If not throw exception
				raise ValueError(f'{origin}.py files attribute not valid')
			
			# Check if attr_l[0] is str
			if type(attr_l[0]) is not str or type(attr_l[1]) is not str:

				# If not throw exception
				raise ValueError(f'"{name}" file from {origin}.py does not have valid path/text')
			
			self.name = name
			self.path = attr_l[0]
			self.text = attr_l[1]

	class __attr:
		
		def __init__(self, _type: type, required: bool):

			self._type    = _type
			self.required = required

	__attr_l = {
		"deps":     __attr(list, False),
		"name":     __attr(str, True),
		"gfxd": 	__attr(dict, False),
		"pkgs":     __attr(list, False),
		"units":    __attr(list, False),
		"groups":   __attr(list, False),
		"shell":    __attr(str, False),
		"aur":      __attr(list, False),
		"files":	__attr(dict, False),
		"flatpaks": __attr(list, False),
		"bash":     __attr(list, False)
	}


	def __init__(self, id: str, obj: ModuleType):

		# Iterate attributes dictionary
		for attr in self.__attr_l:
			
			# Check if attribure is missing but it's required
			if not hasattr(obj, attr) and self.__attr_l[attr].required:
				
				# If yes, throw an exception
				raise ValueError(f'{id}.py MUST have a valid "{attr}" attribute')
			
			# Check if attribure is missing but is not required
			elif not hasattr(obj, attr) and not self.__attr_l[attr].required:
				
				# If yes, set as NoneType
				setattr(self, attr, None)
			
			# Check if attribute is of correct type class
			elif type(getattr(obj, attr)) is not self.__attr_l[attr]._type:

				# If yes, throw an exception
				raise ValueError(f'Attr "{attr}" of {id}.py not a {self.__attr_l[attr]._type}')
			
			# Check if attribute name is "files"
			elif attr == "files":
				
				# Retrieve file dict and declare files attribute
				fdict, files = getattr(obj, "files"), []

				for f in fdict:

					# Create file object
					new = self.__file(id, f, fdict[f])

					# Append obj to files
					files.append(new)

				# Set profile "files" attr as files list
				setattr(self, "files", files)

			# Attribute is ok
			else:

				# Just copy attribute value
				setattr(self, attr, getattr(obj, attr))

def load():

	dir, profiles = os.path.dirname(__file__), {}

	for f in os.listdir(dir):

		# Skip if name starts with __
		if f[0:2] == "__":
			continue

		# Remove .py suffix
		f = f.removesuffix('.py')
		
		# Import to variable
		obj = __import__(f"profiles.{f}", fromlist=[""])

		# Strap profile
		profiles[f] = profile(f, obj)
	
	return profiles