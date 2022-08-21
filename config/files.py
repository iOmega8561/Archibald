from libs.classes import file

files = [

	file(name = ".zshrc",
	     path = "~",
	     text = "HISTFILE=~/.zsh_history\nHISTSIZE=1000\nSAVEHIST=1000\nsetopt appendhistory\nexport EDITOR=nano\nautoload -Uz compinit promptinit\ncompinit\npromptinit\nprompt walters\nzstyle ':completion:*' menu select\nzstyle ':completion::complete:*' gain-privileges 1"),

	file(name = "htoprc",
	     path = "~/.config/htop",
	     text = "show_cpu_frequency=1\nshow_cpu_temperature=1"),

	file(name = "logind.conf",
	     path = "/etc/systemd",
	     text = "[Login]\n#NAutoVTs=6\n#ReserveVT=6\n#KillUserProcesses=no\n#KillOnlyUsers=\n#KillExcludeUsers=root\n#InhibitDelayMaxSec=5\n#UserStopDelaySec=10\n#HandlePowerKey=poweroff\n#HandleSuspendKey=suspend\n#HandleHibernateKey=hibernate\n#HandleLidSwitch=suspend\n#HandleLidSwitchExternalPower=suspend\n#HandleLidSwitchDocked=ignore\n#HandleRebootKey=reboot\n#HandleRebootKeyLongPress=poweroff\n#PowerKeyIgnoreInhibited=no\n#SuspendKeyIgnoreInhibited=no\n#HibernateKeyIgnoreInhibited=no\n#LidSwitchIgnoreInhibited=yes\n#RebootKeyIgnoreInhibited=no\n#HoldoffTimeoutSec=30s\n#IdleAction=ignore\n#IdleActionSec=30min\n#RuntimeDirectorySize=10%\n#RuntimeDirectoryInodesMax=\n#RemoveIPC=yes\n#InhibitorsMax=8192\n#SessionsMax=8192")

]
