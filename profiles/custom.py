deps     = ["gnome"]

name     = "iOmega8561"

flatpaks = ["com.github.tchx84.Flatseal", "org.gnome.TextEditor", "org.gnome.Boxes"]

aur      = ["adw-gtk3", "gnome-console"]

bash     = [
    "sudo rm -f /usr/share/applications/{avahi-discover.desktop,bssh.desktop,bvnc.desktop}",
    "sudo pacman -Rcns --noconfirm gnome-terminal gedit"
]