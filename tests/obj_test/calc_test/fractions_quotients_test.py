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
        os.write(common.output, bytes("--- FRACTIONS QUOTIENTS\n", 'utf-8'))

    div_fraction_9over3_by_fraction_1overminus3 = \
                                 Quotient(('+',
                                          Fraction(('+', Item(9), Item(3))),
                                          Fraction(('+', Item(1), Item(-3)))
                                          ))

    div_fraction_9over3_by_fraction_1overminus3.set_symbol('use_divide_symbol')


    #check(fraction_minus3timesminus1_over_minus2times9.simplification_line(),
    #     ["essai"])
    step_1 = div_fraction_9over3_by_fraction_1overminus3.calculate_next_step()
    check(step_1,
         ["\\frac{9}{3}\\times \\frac{-3}{1}"])

    step_2 = step_1.calculate_next_step()
    check(step_2,
         ["-\\frac{9\\times 3}{3\\times 1}"])
    step_3 = step_2.calculate_next_step()
    check(step_3,
         ["-\\frac{9\\times \\bcancel{3}}{\\bcancel{3}}"])
    step_4 = step_3.calculate_next_step()
    check(step_4,
         ["-9"])
    step_5 = step_4.calculate_next_step()
    check(step_5,
         ["None"])





