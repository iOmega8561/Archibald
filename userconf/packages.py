# Drivers, don't touch

drivers = {

    "NVIDIA Corporation": ["dkms", "nvidia-dkms", "nvidia-prime"],

    "Advanced Micro Devices": ["xf86-video-amdgpu", "libva-mesa-driver", "vulkan-radeon", "mesa-vdpau"],

    "Intel Corporation": ["xf86-video-intel", "libva-mesa-driver", "vulkan-intel", "mesa-vdpau"]

}

##########################

basics = ["acpi", "acpid", "acpi_call", "base-devel", "zsh", "zsh-completions", "net-tools", "gnu-netcat", "openssh", "git", "nano", "networkmanager", "bluez", "bluez-utils", "cronie", "htop", "polkit", "cups", "cups-pdf", "splix"]

display = ["mesa", "mesa-utils", "wayland", "libinput", "libwacom", "xorg-server", "xorg-xinit"]

audio = ["pipewire", "pipewire-alsa", "pipewire-jack", "pipewire-pulse", "gst-plugin-pipewire", "libpulse", "wireplumber"]

cockpit = ["screen", "cockpit", "udisks2", "cockpit-storaged", "dmidecode", "dnsmasq", "qemu-base", "libvirt", "virt-install", "cockpit-machines", "docker"]

gnome = ["gnome-shell", "gdm", "nautilus", "gvfs-mtp", "gnome-keyring", "gnome-terminal", "gnome-tweaks", "power-profiles-daemon", "malcontent", "gnome-control-center", "gnome-backgrounds", "gnome-themes-extra", "gnome-software", "eog", "gnome-calculator", "gedit", "evince", "xdg-user-dirs-gtk", "flatpak", "xdg-desktop-portal-gnome", "xdg-utils", "libqtxdg", "ttf-liberation", "ttf-droid", "noto-fonts-emoji"]

plasma = ["plasma-desktop", "sddm", "sddm-kcm", "plasma-wayland-session", "dolphin", "systemsettings", "kde-gtk-config", "kscreen", "breeze-gtk", "kwallet", "konsole", "bluedevil", "power-profiles-daemon", "powerdevil", "plasma-nm", "plasma-workspace-wallpapers", "discover", "ark", "kate", "kcalc", "spectacle", "krunner", "plasma-disks", "partitionmanager", "okular", "flatpak", "xdg-desktop-portal-kde", "xdg-utils", "libqtxdg", "ttf-liberation", "ttf-droid", "noto-fonts-emoji"]