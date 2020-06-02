#!/usr/bin/env bash

rofi_command="rofi -theme $FVWM_USERDIR/scripts/rofi/theme/yesno.rasi"

# Options
yes=""
no=""

# Variable passed to rofi
optionsYN="$yes\n$no"

chosenYN="$(echo -e "$optionsYN" | $rofi_command -dmenu -selected-row 1)"
case $chosenYN in
    $yes)
        `$1`
        ;;
    $no)
        ;;
esac
