# Archibald
## Disclaimer
This is a personal project, started for fun and personal purposes only. You DO take responsability if this breaks your installation. 

## What's this?
Archibald is a configurable python utility that allows to recreate Arch Linux setups real fast. Archibald can:
- Let the user select a profile;
- Detect graphics cards;
- Install packages via PacMan;
- Enable systemd units;
- Add user to certain groups;
- Create configuration files;
- Change the user shell;
- Configure zram;
- Install aur helper.

It is best to run Archibald on a fresh Arch Linux manual installation, but minimal archinstall setups are ok too.

## How to use
Archibald needs a booting Arch installation, a working internet connection and a sudo-enabled user to run.
You can simply ```git clone``` this repo and
```
sudo pacman -S python

cd Archibald
chmod +x main.py
sudo ./main.py
```
Configuration is found under Archibald/config/. More on it down below.

## Configuration
Once you get to edit Archibald's configuration, you'll see that it's pretty self explanatory.
- packages.py defines (literally) groups of packages. One or more package groups can be used in a configured profile, using just python's algebraic syntax (pkgs = grp1 + grp2 + ... ).
- files.py contains objects wich represent a configuration file that could be included into a profile. Archibald will create files for the selected profile object.
- profiles.py contains a list. An object of that list is a profile, and here is an example:
```
# User defined profiles
# Read carefully any bad config could be catastrofic
# The order of profile childs is not relevant

import profile # data structure class
import file    # data structure class

ExampleFile = file(                                                       
            name = "ExampleConfig",                 # File name                       | str, Mandatory
            path = "example/path",                  # File path                       | str, Mandatory
            text = "sometextto\nbe\nwritten"),      # Text                            | str, Mandatory

ExampleProfile = profile(
    name    = "Example",                            # Profile name                    | str, MANDATORY
    type    = "Example",                            # Target system to be prompt      | str, MANDATORY
    drivers = True,                                 # Install graphics drivers        | bool, can omit, default False
    pkgs    = packages.ex + packages.ex2 + .. OR pkgs = ["pkg1", "pkg2" ...]          | list, can omit, default []
    units   = ["test", "example"],                  # List of systemd units to enable | list, can omit, default None
    grops   = ["wheel", "example"],                 # List of user groups             | list, can omit, default None
    shell   = "/bin/exampleshell",                  # Custom shell binary             | str, can omit, default None
    files   = [                                     # Profile only config files       | list, can omit, default None
        ExampleFile,
        Exaple2,
        ...
    ]
```
