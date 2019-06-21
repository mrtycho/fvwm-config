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
import argparse

from PIL import Image

fvwm_dir = os.path.expandvars('$FVWM_USERDIR')

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def thumbnail_entry(image_path,folder):
    filename,suffix = os.path.splitext(image_path)
    basename = os.path.basename(image_path)
    if (suffix=='.png'):
        try:
            pic = Image.open(image_path)
            thumbname = os.path.join(folder,basename)
            if not os.path.exists(thumbname):
                pic.thumbnail((48,48), Image.ANTIALIAS)
                pic.save(thumbname, "PNG")
            exec_s = 'fvwm-root --dither --retain-pixmap ' + image_path
            conf_s = 'echo "{0}" > {1}'.format(exec_s,os.path.join(fvwm_dir,'background.cfg'))
            print(('+ %{0}%"{1}" Exec exec "`{2} && {3}`"').format(thumbname,basename[:-4],conf_s,exec_s));
        except Exception:
            print ("cannot create thumbnail for", image_path)
    
parser = argparse.ArgumentParser(description='Process image folder for FVWM Backgrounds menu')
parser.add_argument('folder',
                   help='existing folder with background images')
parser.add_argument('-m', '--menu', metavar='name',
                   help='name of the menu')
parser.add_argument('-c', '--clean', action='store_true',
                   help='remove existing thumbnails')

args = parser.parse_args()

menu = 'Backgrounds' if not args.menu else args.menu

try: 
    path = os.path.abspath(args.folder);
    if not os.path.isdir(path):
        raise Exception()
    
except Exception:
    eprint('Argument "{}" is not a folder'.format(path))
    exit(-1)

thumb_path = os.path.join(path,'.thumbs')
try:
    if not os.path.exists(thumb_path):
        os.mkdir(thumb_path)
    elif args.clean:
        for entry in os.listdir(thumb_path):
            ftmp = os.path.join(thumb_path, entry)
            if os.path.isfile(ftmp):
                os.remove(os.path.join(thumb_path, entry))
        
except Exception:
    eprint('Unable to create thumbnail folder')
    exit(-1)
    
print ("DestroyMenu", menu)
print ("AddToMenu ", menu)

for entry in sorted(os.listdir(path)):
    file_path = os.path.join(path, entry)
    if os.path.isfile(file_path):
        thumbnail_entry(file_path,thumb_path)
       
print ("AddToMenu Background-Settings")
print ('+ "$[gt.Browse {0}]" Popup {0}'.format(menu))
            
exit(0)    

