"""This module defines Archibald's profile spec and
   loads modules in profiles/ while also ensuring conformity"""

from types import ModuleType
import os
import dataclasses

@dataclasses.dataclass
class Profile:
    """This class defines how Archibald's profiles are spec'd"""

    @dataclasses.dataclass
    class File:
        """Internal class describes a generic
           file that has a name, path and content"""

        def __init__(self, origin: str, name: str, attributes: list):

            # Check if name is str and attr_l is list
            if not isinstance(name, str) or not isinstance(attributes, list):

                # If not throw exception
                raise ValueError(f'{origin}.py files attribute not valid')

            # Check if attr_l[0] is str
            if not isinstance(attributes[0], str) or not isinstance(attributes[1], str):

                # If not throw exception
                raise ValueError(f'"{name}" file from {origin}.py does not have valid path/text')

            self.name = name
            self.path = attributes[0]
            self.text = attributes[1]

    @dataclasses.dataclass
    class Attribute:
        """Internal class describes a generic profile 
           with all possible attributes"""

        def __init__(self, _type: type, required: bool):

            self._type    = _type
            self.required = required

    __attributes = {
        "deps":     Attribute(list, False),
        "name":     Attribute(str, True),
        "gfxd": 	Attribute(dict, False),
        "pkgs":     Attribute(list, False),
        "units":    Attribute(list, False),
        "groups":   Attribute(list, False),
        "shell":    Attribute(str, False),
        "aur":      Attribute(list, False),
        "files":	Attribute(dict, False),
        "flatpaks": Attribute(list, False),
        "bash":     Attribute(list, False)
    }


    def __init__(self, name: str, obj: ModuleType):

        # Iterate attributes dictionary
        for attr, value in self.__attributes.items():

            # Check if attribure is missing but it's required
            if not hasattr(obj, attr) and value.required:

                # If yes, throw an exception
                raise ValueError(f'{name}.py MUST have a valid "{attr}" attribute')

            # Check if attribure is missing but is not required
            elif not hasattr(obj, attr) and not value.required:

                # If yes, set as NoneType
                setattr(self, attr, None)

            # Check if attribute is of correct type class
            elif not isinstance(getattr(obj, attr), value._type):

                # If yes, throw an exception
                raise ValueError(f'Attr "{attr}" of {name}.py not a {value._type}')

            # Check if attribute name is "files"
            elif attr == "files":

                # Retrieve file dict and declare files attribute
                fdict, files = getattr(obj, "files"), []

                for f in fdict:

                    # Create file object
                    new = self.File(id, f, fdict[f])

                    # Append obj to files
                    files.append(new)

                # Set profile "files" attr as files list
                setattr(self, "files", files)

            # Attribute is ok
            else:

                # Just copy attribute value
                setattr(self, attr, getattr(obj, attr))

def load():
    """Function that loads all profile modules
       and checks if they are conform to spec"""

    directory, profiles = os.path.dirname(__file__), {}

    for f in os.listdir(directory):

        # Skip if name starts with __
        if f[0:2] == "__":
            continue

        # Remove .py suffix
        f = f.removesuffix('.py')

        # Import to variable
        obj = __import__(f"profiles.{f}", fromlist=[""])

        # Strap profile
        profiles[f] = Profile(f, obj)

    return profiles
