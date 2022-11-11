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

import random

from mathmakerlib.calculus import Table

from mathmaker.lib.document.content import component
from mathmaker.lib.tools import deci_and_frac_repr
from mathmaker.lib.LaTeX import SlideContent, TabularCellPictureWording


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        super().setup("proportionality_nb_lines", build_data=build_data,
                      **options)
        row1 = [r"\text{{{nb}}}".format(nb=n.printed) for n in self.line1]
        row2 = [r"\text{{{nb}}}".format(nb=n.printed) for n in self.line2]
        hidden_row = int(options.get('hidden_row', random.choice([0, 1])))
        hidden_col = int(options.get('hidden_col',
                                     random.randint(0, len(row2) - 1)))
        self.answer = [self.line1, self.line2][hidden_row][hidden_col]
        [row1, row2][hidden_row][hidden_col] = \
            r'\textcolor{BrickRed}{\text{?}}'
        compact = not self.slideshow
        bl = {True: '3pt', False: None}[compact]
        self.table_question = Table([(n1, n2) for n1, n2 in zip(row1, row2)],
                                    compact=compact, baseline=bl)
        self.wording = _('Fill this proportional table.')
        self.transduration = 30

    def q(self, **options):
        if self.slideshow:
            output = SlideContent(wording1=self.wording,
                                  picture=self.table_question.printed,
                                  height1='2.5pt')
        else:
            output = TabularCellPictureWording(self.table_question.printed,
                                               self.wording)
        return str(output)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return deci_and_frac_repr(self.answer)

    def js_a(self, **kwargs):
        return deci_and_frac_repr(self.answer, output='js')
