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

from math import gcd
#
from mathmaker.lib import shared
from mathmaker.lib.tools import fix_math_style2_fontsize
from mathmaker.lib.tools.maths import prime_factors
from mathmaker.lib.core.base_calculus import Item, Fraction
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        if len(build_data) == 3:
            build_data = build_data[0:2] \
                + (build_data[0], ) + (build_data[2], )
        super().setup('minimal', **options)
        super().setup('numbers', nb=build_data, shuffle_nbs=False,
                      **options)
        # nb3 * nb4 will be the greatest product
        if self.nb1 * self.nb2 > self.nb3 * self.nb4:
            self.nb1, self.nb2, self.nb3, self.nb4 = \
                self.nb3, self.nb4, self.nb1, self.nb2
        self.transduration = 12
        if self.nb3 * self.nb4 > 25:
            self.transduration = 20
        if self.nb3 * self.nb4 > 40:
            self.transduration = 30
        super().setup('rectangle_grid', **options)
        self.wording = _('Which fraction of the figure matches '
                         'the greyed part?')
        self.fraction = f = Fraction(('+',
                                      Item(self.nb1 * self.nb2),
                                      Item(self.nb3 * self.nb4)))
        if f.is_reducible():
            f1 = f.minimally_reduced(ignore_1_denominator=True)
            if f1.is_reducible():
                f2 = f1.minimally_reduced(ignore_1_denominator=True)
                lpcd = prime_factors(gcd(int(f.numerator.evaluate()),
                                         int(f.denominator.evaluate())))
                if f2.is_reducible():
                    self.answer_wording = _('{} (or {}, or {}...)') \
                        .format(shared.machine.write_math_style2(f.printed),
                                shared.machine.write_math_style2(f1.printed),
                                shared.machine.write_math_style2(f2.printed))
                elif lpcd[0] != lpcd[1]:
                    f3 = f.reduced_by(lpcd[1], ignore_1_denominator=True)
                    self.answer_wording = _('{} (or {}, or {}, or {})') \
                        .format(shared.machine.write_math_style2(f.printed),
                                shared.machine.write_math_style2(f1.printed),
                                shared.machine.write_math_style2(f3.printed),
                                shared.machine.write_math_style2(f2.printed))
                else:
                    self.answer_wording = _('{} (or {}, or {})') \
                        .format(shared.machine.write_math_style2(f.printed),
                                shared.machine.write_math_style2(f1.printed),
                                shared.machine.write_math_style2(f2.printed))
            else:
                self.answer_wording = _('{} (or {})') \
                    .format(shared.machine.write_math_style2(f.printed),
                            shared.machine.write_math_style2(f1.printed))
            self.answer_wording = fix_math_style2_fontsize(self.answer_wording)
        else:
            self.answer_wording = shared.machine.write_math_style2(f.printed)
            self.answer_wording = fix_math_style2_fontsize(self.answer_wording)

    def q(self, **options):
        if options.get('x_layout_variant', 'default') == 'slideshow':
            self.rectangle_grid.scale = 0.5
            return self.rectangle_grid.drawn + '\n\n' + self.wording
        else:
            self.rectangle_grid.scale = 0.4
            return shared.machine.write_layout(
                (1, 2),
                [5, 8],
                [self.rectangle_grid.drawn, self.wording],
                center_vertically=True)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.answer_wording

    def js_a(self, **kwargs):
        f = self.fraction.completely_reduced().jsprinted
        return [f, 'any_fraction == ' + f]
