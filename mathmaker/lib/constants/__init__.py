# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

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

import sys
import random

LOCALE_US = 'en-US' if sys.platform.startswith('win') else 'en_US.UTF-8'
LOCALE_FR = 'fr-FR' if sys.platform.startswith('win') else 'fr_FR.UTF-8'

BOOLEAN = {'true': lambda: True, 'false': lambda: False,
           'random': lambda: random.choice([True, False]),
           True: lambda: True, False: lambda: False, }

EQUAL_PRODUCTS = {(2, 6): [(3, 4)],
                  (3, 4): [(2, 6)],
                  (2, 8): [(4, 4)],
                  (4, 4): [(2, 8)],
                  (3, 6): [(2, 9)],
                  (2, 9): [(3, 6)],
                  (3, 8): [(4, 6)],
                  (4, 6): [(3, 8)],
                  (4, 9): [(6, 6), (3, 12)],
                  (6, 6): [(4, 9), (3, 12)],
                  (3, 12): [(4, 9), (6, 6)]}

MIN_ROW_HEIGHT = 1

DEFAULT_LAYOUT = {'exc': [None, 'all'], 'ans': [None, 'all'],
                  'spacing_w': 'undefined', 'spacing_a': 'undefined',
                  'min_row_height': MIN_ROW_HEIGHT}

DEFAULT = "default"
RANDOMLY = "randomly"
NUMERIC = "numeric"
LITERALS = "literals"
OTHERS = "others"

SLIDE_CONTENT_SEP = '|<SLIDE_CONTENT_SEPARATOR>|'
