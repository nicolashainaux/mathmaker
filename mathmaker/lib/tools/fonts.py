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

import subprocess
from tempfile import TemporaryFile


def create_list(fonts_list_file='mathmaker/data/fonts_list.txt',
                datadir='mathmaker/data',
                force=False) -> tuple:
    """
    Store in a file the list of the fonts available for lualatex.
    """
    if force:
        return []
    with TemporaryFile() as tmp_file:
        p = subprocess.Popen('luaotfload-tool --list "*"',
                             shell=True,
                             stdout=tmp_file)
        p.wait()
        tmp_file.seek(0)
        with open(fonts_list_file, mode='wt') as f:
            for line in tmp_file.readlines():
                if not line.startswith(b'luaotfload') and line[:-1]:
                    f.write(line.decode('utf-8').lower())
    return [(datadir, [fonts_list_file])]
