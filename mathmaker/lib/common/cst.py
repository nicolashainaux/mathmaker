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
from decimal import Decimal

XML_BOOLEANS = {'true': lambda: True,
                'false': lambda: False,
                'random': lambda: random.choice([True, False])}

DEFAULT = "default"
RANDOMLY = "randomly"
NUMERIC = "numeric"
LITERALS = "literals"
OTHERS = "others"

UNIT = "1"
TENTH = "1.0"
HUNDREDTH = "1.00"
THOUSANDTH = "1.000"
TEN_THOUSANDTH = "1.0000"

PRECISION = [UNIT, TENTH, HUNDREDTH, THOUSANDTH, TEN_THOUSANDTH]
PRECISION_REVERSED = {UNIT: 0,
                      TENTH: 1,
                      HUNDREDTH: 2,
                      THOUSANDTH: 3,
                      TEN_THOUSANDTH: 4}

PRECISION_WORDS = {UNIT: "unit",
                   TENTH: "tenth",
                   HUNDREDTH: "hundredth",
                   THOUSANDTH: "thousandth",
                   TEN_THOUSANDTH: "ten thousandth"}

BILLIONS = Decimal("1000000000")
HUNDREDS_OF_MILLIONS = Decimal("100000000")
TENS_OF_MILLIONS = Decimal("10000000")
MILLIONS = Decimal("1000000")
HUNDREDS_OF_THOUSANDS = Decimal("100000")
TENS_OF_THOUSANDS = Decimal("10000")
THOUSANDS = Decimal("1000")
HUNDREDS = Decimal("100")
TENS = Decimal("10")
UNITS = Decimal("1")
TENTHS = Decimal("0.1")
HUNDREDTHS = Decimal("0.01")
THOUSANDTHS = Decimal("0.001")

RANKS_HIGHER = [BILLIONS, HUNDREDS_OF_MILLIONS, TENS_OF_MILLIONS, MILLIONS,
                HUNDREDS_OF_THOUSANDS, TENS_OF_THOUSANDS]

RANKS_LOWER = [THOUSANDS, HUNDREDS, TENS, UNITS]

RANKS_INTEGER = RANKS_HIGHER + RANKS_LOWER

RANKS_DECIMAL = [TENTHS, HUNDREDTHS, THOUSANDTHS]

RANKS_CONFUSING = [THOUSANDS, HUNDREDS, TENS, TENTHS, HUNDREDTHS, THOUSANDTHS]

RANKS = RANKS_LOWER + RANKS_DECIMAL

RANKS_EXTENDED = RANKS_INTEGER + RANKS_DECIMAL

RANKS_WORDS = {BILLIONS: "billions",
               HUNDREDS_OF_MILLIONS: "hundreds of millions",
               TENS_OF_MILLIONS: "tens of millions", MILLIONS: "millions",
               HUNDREDS_OF_THOUSANDS: "hundreds of thousands",
               TENS_OF_THOUSANDS: "tens of thousands",
               THOUSANDS: "thousands", HUNDREDS: "hundreds", TENS: "tens",
               UNITS: "units", TENTHS: "tenths", HUNDREDTHS: "hundredths",
               THOUSANDTHS: "thousandths"}

RANKS_HOW_MANY = {BILLIONS: "How many billions",
                  HUNDREDS_OF_MILLIONS: "How many hundreds of millions",
                  TENS_OF_MILLIONS: "How many tens of millions",
                  MILLIONS: "How many millions",
                  HUNDREDS_OF_THOUSANDS: "How many hundreds of thousands",
                  TENS_OF_THOUSANDS: "How many tens of thousands",
                  THOUSANDS: "How many thousands",
                  HUNDREDS: "How many hundreds",
                  TENS: "How many tens",
                  UNITS: "How many units",
                  TENTHS: "How many tenths",
                  HUNDREDTHS: "How many hundredths",
                  THOUSANDTHS: "How many thousandths"}

LENGTH_UNITS = ['km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm', 'µm', 'nm', 'pm']
CAPACITY_UNITS = ['kL', 'hL', 'daL', 'L', 'dL', 'cL', 'mL', 'µL', 'nL', 'pL']
MASS_UNITS = ['kg', 'hg', 'dag', 'g', 'dg', 'cg', 'mg', 'µg', 'ng', 'pg']
COMMON_LENGTH_UNITS = LENGTH_UNITS[:-3]
COMMON_CAPACITY_UNITS = CAPACITY_UNITS[1:-3]
COMMON_MASS_UNITS = LENGTH_UNITS[:-3]
ANGLE_UNITS = ['\\textdegree']
CURRENCY_UNITS = ['€', '\officialeuro',
                  '$', '\\textdollar',
                  '£', '\\textsterling']
CURRENCIES_DICT = {'euro': '\officialeuro',
                   'dollar': '\\textdollar',
                   'sterling': '\\textsterling'}
AVAILABLE_UNITS = LENGTH_UNITS + CAPACITY_UNITS + MASS_UNITS + ANGLE_UNITS\
    + CURRENCY_UNITS
UNIT_KINDS = {'length': COMMON_LENGTH_UNITS,
              'mass': COMMON_MASS_UNITS,
              'capacity': COMMON_CAPACITY_UNITS,
              'currency': CURRENCY_UNITS}
VALUE_AND_UNIT_SEPARATOR = {'km': "~", 'hm': "~", 'dam': "~", 'm': "~",
                            'dm': "~", 'cm': "~", 'mm': "~", 'µm': "~",
                            'nm': "~", 'pm': "~",
                            'kL': "~", 'hL': "~", 'daL': "~", 'L': "~",
                            'dL': "~", 'cL': "~", 'mL': "~", 'µL': "~",
                            'nL': "~", 'pL': "~",
                            'kg': "~", 'hg': "~", 'dag': "~", 'g': "~",
                            'dg': "~", 'cg': "~", 'mg': "~", 'µg': "~",
                            'ng': "~", 'pg': "~",
                            '\\textdegree': "",
                            '\officialeuro': "~",
                            '\\textdollar': "~",
                            '\\textsterling': "~"}

TEXT_SCALES = ['tiny', 'scriptsize', 'footnotesize', 'small', 'normal',
               'large', 'Large', 'LARGE', 'huge', 'HUGE']

TEXT_RANKS = {'tiny': 0, 'scriptsize': 1, 'footnotesize': 2, 'small': 3,
              'normal': 4, 'large': 5, 'Large': 6, 'LARGE': 7, 'huge': 8,
              'HUGE': 9}
