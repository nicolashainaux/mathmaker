# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

import os
import sys

from core import *
from core.base_calculus import *

from maintenance.autotest import common

check = common.check


def action():
    if common.verbose:
        os.write(common.output, "--- SUMS' REDUCTION\n")

    monomial_3x = Monomial(('+', 3, 1))
    monomial_5x2 = Monomial(('+', 5, 2))
    monomial_minus2x = Monomial(('-', 2, 1))
    item_4 = Item(4)
    item_2 = Item(2)
    product_ab = Product([Item('-a'), Item('b')])
    product_2ab = Product([Item(2), Item('a'), Item('b')])
    product_minus7ab = Product([Item(-7), Item('a'), Item('b')])
    #product_ab.set_compact_display(True)
    #product_2ab.set_compact_display(True)
    #product_minus7ab.set_compact_display(True)
    sum_testing = Sum([monomial_3x, monomial_5x2, product_minus7ab])
    #sum_testing.set_exponent(2)
    sum_to_reduce = Sum([monomial_3x,
                         item_4,
                         sum_testing,
                         product_ab,
                         monomial_5x2,
                         item_2,
                         monomial_minus2x,
                         product_2ab])

    polynomial_rubbish = Polynomial([Monomial(('+',1,2)),
                                     Monomial(('+',7,1)),
                                     Monomial(('-',10,2)),
                                     Monomial(('-',9,1)),
                                     Monomial(('+',9,2))])

    check(sum_to_reduce,
         ["3x+4+3x+5x^{2}-7ab-ab+5x^{2}+2-2x+2ab"])

    check(sum_to_reduce.intermediate_reduction_line(),
         ["(3+3-2)x+4+2+(5+5)x^{2}+(-7-1+2)ab"])

    check(sum_to_reduce.reduce_(),
         ["4x+6+10x^{2}-6ab"])

    check(polynomial_rubbish,
         ["x^{2}+7x-10x^{2}-9x+9x^{2}"])

    check(polynomial_rubbish.intermediate_reduction_line(),
         ["(1-10+9)x^{2}+(7-9)x"])

    check(polynomial_rubbish.reduce_(),
         ["-2x"])



