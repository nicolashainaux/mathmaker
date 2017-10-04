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
from decimal import Decimal, ROUND_HALF_UP

from mathmaker.lib.tools.numbers import Number
from mathmaker.lib.tools.numbers import is_number, is_integer, is_natural
from mathmaker.lib.tools.numbers import move_fracdigits_to
from mathmaker.lib.tools.numbers import remove_fracdigits_from, fix_fracdigits


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
        move_fracdigits_to(14)
    with pytest.raises(TypeError):
        move_fracdigits_to(14, (7, 5))
    with pytest.raises(TypeError):
        move_fracdigits_to(14, {7: 'a', 6: 'b'})
    with pytest.raises(TypeError):
        move_fracdigits_to(14, [7, '5'])
    with pytest.raises(TypeError):
        move_fracdigits_to('14', [7, 5])
    assert move_fracdigits_to(14, [7, 5]) == [14, 7, 5]
    assert move_fracdigits_to(14, [Decimal('0.7'), 5]) \
        == [Decimal('1.4'), Decimal(7), 5]
    assert move_fracdigits_to(14, [Decimal('0.7'), Decimal('0.5')]) \
        == [Decimal('0.14'), Decimal(7), Decimal(5)]


def test_remove_digits_from():
    """Check remove_digits_from() in different cases."""
    with pytest.raises(TypeError):
        remove_fracdigits_from('14', to=[])
    with pytest.raises(TypeError):
        remove_fracdigits_from(14)
    with pytest.raises(TypeError):
        remove_fracdigits_from(1.4)
    with pytest.raises(ValueError):
        remove_fracdigits_from(Decimal('1.4'), to=[])
    with pytest.raises(ValueError):
        remove_fracdigits_from(Decimal('1.4'), to=[10, 20, 30])
    assert remove_fracdigits_from(Decimal('1.4'), to=[10, 20, 36]) ==\
        [Decimal('14'), 10, 20, Decimal('3.6')]


def test_fix_digits():
    """Check fix_digits() in different cases."""
    n1, n2 = fix_fracdigits(Decimal('0.6'), Decimal('2'))
    assert n1 == Decimal('6')
    assert n2 == Decimal('0.2')
    n1, n2 = fix_fracdigits(Decimal('0.6'), Decimal('10'))
    assert n1 == Decimal('6')
    assert not is_integer(n2)
    n1, n2, n3 = fix_fracdigits(Decimal('0.6'), Decimal('10'), Decimal('100'))
    assert n1 == Decimal('6')
    assert not is_integer(n2) or not is_integer(n3)


def test_rounded():
    """Check rounding is good."""
    assert Number(4.2).rounded(0) == 4
    assert Number(4.2).rounded(Decimal('1'), rounding=ROUND_HALF_UP) == 4


def test_is_power_of_10():
    """Check is_power_of_10() in different cases."""
    for n in [1, 10, 100, 1000, 10000, -1, -10, -100]:
        assert Number(n).is_power_of_10()
    for n in [Decimal('0.1'), Decimal('0.01'), Decimal('0.001'),
              Decimal('-0.1'), Decimal('-0.01'), Decimal('-0.001')]:
        assert Number(n).is_power_of_10()
    for n in [0, 2, Decimal('0.5'), Decimal('-0.02'), Decimal('10.09'),
              1001, -999]:
        assert not Number(n).is_power_of_10()


def test_nonzero_digits_nb():
    """Check nonzero_digits_nb() in different cases."""
    assert Number('0').nonzero_digits_nb() == 0
    assert Number('2.0').nonzero_digits_nb() == 1
    assert Number('0.2').nonzero_digits_nb() == 1
    assert Number('0.104').nonzero_digits_nb() == 2
    assert Number('30.506').nonzero_digits_nb() == 3


def test_isolated_zeros():
    """Check isolated_zeros() in different cases."""
    assert Number('0').isolated_zeros() == 0
    assert Number('10').isolated_zeros() == 0
    assert Number('100').isolated_zeros() == 0
    assert Number('1010').isolated_zeros() == 1
    assert Number('3.871').isolated_zeros() == 0
    assert Number('3.801').isolated_zeros() == 1
    assert Number('3.001').isolated_zeros() == 2
    assert Number('3.0001').isolated_zeros() == 3
    assert Number('10.04').isolated_zeros() == 2
    assert Number('0.04').isolated_zeros() == 0
    assert Number('0.0409').isolated_zeros() == 1
    assert Number('0.3006').isolated_zeros() == 2


