deps    = ["minimal"]

name    = "Cockpit"

pkgs    = ["screen", "cockpit", "udisks2", "cockpit-storaged", "dmidecode", "dnsmasq", "qemu-base", "libvirt", "virt-install", "cockpit-machines", "docker"]

units   = ["sshd", "libvirtd", "cockpit.socket", "docker"]

groups  = ["qemu", "libvirt", "docker"]