# Disclaimer
This is a personal project, started for fun and personal purposes only. You DO take responsability if this breaks your installation. 

# Archibald
Archibald is a configurable python utility that allows to recreate Arch Linux setups real fast. Archibald can:
- Install packages
- Detect what graphics driver should be installed
- Enable systemd units
- Add user to certain groups
- Create configuration files such as .zshrc or htoprc
- Change the user shell

# Usage
Clone this repository, edit utilities/configs.py to setup things that you want or need, or you can just run Archibald.py and it will already have a couple of pre-configured profiles to choose from. 

# Configuration
Once you get to edit Archibald's configuration, you'll see that it's pretty self explanatory, it comprehends:
- Driver Sets dictionary, in which are defined the necessary packages to get graphics cards working;
- Package Groups dictionary, in which are defined bundles of packages, for example the DisplayServer bundle contains the necessary packages to have a functioning display server on our system;
- Profiles List, which contains objects of profile class, that will be parsed by Archibald to determine what to do. These can be created or modified like package groups. A profile includes a pkgs attribute, that is the sum of different package groups and will be read by Archibald to pass them as arguments to PacMan;
- Files List, wich contains objects of file class. Archibald will parse this list and create files in their defined path.
