deps = ["minimal"]

name = "Display ready"

gfxd = {
    "NVIDIA Corporation": ["nvidia-dkms", "nvidia-prime"],
    "Advanced Micro Devices": ["xf86-video-amdgpu", "libva-mesa-driver", "vulkan-radeon", "mesa-vdpau"],
    "Intel Corporation": ["xf86-video-intel", "libva-mesa-driver", "vulkan-intel", "mesa-vdpau"]
}

pkgs = ["mesa", "mesa-utils", "wayland", "libinput", "xorg-server", "xorg-xinit", "pipewire", "pipewire-alsa", "pipewire-jack", "pipewire-pulse", "gst-plugin-pipewire", "libpulse", "wireplumber"]