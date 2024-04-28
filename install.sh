#!/bin/bash

export HOME=$(eval echo ~$SUDO_USER)

# Function to install packages
install_packages() {
    echo "Installing fonts with icons for Polybar..."
    sudo pacman -S --noconfirm ttf-nerd-fonts-symbols #for icons in polybar

    echo "Installing Fira Code font..."
    sudo pacman -S --noconfirm ttf-fira-code

    echo "Installing package for touchpad management..."
    sudo pacman -S --noconfirm xorg-xinput #touchpad 

    echo "Installing tools for screen capture and locking..."
    sudo pacman -S --noconfirm scrot imagemagick i3lock #best_i3lock

    echo "Installing i3, Polybar, Nitrogen, Rofi, Alacritty, Picom..."
    sudo pacman -S --noconfirm i3 polybar nitrogen rofi alacritty picom

    echo "Installing additional software..."
    sudo pacman -S --noconfirm micro xclip lsd bat pcmanfm cmus
}

# Function to install configurations
install_configs() {
    
    if [ ! -f "$1" ]; then
        echo "File doesn't exist!"
        exit 1
    fi
    # Read the file line by line and copy folders
    while IFS= read -r folder; do
        if [ -d "$folder" ]; then
            cp -r "$folder" "$HOME/.config/" && echo "Copying $folder to the required directory..."
        else
            echo "Config for $folder doesn't exist"
        fi
    done < "$1"

    chmod +x "$HOME/.config/i3/i3lock-setup.sh" "$HOME/.config/i3/power.sh" "$HOME/.config/i3/touchpad-setup.sh" "$HOME/.config/polybar/hide_unhide.sh" "$HOME/.config/polybar/launch_polybar.sh"
    echo "done"
}

backup_configs() {
    if [ ! -f "$1" ]; then
        echo "File $1 not found"
        exit 1
    fi

    while IFS= read -r folder; do
        if [ -d "$HOME/.config/$folder" ]; then
            echo "Copying $HOME/.config/$folder to the current directory..."
            cp -r "$HOME/.config/$folder" .
        else
            echo "Folder $folder doesn't exist in $HOME/.config"
        fi
    done < "$1"
}

if [ "$1" = "install" ]; then
    install_packages && echo "Dependency installation complete"
    install_configs "confs"
elif [ "$1" = "backup" ]; then
    backup_configs "confs"
else
    echo "Usage: $0 <install|backup>"
    exit 1
fi
