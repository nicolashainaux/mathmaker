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

# import random
#
from mathmaker.lib import shared
from mathmaker.lib.tools import fix_math_style2_fontsize
from mathmaker.lib.tools.maths import gcd, prime_factors
from mathmaker.lib.core.base_calculus import Item, Fraction
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, numbers_to_use, **options):
        if len(numbers_to_use) == 3:
            numbers_to_use = numbers_to_use[0:2] \
                + (numbers_to_use[0], ) + (numbers_to_use[2], )
        super().setup('minimal', **options)
        super().setup('numbers', nb=numbers_to_use, shuffle_nbs=False,
                      **options)
        # nb3 * nb4 will be the greatest product
        if self.nb1 * self.nb2 > self.nb3 * self.nb4:
            self.nb1, self.nb2, self.nb3, self.nb4 = \
                self.nb3, self.nb4, self.nb1, self.nb2
        super().setup('rectangle_grid', **options)
        self.wording = _('Which fraction of the figure matches '
                         'the greyed part?')
        f = Fraction(('+',
                      Item(self.nb1 * self.nb2),
                      Item(self.nb3 * self.nb4)))
        if f.is_reducible():
            f1 = f.minimally_reduced(ignore_1_denominator=True)
            if f1.is_reducible():
                f2 = f1.minimally_reduced(ignore_1_denominator=True)
                lpcd = prime_factors(gcd(f.numerator.evaluate(),
                                         f.denominator.evaluate()))
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
            self.answer_wording = shared.machine.write_math_style1(f.printed)

    def q(self, **options):
        return shared.machine.write_layout(
            (1, 2),
            [5, 8],
            [shared.machine.insert_picture(
             self.rectangle_grid,
             scale=0.4,
             vertical_alignment_in_a_tabular=True),
             self.wording])

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.answer_wording
