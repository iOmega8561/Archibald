import utilities.classes as classes
from utilities.methods import subprocess_try

logname = subprocess_try("logname", None, None, None).stdout.rstrip("\n")

#User defined driver sets
drivers = {
    "QXL paravirtual graphic card": ["xf86-video-qxl"],
    "NVIDIA Corporation": ["dkms", "nvidia-dkms", "nvidia-prime"],
    "Advanced Micro Devices": ["xf86-video-amdgpu", "libva-mesa-driver", "vulkan-radeon", "mesa-vdpau"],
    "Intel Corporation": ["xf86-video-intel", "libva-mesa-driver", "vulkan-intel", "mesa-vdpau"]
}

#User defined package groups
pkgroups = {
    "Basics": ["acpi", "acpid", "acpi_call", "base-devel", "zsh", "zsh-completions", "net-tools", "gnu-netcat", "openssh", "git", "nano", "networkmanager", "bluez", "bluez-utils", "cronie", "htop", "ffmpeg", "polkit", "cups", "cups-pdf", "splix"],

    "DisplayServer": ["mesa", "mesa-utils", "wayland", "libinput", "xorg-server", "xorg-xinit"],

    "PipeWire": ["pipewire", "pipewire-alsa", "pipewire-jack", "pipewire-pulse", "gst-plugin-pipewire", "libpulse", "wireplumber"],

    "CockpitHeadless": ["screen", "cockpit", "udisks2", "cockpit-storaged", "qemu-base", "libvirt", "virt-install", "dnsmasq", "cockpit-machines", "docker"],

    "GnomeMinimal": ["gnome-shell", "gdm", "nautilus", "gnome-keyring", "gnome-terminal", "gnome-tweaks", "gnome-bluetooth-3.0", "gnome-control-center", "gnome-backgrounds", "gnome-themes-extra", "gnome-software", "eog", "gnome-calculator", "gedit", "evince", "xdg-desktop-portal-gnome", "xdg-utils"],

    "PlasmaMinimal": ["plasma-desktop", "sddm", "plasma-wayland-session", "dolphin", "systemsettings", "kscreen", "breeze-gtk", "kwallet", "konsole", "bluedevil", "powerdevil", "plasma-nm", "plasma-workspace-wallpapers", "discover", "ark", "kwrite", "kcalc", "spectacle", "krunner", "plasma-disks", "partitionmanager", "packagekit-qt5", "okular", "xdg-desktop-portal-kde"],

    "DesktopCommons": ["xdg-user-dirs", "xdg-desktop-portal", "libqtxdg", "flatpak", "ttf-liberation", "ttf-droid", "noto-fonts-emoji"]
}

#User defined profiles
profiles = [
    classes.profile(
        name = "Gnome",
        type = "Desktop",
        pkgs = pkgroups["Basics"] + pkgroups["DisplayServer"] + pkgroups["PipeWire"] + pkgroups["GnomeMinimal"] + pkgroups["DesktopCommons"],
        units = ["gdm"],
        groups = [],
        shell = "/bin/zsh"),

    classes.profile(
        name = "Plasma",
        type = "Desktop",
        pkgs = pkgroups["Basics"] + pkgroups["DisplayServer"] + pkgroups["PipeWire"] + pkgroups["PlasmaMinimal"] + pkgroups["DesktopCommons"],
        units = ["sddm"],
        groups = [],
        shell = "/bin/zsh"),

    classes.profile(
        name = "Cockpit",
        type = "Server",
        pkgs = pkgroups["Basics"] + pkgroups["CockpitHeadless"],
        units = ["sshd", "libvirtd", "cockpit.socket", "docker"],
        groups = ["qemu", "libvirt", "docker"],
        shell = "/bin/zsh")
]

#User defined basic config files
files = [
	classes.file(
        name = ".zshrc",
	    path = f"/home/{logname}",
	    text = "HISTFILE=~/.zsh_history\nHISTSIZE=1000\nSAVEHIST=1000\nsetopt appendhistory\nexport EDITOR=nano\nautoload -Uz compinit promptinit\ncompinit\npromptinit\nprompt walters\nzstyle ':completion:*' menu select\nzstyle ':completion::complete:*' gain-privileges 1"),

	classes.file(
        name = "htoprc",
	    path = f"/home/{logname}/.config/htop",
	    text = "show_cpu_frequency=1\nshow_cpu_temperature=1"),

	classes.file(
        name = "logind.conf",
	    path = "/etc/systemd",
	    text = "[Login]\n#NAutoVTs=6\n#ReserveVT=6\n#KillUserProcesses=no\n#KillOnlyUsers=\n#KillExcludeUsers=root\n#InhibitDelayMaxSec=5\n#UserStopDelaySec=10\n#HandlePowerKey=poweroff\n#HandleSuspendKey=suspend\n#HandleHibernateKey=hibernate\n#HandleLidSwitch=suspend\n#HandleLidSwitchExternalPower=suspend\n#HandleLidSwitchDocked=ignore\n#HandleRebootKey=reboot\n#HandleRebootKeyLongPress=poweroff\n#PowerKeyIgnoreInhibited=no\n#SuspendKeyIgnoreInhibited=no\n#HibernateKeyIgnoreInhibited=no\n#LidSwitchIgnoreInhibited=yes\n#RebootKeyIgnoreInhibited=no\n#HoldoffTimeoutSec=30s\n#IdleAction=ignore\n#IdleActionSec=30min\n#RuntimeDirectorySize=10%\n#RuntimeDirectoryInodesMax=\n#RemoveIPC=yes\n#InhibitorsMax=8192\n#SessionsMax=8192")
]