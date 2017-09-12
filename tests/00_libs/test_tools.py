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

from mathmaker.lib.tools import \
    (check_unique_letters_words, rotate, is_number, is_integer, is_natural,
     move_digits_to, split_nb, is_power_of_10, decimal_places_nb,
     remove_digits_from, fix_digits, parse_layout_descriptor,
     fix_math_style2_fontsize, ext_dict, physical_quantity,
     difference_of_orders_of_magnitude)


def test_recursive_update():
    """Check recursive_update()"""
    d1 = ext_dict({'a': 1, 'b': 2,
                   'c': {'z': 26, 'y': 25, 'x': {1: 'a', 2: 'b'}}})
    d2 = ext_dict({'a': 11, 'c': {'y': 24, 'x': {2: 'f', 3: 'g'}, 'w': 23}})
    d1.recursive_update(d2)
    assert d1 == {'a': 11, 'b': 2,
                  'c': {'z': 26, 'y': 24, 'w': 23,
                        'x': {1: 'a', 2: 'f', 3: 'g'}}}


def test_flat():
    """Check flat()"""
    d = ext_dict({'a': 1, 'b': 2,
                  'c': {'z': 26, 'y': 25, 'x': {1: 'a', 2: 64}}})
    assert d.flat() == {'a': 1, 'b': 2,
                        'c.z': 26, 'c.y': 25, 'c.x.1': 'a', 'c.x.2': 64}


def test_check_unique_letters_words():
    """Check check_unique_letters_words() fails when appropriate."""
    with pytest.raises(ValueError):
        check_unique_letters_words(['abc'], 4)
    with pytest.raises(ValueError):
        check_unique_letters_words(['abc', 'djek', 'kel'], 3)
    with pytest.raises(ValueError):
        check_unique_letters_words(['abc', 'defg', 'kel'], 3)
    with pytest.raises(ValueError):
        check_unique_letters_words(['abcd', 'defg', 'kelk'], 4)


def test_rotate():
    """Check rotations of lists."""
    assert rotate([1, 2, 3, 4, 5], 3) == [3, 4, 5, 1, 2]
    assert rotate([1, 2, 3, 4, 5], -3) == [4, 5, 1, 2, 3]
    assert rotate([1, 2, 3], 3) == [1, 2, 3]
    assert rotate([1, 2, 3], -9) == [1, 2, 3]


def test_is_number():
    """Check numbers are correctly identified."""
    assert is_number(104)
    assert is_number(1.0)
    assert is_number(4 + 9.0 ** 3)
    assert is_number(Decimal('4'))
    assert not is_number('4')
    assert not is_number([1])


