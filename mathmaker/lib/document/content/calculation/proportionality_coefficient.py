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

from mathmakerlib.calculus import Table

from mathmaker.lib.document.content import component
from mathmaker.lib.tools import deci_and_frac_repr


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        super().setup("proportionality_nb_lines", build_data=build_data,
                      **options)
        line1 = [r"\text{{{nb}}}".format(nb=n.printed) for n in self.line1]
        line2 = [r"\text{{{nb}}}".format(nb=n.printed) for n in self.line2]
        compact = not self.slideshow
        bl = {True: 3, False: None}[compact]
        self.table_question = Table([(n1, n2) for n1, n2 in zip(line1, line2)],
                                    bubble_value='?', bubble_color='BrickRed',
                                    compact=compact, baseline=bl)
        self.wording = _('Coefficient of this proportional table?')
        self.transduration = 30

    def q(self, **options):
        if self.slideshow:
            template_name = 'templates/slide_picture_wording.tex'
        else:
            template_name = 'templates/inline_picture_wording.tex'
        template = (Path(__file__).parent / template_name).read_text()
        template = template.replace('PICTURE', self.table_question.printed)\
            .replace('WORDING', self.wording)
        if self.slideshow:
            return template.replace('HEIGHT', '2.5')
        else:
            return template.replace('COLW1', '5').replace('COLW2', '8')

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return deci_and_frac_repr(self.coeff)

    def js_a(self, **kwargs):
        return deci_and_frac_repr(self.coeff, output='js')
