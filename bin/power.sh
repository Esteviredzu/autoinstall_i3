#!/bin/bash

options="VPN\nShutdown\nReboot\nSuspend\nLogout\nLock"

selected_option=$(echo -e "$options" | rofi -dmenu -i -p "Choose an action:")

search_google() {
    query=$1
    firefox "https://www.google.com/search?q=$(echo $query | sed 's/ /+/g')"
}

search_youtube() {
    query=$1
    firefox "https://www.youtube.com/results?search_query=$(echo $query | sed 's/ /+/g')"
}

vpn() {
    if pgrep -x "sslocal" > /dev/null
    then
        echo "Останавливаю sslocal..."
        killall sslocal
        dunstify "vpn disabled"
    else
        echo "Запускаю sslocal..."
        dunstify "vpn enabled"
        cd ~/git/shadowsocks-vpn && sh start_vpn.sh
        
    fi
}

if [[ $selected_option == "?"* ]]; then
    echo "$selected_option"
    search_google "${selected_option:1}"
    exit 0
fi

if [[ $selected_option == "y?"* ]]; then
    echo "$selected_option"
    search_youtube "${selected_option:2}"
    exit 0
fi

case "$selected_option" in
	"VPN")
		vpn
		;;
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
        pkill -KILL -u $USER
        ;;
    "Lock")
        $HOME/.config/bin/i3lock-setup.sh
        ;;
    *)
        echo "Invalid option selected"
        ;;
esac

exit 0
