#!/bin/sh
thumbsDir=$FVWM_USERDIR/.thumbs/$(basename $1)
[ -d $thumbsDir ] || mkdir -p $thumbsDir
for pic in `ls $1/*.* | sort -V --ignore-case`
do
    bname=` basename "$pic" `
    base=`echo $bname | sed s/\.[^\.]*$//`
    [ -f $thumbsDir/$base.png ] || convert -quality 0 -resize 48 $pic $thumbsDir/$base.png
    echo "+ %$thumbsDir/$base.png%\"$base\" Exec exec \`echo \"fvwm-root --dither --retain-pixmap $1/$bname\" > $FVWM_USERDIR/background.cfg && fvwm-root --dither --retain-pixmap $1/$bname\`"
done

