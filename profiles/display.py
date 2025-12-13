"""Display server and drivers, with audio subsystem"""

deps = [
    "minimal"
]

name = "Display ready"

gfxd = {
    "NVIDIA Corporation": [
        "nvidia-dkms",
        "nvidia-utils"
    ],

    "Advanced Micro Devices": [
        "xf86-video-amdgpu",
        "libva-mesa-driver",
        "vulkan-radeon"
    ],

    "Intel Corporation": [
        "libva-mesa-driver", 
        "vulkan-intel"
    ]
}

pkgs = [
    "mesa",
    "mesa-utils",
    "wayland",
    "libinput",
    "xorg-server",
    "xorg-xinit",
    "pipewire",
    "pipewire-alsa",
    "pipewire-jack",
    "pipewire-pulse",
    "gst-plugin-pipewire",
    "libpulse",
    "wireplumber"
]
