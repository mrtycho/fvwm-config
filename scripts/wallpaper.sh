#!/bin/sh
[ -d $1/.thumbs ] || mkdir $1/.thumbs
for pic in $1/*.*
do
    bname=` basename "$pic" `
    base=`echo $bname | sed s/\.[^\.]*$//`
    [ -f $1/.thumbs/$base.png ] || convert -quality 0 -resize 48 $pic $1/.thumbs/$base.png
    echo "+ %$1/.thumbs/$base.png%\"$base\" exec exec \`ln -sf $pic $1/.current--fvwm && fvwm-root --dither --retain-pixmap $1/$bname\`"
done

