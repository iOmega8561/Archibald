from config import packages, files
from common.datastores import profile

# Check readme to edit these
list = [

    profile(
        name    = "Gnome",
        type    = "Desktop",
        drivers = True,
        pkgs    = packages.basics + packages.display + packages.audio + packages.gnome,
        units   = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups", "gdm"],
        shell   = "/bin/zsh",

        files = [
            files.logind,
            files.zshrc,
            files.htoprc
        ]),

    profile(
        name    = "Plasma",
        type    = "Desktop",
        drivers = True,
        pkgs    = packages.basics + packages.display + packages.audio + packages.plasma,
        units   = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups", "sddm"],
        shell   = "/bin/zsh",

        files = [
            files.logind,
            files.zshrc,
            files.htoprc
        ]),

    profile(
        name    = "Cockpit",
        type    = "Server",
        pkgs    = packages.basics + packages.cockpit,
        units   = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups", "sshd", "libvirtd", "cockpit.socket", "docker"],
        groups  = ["qemu", "libvirt", "docker"],
        shell   = "/bin/zsh",

        files = [
            files.logind,
            files.zshrc,
            files.htoprc
        ]),
]