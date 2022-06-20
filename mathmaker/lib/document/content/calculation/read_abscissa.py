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
from decimal import ROUND_DOWN

from mathmakerlib.geometry import XAxis
from mathmakerlib.calculus import Fraction
from mathmakerlib.calculus import Number

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import setup_wording_format_of
# from mathmaker.lib.tools.wording import post_process


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        """
        :param build_data: pair of numbers (a, b).
        :type build_data: tuple
        """
        super().setup("minimal", **options)
        super().setup("numbers", nb=build_data, shuffle_nbs=False, **options)
        self.transduration = 20
        start_at_zero = options.get('start_at_zero', 'false')
        start_at_zero = {'true': True, 'false': False}[start_at_zero]
        self.point_name = next(shared.uppercase_letters_source)[0]

        self.answer = Fraction(self.nb1, self.nb2)
        deci_value = Number(self.answer.evaluate()).rounded(Number('1.000'))
        floor = deci_value.rounded(Number('1'), rounding=ROUND_DOWN)

        # default amplitude between mini and maxi values
        amplitude = 3
        if 3 <= self.nb2 <= 5:
            amplitude = 2
        elif self.nb2 >= 6:
            amplitude = 1

        mini = random.choice([floor, floor - 1])
        if start_at_zero or mini < 0:
            mini = 0

        maxi = mini + amplitude

        if deci_value >= (maxi + 2 / self.nb2):
            maxi += 1

        self.xaxis = XAxis(mini, maxi, length=8, subdivisions=self.nb2,
                           points_def=[(deci_value, self.point_name)])
        self.xaxis.baseline = '-6pt'

        # This default wording is meant for mental calculation.
        self.wording = _('Abscissa of {point_name}?')
        setup_wording_format_of(self)

    def q(self, **options):
        if self.slideshow:
            return r'{}\par {}'\
                .format(self.wording.format(**self.wording_format),
                        self.xaxis.drawn)
        else:
            return shared.machine.write_layout(
                (1, 2), [8.5, 4.5],
                [self.xaxis.drawn, self.wording.format(**self.wording_format)],
                justify=['left', 'center'])
        # return post_process(self.wording.format(**self.wording_format))

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        answer = shared.machine.write_math_style2(self.answer.printed)
        deci_value = self.answer.evaluate()
        if deci_value.fracdigits_nb() <= 3:
            answer += _(' (or {})').format(deci_value.printed)
        return answer

    def js_a(self, **kwargs):
        answers = []
        deci_value = self.answer.evaluate()
        if deci_value.fracdigits_nb() <= 3:
            answers = [deci_value.uiprinted]
        f = self.answer.uiprinted
        answers.append(f)
        answers.append('any_fraction == ' + f)
        return answers
