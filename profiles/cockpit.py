deps   = ["minimal"]

name   = "Cockpit server"

pkgs   = ["screen", "cockpit", "firewalld", "udisks2", "cockpit-storaged", "dmidecode", "dnsmasq", "qemu-base", "libvirt", "virt-install", "cockpit-machines", "cockpit-podman", "podman", "podman-docker"]

units  = ["sshd", "libvirtd", "cockpit.socket", "podman"]

groups = ["qemu", "libvirt"]