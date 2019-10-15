include(`forloop.m4')dnl
divert(-1)
define(`CONCAT',`$1$2')dnl
define(`SET_COLOR', format(%s:	COLOR_%s
,`$1',`$2'))dnl
divert`'dnl
! Xresources
!-----------

*.foreground: FOREGROUND
*.background: BACKGROUND

Xft*antialias: true
Xft*hinting: true

! Common colors
forloop(`i',`0',`15', `SET_COLOR(CONCAT(*.color,i),i)')dnl

! xterm
!-------

! Use a nice truetype font and size by default... 
xterm*faceName: DejaVu Sans Mono for Powerline 
xterm*faceSize: 11

*customization: -color
xterm*termName:  xterm-256color

! Every shell is a login shell by default (for inclusion of all necessary environment variables)
xterm*loginshell: true

! I like a LOT of scrollback...
xterm*savelines: 16384

! double-click to select whole URLs :D
xterm*charClass: 33:48,36-47:48,58-59:48,61:48,63-64:48,95:48,126:48

xterm*foreground:   FOREGROUND
xterm*background:   BACKGROUND

! xterm colors
forloop(`i',`0',`15', `SET_COLOR(CONCAT(xterm*color,i),i)')dnl
