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
from lib.maths_lib import *

from maintenance.autotest import common

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- FRACTION SIMPLIFICATION\n", 'utf-8'))

    fraction_92_76 = Fraction(('+', 92, 76))
    fraction_92_76_bis = Fraction(('+', 92, 76))
    fraction_10times6_over_7times2 = Fraction(('+',
                                               Product([Item(10), Item(6)]),
                                               Product([Item(7), Item(2)])
                                              ))

    fraction_7times6_over_3times3 = Fraction(('+',
                                              Product([Item(7), Item(6)]),
                                              Product([Item(3), Item(3)])
                                            ))

    fraction_3times7_over_10times4 = Fraction(('+',
                                              Product([Item(3), Item(7)]),
                                              Product([Item(10), Item(4)])
                                              ))

    fraction_8times3_over_5times6 = Fraction(('+',
                                              Product([Item(8), Item(3)]),
                                              Product([Item(5), Item(6)])
                                             ))

    fraction_10times5_over_5times9 = Fraction(('+',
                                              Product([Item(10), Item(5)]),
                                              Product([Item(5), Item(9)])
                                             ))

    #fraction_minus3timesminus1_over_minus2times9 = Fraction(( \
    #                                          '+',
    #                                          Product([Item(-3),
    #                                                            Item(-1)]),
    #                                          Product([Item(-2),
    #                                                            Item(9)])
    #                                                  ))

    check(str(ten_power_gcd(3,4)),
         ["1"])

    check(str(ten_power_gcd(10,4)),
         ["1"])

    check(str(ten_power_gcd(10,10)),
         ["10"])

    check(str(ten_power_gcd(200,50)),
         ["10"])

    check(str(ten_power_gcd(21000,400)),
         ["100"])

    check(fraction_92_76,
         ["\\frac{92}{76}"])

    fraction_92_76 = fraction_92_76.calculate_next_step()
    check(fraction_92_76,
         ["\\frac{\\bcancel{2}\\times 46}{\\bcancel{2}\\times 38}"])

    fraction_92_76 = fraction_92_76.calculate_next_step()
    check(fraction_92_76,
         ["\\frac{\\bcancel{2}\\times 23}{\\bcancel{2}\\times 19}"])

    check(fraction_92_76_bis.simplified(),
         ["\\frac{46}{38}"])

    check(fraction_92_76_bis.simplification_line().simplified(),
         ["\\frac{46}{38}"])

    #check(fraction_10times6_over_7times2,
    #     ["essai"])

    check(fraction_10times6_over_7times2.is_reducible(),
         ["True"])

    check(fraction_10times6_over_7times2.calculate_next_step(),
         ["\\frac{\\bcancel{2}\\times 5\\times 6}{7\\times \\bcancel{2}}"])

    check(fraction_7times6_over_3times3.simplification_line(),
         ["\\frac{7\\times \\bcancel{3}\\times 2}{\\bcancel{3}\\times 3}"])

    check(fraction_3times7_over_10times4.calculate_next_step(),
         ["\\frac{21}{40}"])

    check(fraction_8times3_over_5times6.simplification_line(),
         ["\\frac{\\bcancel{2}\\times 4\\times \\bcancel{3}}{5\\times" \
          + " \\bcancel{2}\\times \\bcancel{3}}"])

    check(fraction_10times5_over_5times9.simplification_line(),
         ["\\frac{10\\times \\bcancel{5}}{\\bcancel{5}\\times 9}"])


    f1 = Fraction(('+', 3, 7))

    check(f1.completely_reduced(),
         ["\\frac{3}{7}"])

    check(str(f1.is_a_decimal_number()),
         ["False"])

    f2 = Fraction(('+', 9, 700))

    check(str(f2.is_a_decimal_number()),
         ["False"])

    f3 = Fraction(('+', 9, 2500))

    check(str(f3.is_a_decimal_number()),
         ["True"])

    f4 = Fraction(('+', 7, 700))

    check(str(f4.is_a_decimal_number()),
         ["True"])