def test_is_integer():
    """Check integers are correctly identified."""
    assert is_integer(9)
    assert is_integer(-9)
    assert is_integer(10 + 59 // 7)
    assert is_integer(1.0)
    assert is_integer(-1.0)
    assert is_integer(Decimal('1.0'))
    assert is_integer(Decimal('-1.0'))
    assert not is_integer(Decimal('1.01'))
    assert not is_integer(Decimal('-1.01'))
    with pytest.raises(TypeError):
        is_integer('1.0')
    with pytest.raises(TypeError):
        is_integer('-1.0')


def test_is_natural():
    """Check naturals are correctly identified."""
    assert is_natural(0)
    assert is_natural(-0)
    assert is_natural(9)
    assert not is_natural(-9)
    assert is_natural(10 + 59 // 7)
    assert is_natural(1.0)
    assert not is_natural(-1.0)
    assert is_natural(Decimal('1.0'))
    assert not is_natural(Decimal('-1.0'))
    assert not is_natural(Decimal('1.01'))
    assert not is_natural(Decimal('-1.01'))
    with pytest.raises(TypeError):
        is_natural('1.0')
    with pytest.raises(TypeError):
        is_natural('-1.0')


def test_move_digits_to():
    """Check move_digits_to() in different cases."""
    with pytest.raises(TypeError):
        move_digits_to(14)
    with pytest.raises(TypeError):
        move_digits_to(14, (7, 5))
    with pytest.raises(TypeError):
        move_digits_to(14, {7: 'a', 6: 'b'})
    with pytest.raises(TypeError):
        move_digits_to(14, [7, '5'])
    with pytest.raises(TypeError):
        move_digits_to('14', [7, 5])
    assert move_digits_to(14, [7, 5]) == [14, 7, 5]
    assert move_digits_to(14, [Decimal('0.7'), 5]) \
        == [Decimal('1.4'), Decimal(7), 5]
    assert move_digits_to(14, [Decimal('0.7'), Decimal('0.5')]) \
        == [Decimal('0.14'), Decimal(7), Decimal(5)]


def test_remove_digits_from():
    """Check remove_digits_from() in different cases."""
    with pytest.raises(TypeError):
        remove_digits_from('14', to=[])
    with pytest.raises(TypeError):
        remove_digits_from(14)
    with pytest.raises(TypeError):
        remove_digits_from(1.4)
    with pytest.raises(ValueError):
        remove_digits_from(Decimal('1.4'), to=[])
    with pytest.raises(ValueError):
        remove_digits_from(Decimal('1.4'), to=[10, 20, 30])
    assert remove_digits_from(Decimal('1.4'), to=[10, 20, 36]) ==\
        [Decimal('14'), 10, 20, Decimal('3.6')]


def test_fix_digits():
    """Check fix_digits() in different cases."""
    n1, n2 = fix_digits(Decimal('0.6'), Decimal('2'))
    assert n1 == Decimal('6')
    assert n2 == Decimal('0.2')
    n1, n2 = fix_digits(Decimal('0.6'), Decimal('10'))
    assert n1 == Decimal('6')
    assert not is_integer(n2)
    n1, n2, n3 = fix_digits(Decimal('0.6'), Decimal('10'), Decimal('100'))
    assert n1 == Decimal('6')
    assert not is_integer(n2) or not is_integer(n3)


def test_is_power_of_10():
    """Check is_power_of_10() in different cases."""
    with pytest.raises(TypeError):
        is_power_of_10(0.01)
    with pytest.raises(TypeError):
        is_power_of_10('10')
    for n in [1, 10, 100, 1000, 10000, -1, -10, -100]:
        assert is_power_of_10(n)
    for n in [Decimal('0.1'), Decimal('0.01'), Decimal('0.001'),
              Decimal('-0.1'), Decimal('-0.01'), Decimal('-0.001')]:
        assert is_power_of_10(n)
    for n in [0, 2, Decimal('0.5'), Decimal('-0.02'), Decimal('10.09'),
              1001, -999]:
        assert not is_power_of_10(n)


def test_decimal_places_nb():
    """Check decimal_places_nb() in different cases."""
    assert all(decimal_places_nb(n) == 0 for n in [0, 1, 8, Decimal(4),
                                                   Decimal('4.0'),
                                                   Decimal('4.0000000000000000'
                                                           '0000')])
    assert all(decimal_places_nb(n) == 1 for n in [Decimal('0.4'),
                                                   Decimal('10.000') / 4])
    assert all(decimal_places_nb(n) == 0 for n in [-0, -1, -8, Decimal(-4),
                                                   Decimal('-4.0'),
                                                   Decimal('-4.000000000000000'
                                                           '00000')])
    assert all(decimal_places_nb(n) == 1 for n in [Decimal('-0.4'),
                                                   Decimal('-10.000') / 4])


def test_split_nb():
    """Check split_nb() in different cases."""
    with pytest.raises(ValueError):
        split_nb(10, operation='*')
    with pytest.warns(UserWarning):
        split_nb(1)
    with pytest.warns(UserWarning):
        split_nb(Decimal('0.1'))
    with pytest.warns(UserWarning):
        split_nb(Decimal('0.01'))
    result = split_nb(14)
    assert type(result) is tuple
    assert len(result) is 2
    assert is_integer(result[0]) and is_integer(result[1])
    assert 1 <= result[0] <= 13
    assert 1 <= result[1] <= 13
    for i in range(99):
        result = split_nb(14)
        assert 1 <= result[0] <= 13
        assert 1 <= result[1] <= 13
    result = split_nb(14, operation='-')
    assert all([is_integer(r) for r in result])
    assert result[0] - result[1] == 14
    result = split_nb(Decimal('4.3'))
    # Can not say 'all' will be decimals, because we could have: 3 + 1.3
    assert any([decimal_places_nb(r) == 1 for r in result])
    result = split_nb(4, dig=2)
    assert all([decimal_places_nb(r) == 2 for r in result])
    result = split_nb(-7)
    assert all(-6 <= r <= -1 for r in result)
    result = split_nb(Decimal('4.3'), dig=1)
    assert all([decimal_places_nb(r) == 2 for r in result])


def test_parse_layout_descriptor():
    """Test parse_layout_descriptor() in several cases."""
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor(4)
    assert 'The layout descriptor must be str' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', sep=[1])
    assert 'All items of the sep list must be str' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', sep=1)
    assert 'sep must be a str or a list' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', special_row_chars=4)
    assert 'special_row_char must be a list' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', special_row_chars=[4])
    assert 'All items of the special_row_chars list must be str' \
        in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', min_row='a')
    assert 'min_row and min_col must both be int' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', min_col='a')
    assert 'min_row and min_col must both be int' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', min_row=-2)
    assert 'min_row and min_col must both be positive' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', min_col=-2)
    assert 'min_row and min_col must both be positive' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×')
    assert 'The layout format must be a string like '\
        '\'row×col\', where × is your delimiter. ' \
        'Cannot find a row and a col in \'' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2x3')
    assert 'Cannot find a row and a col in \'' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2;')
    assert ' with any of the str from this list as delimiter: ' \
        in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×3', sep=['x'])
    assert ' with any of the str from this list as delimiter: ' \
        in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('a×3')
    assert 'Number of rows: \'a\' cannot be turned into int' \
        in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('3×a')
    assert 'Number of cols: \'a\' cannot be turned into int' \
        in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('?×3')
    assert 'Number of rows: \'?\' cannot be turned into int' \
        in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('0×3', min_row=1)
    assert 'nrow must be greater than 1' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('4×0', min_col=1)
    assert 'ncol must be greater than 1' in str(excinfo.value)

    assert parse_layout_descriptor('?×0', special_row_chars=['?'],
                                   min_row=1) == ('?', 0)
    assert parse_layout_descriptor('2×3', sep=['x', '×']) == (2, 3)
    assert parse_layout_descriptor('4×5') == (4, 5)
    assert parse_layout_descriptor('6×7', special_row_chars=['?']) == (6, 7)


def test_fix_math_style2_fontsize():
    """Test fix_math_style2_fontsize() in several cases."""
    assert fix_math_style2_fontsize('$ \\frac{\\text{6}}{\\text{20}} $ '
                                    '(or $ \\frac{\\text{3}}{\\text{10}} $) ')\
        == '{\Large{$ \\frac{\\text{6}}{\\text{20}} $}}' \
           '\\normalsize{ (or }' \
           '{\Large{$ \\frac{\\text{3}}{\\text{10}} $}}' \
           '\\normalsize{) }'
    assert fix_math_style2_fontsize(
        '$ \\frac{\\text{18}}{\\text{24}} $ '
        '(or $ \\frac{\\text{9}}{\\text{12}} $, '
        'or $ \\frac{\\text{6}}{\\text{8}} $, '
        'or $ \\frac{\\text{3}}{\\text{4}} $)') == \
        '{\Large{$ \\frac{\\text{18}}{\\text{24}} $}}' \
        '\\normalsize{ (or }' \
        '{\Large{$ \\frac{\\text{9}}{\\text{12}} $}}' \
        '\\normalsize{, or }' \
        '{\Large{$ \\frac{\\text{6}}{\\text{8}} $}}' \
        '\\normalsize{, or }' \
        '{\Large{$ \\frac{\\text{3}}{\\text{4}} $}}' \
        '\\normalsize{)}'


def test_physical_quantity_exceptions():
    """Check unknown units raise an error."""
    with pytest.raises(ValueError) as excinfo:
        physical_quantity('unknown')
    assert str(excinfo.value) == 'Cannot determine the physical quantity ' \
        'of provided unit (unknown).'


def test_physical_quantity():
    """Check units are recognized correctly."""
    assert physical_quantity('L') == 'capacity'
    assert physical_quantity('m') == 'length'
    assert physical_quantity('g') == 'mass'


def test_difference_of_orders_of_magnitude_exceptions():
    """Check wrong units trigger an error."""
    with pytest.raises(TypeError) as excinfo:
        difference_of_orders_of_magnitude('cm', 'hL')
    assert str(excinfo.value) == 'Cannot give the difference of orders of ' \
        'magnitude between two units that do not belong to the same physical '\
        'quantity (cm and hL).'


def test_difference_of_orders_of_magnitude():
    """Check the difference of orders of magnitude is calculated correctly."""
    assert difference_of_orders_of_magnitude('L', 'mL') == Decimal('1000')
    assert difference_of_orders_of_magnitude('cm', 'm') == Decimal('0.01')
    assert difference_of_orders_of_magnitude('kg', 'mg') == Decimal('1000000')
