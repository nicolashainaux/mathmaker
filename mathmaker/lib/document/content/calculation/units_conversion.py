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
from operator import xor
from decimal import Decimal

from mathmakerlib.calculus import difference_of_orders_of_magnitude
from mathmakerlib.calculus import Number, Unit, physical_quantity

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.database import generate_random_decimal_nb
from mathmaker.lib.tools.wording import post_process
from mathmaker.lib.tools.wording import setup_wording_format_of


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup('minimal', **options)
        # if (self.nb1 > 20 and self.nb2 > 20
        #     and not self.nb1 % 10 == 0 and not self.nb2 % 10 == 0):
        #     self.transduration = 12
        unit1, unit2, direction, category, level, dimension = build_data
        self.transduration = {1: 20, 2: 25, 3: 25}.get(int(level), 30)
        unit1 = Unit(unit1)
        unit2 = Unit(unit2)
        if physical_quantity(unit1) == 'length' and dimension != 1:
            self.length_unit1 = unit1.content
            unit1 = Unit(unit1.content, exponent=dimension)
        if physical_quantity(unit2) == 'length' and dimension != 1:
            self.length_unit2 = unit2.content
            unit2 = Unit(unit2.content, exponent=dimension)
        if xor(hasattr(self, 'length_unit1'), hasattr(self, 'length_unit2')):
            if hasattr(self, 'length_unit1'):
                self.length_unit = getattr(self, 'length_unit1')
            else:
                self.length_unit = getattr(self, 'length_unit2')
        start_position = [Decimal('10'), Decimal('1'), Decimal('0.1')]
        if difference_of_orders_of_magnitude(unit1, unit2) >= Decimal('100'):
            start_position = [Decimal('1'), Decimal('0.1'), Decimal('0.01')]
        if difference_of_orders_of_magnitude(unit1, unit2) <= Decimal('0.01'):
            start_position = [Decimal('100'), Decimal('10'), Decimal('1')]
        sp = random.choice(start_position)
        nb1 = \
            generate_random_decimal_nb(position=sp,
                                       width=random.choice([1, 2, 3]),
                                       unique_figures=options.get(
                                           'unique_figures', False),
                                       generation_type='default')[0]
        super().setup('numbers',
                      nb=[Number(nb1),  # self.nb1
                          Number(Number(nb1,
                                        unit=unit1).converted_to(unit2),
                                 unit=None)  # self.nb2
                          ],
                      shuffle_nbs=False, standardize_decimal_numbers=True)
        self.answer = Number(self.nb2, unit=unit2).printed
        self.js_answer = self.nb2.uiprinted
        phq1 = physical_quantity(unit1)
        phq2 = physical_quantity(unit2)
        suffix1 = suffix2 = ''
        if phq1 == phq2:
            suffix1 = '1'
            suffix2 = '2'
        unit1_attr_name = phq1 + '_unit' + suffix1
        unit2_attr_name = phq2 + '_unit' + suffix2
        hint = ' |hint:{}_unit{}|'.format(phq2, suffix2)
        setattr(self, unit1_attr_name, unit1)
        setattr(self, unit2_attr_name, unit2)
        self.wording = '{{nb1}} {{{u1}}} = QUESTION_MARK~{{{u2}}}{h}'\
            .format(u1=unit1_attr_name, u2=unit2_attr_name, h=hint)
        setup_wording_format_of(self)

    def q(self, **options):
        return post_process(self.wording.format(**self.wording_format))\
            .replace('QUESTION_MARK', COLORED_QUESTION_MARK)

    def a(self, **options):
        return shared.machine.write_math_style2(self.answer)

    def js_a(self, **kwargs):
        return [self.js_answer]
