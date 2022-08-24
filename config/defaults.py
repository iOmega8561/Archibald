import config.dicts as dicts
import utilities.classes as classes

from utilities.methods import justLogname

# Need to know username to find $home
logname = justLogname()

# User defined profiles, refer to README
profiles = [
    classes.profile(
        name    = "Gnome",
        type    = "Desktop",
        drivers = True,
        pkgs    = dicts.pkgs["Basics"] + dicts.pkgs["Xorg"] + dicts.pkgs["Audio"] + dicts.pkgs["Gnome"] + dicts.pkgs["Flatpak"],
        units   = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups", "gdm"],
        shell   = "/bin/zsh",

        files = [
            classes.file(name = "logind.conf", path = "/etc/systemd", text = dicts.texts["logind"]),
	        classes.file(name = ".zshrc", path = f"/home/{logname}", text = dicts.texts["zshrc"]),
	        classes.file(name = "htoprc", path = f"/home/{logname}/.config/htop", text = dicts.texts["htoprc"])
        ]),

    classes.profile(
        name    = "Plasma",
        type    = "Desktop",
        drivers = True,
        pkgs    = dicts.pkgs["Basics"] + dicts.pkgs["Xorg"] + dicts.pkgs["Audio"] + dicts.pkgs["Plasma"] + dicts.pkgs["Flatpak"],
        units   = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups", "sddm"],
        shell   = "/bin/zsh",

        files = [
            classes.file(name = "logind.conf", path = "/etc/systemd", text = dicts.texts["logind"]),
	        classes.file(name = ".zshrc", path = f"/home/{logname}", text = dicts.texts["zshrc"]),
	        classes.file(name = "htoprc", path = f"/home/{logname}/.config/htop", text = dicts.texts["htoprc"])
        ]),

    classes.profile(
        name    = "Cockpit",
        type    = "Server",
        pkgs    = dicts.pkgs["Basics"] + dicts.pkgs["Cockpit"],
        units   = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups", "sshd", "libvirtd", "cockpit.socket", "docker"],
        groups  = ["qemu", "libvirt", "docker"],
        shell   = "/bin/zsh",

        files = [
            classes.file(name = "logind.conf", path = "/etc/systemd", text = dicts.texts["logind"]),
	        classes.file(name = ".zshrc", path = f"/home/{logname}", text = dicts.texts["zshrc"]),
	        classes.file(name = "htoprc", path = f"/home/{logname}/.config/htop", text = dicts.texts["htoprc"])
        ]),
]