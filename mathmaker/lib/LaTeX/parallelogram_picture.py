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

from mathmakerlib import required
from mathmakerlib.LaTeX import TikZPicture, OptionsList


class ParallelogramPicture(object):

    def __init__(self, mode, layout, length_text, width_text, height_text,
                 baseline='', scale=''):
        """
        :param mode: whether 'any' or 'tabular'
        :type mode: str
        :param layout: number of the chosen layout (see tikz files for the
                       available ones)
        :type layout: int
        """
        self.mode = mode
        self.layout = layout
        self.length_text = length_text
        self.width_text = width_text
        self.height_text = height_text
        self.baseline = baseline
        self.scale = scale

    def __str__(self):
        required.package['tikz'] = True
        template_name = \
            f'templates/spreadsheet_{self.variant}_{self.scheme}.tikz'
        content = (Path(__file__).parent / template_name).read_text()
        row1 = r'\text{{{r1}}}'.format(r1=self.row1)
        row2 = r'\text{{{r2}}}'.format(r2=self.row2)
        content = content.replace('ROW1', row1).replace('ROW2', row2)
        col1 = r'\text{{{c1}}}'.format(c1=self.col1)
        col2 = r'\text{{{c2}}}'.format(c2=self.col2)
        content = content.replace('COL1', col1).replace('COL2', col2)
        content = content.replace('CELL1', self.cell1)\
            .replace('CELL2', self.cell2)
        content = content.replace('CELLNODEOPTIONS',
                                  str(OptionsList(self.cellnodeoptions)))
        content = content.replace('COORDOPTIONS',
                                  str(OptionsList(self.coordoptions)))
        pic_options = []
        if self.baseline:
            pic_options.append({'baseline': self.baseline})
        if self.scale:
            pic_options.append({'scale': self.scale})
        return str(TikZPicture(content, *pic_options))
