#!/bin/bash

for folder in `ls -d $1/* | sort -V --ignore-case`
do
    if [ -d "$folder" ]; then
        theme="`basename $folder`"
        echo "+ \"${theme^}\" Function SetFVWMTheme $theme"
    fi
done

