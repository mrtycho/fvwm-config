#!/bin/sh
[ -d $1/.thumbs ] || mkdir $1/.thumbs
for pic in `ls $1/*.* | sort -V --ignore-case`
do
    bname=` basename "$pic" `
    base=`echo $bname | sed s/\.[^\.]*$//`
    [ -f $1/.thumbs/$base.png ] || convert -quality 0 -resize 48 $pic $1/.thumbs/$base.png
    echo "+ %$1/.thumbs/$base.png%\"$base\" Exec exec \`echo \"fvwm-root --dither --retain-pixmap $1/$bname\" > $FVWM_USERDIR/background.cfg && fvwm-root --dither --retain-pixmap $1/$bname\`"
done

