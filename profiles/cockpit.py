"""Bare minimum comodities for a home server machine"""

deps = [
    "minimal"
]

name = "Cockpit server"

pkgs = [
    "screen",
    "cockpit",
    "firewalld",
    "udisks2",
    "cockpit-storaged",
    "dmidecode",
    "dnsmasq",
    "qemu-base",
    "libvirt",
    "virt-install",
    "cockpit-machines",
    "cockpit-podman",
    "podman",
    "podman-docker",
    "cockpit-pcp"
]

units = [
    "sshd",
    "libvirtd",
    "cockpit.socket"
]

groups = [
    "qemu",
    "libvirt",
    "kvm"
]
