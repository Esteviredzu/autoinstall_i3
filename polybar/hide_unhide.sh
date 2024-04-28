#!/bin/bash

# Название вашего Polybar
bar_name="example"

# Проверяем, запущен ли Polybar
if pgrep -x "polybar" > /dev/null; then
    # Если запущен, то закрываем
    pkill -x "polybar"
else
    # Если не запущен, то запускаем
    polybar "$bar_name" &
fi
