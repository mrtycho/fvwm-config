#!/usr/bin/env bash

rofi_command="rofi -theme $FVWM_USERDIR/scripts/rofi/theme/logout.rasi"

# Options
shutdown=""
reboot=""
lock=""
restart=""
logout=""

# Variable passed to rofi
options="$shutdown\n$reboot\n$lock\n$restart\n$logout"

chosen="$(echo -e "$options" | $rofi_command -dmenu -selected-row 2)"
case $chosen in
    $shutdown)
        systemctl poweroff
        ;;
    $reboot)
        systemctl reboot
        ;;
    $lock)
        xscreensaver-command -l
        ;;
    $restart)
        FvwmCommand restart
        ;;
    $logout)
        FvwmCommand quit
        ;;
esac
