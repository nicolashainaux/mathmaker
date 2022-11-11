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

from mathmakerlib.LaTeX import TikZPicture, OptionsList


class SpreadsheetPicture(object):

    def __init__(self, variant, scheme, row1, row2, col1, col2, cell1, cell2,
                 cellnodeoptions='', coordoptions='', baseline='', scale=''):
        """
        :param variant: may be 1 or 2 (used to pick up the right tikz template)
        :type variant: int
        :param mode: whether 'default' or 'slideshow'
        :type mode: str
        """
        self.variant = variant
        self.scheme = scheme
        self.row1 = row1
        self.row2 = row2
        self.col1 = col1
        self.col2 = col2
        self.cell1 = cell1
        self.cell2 = cell2
        self.cellnodeoptions = cellnodeoptions
        self.coordoptions = coordoptions
        self.baseline = baseline
        self.scale = scale

    def __str__(self):
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
