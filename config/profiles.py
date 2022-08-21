from libs.classes import profile
from config.pkgs import *

profiles = [
        profile(name = "Gnome",
                type = "Desktop",
                pkgs = basics + pipeWire + displayServer + gnomeMinimal + desktopCommon,
                units = ["gdm"],
                groups = []),

        profile(name = "Plasma",
                type = "Desktop",
                pkgs = basics + pipeWire + displayServer + plasmaMinimal + desktopCommon,
                units = ["sddm"],
                groups = []),

        profile(name = "Cockpit",
                type = "Server",
                pkgs = basics + cockpitHeadless,
                units = ["sshd", "libvirtd", "cockpit.socket", "docker"],
                groups = ["qemu", "libvirt", "docker"])
]

