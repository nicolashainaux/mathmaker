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
import math
#import locale

#from lib.common import default

from core import *
from core.base_calculus import *
from core.base_geometry import *

from maintenance.autotest import common

#try:
#   locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
#except:
#    locale.setlocale(locale.LC_ALL, '')

check = common.check

def action():
    if common.verbose:
        os.write(common.output, "--- FUNCTIONAL ITEMS\n")

    # Don't forget to uncomment the convenient lines above if a test
    # requires to use the locale module.

    f1 = FunctionalItem(("f", Item("x"), None, None))

    check(f1.into_str(),
         ["f(x)"])

    f1.set_sign('-')

    check(f1.into_str(),
         ["-f(x)"])

    f1.set_exponent(Item(2))

    check(f1.into_str(),
         ["-f^{2}(x)"])

    theta = Angle((Point(["A", (0, 0)]),
                   Point(["B", (1, 0)]),
                   Point(["C", (0, 1)])))

    f2 = FunctionalItem(("\cos", theta, math.cos, math.acos))

    check(f2.into_str(),
         ["\cos(\widehat{ABC})"])

    f2.set_numeric_value(Value(60, unit="\textdegree"))

    f2.swap_to_numeric()

    check(f2.into_str(),
         ["\cos(60\\textdegree)"])

    f2.swap_to_literal()

    check(f2.into_str(),
         ["\cos(\widehat{ABC})"])

    f2.calculate_next_step()

    check(f2.into_str(),
         ["\cos(60\textdegree)"])

    f2.calculate_next_step()

    check(f2.into_str(),
         ["None"])

    f2.calculate_next_step(do_evaluate_fct=True)

    check(f2.into_str(),
         ["0.5"])

    f3 = FunctionalItem(("\sin", theta, math.sin, math.asin))

    check(f3.into_str(),
         ["\sin(\widehat{ABC})"])

    check(str(f3.calculate_next_step()),
         ["None"])


