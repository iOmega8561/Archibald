deps     = ["gnome"]

name     = "Custom"

flatpaks = ["com.github.tchx84.Flatseal", "com.github.GradienceTeam.Gradience", "org.gnome.Boxes"]

bash     = ["sudo rm -f /usr/share/applications/{avahi-discover.desktop,bssh.desktop,bvnc.desktop}"]