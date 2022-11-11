# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

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

from pathlib import Path


class TabularCellPictureWording(object):

    def __init__(self, picture, wording, w1=5, w2=8):
        self.picture = picture
        self.wording = wording
        self.w1 = str(w1)
        self.w2 = str(w2)

    def __str__(self):
        content = (Path(__file__).parent
                   / 'templates/tabular_cell_picture_wording.tex').read_text()
        content = content.replace('COLW1', self.w1)
        content = content.replace('COLW2', self.w2)
        content = content.replace('PICTURE', self.picture)
        content = content.replace('WORDING', self.wording)
        return content