def test_decimal_places_nb():
    """Check decimal_places_nb() in different cases."""
    assert all(Number(n).decimal_places_nb() == 0
               for n in [0, 1, 8, Decimal(4), Decimal('4.0'),
                         Decimal('4.00000000000000000000')])
    assert all(Number(n).decimal_places_nb() == 1
               for n in [Decimal('0.4'), Decimal('10.000') / 4])
    assert all(Number(n).decimal_places_nb() == 0
               for n in [-0, -1, -8, Decimal(-4), Decimal('-4.0'),
                         Decimal('-4.00000000000000000000')])
    assert all(Number(n).decimal_places_nb() == 1
               for n in [Decimal('-0.4'), Decimal('-10.000') / 4])


def test_atomized():
    """Check atomized()."""
    assert Number('0').atomized() == [Number('0')]
    assert Number('0.683').atomized() == [Number('0.6'), Number('0.08'),
                                          Number('0.003')]
    assert Number('25.104').atomized() == [Number('20'), Number('5'),
                                           Number('0.1'), Number('0.004')]
    assert Number('25.104').atomized(keep_zeros=True) == \
        [Number('20'), Number('5'), Number('0.1'), Number('0.0'),
         Number('0.004')]


def test_overlap_level():
    """Check overlap_level()."""
    assert Number('0.724').overlap_level() == 1
    assert Number('0.714').overlap_level() == 0
    assert Number('0.704').overlap_level() == 0
    assert Number('0.74').overlap_level() == 0
    assert Number('0.7').overlap_level() == -1
    assert Number('0.7224').overlap_level() == 2
    assert Number('0.7124').overlap_level() == 1
    assert Number('0.7214').overlap_level() == 1
    assert Number('0.7024').overlap_level() == 1
    assert Number('0.7204').overlap_level() == 1
    assert Number('0.7114').overlap_level() == 0
    assert Number('0.7104').overlap_level() == 0
    assert Number('0.17').overlap_level() == 0


def test_cut_exceptions():
    """Check cut() raises exceptions in expected cases."""
    with pytest.raises(ValueError) as excinfo:
        Number(10).cut(overlap=-1)
    assert str(excinfo.value) == 'overlap must be a positive int. Got a ' \
        'negative int instead.'
    with pytest.raises(TypeError) as excinfo:
        Number(10).cut(overlap='a')
    assert str(excinfo.value) == 'When overlap is used, it must be an int. ' \
        'Got a <class \'str\'> instead.'
    with pytest.raises(ValueError) as excinfo:
        Number('4.3').cut(overlap=1)
    assert str(excinfo.value) == 'Given overlap is too high.'
    with pytest.raises(ValueError) as excinfo:
        Number('4.63').cut(overlap=1)
    assert str(excinfo.value) == 'Only overlap=0 is implemented yet.'


def test_cut():
    """Check cut() in various cases."""
    assert Number('4.3').cut() == (Number('4'), Number('0.3'))
    assert Number('4.03').cut() == (Number('4'), Number('0.03'))
    assert Number('4.63').cut(return_all=True) == \
        [(Number('4'), Number('0.63')), (Number('4.6'), Number('0.03'))]
    assert Number('5.836').cut(return_all=True) == \
        [(Number('5'), Number('0.836')),
         (Number('5.8'), Number('0.036')),
         (Number('5.83'), Number('0.006'))]
    assert Number('5.806').cut(return_all=True) == \
        [(Number('5'), Number('0.806')),
         (Number('5.8'), Number('0.006'))]
    # assert Number('5.36').cut(overlap=1, return_all=True) == \
    #     [(Number('5.1'), Number('0.26')),
    #      (Number('5.2'), Number('0.16'))]


def test_split_exceptions():
    """Check split() raises exceptions in expected cases."""
    with pytest.raises(ValueError):
        Number(10).split(operation='*')
    with pytest.warns(UserWarning):
        Number(1).split()
    with pytest.warns(UserWarning):
        Number('0.1').split()
    with pytest.warns(UserWarning):
        Number('0.01').split()


def test_split():
    """Check split() in different cases."""
    result = Number(14).split()
    assert type(result) is tuple
    assert len(result) is 2
    assert is_integer(result[0]) and is_integer(result[1])
    assert 1 <= result[0] <= 13
    assert 1 <= result[1] <= 13
    for i in range(99):
        result = Number(14).split()
        assert 1 <= result[0] <= 13
        assert 1 <= result[1] <= 13
    result = Number(14).split(operation='-')
    assert all([is_integer(r) for r in result])
    assert result[0] - result[1] == 14
    result = Number('4.3').split()
    # Can not say 'all' will be decimals, because we could have: 3 + 1.3
    assert any([Number(r).decimal_places_nb() == 1 for r in result])
    result = Number(4).split(dig=2)
    assert all([Number(r).decimal_places_nb() == 2 for r in result])
    result = Number(-7).split()
    assert all(-6 <= r <= -1 for r in result)
    result = Number('4.3').split(dig=1)
    assert all([Number(r).decimal_places_nb() == 2 for r in result])
