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

import pytest
from decimal import Decimal

from mathmaker.lib.tools.auxiliary_functions import \
    (check_unique_letters_words, rotate, is_number, is_integer, is_natural,
     remove_division_by_decimal, split_nb_into)


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


def test_remove_division_by_decimal():
    """Check remove_division_by_decimal() in different cases."""
    with pytest.raises(TypeError):
        remove_division_by_decimal(14)
    with pytest.raises(TypeError):
        remove_division_by_decimal(14, (7, 5))
    with pytest.raises(TypeError):
        remove_division_by_decimal(14, {7: 'a', 6: 'b'})
    with pytest.raises(TypeError):
        remove_division_by_decimal(14, [7, '5'])
    with pytest.raises(TypeError):
        remove_division_by_decimal('14', [7, 5])
    assert remove_division_by_decimal(14, [7, 5]) == [14, 7, 5]
    assert remove_division_by_decimal(14, [Decimal('0.7'), 5]) \
        == [Decimal('1.4'), Decimal(7), 5]
    assert remove_division_by_decimal(14, [Decimal('0.7'), Decimal('0.5')]) \
        == [Decimal('0.14'), Decimal(7), Decimal(5)]


def test_split_nb_into():
    """Check split_nb_into() in different cases."""
    with pytest.raises(ValueError):
        split_nb_into('+', 10)
    with pytest.raises(ValueError):
        split_nb_into('sum', Decimal('10.1'), nb_variant='decimal')
    with pytest.warns(UserWarning):
        split_nb_into('sum', 1)
    result = split_nb_into('sum', 14)
    assert type(result) is tuple
    assert len(result) is 2
    assert is_integer(result[0]) and is_integer(result[1])
    assert 1 <= result[0] <= 13
    assert 1 <= result[1] <= 13
    for i in range(99):
        result = split_nb_into('sum', 14)
        assert 1 <= result[0] <= 13
        assert 1 <= result[1] <= 13
    result = split_nb_into('difference', 14)
    assert all([is_integer(r) for r in result])
    assert result[0] - result[1] == 14
    result = split_nb_into('sum', 4, nb_variant='decimal1')
    assert all([is_integer(r) for r in result])
    result = split_nb_into('sum', Decimal('4.3'), nb_variant='decimal1')
    assert any([not is_integer(r) for r in result])
    result = split_nb_into('sum', 4, nb_variant='decimal1',
                           deci_restriction='+', extra_digits=1)
    assert all([len(str(r)) == 4 for r in result])
    result = split_nb_into('sum', -7)
    assert all(-6 <= r <= -1 for r in result)
