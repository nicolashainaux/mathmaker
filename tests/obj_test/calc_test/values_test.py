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
import locale

from settings import config

from lib.core import *
from lib.core.base_calculus import *

from maintenance.autotest import common

try:
    locale.setlocale(locale.LC_ALL, config.LANGUAGE + '.' + config.ENCODING)
except:
    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- VALUES\n", 'utf-8'))

    integer_value = Value(4)

    one_digit_value = Value(4.2)

    two_digits_value = Value(4.25)

    three_digits_value = Value(4.257)

    four_digits_value = Value(4.2571)

    perfect_square = Value(16)

    perfect_decimal_square = Value(1.96)

    # 01
    check(integer_value.digits_number(),
          ["0"])

    check(one_digit_value.digits_number(),
          ["1"])

    check(two_digits_value.digits_number(),
          ["2"])

    check(three_digits_value.digits_number(),
          ["3"])

    check(four_digits_value.digits_number(),
          ["4"])

    check(integer_value.round(0),
          ["4"])

    check(one_digit_value.round(0),
          ["4"])

    check(two_digits_value.round(0),
          ["4"])

    check(three_digits_value.round(0),
          ["4"])

    # 10
    check(four_digits_value.round(0),
          ["4"])

    check(integer_value.round(1),
          ["4"])

    check(one_digit_value.round(1),
          [locale.str(4.2)])

    check(two_digits_value.round(1),
          [locale.str(4.3)])

    check(three_digits_value.round(1),
          [locale.str(4.3)])

    check(four_digits_value.round(1),
          [locale.str(4.3)])

    check(integer_value.round(2),
          ["4"])

    check(one_digit_value.round(2),
          [locale.str(4.2)])

    check(two_digits_value.round(2),
          [locale.str(4.25)])

    check(three_digits_value.round(2),
          [locale.str(4.26)])

    check(four_digits_value.round(2),
          [locale.str(4.26)])

    check(integer_value.round(3),
          ["4"])

    check(one_digit_value.round(3),
          [locale.str(4.2)])

    check(two_digits_value.round(3),
          [locale.str(4.25)])

    check(three_digits_value.round(3),
          [locale.str(4.257)])

    check(four_digits_value.round(3),
          [locale.str(4.257)])

    check(integer_value.round(4),
          ["4"])

    check(one_digit_value.round(4),
          [locale.str(4.2)])

    check(two_digits_value.round(4),
          [locale.str(4.25)])

    check(three_digits_value.round(4),
          [locale.str(4.257)])

    check(four_digits_value.round(4),
          [locale.str(4.2571)])

    check(integer_value.needs_to_get_rounded(0),
          ["False"])

    check(integer_value.needs_to_get_rounded(1),
          ["False"])

    check(one_digit_value.needs_to_get_rounded(0),
          ["True"])

    check(one_digit_value.needs_to_get_rounded(1),
          ["False"])

    check(one_digit_value.needs_to_get_rounded(2),
          ["False"])

    check(two_digits_value.needs_to_get_rounded(0),
          ["True"])

    check(two_digits_value.needs_to_get_rounded(1),
          ["True"])

    check(two_digits_value.needs_to_get_rounded(2),
          ["False"])

    check(three_digits_value.needs_to_get_rounded(0),
          ["True"])

    check(three_digits_value.needs_to_get_rounded(1),
          ["True"])

    check(three_digits_value.needs_to_get_rounded(2),
          ["True"])

    check(three_digits_value.needs_to_get_rounded(3),
          ["False"])

    check(four_digits_value.needs_to_get_rounded(0),
          ["True"])

    check(four_digits_value.needs_to_get_rounded(1),
          ["True"])

    check(four_digits_value.needs_to_get_rounded(2),
          ["True"])

    check(four_digits_value.needs_to_get_rounded(3),
          ["True"])

    check(four_digits_value.needs_to_get_rounded(4),
          ["False"])

    check(perfect_square.is_a_perfect_square(),
          ["True"])

    check(perfect_square.sqrt().digits_number(),
          ["0"])

    check(integer_value.is_an_integer(),
          ["True"])

    check(one_digit_value.is_an_integer(),
          ["False"])

    check(perfect_decimal_square.is_a_perfect_square(),
          ["True"])

    check(two_digits_value.is_a_perfect_square(),
          ["False"])















