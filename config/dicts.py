# Don't edit if you don't know what you're doing

drivers = {

    "QXL paravirtual graphic card": ["xf86-video-qxl"],
    
    "NVIDIA Corporation": ["dkms", "nvidia-dkms", "nvidia-prime"],
    
    "Advanced Micro Devices": ["xf86-video-amdgpu", "libva-mesa-driver", "vulkan-radeon", "mesa-vdpau"],
    
    "Intel Corporation": ["xf86-video-intel", "libva-mesa-driver", "vulkan-intel", "mesa-vdpau"]

}

pkgs = {

    "Basics": ["acpi", "acpid", "acpi_call", "base-devel", "zsh", "zsh-completions", "net-tools", "gnu-netcat", "openssh", "git", "nano", "networkmanager", "bluez", "bluez-utils", "cronie", "htop", "ffmpeg", "polkit", "cups", "cups-pdf", "splix"],

    "Xorg": ["mesa", "mesa-utils", "wayland", "libinput", "libwacom", "xorg-server", "xorg-xinit"],

    "Audio": ["pipewire", "pipewire-alsa", "pipewire-jack", "pipewire-pulse", "gst-plugin-pipewire", "libpulse", "wireplumber"],

    "Cockpit": ["screen", "cockpit", "udisks2", "cockpit-storaged", "qemu-base", "libvirt", "virt-install", "dnsmasq", "cockpit-machines", "docker"],

    "Gnome": ["gnome-shell", "gdm", "nautilus", "gnome-keyring", "gnome-terminal", "gnome-tweaks", "gnome-bluetooth-3.0", "power-profiles-daemon","gnome-control-center", "gnome-backgrounds", "gnome-themes-extra", "gnome-software", "eog", "gnome-calculator", "gedit", "evince", "xdg-desktop-portal-gnome", "xdg-utils", "xdg-user-dirs", "xdg-desktop-portal", "libqtxdg", "flatpak", "ttf-liberation", "ttf-droid", "noto-fonts-emoji"],

    "Plasma": ["plasma-desktop", "sddm", "plasma-wayland-session", "dolphin", "systemsettings", "kscreen", "breeze-gtk", "kwallet", "konsole", "bluedevil", "power-profiles-daemon", "powerdevil", "plasma-nm", "plasma-workspace-wallpapers", "discover", "ark", "kwrite", "kcalc", "spectacle", "krunner", "plasma-disks", "partitionmanager", "packagekit-qt5", "okular", "xdg-desktop-portal-kde", "xdg-utils", "xdg-user-dirs", "xdg-desktop-portal", "libqtxdg", "flatpak", "ttf-liberation", "ttf-droid", "noto-fonts-emoji"]

}

texts = {

    "logind": "[Login]\n#NAutoVTs=6\n#ReserveVT=6\n#KillUserProcesses=no\n#KillOnlyUsers=\n#KillExcludeUsers=root\n#InhibitDelayMaxSec=5\n#UserStopDelaySec=10\n#HandlePowerKey=poweroff\n#HandleSuspendKey=suspend\n#HandleHibernateKey=hibernate\n#HandleLidSwitch=suspend\n#HandleLidSwitchExternalPower=suspend\n#HandleLidSwitchDocked=ignore\n#HandleRebootKey=reboot\n#HandleRebootKeyLongPress=poweroff\n#PowerKeyIgnoreInhibited=no\n#SuspendKeyIgnoreInhibited=no\n#HibernateKeyIgnoreInhibited=no\n#LidSwitchIgnoreInhibited=yes\n#RebootKeyIgnoreInhibited=no\n#HoldoffTimeoutSec=30s\n#IdleAction=ignore\n#IdleActionSec=30min\n#RuntimeDirectorySize=10%\n#RuntimeDirectoryInodesMax=\n#RemoveIPC=yes\n#InhibitorsMax=8192\n#SessionsMax=8192",

    "zshrc": "HISTFILE=~/.zsh_history\nHISTSIZE=1000\nSAVEHIST=1000\nsetopt appendhistory\nexport EDITOR=nano\nautoload -Uz compinit promptinit\ncompinit\npromptinit\nprompt walters\nzstyle ':completion:*' menu select\nzstyle ':completion::complete:*' gain-privileges 1",

    "htoprc": "show_cpu_frequency=1\nshow_cpu_temperature=1"
}