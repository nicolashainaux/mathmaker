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

from mathmakerlib.calculus import Number, Fraction, prime_factors
from mathmakerlib.geometry import Point, DividedLineSegment

from mathmaker.lib import shared
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        """

        :param build_data: either two numbers (will be numerator and
        denominator of the fraction) or three numbers, the first being then a
        coefficient to multiply both others by.
        """
        if len(build_data) == 3:
            build_data = (Number(build_data[0]) * Number(build_data[1]),
                          Number(build_data[0]) * Number(build_data[2]))
        elif len(build_data) != 2:
            raise ValueError('Need either 2, or 3 numbers to build this '
                             'question.')
        super().setup('minimal', **options)
        super().setup('numbers', nb=build_data, shuffle_nbs=False,
                      **options)
        # We must have nb1 < nb2 in order to build the DividedLineSegment:
        if self.nb1 > self.nb2:
            self.nb1, self.nb2 = self.nb2, self.nb1
        self.transduration = 8
        if self.nb2 >= 5:
            self.transduration += 2 * (self.nb2 - 5)
        fc = next(shared.dvipsnames_selection_source)[0]
        self.dividedlinesegment = DividedLineSegment(Point(0, 0, 'A'),
                                                     Point(10, 0, 'B'),
                                                     n=self.nb2, fill=self.nb1,
                                                     fillcolor=fc)
        self.dividedlinesegment.scale = Number('0.6')
        self.dividedlinesegment.baseline = '4pt'
        self.wording = _('Which fraction of the line segment represents '
                         'the colored part?')
        self.fraction = f = Fraction(self.nb1, self.nb2)
        if f.is_reducible():
            f1 = f.reduce()
            if isinstance(f1, Fraction) and f1.is_reducible():
                f2 = f1.reduce()
                lpcd = prime_factors(gcd(int(f.numerator), int(f.denominator)))
                if isinstance(f2, Fraction) and f2.is_reducible():
                    self.answer_wording = _('{} (or {}, or {}...)') \
                        .format(shared.machine.write_math_style2(f.printed),
                                shared.machine.write_math_style2(f1.printed),
                                shared.machine.write_math_style2(f2.printed))
                elif lpcd[0] != lpcd[1]:
                    f3 = f.reduced_by(lpcd[1])
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
        else:
            self.answer_wording = shared.machine.write_math_style2(f.printed)

    def q(self, **options):
        if options.get('x_layout_variant', 'default') == 'slideshow':
            return self.dividedlinesegment.drawn + '\n' + self.wording
        else:
            return shared.machine.write_layout(
                (1, 2),
                [6.25, 6.75],
                [self.dividedlinesegment.drawn, self.wording],
                justify=['left', 'center'])

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.answer_wording

    def js_a(self, **kwargs):
        f = self.fraction.reduced().uiprinted
        return [f, 'any_fraction == ' + f]
