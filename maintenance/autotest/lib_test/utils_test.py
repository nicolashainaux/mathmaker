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
from decimal import *
#import locale

from maintenance.autotest import common

from lib import utils

#from core import *
#from core.base_calculus import *
#from core.base_geometry import *
#from core.geometry import *



#try:
#   locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
#except:
#    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- [LIB] UTILS \n", 'utf-8'))

    # Don't forget to uncomment the convenient lines above if a test
    # requires to use the locale module.

    # 1
    check(str(utils.correct_normalize_results(Decimal('40').normalize())),
          ["40"])

    # 2
    check(str(utils.correct_normalize_results(Decimal('700').normalize())),
          ["700"])

    # 3
    check(str(utils.correct_normalize_results(Decimal('10').normalize())),
          ["10"])

    # 4
    check(str(utils.correct_normalize_results(Decimal('2740000').normalize())),
          ["2740000"])

    # 5
    check(str(utils.correct_normalize_results(Decimal('1600').normalize())),
          ["1600"])

    # 6
    check(str(utils.correct_normalize_results(Decimal('0.098').normalize())),
          ["0.098"])

    # 7
    check(str(utils.correct_normalize_results(Decimal('0.0100').normalize())),
          ["0.01"])


