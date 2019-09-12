# fvwm_menugen.py
#
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
import html
import gi
import re
import sys
gi.require_version('GMenu', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GMenu, GLib
from io import BytesIO
import argparse

terminal = 'xterm -e'
use_icons = False
icon_size = 16

def get_default_menu():
	prefix = os.environ.get('XDG_MENU_PREFIX', '')
	return prefix + 'applications.menu'

def get_system_menupath(file_id):
	for path in GLib.get_system_config_dirs():
		file_path = os.path.join(path, 'menus', file_id)
		if os.path.isfile(file_path):
			return file_path
	return None

def get_icon(gicon):
	if not use_icons:
		return None
	if not gicon:
		return None
	theme = Gtk.IconTheme.get_default()
	icon_info = theme.lookup_by_gicon(gicon, icon_size, 0)
	if icon_info is None:
		return None
	filename,suffix = os.path.splitext(icon_info.get_filename())
	if suffix=='.svg' or suffix=='.svgz':
		return icon_info.get_filename()+':{0}x{0}'.format(str(icon_size))
	if filename.find(str(icon_size)) == -1:
		return None

	return filename + suffix

def get_menu_icon(directory):
	return get_icon(directory.get_icon())
        
def get_app_icon(entry):
	return get_icon(entry.get_app_info().get_icon())

def get_menu(menu_id,title):
	return '\nDestroyMenu Popup_{0} \nAddToMenu Popup_{0} "{1}" Title'.format(menu_id,title)
	
def get_menu_entry(menu_id, name, directory):
	icon = get_menu_icon(directory)
	if not icon: 
		return ' + "{0}"  Popup Popup_{1}'.format(name,menu_id)
	return ' + %{0}%"{1}"  Popup Popup_{2}'.format(icon,name,menu_id)
	
def get_app_entry(entry):
	me = re.compile('%[A-Z]?', re.I)
	app_info = entry.get_app_info()
	execStr = ''
	if requires_terminal(entry):	
		execStr += terminal + ' '
	execStr += me.sub('',app_info.get_string('Exec'))
	icon = get_app_icon(entry)
	app_name = app_info.get_display_name().replace('&','&&')
	if not icon: 
		return ' + "{0}"  Exec exec {1}'.format(app_name,execStr)
	return ' + %{0}%"{1}"  Exec exec {2}'.format(icon,app_name,execStr)
	
def requires_terminal(entry):
	term = entry.get_app_info().get_string('Terminal')
	return ( term is not None and term == 'true') 
	
def parse_folder(directory,mname):
	menu_str = BytesIO()
	encoding = sys.stdin.encoding
	m_iter = directory.iter()
	item_type = m_iter.next()
	
	while item_type != GMenu.TreeItemType.INVALID:
		if item_type == GMenu.TreeItemType.DIRECTORY:
			entry = m_iter.get_directory()
			if not entry.get_is_nodisplay():
				m_id = entry.get_menu_id()
				name = html.escape(entry.get_name())
				menu_str.write(get_menu_entry(m_id,name,entry).encode(encoding,'ignore'))
				menu_str.write(b'\n')
				parse_folder(entry,m_id)
		elif item_type == GMenu.TreeItemType.SEPARATOR:
			menu_str.write(b' + ""  Nop\n')
		elif item_type == GMenu.TreeItemType.ENTRY:
			entry = m_iter.get_entry()
			if not (entry.get_is_excluded() or entry.get_app_info().get_nodisplay()):
				menu_str.write(get_app_entry(entry).encode(encoding,'ignore'))
				menu_str.write(b'\n')
		item_type = m_iter.next()
	print(get_menu(mname,html.escape(directory.get_name())))
	print(menu_str.getvalue().decode(encoding))
	menu_str.close()

parser = argparse.ArgumentParser(description='Generate application menu for FVWM2')
parser.add_argument('-d', '--desktop', metavar='desktop',
                   help='name of the desktop menu definiton (gnome,kde,xfce,lxde,...)')
parser.add_argument('-t', '--term', metavar='terminal',
                   help='terminal + execute flag (e.g. xterm -e)')
parser.add_argument('-n', '--name', metavar='Programs',
                   help='root menu name')
parser.add_argument('-i', '--icons', action='store_true',
                   help='show icons')
parser.add_argument('-s', '--size', metavar='pixel', type=int,
                   help='icon size (e.g. 16)')

args = parser.parse_args()

basename = get_default_menu() if args.desktop is None else args.desktop + '-applications.menu'
if args.term:
	terminal = args.term
title = 'Programs' if not args.name else args.name

use_icons = args.icons

if args.size:
	icon_size = args.size

tree = GMenu.Tree.new(basename, GMenu.TreeFlags.SORT_DISPLAY_NAME)

if not tree.load_sync():
	raise ValueError("can not load menu tree {}".format(basename))
parse_folder(tree.get_root_directory(), title)
print('+ "" Nop')
print('+ "$[gt.Refresh]" CreateAppMenu')
