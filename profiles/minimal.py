name = "Minimal setup"

pkgs = ["acpi", "acpid", "acpi_call", "base-devel", "usbutils", "fish", "fisher", "net-tools", "gnu-netcat", "openssh", "git", "nano", "networkmanager", "bluez-tools", "cronie", "htop", "polkit", "cups", "cups-pdf", "splix", "fuse"]

units = ["acpid", "bluetooth", "NetworkManager", "cronie", "cups"]

shell = "/bin/fish"

files = {
    ".bashrc": [
        "{home}",
        "# misc\nexport EDITOR=nano"
    ],

    "config.fish": [
        "{home}/.config/fish",
        'set -U fish_greeting ""\nset -Ux EDITOR nano'
    ],

    "htoprc": [
        "{home}/.config/htop",
        "highlight_base_name=1\nshow_cpu_frequency=1\nshow_cpu_temperature=1\ntree_view=1"
    ]
}