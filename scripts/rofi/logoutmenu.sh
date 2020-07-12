#!/usr/bin/env bash

rofi_command="rofi -theme $FVWM_USERDIR/scripts/rofi/theme/logoutmenu.rasi"

# Options
shutdown=" $1"
reboot=" $2"
lock=" $3"
restart=" $4"
logout=" $5"

# Variable passed to rofi
options="$shutdown\n$reboot\n$lock\n$restart\n$logout"

chosen="$(echo -e "$options" | $rofi_command -p "" -dmenu -selected-row 2)"
case $chosen in
    $shutdown)
        $FVWM_USERDIR/scripts/rofi/yesno.sh "systemctl poweroff"
        ;;
    $reboot)
        $FVWM_USERDIR/scripts/rofi/yesno.sh "systemctl reboot"
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
