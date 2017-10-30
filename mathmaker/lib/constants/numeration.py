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

from decimal import Decimal

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

DIGITSPLACES_HIGHER = [BILLIONS, HUNDREDS_OF_MILLIONS, TENS_OF_MILLIONS,
                       MILLIONS, HUNDREDS_OF_THOUSANDS, TENS_OF_THOUSANDS]

DIGITSPLACES_LOWER = [THOUSANDS, HUNDREDS, TENS, UNITS]

DIGITSPLACES_INTEGER = DIGITSPLACES_HIGHER + DIGITSPLACES_LOWER

DIGITSPLACES_DECIMAL = [TENTHS, HUNDREDTHS, THOUSANDTHS]

DIGITSPLACES_CONFUSING = [THOUSANDS, HUNDREDS, TENS, TENTHS, HUNDREDTHS,
                          THOUSANDTHS]

DIGITSPLACES = DIGITSPLACES_LOWER + DIGITSPLACES_DECIMAL

DIGITSPLACES_EXTENDED = DIGITSPLACES_INTEGER + DIGITSPLACES_DECIMAL

DIGITSPLACES_WORDS = {BILLIONS: 'billions',
                      HUNDREDS_OF_MILLIONS: 'hundreds of millions',
                      TENS_OF_MILLIONS: 'tens of millions',
                      MILLIONS: 'millions',
                      HUNDREDS_OF_THOUSANDS: 'hundreds of thousands',
                      TENS_OF_THOUSANDS: 'tens of thousands',
                      THOUSANDS: 'thousands', HUNDREDS: 'hundreds',
                      TENS: 'tens',
                      UNITS: 'units', TENTHS: 'tenths',
                      HUNDREDTHS: 'hundredths',
                      THOUSANDTHS: 'thousandths'}

DIGITSPLACES_HOW_MANY = {BILLIONS: 'How many billions',
                         HUNDREDS_OF_MILLIONS: 'How many hundreds of millions',
                         TENS_OF_MILLIONS: 'How many tens of millions',
                         MILLIONS: 'How many millions',
                         HUNDREDS_OF_THOUSANDS: 'How many hundreds of '
                         'thousands',
                         TENS_OF_THOUSANDS: 'How many tens of thousands',
                         THOUSANDS: 'How many thousands',
                         HUNDREDS: 'How many hundreds',
                         TENS: 'How many tens',
                         UNITS: 'How many units',
                         TENTHS: 'How many tenths',
                         HUNDREDTHS: 'How many hundredths',
                         THOUSANDTHS: 'How many thousandths'}
