#!/bin/bash

ThumbDir=$HOME/.fvwm/.thumbs
[ -d $ThumbDir ] || mkdir $ThumbDir

Colors="tan peru sienna olivedrab midnightblue cadetblue steelblue slategrey grey30"

for col in $Colors;
do
	[ -d $ThumbDir/$col.png ] || convert $HOME/.fvwm/images/tile.png -fill $col -colorize 100 $ThumbDir/$col.png

	echo "+ \"$col%$ThumbDir/$col.png%\" Exec exec xsetroot -solid $col"
done
