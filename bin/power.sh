#!/bin/bash

options="Shutdown\nReboot\nSuspend\nLogout\nLock"

selected_option=$(echo -e "$options" | rofi -dmenu -i -p "Choose an action:")

case "$selected_option" in
    "Shutdown")
        shutdown 0
        ;;
    "Reboot")
        reboot
        ;;
    "Suspend")
    	$HOME/.config/i3/i3lock-setup.sh
        systemctl suspend
        ;;
    "Logout")
        i3 exit
        ;;
    "Lock")
        $HOME/.config/i3/i3lock-setup.sh
        ;;
    *)
        echo "Invalid option selected"
        ;;
esac

exit 0
