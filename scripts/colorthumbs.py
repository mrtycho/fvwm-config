# Copyright (C) 2019 Stefan Mayer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from PIL import Image

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def create_color(col):
   path = os.path.join(thumb_dir,col+'.png')
   if not os.path.exists(path):           
      try:
         Image.new('RGB', (32,32), color = col).save(path,'PNG')
      except Exception:
         eprint('Unable to create color {0}'.format(col))
         return ""
   return path

fvwm_dir = os.path.expandvars('$FVWM_USERDIR')
thumb_dir = os.path.join(fvwm_dir,'.thumbs')
if not os.path.exists(thumb_dir):
   os.mkdir(thumb_dir)

acolors = ['Tan', 'Peru', 'Sienna', 'IndianRed', 'SteelBlue', 'Slategrey', 'Gray', 'DarkGray', 'LightGray', 'CadetBlue', 'Teal', 'DarkSlateGray', 'Black']

for col in acolors:
   col_file = create_color(col)
   if col_file:
      exec_s = 'fvwm-root --retain-pixmap ' + col_file
      conf_s = 'echo "{0}" > $FVWM_USERDIR/background.cfg'.format(exec_s,os.path.join(fvwm_dir,'background.cfg'))      
      print('+ %{0}%"{1}" Exec exec "`{2} && {3}`"'.format(col_file,col,conf_s,exec_s))

