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
import cgi
import gi
import re
gi.require_version('GMenu', '3.0')
from gi.repository import GMenu, GLib
from io import StringIO
import argparse

terminal = 'xterm -e'

def get_default_menu():
	prefix = os.environ.get('XDG_MENU_PREFIX', '')
	return prefix + 'applications.menu'

def getSystemMenuPath(file_id):
	for path in GLib.get_system_config_dirs():
		file_path = os.path.join(path, 'menus', file_id)
		if os.path.isfile(file_path):
			return file_path
	return None
	
def get_menu(name,title):
	return '\nDestroyMenu Popup_{0} \nAddToMenu Popup_{0} "{1}" Title'.format(name,title)
	
def get_menu_entry(name):
	return ' + "{0}"  Popup Popup_{0}'.format(name)
	
def get_app_entry(entry):
	me = re.compile('%[A-Z]?', re.I)
	app_info = entry.get_app_info()
	execStr = ''
	if requires_terminal(entry):	
		execStr += terminal + ' '
	execStr += me.sub('',app_info.get_string('Exec')) 
	return ' + "{0}"  Exec exec {1}'.format(cgi.escape(app_info.get_display_name()),execStr)
	
def requires_terminal(entry):
	term = entry.get_app_info().get_string('Terminal')
	return ( term is not None and term == 'true') 
	
def parse_folder(directory,mname):
	menu_str = StringIO()
	m_iter = directory.iter()
	item_type = m_iter.next()
	
	while item_type != GMenu.TreeItemType.INVALID:
		if item_type == GMenu.TreeItemType.DIRECTORY:
			entry = m_iter.get_directory()
			if not entry.get_is_nodisplay():
				name = cgi.escape(entry.get_name())
				menu_str.write(get_menu_entry(name))
				menu_str.write('\n')
				parse_folder(entry,name)
		elif item_type == GMenu.TreeItemType.ENTRY:
			entry = m_iter.get_entry()
			if not (entry.get_is_excluded() or entry.get_app_info().get_nodisplay()):
				menu_str.write(get_app_entry(entry))
				menu_str.write('\n')
		item_type = m_iter.next()
	print(get_menu(mname,cgi.escape(directory.get_name())))
	print(menu_str.getvalue())

parser = argparse.ArgumentParser(description='Generate application menu for FVWM2')
parser.add_argument('-d', '--desktop', metavar='desktop',
                   help='name of the desktop menu definiton (gnome,kde,xfce,lxde,...)')
parser.add_argument('-t', '--term', metavar='terminal',
                   help='terminal + execute flag (e.g. xterm -e)')
parser.add_argument('-n', '--name', metavar='Programs',
                   help='root menu name')

args = parser.parse_args()

basename = get_default_menu() if args.desktop is None else args.desktop + '-applications.menu'
if args.term:
	terminal = args.term
title = 'Programs' if not args.name else args.name

tree = GMenu.Tree.new(basename, GMenu.TreeFlags.SORT_DISPLAY_NAME)
if not tree.load_sync():
	raise ValueError("can not load menu tree {}".format(basename))
parse_folder(tree.get_root_directory(), title)

