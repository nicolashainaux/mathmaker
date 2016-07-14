# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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

import polib

from mathmaker import settings


def retrieve(language, po_filename):
    po = polib.pofile(settings.localedir
                      + settings.language
                      + "/LC_MESSAGES/"
                      + po_filename
                      + ".po")
    return [entry.msgstr for entry in po if entry.msgstr != ""]


def get_list_of(what, language, arg):
    what_map = {"words": "w" + str(arg) + "l",
                "names": str(arg) + "_names"}
    output = retrieve(language, what_map[what])
    if len(output) < 20:
        output.append(retrieve('en', what_map[what]))
    return output
