# Disclaimer
This is a personal project, started for fun and personal purposes only. You DO take responsability if this breaks your installation. 

# Archibald
Archibald is a configurable python utility that allows to recreate Arch Linux setups real fast. It is possible to configure profiles wich will be parsed by Archibald. Profiles generally set packages to install, systemd units to be enabled, groups the user should be added to and configuration files to be created on the system (.zshrc for example)

# Usage
Clone this repository, edit utilities/configs.py to setup things that you want or need, or you can just run Archibald.py and it will already have a couple of pre-configured profiles to choose from. Archibald's configuration is pretty self explanatory, it comprehends:
- Driver Sets dictionary, in which are defined the necessary packages to get graphics cards working well.
- Package Groups dictionary, in which are defined bundles of packages, for example the DisplayServer bundle, contains the necessary packages to have a functioning display server on our system. The user defined sum of different groups will be a Profile package list.
- Profiles List, which contains objects of profile class, that will be parsed by Archibald to determine what to do. These can be created or modified like package groups.
- Files List, wich contains objects of file class. Archibald will parse this list and create these files.
