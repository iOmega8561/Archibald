basics = ["acpi", "acpid", "acpi_call", "base-devel", "zsh", "zsh-completions", "net-tools", "gnu-netcat", "openssh", "git", "nano", "networkmanager", "bluez", "bluez-utils", "cronie", "htop", "ffmpeg", "polkit", "cups", "cups-pdf", "splix"]

displayServer = ["mesa", "mesa-utils", "wayland", "libinput", "xorg-server", "xorg-xinit"]

pipeWire = ["pipewire", "pipewire-alsa", "pipewire-jack", "pipewire-pulse", "gst-plugin-pipewire", "libpulse", "wireplumber"]

qxl = ["xf86-video-qxl"]

nvidia = ["dkms", "nvidia-dkms"]

amdGpu = ["xf86-video-amdgpu", "libva-mesa-driver", "vulkan-radeon", "mesa-vdpau"]

intel = ["xf86-video-intel", "libva-mesa-driver", "vulkan-intel", "mesa-vdpau"]

cockpitHeadless = ["screen", "cockpit", "udisks2", "cockpit-storaged", "qemu-base", "libvirt", "virt-install", "dnsmasq", "cockpit-machines", "docker"]

desktopCommon = ["xdg-user-dirs", "xdg-desktop-portal", "libqtxdg", "flatpak", "ttf-liberation", "noto-fonts-emoji"]

gnomeMinimal = ["gnome-shell", "gdm", "nautilus", "gnome-keyring", "gnome-terminal", "gnome-tweaks", "gnome-bluetooth-3.0", "gnome-control-center", "gnome-backgrounds", "gnome-themes-extra", "gnome-software", "eog", "gnome-calculator", "gedit", "evince", "xdg-desktop-portal-gnome", "xdg-utils"]

plasmaMinimal = ["plasma-desktop", "sddm", "plasma-wayland-session", "dolphin", "systemsettings", "kscreen", "breeze-gtk", "kwallet", "konsole", "bluedevil", "powerdevil", "plasma-nm", "plasma-workspace-wallpapers", "discover", "ark", "kwrite", "kcalc", "spectacle", "krunner", "plasma-disks", "partitionmanager", "packagekit-qt5", "okular", "xdg-desktop-portal-kde"]
