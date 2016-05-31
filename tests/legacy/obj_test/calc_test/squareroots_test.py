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
from lib.core.calculus import *

from maintenance.autotest import common

try:
   locale.setlocale(locale.LC_ALL, config.LANGUAGE + '.' + config.ENCODING)
except:
    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- SQUARE ROOTS\n", 'utf-8'))


    sq1 = SquareRoot(Item(5))

    sq2 = SquareRoot(Item(16))




    check(sq1,
          ["\\sqrt{5}"])

    check(sq1.calculate_next_step(decimal_result=4),
          [locale.str(2.2361)])

    check(sq2.calculate_next_step(decimal_result=4),
          [locale.str(4)])



