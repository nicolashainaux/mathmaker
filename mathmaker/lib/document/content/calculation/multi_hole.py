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

from mathmakerlib.calculus import Fraction, Number

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.core.base_calculus import Item
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, hidden=None, **options):
        super().setup('numbers', nb=build_data, shuffle_nbs=False,
                      standardize_decimal_numbers=True, **options)
        if hidden is None:
            hidden = random.choice([1, 2])
        else:
            hidden = int(hidden)
        hole = Item(Value(COLORED_QUESTION_MARK))
        self.hidden_one = None
        visible_one = None
        # We know we'll get an integer as "result" (in ?×...=result)
        # so we round to integer to avoid trailing zeros (there are still some
        # though seldom)
        self.product = (self.nb1.evaluate() * self.nb2.evaluate())\
            .rounded(Number('1')).printed
        self.transduration = 9

        if isinstance(self.nb2, Fraction):
            self.hidden_one = self.nb2
            visible_one = self.nb1
        else:
            L = [self.nb1, self.nb2]
            random.shuffle(L)
            self.hidden_one = L.pop()
            visible_one = L.pop()

        factors = [visible_one, hole]
        if hidden == 1:
            # TODO: better use a Product (when it's available in mathmakerlib)
            self.holed_product = r' \times '.join([factors[1].printed,
                                                   factors[0].printed])
        elif hidden == 2:
            # TODO: better use a Product (when it's available in mathmakerlib)
            self.holed_product = r' \times '.join([factors[0].printed,
                                                   factors[1].printed])
        # self.holed_product.set_compact_display(False)

    def q(self, **options):
        self.substitutable_question_mark = True
        m_expr = '{} = {}'.format(self.holed_product, self.product)
        return _('{math_expr}') \
            .format(math_expr=shared.machine.write_math_style2(m_expr))

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return shared.machine.write_math_style2(self.hidden_one.printed)

    def js_a(self, **kwargs):
        if isinstance(self.hidden_one, Fraction):
            f = self.hidden_one.reduced().uiprinted
            return [f, 'any_fraction == ' + f]
        else:
            return [self.hidden_one.uiprinted]
