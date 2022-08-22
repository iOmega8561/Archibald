# Archibald
## Disclaimer
This is a personal project, started for fun and personal purposes only. You DO take responsability if this breaks your installation. 

## What's this?
Archibald is a configurable python utility that allows to recreate Arch Linux setups real fast. Archibald can:
- Install packages
- Detect what graphics driver should be installed
- Enable systemd units
- Add user to certain groups
- Create configuration files such as .zshrc or htoprc
- Change the user shell

## How to use
Clone this repository, edit utilities/configs.py to setup things that you want or need, or you can just run Archibald.py and it will already have a couple of pre-configured profiles to choose from. 

## Configuration
Once you get to edit Archibald's configuration, you'll see that it's pretty self explanatory, it comprehends:
- Driver Sets dictionary, in which are defined the necessary packages to get graphics cards working;
- Package Groups dictionary, in which are defined bundles of packages, for example the DisplayServer bundle contains the necessary packages to have a functioning display server on our system;
- Profiles List, which contains objects of profile class, that will be parsed by Archibald to determine what to do. Here is an example profile configuration:
```
#User defined profiles

ExampleProfile = classes.profile(
    name = "Example",                                   # Profile name                    | Mandatory
    type = "Example",                                   # Target system to be prompt      | Mandatory
    pkgs = pkgroups["example"] + pkgroups ["example2"], # One or sum of multiple pkgroups | = [] for none
    units = ["test", "example"],                        # List of systemd units to enable | = [] for none
    grops = ["wheel", "example"],                       # List of user groups             | = [] for none
    shell = "/bin/exampleshell",                        # Custom shell binary             | = None for none
    files = [                                           # Profile only config files       | = [] for none
        classes.file(
            name = "ExampleConfig",                     # File name                       | Mandatory
            path = "example/path",                      # File path                       | Mandatory
            text = "sometextto\nbe\nwritten"),          # Text                            | Mandatory
        classes.file( .... )])
```
- Profiles also have a list of file objects, these can be used to define files like .zshrc or .bashrc that will be created by Archibald.
