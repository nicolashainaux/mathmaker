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
        os.write(common.output, "--- QUOTIENTS\n")

    quo_fraction_8over9_div_7over2 = Quotient(('+',
                                               Fraction(('+', 8, 9)),
                                               Fraction(('+', 7, 2)),
                                               1,
                                               'use_divide_symbol'
                                              ))

    quo_fraction_minus1over2_div_1over3 = Quotient(('-',
                                               Fraction(('+', 1, 2)),
                                               Fraction(('+', 1, 3)),
                                               1,
                                               'use_divide_symbol'
                                              ))




    check(quo_fraction_8over9_div_7over2,
         ["\\frac{8}{9}\div \\frac{7}{2}"])

    check(quo_fraction_8over9_div_7over2.calculate_next_step(),
         ["\\frac{8}{9}\\times \\frac{2}{7}"])

    #print str(quo_fraction_8over9_div_7over2.calculate_next_step())

    check(quo_fraction_8over9_div_7over2.calculate_next_step()\
          .calculate_next_step(),
         ["\\frac{8\\times 2}{9\\times 7}"])


    check(quo_fraction_minus1over2_div_1over3,
         ["-\\frac{1}{2}\div \\frac{1}{3}"])  #-\\frac{1}{2}\div \\frac{1}{3}

    next_step = quo_fraction_minus1over2_div_1over3.calculate_next_step()
    check(next_step,
         ["-\\frac{1}{2}\\times \\frac{3}{1}"])

    next_step = next_step.calculate_next_step()
    check(next_step,
         ["-\\frac{1\\times 3}{2\\times 1}"])

    next_step = next_step.calculate_next_step()
    check(next_step,
         ["-\\frac{3}{2}"])



