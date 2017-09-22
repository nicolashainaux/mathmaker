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
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.base_calculus import Product


class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        nb_list = list(numbers_to_use)
        self.nb1, self.nb2 = random.sample(nb_list, 2)
        self.product = Product([self.nb1, self.nb2]).evaluate()
        self.transduration = 9

    def q(self, **options):
        # self.substitutable_question_mark = True
        return _('{q_mark} × {q_mark} = {n}\n\n'
                 '(in the multiplication tables, from 2 to 9)')\
            .format(n=Value(self.product).into_str(),
                    q_mark=COLORED_QUESTION_MARK)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        if self.product == 12:
            return _("{product1} or {product2}")\
                .format(product1=shared.machine.write_math_style2(
                        Product([2, 6]).printed),
                        product2=shared.machine.write_math_style2(
                        Product([3, 4]).printed))

        elif self.product == 16:
            return _("{product1} or {product2}")\
                .format(product1=shared.machine.write_math_style2(
                        Product([2, 8]).printed),
                        product2=shared.machine.write_math_style2(
                        Product([4, 4]).printed))

        elif self.product == 18:
            return _("{product1} or {product2}")\
                .format(product1=shared.machine.write_math_style2(
                        Product([2, 9]).printed),
                        product2=shared.machine.write_math_style2(
                        Product([3, 6]).printed))

        elif self.product == 24:
            return _("{product1} or {product2}")\
                .format(product1=shared.machine.write_math_style2(
                        Product([3, 8]).printed),
                        product2=shared.machine.write_math_style2(
                        Product([4, 6]).printed))

        elif self.product == 36:
            return _("{product1} or {product2}")\
                .format(product1=shared.machine.write_math_style2(
                        Product([6, 6]).printed),
                        product2=shared.machine.write_math_style2(
                        Product([4, 9]).printed))

        else:
            return shared.machine.write_math_style2(Product([self.nb1,
                                                             self.nb2])
                                                    .printed)
