from profiles import pClass, fClass, pAdd

pAdd(pClass(
    
    name    = "Cockpit",

    type    = "Headless",

    pkgs    = ["acpi", "acpid", "acpi_call", "base-devel", "usbutils", "zsh", "zsh-completions", "net-tools", "gnu-netcat", "openssh", "git", "nano", "networkmanager", "bluez", "bluez-utils", "cronie", "htop", "polkit", "cups", "cups-pdf", "splix", "screen", "cockpit", "udisks2", "cockpit-storaged", "dmidecode", "dnsmasq", "qemu-base", "libvirt", "virt-install", "cockpit-machines", "docker"],

    units   = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups", "sshd", "libvirtd", "cockpit.socket", "docker"],

    groups  = ["qemu", "libvirt", "docker"],

    shell   = "/bin/zsh",

    files   = [
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