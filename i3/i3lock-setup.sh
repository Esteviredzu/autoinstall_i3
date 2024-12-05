#!/bin/bash
# Esteviredzu (veltall fork)
overlay=/usr/share/pixmaps/lockoverlay.png
setxkbmap us
scrot /tmp/currentworkspace.png
convert /tmp/currentworkspace.png -blur 0x30 /tmp/currentworkspaceblur.png
composite -gravity southeast $overlay /tmp/currentworkspaceblur.png /tmp/lockbackground.png
i3lock -i /tmp/lockbackground.png
setxkbmap us,ru #change if you need
rm /tmp/currentworkspace.png
