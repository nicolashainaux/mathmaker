# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2013 Nicolas Hainaux <nico_h@users.sourceforge.net>

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
        os.write(common.output, "--- FRACTIONS PRODUCTS\n")

    product_fraction_5_4_times_5_5 = Product([Fraction((5, 4)),
                                              Fraction((5, 5))])

    product_fraction_9_minus2_times_minus8_10 = Product([Fraction((9, -2)),
                                                         Fraction((-8, 10))])


    #\frac{14}{7}\times \frac{12}{12}
    product_fraction_14_7_times_fraction_12_12 = Product([Fraction((14, 7)),
                                                         Fraction((12, 12))])

    check(product_fraction_5_4_times_5_5,
         ["\\frac{5}{4}\\times \\frac{5}{5}"])

    step_1 = product_fraction_5_4_times_5_5.calculate_next_step()
    check(step_1,
         ["\\frac{5\\times 5}{4\\times 5}"])

    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["\\frac{\\bcancel{5}\\times 5}{4\\times \\bcancel{5}}"])
    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["\\frac{5}{4}"])
    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["None"])

    check(product_fraction_14_7_times_fraction_12_12,
         ["\\frac{14}{7}\\times \\frac{12}{12}"])

    step_1 = product_fraction_14_7_times_fraction_12_12.calculate_next_step()
    check(step_1,
         ["\\frac{14\\times 12}{7\\times 12}"])

    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["\\frac{\\bcancel{7}\\times 2\\times \\bcancel{12}}" \
          + "{\\bcancel{7}\\times \\bcancel{12}}"])
    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["2"])
    #     ["\\frac{2}{1}"])
    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["None"])
    #step_5 = step_4.calculate_next_step()
    #check(step_5,
    #     ["None"])



    check(product_fraction_9_minus2_times_minus8_10,
         ["\\frac{9}{-2}\\times \\frac{-8}{10}"])

    step_1 = product_fraction_9_minus2_times_minus8_10.calculate_next_step()
    check(step_1,
         ["\\frac{9\\times 8}{2\\times 10}"])

    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["\\frac{9\\times \\bcancel{2}\\times 4}{\\bcancel{2}\\times 10}"])
    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["\\frac{9\\times \\bcancel{2}\\times 2}{\\bcancel{2}\\times 5}"])
    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["\\frac{18}{5}"])


