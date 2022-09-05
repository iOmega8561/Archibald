# Archibald
## Disclaimer
This is a personal project, started for fun and personal purposes only. You DO take responsability if this breaks your installation. 

## What's this?
Archibald is a python utility, meant to be used on a fresh system, that can help the user automate post-install procedures, such as installing a desktop environment or writing config files somewhere in the system.

## How to use
Archibald can be run either in arch-chroot or a booted system.
### Requirements
Python 3 must be installed and path-accessible
A sudo user must be configured and used to run Archibald.
### When ready
Then you can simply ```git clone``` this repo and
```
cd Archibald
chmod +x main
./main
```
Profiles are found under Archibald/profiles/. More on it down below.

## Configuration
Profiles can be created and dropped under Archibald/profiles/, they must contain a specific set of attributes that will be parsed by Archibald at runtime. Here is an example.py profile:
```
from profiles import pClass, fClass, pAdd

pAdd(pClass(
    name     = "Example",                            # Profile name                    | str, MANDATORY
    
    type     = "Example",                            # Target system to be prompt      | str, MANDATORY
    
    drivers  = True,                                 # Install graphics drivers        | bool, can omit, default False
    
    pkgs     = packages.ex + packages.ex2 + .. OR pkgs = ["pkg1", "pkg2" ...]          | list, can omit, default []
    
    units    = ["test", "example"],                  # List of systemd units to enable | list, can omit, default None
    
    groups   = ["wheel", "example"],                 # List of user groups             | list, can omit, default None
    
    shell    = "/bin/somecustomshell",               # Custom shell binary             | str, can omit, default None
    
    aur      = True                                  # Install or not paru             | bool, can omit, default False

    flatpaks = ["org.some.flatpak", "another"]       # Flatpak list                    | list, can omit, default None

    bashcmd  = ["a command", "another command"]      # Bash arbitrary commands         | list, can omit, default None

    files    = [                                     # Profile only config files       | list, can omit, default None
        
        pFile( 
            name = "somerandomconfig.conf",                                           | str, MANDATORY
            path = "{home}/path/in/your/home",                                        | str, MANDATORY
            text = "somefilecontents\nhelloworld"                                     | str, MANDATORY
        )
    ]
```
After creating your profile.py file, you must append ```import profiles.yourprofile``` to Archibald/profiles/\___init___.py