from profiles import pClass, fClass, pAdd

pAdd(pClass(
    
    name     = "Custom",

    type     = "Desktop",

    drivers  = {
        "NVIDIA Corporation": ["dkms", "nvidia-dkms", "nvidia-prime"],
        "Advanced Micro Devices": ["xf86-video-amdgpu", "libva-mesa-driver", "vulkan-radeon", "mesa-vdpau"],
        "Intel Corporation": ["xf86-video-intel", "libva-mesa-driver", "vulkan-intel", "mesa-vdpau"]
    },

    pkgs     = ["acpi", "acpid", "acpi_call", "base-devel", "usbutils", "zsh", "zsh-completions", "net-tools", "gnu-netcat", "openssh", "git", "nano", "networkmanager", "bluez", "bluez-utils", "cronie", "htop", "polkit", "cups", "cups-pdf", "splix", "mesa", "mesa-utils", "wayland", "libinput", "libwacom", "xorg-server", "xorg-xinit", "pipewire", "pipewire-alsa", "pipewire-jack", "pipewire-pulse", "gst-plugin-pipewire", "libpulse", "wireplumber", "gnome-shell", "gdm", "nautilus", "gvfs-mtp", "gnome-keyring", "gnome-terminal", "gnome-tweaks", "power-profiles-daemon", "malcontent", "gnome-control-center", "gnome-backgrounds", "gnome-software", "eog", "gnome-calculator", "gedit", "evince", "xdg-user-dirs-gtk", "xdg-desktop-portal-gnome", "xdg-utils", "libqtxdg", "ttf-liberation", "ttf-droid", "noto-fonts-emoji"],

    units    = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups", "gdm"],

    shell    = "/bin/zsh",

    aur      = True,

    flatpaks = ["com.github.tchx84.Flatseal", "com.github.GradienceTeam.Gradience", "org.gnome.Boxes"],

    bashcmd  = ["sudo rm -f /usr/share/applications/{avahi-discover.desktop,bssh.desktop,bvnc.desktop}"],

    files    = [
        fClass(
            name = "logind.conf",
            path = "/etc/systemd", 
            text = "[Login]\n#NAutoVTs=6\n#ReserveVT=6\n#KillUserProcesses=no\n#KillOnlyUsers=\n#KillExcludeUsers=root\n#InhibitDelayMaxSec=5\n#UserStopDelaySec=10\n#HandlePowerKey=poweroff\n#HandleSuspendKey=suspend\n#HandleHibernateKey=hibernate\n#HandleLidSwitch=suspend\n#HandleLidSwitchExternalPower=suspend\n#HandleLidSwitchDocked=ignore\n#HandleRebootKey=reboot\n#HandleRebootKeyLongPress=poweroff\n#PowerKeyIgnoreInhibited=no\n#SuspendKeyIgnoreInhibited=no\n#HibernateKeyIgnoreInhibited=no\n#LidSwitchIgnoreInhibited=yes\n#RebootKeyIgnoreInhibited=no\n#HoldoffTimeoutSec=30s\n#IdleAction=ignore\n#IdleActionSec=30min\n#RuntimeDirectorySize=10%\n#RuntimeDirectoryInodesMax=\n#RemoveIPC=yes\n#InhibitorsMax=8192\n#SessionsMax=8192"    
        ),

        fClass(
            name = ".zshrc",
            path = "{home}",
            text = "# history\nHISTFILE=~/.zsh_history\nHISTSIZE=1000\nSAVEHIST=1000\nsetopt appendhistory\n\n# misc\nexport EDITOR=nano\n\n# corrections\nsetopt correct\n\n# completions\nautoload -Uz compinit\ncompinit\nzstyle ':completion:*' menu select\nzstyle ':completion::complete:*' gain-privileges 1\n\n# themes\nautoload -Uz promptinit\npromptinit\nprompt walters"
        ),

        fClass(
            name = "htoprc",
            path = "{home}/.config/htop",
            text = "highlight_base_name=1\nshow_cpu_frequency=1\nshow_cpu_temperature=1\ntree_view=1"
        )
    ]
))