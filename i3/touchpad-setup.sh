#!/bin/bash

# Замените "YOUR_TOUCHPAD_ID" на фактический ID вашего тачпада
TOUCHPAD_ID="17"

# Включить натуральный скроллинг
xinput --set-prop $TOUCHPAD_ID "libinput Natural Scrolling Enabled" 1

# Включить одиночное нажатие для левой кнопки мыши
xinput --set-prop $TOUCHPAD_ID "libinput Tapping Enabled" 1
xinput --set-prop $TOUCHPAD_ID "libinput Tapping Drag Enabled" 1

# Включить правую кнопку мыши на нажатие двумя пальцами
xinput --set-prop $TOUCHPAD_ID "libinput Click Method Enabled" 0 1
