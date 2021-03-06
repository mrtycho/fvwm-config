#!/bin/bash

ThumbDir=$FVWM_USERDIR/.thumbs/colors
[ -d $ThumbDir ] || mkdir -p $ThumbDir

Colors="tan peru sienna maroon indianred orchid midnightblue steelblue slategrey grey30 cadetblue teal darkslategrey black"

for col in $Colors;
do
	[ -f $ThumbDir/$col.png ] || convert -size 32x32 xc:$col $ThumbDir/$col.png
	echo "+ \"$col%$ThumbDir/$col.png%\" Exec exec \`echo \"fvwm-root --dither --retain-pixmap $ThumbDir/$col.png\" > $FVWM_USERDIR/background.cfg && fvwm-root --dither --retain-pixmap $ThumbDir/$col.png\`"
done
