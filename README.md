# Archibald
## Disclaimer
This is a personal project, started for fun and personal purposes only. You DO take responsability if this breaks your installation. 

## What's this?
Archibald is a utility that deploys user defined configuration, atomatically. Archibald can:
- Let the user select a profile;
- Detect graphics cards;
- Install packages using pacman;
- Enable systemd units;
- Add user to certain groups;
- Create configuration files;
- Change the user shell;
- Configure zram;
- Install aur helper.

## How to use
Archibald can be run either in arch-chroot or an already installed/configured system.
It is best to have a bootloader installed and already set locale configuration.

After that you can simply ```git clone``` this repo and
```
sudo pacman -S python

cd Archibald
chmod +x main.py
./main.py
```
Configuration is found under Archibald/userconf/. More on it down below.

## Configuration
Once you get to edit Archibald's configuration, you'll see that it's pretty self explanatory.
- packages.py defines (literally) groups of packages. One or more package groups can be used in a configured profile, using just python's algebraic syntax (pkgs = grp1 + grp2 + ... ).
- files.py contains descriptions of files that will be created on your system by Archibald (they should be included in the selected profile),
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
