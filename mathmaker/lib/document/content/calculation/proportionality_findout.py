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

from mathmakerlib.calculus import Table, Number

from mathmaker.lib.tools import closest_nn_outside_data
from mathmaker.lib.document.content import component
from mathmaker.lib.LaTeX import SlideContent, TabularCellPictureWording


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        super().setup("proportionality_nb_lines", build_data=build_data,
                      **options)
        if self.variant == 'default':
            self.variant = random.choice(['true', 'false'])
        if self.variant == 'true':
            self.answer = _('True')
        else:
            self.answer = _('False')
            if self.variant == 'false_additive':
                self.line2 = [Number(self.coeff.evaluate() + n)
                              .rounded(Number('1.00')).standardized()
                              for n in self.line1]
            else:
                i = random.randint(0, self.nb_nb - 1)
                err = closest_nn_outside_data(self.line1, i)
                wrong = self.coeff.evaluate() * err
                self.line2[i] = Number(wrong).rounded(Number('1.00'))\
                    .standardized()

        line1 = [r"\text{{{nb}}}".format(nb=n.printed) for n in self.line1]
        line2 = [r"\text{{{nb}}}".format(nb=n.printed) for n in self.line2]
        compact = not self.slideshow
        bl = {True: '10pt', False: None}[compact]
        self.table_question = Table([(n1, n2) for n1, n2 in zip(line1, line2)],
                                    compact=compact, baseline=bl)
        self.wording = _('This table is proportional. True or false?')
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
        return str(self.answer)

    def js_a(self, **kwargs):
        return [self.answer, self.answer.lower(), self.answer[0],
                self.answer[0].lower()]
