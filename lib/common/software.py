# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

# This file is part of Mathmaker.

# Mathmaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Mathmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys

# DATA RELATING TO THE SOFTWARE
NAME = "mathmaker"
NAME_PRINTABLE = "Mathmaker"
VERSION = "0.5 (alpha)"
LICENSE = "GNU GPL 3"
AUTHOR = "Nicolas Hainaux <nico_h@users.sourceforge.net>"
COPYRIGHT = "Copyright 2006-2014"
WEBSITE = "http://mathmaker.sourceforge.net"

__cwd = os.path.abspath(sys.argv[0])
ROOT_PATH = __cwd[:__cwd.find(NAME)+len(NAME)] + '/'

CFG_FILE_SUFFIX = 'cfg'
