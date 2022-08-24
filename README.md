# Archibald
## Disclaimer
This is a personal project, started for fun and personal purposes only. You DO take responsability if this breaks your installation. 

## What's this?
Archibald is a configurable python utility that allows to recreate Arch Linux setups real fast. Archibald can:
- Prompt the user a selection between profiles
- Detect QXL/Nvidia/Amd/Intel graphics cards
- Install packages via PacMan
- Enable systemd units
- Add user to certain groups
- Create configuration files such as .zshrc or htoprc
- Change the user shell
- Install paru, the AUR helper

## How to use
Archibald includes a default configuration, just clone this repository and simply run
```
cd Archibald && chmod +x archibald.py && sudo ./archibald
```
To configure Archibald edit config.py under the "utils" folder and follow instructions below.

## Configuration
Once you get to edit Archibald's configuration, you'll see that it's pretty self explanatory, it comprehends:
- Driver Sets dictionary, in which are defined the necessary packages to get graphics cards working;
- Package Groups dictionary, in which are defined bundles of packages, for example the DisplayServer bundle contains the necessary packages to have a functioning display server on our system;
- Profiles List, which contains objects of profile class, that will be parsed by Archibald to determine what to do. Here is an example profile configuration:
```
# User defined profiles
# Read carefully any bad config could be catastrofic
# The order of profile childs is not relevant

ExampleProfile = classes.profile(
    name = "Example",                            # Profile name                    | str, MANDATORY
    type = "Example",                            # Target system to be prompt      | str, MANDATORY
    drivers = True,                              # Install graphics drivers        | bool, can omit, default False
    pkgs = pkgs[0] + pkgs [1],                   # One or sum of multiple pkgroups | list, can omit, default []
    units = ["test", "example"],                 # List of systemd units to enable | list, can omit, default None
    grops = ["wheel", "example"],                # List of user groups             | list, can omit, default None
    shell = "/bin/exampleshell",                 # Custom shell binary             | str, can omit, default None
    files = [                                    # Profile only config files       | list, can omit, default []
        classes.file(                                                              | BELOW ONLY IF FILES ARE PRESENTs
            name = "ExampleConfig",              # File name                       | str, Mandatory
            path = "example/path",               # File path                       | str, Mandatory
            text = "sometextto\nbe\nwritten"),   # Text                            | str, Mandatory
        classes.file( .... )])
```
- Profiles also have a list of file objects, these can be used to define files like .zshrc or .bashrc that will be created by Archibald. A list of global configuration files is also present, these will be merged with profile.files at runtime simply by summing the two lists.
