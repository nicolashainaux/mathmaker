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

import pytest
from decimal import Decimal

from mathmaker.lib.tools.database import generate_random_decimal_nb


def test_generate_random_decimal_nb_exceptions():
    """Check if wrong values generate errors."""
    with pytest.raises(ValueError) as excinfo:
        generate_random_decimal_nb(Decimal('0.1'), width='a')
    assert str(excinfo.value) == 'As width you can specify either \'random\' '\
        'or an int.'
    with pytest.warns(UserWarning) as record:
        generate_random_decimal_nb(Decimal('0.1'), width=8)
    assert len(record) == 1
    assert str(record[0].message) == 'The chosen width (random) is not '\
        'greater than 1 and lower than the length of ranks scale (7). '\
        'A random value will be chosen instead.'


def test_generate_random_decimal_nb():
    """Check the two ways of generating a random decimal number."""
    d = generate_random_decimal_nb(Decimal('0.1'), width=2,
                                   generation_type='default')
    assert len(str(d)) in [3, 4]
    d = generate_random_decimal_nb(Decimal('0.001'), width=2,
                                   generation_type='default')
    assert len(str(d)) == 5
    assert str(d).startswith('0.0')
