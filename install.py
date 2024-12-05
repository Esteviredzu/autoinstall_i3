import os
import subprocess

# Configuration for packages
packages = {
    "fonts": ["ttf-nerd-fonts-symbols", "ttf-dejavu", "ttf-fira-code"],
    "touchpad": ["xorg-xinput"],
    "screen_tools": ["scrot", "imagemagick", "i3lock"],
    "wm_tools": ["i3", "polybar", "nitrogen", "rofi", "alacritty", "picom"],
    "additional_software": [
        "micro", "xclip", "lsd", "bat", "pcmanfm", "cmus", "net-tools", "playerctl",
        "shadowsocks", "papirus-icon-theme", "obsidian", "networkmanager", "firefox",
        "lxappearance", "nano", "sudo", "openssh", "zip", "unzip", "tree", "wget",
        "fish", "cmake", "make", "keepassxc", "veracrypt", "telegram-desktop",
        "code", "flameshot", "sqlitebrowser", "python-pip", "wine"
    ],
    "sound": ["pipewire", "pipewire-pulse", "wireplumber"]
}

# Functions to install packages
def install_packages():
    if not shutil.which("pacman"):
        print("Pacman is not available. Ensure you are using an Arch-based system.")
        return

    for category, pkgs in packages.items():
        print(f"Installing {category} packages...")
        subprocess.run(["sudo", "pacman", "-S", "--noconfirm", *pkgs], check=True)

    print("Enabling and starting sound services...")
    subprocess.run(["systemctl", "--user", "enable", "pipewire", "pipewire-pulse", "wireplumber"], check=True)
    subprocess.run(["systemctl", "--user", "start", "pipewire", "pipewire-pulse", "wireplumber"], check=True)

# Function to copy configs
def install_configs(config_file):
    home = os.path.expanduser("~")
    if not os.path.isfile(config_file):
        print(f"Config file {config_file} does not exist!")
        return

    with open(config_file, "r") as file:
        for folder in file:
            folder = folder.strip()
            if os.path.isdir(folder):
                dest = os.path.join(home, ".config")
                print(f"Copying {folder} to {dest}...")
                shutil.copytree(folder, dest, dirs_exist_ok=True)
            else:
                print(f"Config folder {folder} does not exist")

    print("Setting execute permissions for scripts...")
    scripts = [
        "i3lock-setup.sh", "power.sh", "touchpad-setup.sh",
        "hide_unhide.sh", "launch_polybar.sh"
    ]
    for script in scripts:
        script_path = os.path.join(home, ".config", "bin", script)
        if os.path.isfile(script_path):
            os.chmod(script_path, 0o755)

# Function to backup configs
def backup_configs(config_file):
    home = os.path.expanduser("~")
    if not os.path.isfile(config_file):
        print(f"Config file {config_file} does not exist!")
        return

    with open(config_file, "r") as file:
        for folder in file:
            folder = folder.strip()
            source = os.path.join(home, ".config", folder)
            if os.path.isdir(source):
                print(f"Backing up {source} to current directory...")
                shutil.copytree(source, folder, dirs_exist_ok=True)
            else:
                print(f"Folder {folder} does not exist in {home}/.config")

if __name__ == "__main__":
    import sys
    import shutil

    if len(sys.argv) < 2:
        print("Usage: python script.py <install|backup>")
        sys.exit(1)

    action = sys.argv[1]
    if action == "install":
        install_packages()
        install_configs("confs")
    elif action == "backup":
        backup_configs("confs")
    else:
        print("Invalid action. Use 'install' or 'backup'.")
