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
        os.write(common.output, bytes("--- PRODUCTS' REDUCTION\n", 'utf-8'))

    temp_sum = Sum(['x', 3])
    temp_sum.set_exponent(3)
    temp_product = Product(Monomial((1, 2)))
    temp_product.set_exponent(3)
    temp_product_bis = Product([2, 3])
    temp_product_bis.set_exponent(3)

    big_product = Product([Monomial((2, 1)),
                           Monomial((-4, 2)),
                           temp_sum,
                           Item(5),
                           temp_product,
                           Item(('+', -1, 2)),
                           temp_product_bis])


    check(big_product,
         ["2x\\times (-4x^{2})(x+3)^{3}\\times 5\\times (x^{2})^{3}\\" \
          + "times (-1)^{2}\\times (2\\times 3)^{3}"])

    temp_product = big_product.order()
    check(temp_product,
         ["2\\times (-4)\\times 5\\times (-1)^{2}\\times 2^{3}\\times 3^{3}x" \
          + "\\times x^{2}x^{6}(x+3)^{3}"])

    big_product = big_product.reduce_()

    check(big_product,
         ["-8640x^{9}(x+3)^{3}"])







