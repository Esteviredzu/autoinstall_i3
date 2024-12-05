import os
import subprocess
import shutil
import sys
import time

# Глобальная переменная с конфигурациями
config_folders = [
    "alacritty", "picom", "polybar", "i3", "dunst", "rofi", "bin", "neofetch", "bspwm", "sxhkd"
]

# Configuration for packages
packages = {
    "fonts": ["ttf-nerd-fonts-symbols", "ttf-dejavu", "ttf-fira-code"],
    "touchpad": ["xorg-xinput"],
    "screen_tools": ["scrot", "imagemagick", "i3lock"],
    "ui": ["polybar", "nitrogen", "rofi", "alacritty", "picom"],
    "wm_tools": {
        "i3": ["i3"],
        "bspwm": ["bspwm", "sxhkd"]
    },
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
def install_packages(wm_choice):
    if not shutil.which("pacman"):
        print("Pacman is not available. Ensure you are using an Arch-based system.")
        return

    # Install common packages
    for category, pkgs in packages.items():
        if category == "wm_tools":
            # Install selected window manager tools based on user's choice
            wm_pkgs = packages[category].get(wm_choice)
            if wm_pkgs:
                print(f"Installing {wm_choice} packages...")
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", *wm_pkgs], check=True)
            else:
                print(f"Invalid window manager selected: {wm_choice}")
        else:
            print(f"Installing {category} packages...")
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", *pkgs], check=True)

    print("Enabling and starting sound services...")
    subprocess.run(["systemctl", "--user", "enable", "pipewire", "pipewire-pulse", "wireplumber"], check=True)
    subprocess.run(["systemctl", "--user", "start", "pipewire", "pipewire-pulse", "wireplumber"], check=True)


def install_configs():
    home = os.path.expanduser("~")
    config_base_dir = os.path.join(home, ".config")

    for folder in config_folders:
        source = os.path.join(home, ".config", folder)
        dest = os.path.join(config_base_dir, folder)
        
        # Удаляем старую папку, если она существует
        if os.path.isdir(dest):
            print(f"Removing existing config folder {dest}...")
            try:
                shutil.rmtree(dest)
                print(f"Successfully removed {dest}")
            except Exception as e:
                print(f"Error removing {dest}: {e}")

        # Копируем новую папку конфигурации
        if os.path.isdir(source):
            print(f"Copying {folder} to {config_base_dir}...")
            try:
                shutil.copytree(source, dest, dirs_exist_ok=True)
                print(f"Successfully copied {folder} to {config_base_dir}")
            except Exception as e:
                print(f"Error copying {folder}: {e}")
        else:
            print(f"Config folder {folder} does not exist in {home}/.config")
    
    print("Setting execute permissions for scripts...")
    scripts = [
        "~/.config/bin/power.sh", "~/.config/bin/touchpad-setup.sh",
        "~/.config/polybar/hide_unhide.sh", "~/.config/polybar/launch_polybar.sh"
    ]
    for script in scripts:
        script_path = os.path.expanduser(script)  # Преобразуем ~ в домашнюю директорию
        if os.path.isfile(script_path):
            try:
                os.chmod(script_path, 0o755)
                print(f"Successfully set execute permissions for {script}")
            except Exception as e:
                print(f"Error setting permissions for {script}: {e}")
        else:
            print(f"Script {script} does not exist.")


# Function to backup configs
def backup_configs():
    home = os.path.expanduser("~")

    # Создание папки для бэкапов с уникальной меткой времени
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    backup_folder = f"older_backups/{timestamp}"
    os.makedirs(backup_folder, exist_ok=True)


    for folder in config_folders:
        if os.path.isdir(folder) and os.listdir(folder):  # Проверка, что папка существует и не пуста
            try:
                # Перемещаем папку в бэкап-папку
                shutil.move(folder, os.path.join(backup_folder, folder))
                print(f"Moved {folder} to {os.path.join(backup_folder, folder)}")
            except Exception as e:
                print(f"Error moving {folder}: {e}")
        else:
            print(f"Folder {folder} does not exist or is empty")


    backup_folder = "."

    for folder in config_folders:
        source = os.path.join(home, ".config", folder)
        if os.path.isdir(source) and os.listdir(source):  # Проверка, что папка существует и не пуста
            print(f"Backing up {source} to {backup_folder}...")
            try:
                shutil.copytree(source, os.path.join(backup_folder, folder), symlinks=True, dirs_exist_ok=True)
            except Exception as e:
                print(f"Error backing up {source}: {e}")
        else:
            print(f"Folder {folder} does not exist or is empty in {home}/.config")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <install|backup> <wm_choice>")
        sys.exit(1)

    action = sys.argv[1]

    if action == 'install' and len(sys.argv) != 3:
        print("Usage: python script.py <install|backup> <wm_choice>")
        sys.exit(1)



    if action == "install":
        wm_choice = sys.argv[2]
        if input('Do you want install packages? y/n').lower == 'y': install_packages(wm_choice)
        install_configs()
    elif action == "backup":
        backup_configs()
    else:
        print("Invalid action. Use 'install' or 'backup'.")
