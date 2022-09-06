name    = "Plasma"

type    = "Desktop"

drivers = {
    "NVIDIA Corporation": ["dkms", "nvidia-dkms", "nvidia-prime"],
    "Advanced Micro Devices": ["xf86-video-amdgpu", "libva-mesa-driver", "vulkan-radeon", "mesa-vdpau"],
    "Intel Corporation": ["xf86-video-intel", "libva-mesa-driver", "vulkan-intel", "mesa-vdpau"]
}
    
pkgs    = ["acpi", "acpid", "acpi_call", "base-devel", "usbutils", "zsh", "zsh-completions", "net-tools", "gnu-netcat", "openssh", "git", "nano", "networkmanager", "bluez-tools", "cronie", "htop", "polkit", "cups", "cups-pdf", "splix", "mesa", "mesa-utils", "wayland", "libinput", "libwacom", "xorg-server", "xorg-xinit", "pipewire", "pipewire-alsa", "pipewire-jack", "pipewire-pulse", "gst-plugin-pipewire", "libpulse", "wireplumber", "plasma-desktop", "sddm", "sddm-kcm", "plasma-wayland-session", "dolphin", "systemsettings", "kde-gtk-config", "kscreen", "breeze-gtk", "kwallet", "konsole", "bluedevil", "power-profiles-daemon", "powerdevil", "plasma-nm", "plasma-workspace-wallpapers", "discover", "ark", "kate", "kcalc", "spectacle", "krunner", "plasma-disks", "partitionmanager", "okular", "xdg-desktop-portal-kde", "xdg-utils", "libqtxdg", "ttf-liberation", "ttf-droid", "noto-fonts-emoji"]

units   = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups", "sddm"]

shell   = "/bin/zsh"

files   = {
    ".zshrc": [
        "{home}",
        "# history\nHISTFILE=~/.zsh_history\nHISTSIZE=1000\nSAVEHIST=1000\nsetopt appendhistory\n\n# misc\nexport EDITOR=nano\n\n# corrections\nsetopt correct\n\n# completions\nautoload -Uz compinit\ncompinit\nzstyle ':completion:*' menu select\nzstyle ':completion::complete:*' gain-privileges 1\n\n# themes\nautoload -Uz promptinit\npromptinit\nprompt walters"
    ],

    "htoprc": [
        "{home}/.config/htop",
        "highlight_base_name=1\nshow_cpu_frequency=1\nshow_cpu_temperature=1\ntree_view=1"
    ]
}