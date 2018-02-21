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
from mathmaker.lib.tools.database import IntspansProduct


def test_intspansproduct_errors():
    """Check instanciation errors of IntspansProduct."""
    with pytest.raises(TypeError) as excinfo:
        IntspansProduct('4-9,10', 'a')
    assert str(excinfo.value) == 'elt_nb must be an int, found '\
        '<class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        IntspansProduct(10, 3)
    assert str(excinfo.value) == 'cartesianpower_spans must be a str, found '\
        '<class \'int\'> instead.'
    with pytest.raises(RuntimeError) as excinfo:
        IntspansProduct('1×2×3', 4)
    assert str(excinfo.value) == 'Found 3 elements in this spans product: '\
        '1×2×3, but 4 were expected.'
    with pytest.raises(ValueError) as excinfo:
        IntspansProduct('1×2×a')
    assert str(excinfo.value) == 'Syntax error found in this integers\' '\
        'span: a, what should complain with intspan syntax. See '\
        'http://intspan.readthedocs.io/en/latest/index.html'


def test_intspansproduct_turn_to_query_conditions():
    """Check IntspansProduct."""
    assert IntspansProduct('').turn_to_query_conditions() == {}
    assert IntspansProduct('4,9').turn_to_query_conditions() \
        == {'raw': "(nb1 IN ('4', '9'))"}
    assert IntspansProduct('4-9').turn_to_query_conditions() \
        == {'raw': '(nb1 BETWEEN 4 AND 9)'}
    assert IntspansProduct('2-9,15,25').turn_to_query_conditions() \
        == {'raw': "(nb1 IN ('15', '25') OR (nb1 BETWEEN 2 AND 9))"}
    assert IntspansProduct('2-9', elt_nb=2).turn_to_query_conditions() \
        == {'raw': '((nb1 BETWEEN 2 AND 9) AND (nb2 BETWEEN 2 AND 9))'}
    assert IntspansProduct('2-9,15,25×10-100').turn_to_query_conditions() \
        == {'raw': "((nb1 IN ('15', '25') OR (nb1 BETWEEN 2 AND 9)) "
                   'AND (nb2 BETWEEN 10 AND 100))'}
    assert IntspansProduct('2-9,15,25', elt_nb=2).turn_to_query_conditions() \
        == {'raw': "((nb1 IN ('15', '25') OR (nb1 BETWEEN 2 AND 9)) "
                   "AND (nb2 IN ('15', '25') OR (nb2 BETWEEN 2 AND 9)))"}


def test_intspansproduct_random_draw():
    """Check IntspansProduct."""
    r = IntspansProduct('2-9', elt_nb=2)
    d = r.random_draw()
    assert len(d) == 2
    assert 2 <= d[0] <= d[1] <= 9
    r = IntspansProduct('2-9')
    d = r.random_draw(return_all=True)
    assert d == [[2, 3, 4, 5, 6, 7, 8, 9]]
    d = r.random_draw(return_all=True, nb1_notmod=2)
    assert d == [[3, 5, 7, 9]]
    d = r.random_draw(return_all=True, nb1_mod=2)
    assert d == [[2, 4, 6, 8]]
    d = r.random_draw(return_all=True, not_in=['4', '5', '7'])
    assert d == [[2, 3, 6, 8, 9]]
    r = IntspansProduct('6-9×6-9')
    d = r.random_draw(return_all=True)
    assert d == [[6, 7, 8, 9], [6, 7, 8, 9]]
    d = r.random_draw(return_all=True, nb1_mod=3, nb2_notmod=3)
    assert d == [[6, 9], [7, 8]]
    d = r.random_draw(return_all=True, nb2_in=['4', '5', '7'])
    assert d == [[6, 7, 8, 9], [7]]
    d = r.random_draw(return_all=True, nb1_max=8, nb2_min=7)
    assert d == [[6, 7, 8], [7, 8, 9]]
    d = r.random_draw(return_all=True, nb1_lt=9, nb2_ge=7)
    assert d == [[6, 7, 8], [7, 8, 9]]
    d = r.random_draw(return_all=True, nb1_neq=6, nb2_neq=8)
    assert d == [[7, 8, 9], [6, 7, 9]]
    with pytest.raises(RuntimeError) as excinfo:
        r.random_draw(nb1_max=5)
    assert str(excinfo.value) == 'Impossible to draw an int tuple from '\
        "['6-9', '6-9'] under these conditions: nb1_max=5.\n"
    with pytest.raises(RuntimeError) as excinfo:
        r.random_draw(nb2_mod=5)
    assert str(excinfo.value) == 'Impossible to draw an int tuple from '\
        "['6-9', '6-9'] under these conditions: nb2_mod=5.\n"
    r = IntspansProduct('3×4×6,7')
    d = r.random_draw(constructible=True)
    assert d == (3, 4, 6)
    d = r.random_draw(constructible=False)
    assert d == (3, 4, 7)
    r = IntspansProduct('3×4×7-10')
    with pytest.raises(RuntimeError) as excinfo:
        r.random_draw(constructible=True)
    assert str(excinfo.value) == 'Impossible to draw a constructible int '\
        "tuple from ['3', '4', '7-10'].\n"
    r = IntspansProduct('4-5×8×12')
    d = r.random_draw(constructible=True)
    assert d == (5, 8, 12)
    d = r.random_draw(constructible=False)
    assert d == (4, 8, 12)
    r = IntspansProduct('4×8-9×12-16')
    d = r.random_draw(constructible=True)
    assert d[0:2] == (4, 9)
    r = IntspansProduct('4×12-16×8-9')
    d = r.random_draw(constructible=True)
    assert d[0:2] == (4, 9)
    r = IntspansProduct('4×1-1002×1006-2006')
    with pytest.raises(RuntimeError) as excinfo:
        r.random_draw(constructible=True)
    assert str(excinfo.value) == 'Impossible to draw a constructible int '\
        "tuple from ['4', '1-1002', '1006-2006'].\n"
    r = IntspansProduct('3-5×3-5×3-5')
    with pytest.raises(RuntimeError) as excinfo:
        d = r.random_draw(constructible=False)
        import sys
        sys.stderr.write('d={}\n'.format(d))
    assert str(excinfo.value) == 'Impossible to draw an int tuple from '\
        "['3-5', '3-5', '3-5'] under these conditions: constructible=False.\n"
    # 'Impossible to draw a not constructible int '\
    #     "tuple from ['3-5', '3-5', '3-5'].\n"


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
