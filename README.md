# Archibald
## Disclaimer
This is a learning project, and although i use it quite a lot without issues, it's really not production-ready so use it carefully.
## What's this?
Archibald is a utility meant to be used on a fresh system, that can help the user automate post-install procedures, such as installing a desktop environment or writing config files somewhere in the system.
# Why just not use archinstall?
Archibald is for people who like to perform the manual installation by hand-book, but can't bother to install and configure every time their favourite set of packages afterwards. Custom window manager setup? No issue for Archibald, create your config file and it's done.
### Requirements
Python 3 is needed.
A standard user with SUDO permissions must be configured to use Archibald correctly as some of it's functions require running as a non root user.
Users with NVIDIA hardware should install the right headers for their current kernel before running Archiabald, this is required to build nvidia drivers km with dkms.
## How to use
Archibald can be run either in arch-chroot or a booted system. It is meant to be run as a standalone application, so it cannot be installed as a python module yet or used in another project (Maybe in the future).
### When ready
Then you can simply ```git clone``` this repo and
```
cd archibald
chmod +x archibald.py
./archibald.py
```
Configuration Profiles are found under Archibald/profiles/. More on it down below.

## Configuration
Profiles can be created and dropped under archibald/profiles/, they must respect a specific set of attributes that will be parsed by Archibald at runtime. Here is an example.py profile:
```
deps     = ["a_profile", "another"]              # Profile dependencies            | list, optional

name     = "Example"                             # Profile name                    | str, MANDATORY
        
drivers  = {                                     # Graphics drivers                | dict, optional

    "A Gpu Manifacturer": ["driverpackage1", "mesasomething"]

}
    
pkgs     = packages.ex + packages.ex2 + .. OR pkgs = ["pkg1", "pkg2" ...]          | list, optional
    
units    = ["test", "example"]                   # Systemd services to enable      | list, optional
    
groups   = ["wheel", "example"]                  # User groups to be assigned      | list, optional
    
shell    = "/bin/somecustomshell"                # Custom shell binary (chsh)      | str, optional

# If aur packages are present in your profile, paru will also be installed automatically
aur      = ["aurpkg", "another"]                 # Favourite aur packages          | list, optional

# If flatpak packages are present in your profile, flatpak will be installed automatically
flatpaks = ["org.some.flatpak", "another"]       # Flatpak list                    | list, optional

bash     = ["a command", "another command"]      # Bash arbitrary commands         | list, optional

files    = {                                     # Custom configuration files      | dict, optional
        
    "filename": [
        "some/system/path/like/{home}",
        "somerandomtexttoputinyourfile"
    ]
}
```
