#!/bin/bash

ThumbDir=$FVWM_USERDIR/.thumbs
[ -d $ThumbDir ] || mkdir $ThumbDir

Colors="tan peru sienna indianred olivedrab midnightblue steelblue slategrey grey30 cadetblue teal darkslategrey black"

for col in $Colors;
do
	 [ -f $ThumbDir/$col.png ] || convert -size 32x32 xc:$col $ThumbDir/$col.png
	echo "+ \"$col%$ThumbDir/$col.png%\" Exec exec \`xsetroot -solid $col && echo \"xsetroot -solid $col\"  > $FVWM_USERDIR/background.cfg \`"
done
