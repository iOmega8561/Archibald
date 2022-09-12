name  = "Minimal setup"

pkgs  = ["acpi", "acpid", "acpi_call", "base-devel", "usbutils", "zsh", "zsh-completions", "net-tools", "gnu-netcat", "openssh", "git", "nano", "networkmanager", "bluez-tools", "cronie", "htop", "polkit", "cups", "cups-pdf", "splix", "fuse"]

units = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups"]

shell = "/bin/fish"

files = {

    ".zshrc": [
        "{home}",
        "# history\nHISTFILE=~/.zsh_history\nHISTSIZE=1000\nSAVEHIST=1000\nsetopt appendhistory\n\n# misc\nexport EDITOR=nano\n\n# corrections\nsetopt correct\n\n# completions\nautoload -Uz compinit\ncompinit\nzstyle ':completion:*' menu select\nzstyle ':completion::complete:*' gain-privileges 1\n\n# themes\nautoload -Uz promptinit\npromptinit\nprompt walters"
    ],

    "htoprc": [
        "{home}/.config/htop",
        "highlight_base_name=1\nshow_cpu_frequency=1\nshow_cpu_temperature=1\ntree_view=1"
    ]
}