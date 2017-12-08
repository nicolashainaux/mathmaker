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
from mathmaker.lib.tools.database import parse_sql_creation_query


def test_parse_sql_creation_query():
    """Check if parse_sql_creation_query parses correctly."""
    assert parse_sql_creation_query('''CREATE TABLE w3l
            (id INTEGER PRIMARY KEY, language TEXT, word TEXT,
             drawDate INTEGER)''') == \
        ('w3l', ['id', 'language', 'word', 'drawDate'])
    assert parse_sql_creation_query('''CREATE TABLE int_pairs
            (id INTEGER PRIMARY KEY, nb1 INTEGER, nb2 INTEGER,
             lock_equal_products INTEGER, drawDate INTEGER, clever INTEGER,
             suits_for_deci1 INTEGER, suits_for_deci2 INTEGER)''') == \
        ('int_pairs', ['id', 'nb1', 'nb2', 'lock_equal_products',
                       'drawDate', 'clever', 'suits_for_deci1',
                       'suits_for_deci2'])
    assert parse_sql_creation_query('''CREATE TABLE digits_places
            (id INTEGER PRIMARY KEY, place DECIMAL(4, 3),
             drawDate INTEGER)''') == \
        ('digits_places', ['id', 'place', 'drawDate'])


def test_generate_random_decimal_nb_exceptions():
    """Check if wrong values generate errors."""
    with pytest.raises(ValueError) as excinfo:
        generate_random_decimal_nb(position=Decimal('0.1'), width='a')
    assert str(excinfo.value) == 'As width you can specify either ' \
        '\'random\', \'random_xtoy\' or an int.'
    with pytest.warns(UserWarning) as record:
        generate_random_decimal_nb(position=Decimal('0.1'), width=8)
    assert len(record) == 1
    assert str(record[0].message) == 'The chosen width (random) is not '\
        'greater than 1 and lower than the length of digits positions (7). '\
        'A random value will be chosen instead.'
    with pytest.warns(UserWarning) as record:
        generate_random_decimal_nb(position=Decimal('0.1'), width='random8')
    assert len(record) == 1
    assert str(record[0].message) == 'Malformed random width. '\
        'A random value will be chosen instead.'
    with pytest.warns(UserWarning) as record:
        generate_random_decimal_nb(position=Decimal('0.1'), width='random_8')
    assert len(record) == 1
    assert str(record[0].message) == 'Malformed random width\'s span. '\
        'A random value will be chosen instead.'
    with pytest.warns(UserWarning) as record:
        generate_random_decimal_nb(position=Decimal('0.1'),
                                   width='random_8tob')
    assert len(record) == 1
    assert str(record[0].message) == 'Malformed random width\'s span bounds ' \
        '(both should be int). A random value will be chosen instead.'


def test_generate_random_decimal_nb():
    """Check the two ways of generating a random decimal number."""
    d = generate_random_decimal_nb(position=Decimal('0.1'), width=2,
                                   generation_type='default')[0]
    assert len(str(d)) in [3, 4]
    d = generate_random_decimal_nb(position=Decimal('0.001'), width=2,
                                   generation_type='default')[0]
    assert len(str(d)) == 5
    assert str(d).startswith('0.0')
    d = generate_random_decimal_nb(width=7,
                                   generation_type='default',
                                   pos_matches_invisible_zero=True)[0]
    d = generate_random_decimal_nb(width=1,
                                   generation_type='default',
                                   pos_matches_invisible_zero=True)[0]
