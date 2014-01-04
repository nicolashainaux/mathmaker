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
        os.write(common.output, "--- MONOMIALS\n")

    monom_6 = Monomial(('+', 6, 0))
    monom_6_ones_away = monom_6.throw_away_the_neutrals()

    monom_1 = Monomial((1, 0))

    square_monom_3x = Monomial(('+', 3, 1))
    square_monom_3x.set_exponent(2)

    square_monom_5 = Monomial(('+', 5, 0))
    square_monom_5.set_exponent(2)

    check(monom_6_ones_away,
         ["6"])

    check(monom_1.is_displ_as_a_single_neutral(Item(0)),
          ["False"])

    check(square_monom_3x,
          ["(3x)^{2}"])

    check(square_monom_5,
          ["5^{2}"])






