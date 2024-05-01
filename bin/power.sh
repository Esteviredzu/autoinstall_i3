#!/bin/bash

options="Shutdown\nReboot\nSuspend\nLogout\nLock"

selected_option=$(echo -e "$options" | rofi -dmenu -i -p "Choose an action:")

search_google() {
    query=$1
    firefox "https://www.google.com/search?q=$(echo $query | sed 's/ /+/g')" # Открытие Firefox с результатами поиска
}

search_youtube() {
    query=$1
    firefox "https://www.youtube.com/results?search_query=$(echo $query | sed 's/ /+/g')"
}

if [[ $selected_option == "?"* ]]; then
    echo "$selected_option"
    search_google "${selected_option:1}"
	i3-msg workspace 8:br
    exit 0
fi

if [[ $selected_option == "y?"* ]]; then
    echo "$selected_option"
    search_youtube "${selected_option:2}"
    i3-msg workspace 8:br
    exit 0
fi

case "$selected_option" in
    "Shutdown")
        shutdown 0
        ;;
    "Reboot")
        reboot
        ;;
    "Suspend")
    	$HOME/.config/bin/i3lock-setup.sh
        systemctl suspend
        ;;
    "Logout")
        i3 exit
        ;;
    "Lock")
        $HOME/.config/bin/i3lock-setup.sh
        ;;
    *)
        echo "Invalid option selected"
        ;;
esac

exit 0
