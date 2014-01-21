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
        os.write(common.output, "--- FRACTIONS SUMS\n")

    fraction_2_3_plus_fraction_3_4 = Sum([Fraction(('+', 2, 3)),
                                          Fraction(('+', 3, 4))])

    fraction_1_4_plus_fraction_1_8 = Sum([Fraction(('+', 1, 4)),
                                          Fraction(('+', 1, 8))])

    fraction_1_9_plus_fraction_1_minus12 = Sum([Fraction(('+', 1, 9)),
                                                Fraction(('+', 1, -12))])

    fraction_minus7_10_plus_fraction_minus11_minus15 = \
                                     Sum([Fraction(('+', -7, 10)),
                                          Fraction(('-', 11, -15))])

    sum_of_fraction_3_4_and_number_minus2 = Sum([Fraction(('+', 3, 4)),
                                                 Item(-5)])

    sum_of_fraction_25_10_and_1_10 = Sum([Fraction(('+', 25, 10)),
                                          Fraction(('+', 1, 10))])

    sum_of_fraction_minus18_5_minus_2_5 = Sum([Fraction(('-', 18, 5)),
                                               Fraction(('-', 2, 5))])

    #4 + 25/10 - 7 + 1/10
    long_sum = Sum([Item(4),
                    Fraction((25, 10)),
                    Item(-7),
                    Fraction((1, 10))])


    # 01
    check(fraction_2_3_plus_fraction_3_4,
         ["\\frac{2}{3}+\\frac{3}{4}"])

    # 02
    step_1 = fraction_2_3_plus_fraction_3_4.calculate_next_step()
    check(step_1,
         ["\\frac{2\\times 4}{3\\times 4}+\\frac{3\\times 3}{4\\times 3}"])

    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["\\frac{8}{12}+\\frac{9}{12}"])

    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["\\frac{8+9}{12}"])

    # 05
    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["\\frac{17}{12}"])

    step_5 = step_4.calculate_next_step()
    check(step_5,
         ["None"])

    check(fraction_1_4_plus_fraction_1_8,
         ["\\frac{1}{4}+\\frac{1}{8}"])

    step_1 = fraction_1_4_plus_fraction_1_8.calculate_next_step()
    check(step_1,
         ["\\frac{1\\times 2}{4\\times 2}+\\frac{1}{8}"])

    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["\\frac{2}{8}+\\frac{1}{8}"])

    # 10
    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["\\frac{2+1}{8}"])

    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["\\frac{3}{8}"])

    step_5 = step_4.calculate_next_step()
    check(step_5,
         ["None"])

    check(fraction_1_9_plus_fraction_1_minus12,
         ["\\frac{1}{9}+\\frac{1}{-12}"])

    step_1 = fraction_1_9_plus_fraction_1_minus12.calculate_next_step()
    check(step_1,
         ["\\frac{1}{9}-\\frac{1}{12}"])

    # 15
    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["\\frac{1\\times 4}{9\\times 4}-\\frac{1\\times 3}{12\\times 3}"])

    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["\\frac{4}{36}-\\frac{3}{36}"])

    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["\\frac{4-3}{36}"])

    step_5 = step_4.calculate_next_step()
    check(step_5,
         ["\\frac{1}{36}"])

    step_6 = step_5.calculate_next_step()
    check(step_6,
         ["None"])


    # 20
    check(fraction_minus7_10_plus_fraction_minus11_minus15,
         ["\\frac{-7}{10}-\\frac{11}{-15}"])

    step_1 = fraction_minus7_10_plus_fraction_minus11_minus15.\
             calculate_next_step()
    check(step_1,
         ["-\\frac{7}{10}+\\frac{11}{15}"])

    step_2 = step_1.calculate_next_step()
    check(step_2,
        ["-\\frac{7\\times 3}{10\\times 3}+\\frac{11\\times 2}{15\\times 2}"])

    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["-\\frac{21}{30}+\\frac{22}{30}"])

    # 24
    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["\\frac{-21+22}{30}"])

    # 25
    step_5 = step_4.calculate_next_step()
    check(step_5,
         ["\\frac{1}{30}"])

    step_6 = step_5.calculate_next_step()
    check(step_6,
         ["None"])


    check(sum_of_fraction_3_4_and_number_minus2,
         ["\\frac{3}{4}-5"])

    step_1 = sum_of_fraction_3_4_and_number_minus2.calculate_next_step()
    check(step_1,
         ["\\frac{3}{4}-\\frac{5}{1}"])

    # 29
    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["\\frac{3}{4}-\\frac{5\\times 4}{1\\times 4}"])

    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["\\frac{3}{4}-\\frac{20}{4}"])

    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["\\frac{3-20}{4}"])

    step_5 = step_4.calculate_next_step()
    check(step_5,
         ["-\\frac{17}{4}"])

    step_6 = step_5.calculate_next_step()
    check(step_6,
         ["None"])



    # 34
    check(sum_of_fraction_25_10_and_1_10,
         ["\\frac{25}{10}+\\frac{1}{10}"])

    step_1 = sum_of_fraction_25_10_and_1_10.calculate_next_step()
    check(step_1,
         ["\\frac{25+1}{10}"])

    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["\\frac{26}{10}"])

    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["\\frac{\\bcancel{2}\\times 13}{\\bcancel{2}\\times 5}"])

    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["\\frac{13}{5}"])

    # 39
    step_5 = step_4.calculate_next_step()
    check(step_5,
         ["None"])






    check(sum_of_fraction_minus18_5_minus_2_5,
         ["-\\frac{18}{5}-\\frac{2}{5}"])

    # 41
    step_1 = sum_of_fraction_minus18_5_minus_2_5.calculate_next_step()
    check(step_1,
         ["\\frac{-18-2}{5}"])

    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["-\\frac{20}{5}"])

    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["-\\frac{\\bcancel{5}\\times 4}{\\bcancel{5}}"])

    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["-4"])

    step_5 = step_4.calculate_next_step()
    check(step_5,
         ["None"])


    # 46
    check(long_sum,
         ["4+\\frac{25}{10}-7+\\frac{1}{10}"])

    step_1 = long_sum.calculate_next_step()
    check(step_1,
         ["4-7+\\frac{25+1}{10}"])

    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["-3+\\frac{26}{10}"])

    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["-3+\\frac{\\bcancel{2}\\times 13}{\\bcancel{2}\\times 5}"])

    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["-3+\\frac{13}{5}"])

    step_5 = step_4.calculate_next_step()
    check(step_5,
         ["-\\frac{3}{1}+\\frac{13}{5}"])

    # 52
    step_6 = step_5.calculate_next_step()
    check(step_6,
         ["-\\frac{3\\times 5}{1\\times 5}+\\frac{13}{5}"])

    step_7 = step_6.calculate_next_step()
    check(step_7,
         ["-\\frac{15}{5}+\\frac{13}{5}"])



