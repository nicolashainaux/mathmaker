# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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

import random

XML_BOOLEANS = {'true': lambda: True,
                'false': lambda: False,
                'random': lambda: random.choice([True, False])}

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

DEFAULT = "default"
RANDOMLY = "randomly"
NUMERIC = "numeric"
LITERALS = "literals"
OTHERS = "others"