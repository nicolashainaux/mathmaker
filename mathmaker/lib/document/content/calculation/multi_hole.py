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

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.core.base_calculus import Product, Item, Fraction
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.calculus import Equality


class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        nb_list = list(numbers_to_use)
        hole = Item(Value(COLORED_QUESTION_MARK))
        self.hidden_one = None
        visible_one = None
        self.product = Item(Product([nb_list[0], nb_list[1]]).evaluate())
        self.transduration = 9

        if isinstance(nb_list[1], Fraction):
            self.hidden_one = nb_list[1]
            visible_one = nb_list[0]
        else:
            random.shuffle(nb_list)
            nb1 = nb_list.pop()
            nb2 = nb_list.pop()
            nb_list = [nb1, nb2]
            self.hidden_one = Item(nb_list.pop())
            visible_one = nb_list.pop()

        factors = [visible_one, hole]
        random.shuffle(factors)
        self.holed_product = Product([factors.pop(), factors.pop()])
        self.holed_product.set_compact_display(False)

    def q(self, **options):
        self.substitutable_question_mark = True
        m_expr = Equality([self.holed_product, self.product]).printed
        return _('{math_expr}') \
            .format(math_expr=shared.machine.write_math_style2(m_expr))

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return shared.machine.write_math_style2(self.hidden_one.printed)
