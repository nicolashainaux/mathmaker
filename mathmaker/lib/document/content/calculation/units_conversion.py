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
from decimal import Decimal

from mathmaker.lib import shared
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.base_calculus import Item
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.document.content import component
from mathmaker.lib.tools import difference_of_orders_of_magnitude
from mathmaker.lib.tools.database import generate_random_decimal_nb


class sub_object(component.structure):

    def __init__(self, numbers_to_use, **options):
        super().setup('minimal', **options)
        self.transduration = 10
        # if (self.nb1 > 20 and self.nb2 > 20
        #     and not self.nb1 % 10 == 0 and not self.nb2 % 10 == 0):
        #     self.transduration = 12
        unit1, unit2, direction, physical_quantity, level = numbers_to_use
        start_ranks = [Decimal('10'), Decimal('1'), Decimal('0.1')]
        if difference_of_orders_of_magnitude(unit1, unit2) >= Decimal('100'):
            start_ranks = [Decimal('1'), Decimal('0.1'), Decimal('0.01')]
        if difference_of_orders_of_magnitude(unit1, unit2) <= Decimal('0.01'):
            start_ranks = [Decimal('100'), Decimal('10'), Decimal('1')]
        start_rank = random.choice(start_ranks)
        chosen_deci = \
            generate_random_decimal_nb(start_rank,
                                       width=random.choice([1, 2, 3]),
                                       unique_figures=options.get(
                                           'unique_figures', False),
                                       generation_type='default')
        self.start_nb = Item(Value(chosen_deci), unit=unit1)
        self.hidden_nb = Item(Value(COLORED_QUESTION_MARK), unit=unit2)
        self.answer = self.start_nb.convert_to(unit2)\
            .into_str(display_unit=True, force_expression_begins=True)
        self.wording = '{} = {}'.format(
            self.start_nb.into_str(display_unit=True,
                                   force_expression_begins=True),
            self.hidden_nb.into_str(display_unit=True,
                                    force_expression_begins=True))

    def q(self, **options):
        return shared.machine.write_math_style2(self.wording)

    def a(self, **options):
        return shared.machine.write_math_style2(self.answer)
