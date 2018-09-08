#!/bin/bash

ThumbDir=$FVWM_USERDIR/.thumbs
[ -d $ThumbDir ] || mkdir $ThumbDir

Colors="tan peru sienna indianred olivedrab midnightblue cadetblue steelblue slategrey grey30 black"

for col in $Colors;
do
	[ -d $ThumbDir/$col.png ] || convert $FVWM_USERDIR/.tile.png -fill $col -colorize 100 $ThumbDir/$col.png

	echo "+ \"$col%$ThumbDir/$col.png%\" Exec exec \`xsetroot -solid $col && echo \"xsetroot -solid $col\"  > $FVWM_USERDIR/background.cfg \`"
done
