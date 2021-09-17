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

from mathmakerlib.calculus import Number, Fraction

from mathmaker.lib import shared
from mathmaker.lib.tools import fix_math_style2_fontsize
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, **options):
        # build_data will bring a single int, that must match the denominator
        # of the fraction written as percentage: 20 for 1/5, 25 for 1/4,
        # 50 for 1/2, 75 for 3/4 etc.
        self.preset = options.get('preset', 'default')
        self.decimal_repr = Number(str(options.get('build_data')[0])) / 100
        self.fraction = Fraction(from_decimal=self.decimal_repr).reduced()
        choices = ['to_decimal', 'to_fraction']
        random.shuffle(choices)
        self.direction = choices.pop()
        self.transduration = 18

    def q(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        if self.direction == 'to_decimal':
            result = _('What is {} as a decimal?') \
                .format(fix_math_style2_fontsize(
                    shared.machine.write_math_style2(
                        self.fraction.printed)))
        else:
            result = _('What is {} as a simple fraction?') \
                .format(shared.machine.write_math_style2(
                    self.decimal_repr.printed))
        return result

    def a(self, **options):
        if self.direction == 'to_decimal':
            return shared.machine.write_math_style2(self.decimal_repr.printed)
        else:
            return fix_math_style2_fontsize(_('{}').format(
                shared.machine.write_math_style2(self.fraction.printed)))

    def js_a(self, **kwargs):
        if self.direction == 'to_decimal':
            return [self.decimal_repr.printed]
        else:
            nume = self.fraction.numerator
            deno = self.fraction.denominator
            f = f'{nume}/{deno}'
            return [f, 'any_decimal_fraction == ' + f]
