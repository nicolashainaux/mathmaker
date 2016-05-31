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

from lib.core import *
from lib.core.base_calculus import *

from maintenance.autotest import common

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- SUMS\n", 'utf-8'))


# --------------------------------------------------------------------------

    sum_a_plus_b_plus_sum_a_plus_b = Sum([Sum(['a', 'b']),
                                          Sum(['a', 'b'])])

    sum_minus_one_plus_x = Sum([Monomial(('-', 1, 0)),
                                Monomial(('+', 1, 1))])

    sum_minus_one_plus_x_bis = Sum([Product(Item(-1)), Item('x')])

    sum_one_plus_x = Sum([Product(Item(1)), Item('x')])

    temp_product = Product([Item(3)])
    temp_product.set_exponent(2)
    sum_1 = Sum([temp_product,
                 Item(5)
                ])

    sum_2_product_polynomial_minus10x2_9 = \
                  Sum([Item(2),
                       Product([
                                Polynomial([Monomial(('-', 10, 2)),
                                            Monomial(('+', 9, 0))])
                                ])

                       ])

    sum_binomial_followed_by_positive_simple_expd = \
            Sum([BinomialIdentity((Monomial(('+', 6, 0)),
                                   Monomial(('+', 1, 1)))),
                 Expandable((Monomial(('+', 12, 0)),
                             Sum([
                                  Polynomial([Monomial(('+', 2, 0)),
                                              Monomial(('+', 11, 1))])
                                ])
                           ))
               ])

    sum_binomial_followed_by_positive_item = \
            Sum([BinomialIdentity((Monomial(('+', 6, 0)),
                                   Monomial(('+', 1, 1)))),
                 Item(1)
               ])

    sum_sum_and_positive_item = \
            Sum([Sum([Item(5),
                      Item(7)
                    ]),
                 Item(1)
               ])

    check(sum_a_plus_b_plus_sum_a_plus_b,
         ["a+b+a+b"])

    check(sum_minus_one_plus_x,
         ["-1+x"])

    check(sum_minus_one_plus_x_bis,
         ["-1+x"])

    check(sum_one_plus_x,
         ["1+x"])

    check(sum_1,
         ["3^{2}+5"])

    check(sum_2_product_polynomial_minus10x2_9,
         ["2-10x^{2}+9"])

    check(sum_binomial_followed_by_positive_simple_expd,
         ["(6+x)^{2}+12(2+11x)"])

    check(sum_binomial_followed_by_positive_item,
         ["(6+x)^{2}+1"])

    check(sum_sum_and_positive_item,
         ["5+7+1"])


# --------------------------------------------------------------------------

    sum_of_squared_numbers = Sum([Item(('+', 4, 2)),
                                  Item(('+', 5, 2))])

    check(sum_of_squared_numbers,
          ["4^{2}+5^{2}"])

    check(sum_of_squared_numbers.calculate_next_step(),
          ["16+25"])



