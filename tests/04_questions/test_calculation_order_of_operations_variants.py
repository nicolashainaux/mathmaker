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

# import pytest
from decimal import Decimal

from mathmaker.lib.tools.auxiliary_functions import is_integer, digits_nb
from mathmaker.lib.sheet.exercise.question.calculation_modules \
    import calculation_order_of_operations


def test_variant1():
    """Check variant1 in several problematic cases."""
    # a + b÷c
    o = calculation_order_of_operations.sub_object(numbers_to_use=[10, 4, 5],
                                                   nb_variant='decimal1',
                                                   variant=1,
                                                   subvariant='only_positive')
    assert not is_integer(o.abcd[0])
    assert o.abcd[1] == Decimal('20')
    assert o.abcd[2] in [Decimal('4'), Decimal('5')]
    o = calculation_order_of_operations.sub_object(numbers_to_use=[10, 10, 10],
                                                   nb_variant='decimal1',
                                                   variant=1,
                                                   subvariant='only_positive')
    assert not is_integer(o.abcd[0])
    o = calculation_order_of_operations.sub_object(
        numbers_to_use=[10, 5, Decimal('0.4')],
        nb_variant='decimal1',
        variant=1,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[1] == Decimal('20')
    assert o.abcd[2] == Decimal('5')


def test_variant2():
    """Check variant2 in several problematic cases."""
    # a - b×c
    o = calculation_order_of_operations.sub_object(numbers_to_use=[1, 4, 5],
                                                   variant=2,
                                                   subvariant='only_positive')
    assert o.abcd[0] == Decimal('21')
    o = calculation_order_of_operations.sub_object(numbers_to_use=[10, 10, 10],
                                                   nb_variant='decimal1',
                                                   variant=2,
                                                   subvariant='only_positive')
    assert o.abcd[0] - o.abcd[1] * o.abcd[2] > 0


def test_variant3():
    """Check variant3 in a problematic case."""
    # a - b÷c
    o = calculation_order_of_operations.sub_object(
        numbers_to_use=[1, 5, Decimal('0.4')],
        nb_variant='decimal1',
        variant=3,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] - o.abcd[1] / o.abcd[2] > 0
    assert any(digits_nb(x) == 1 for x in [o.abcd[0], o.abcd[1]])


def test_variant5():
    """Check variant5 in a problematic case."""
    # a÷b + c
    o = calculation_order_of_operations.sub_object(
        numbers_to_use=[5, Decimal('0.4'), 1],
        nb_variant='decimal1',
        variant=5,
        subvariant='only_positive',
        direct_test=True)
    assert is_integer(o.abcd[1])
    assert any(digits_nb(x) == 1 for x in [o.abcd[0], o.abcd[2]])


def test_variant6():
    """Check variant6 in several problematic cases."""
    # a×b - c
    o = calculation_order_of_operations.sub_object(numbers_to_use=[2, 4, 5],
                                                   variant=6,
                                                   subvariant='only_positive',
                                                   direct_test=True)
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] >= 0
    o = calculation_order_of_operations.sub_object(
        numbers_to_use=[5, Decimal('0.4'), 10],
        nb_variant='decimal1',
        variant=6,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] >= 0
    assert o.abcd[0] != 1 and o.abcd[1] != 1


def test_variant7():
    """Check variant7 in several problematic cases."""
    # a÷b - c
    o = calculation_order_of_operations.sub_object(
        numbers_to_use=[5, Decimal('0.4'), 10],
        nb_variant='decimal1',
        variant=7,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] >= 0
    o = calculation_order_of_operations.sub_object(
        numbers_to_use=[Decimal('0.4'), 5, 3],
        nb_variant='decimal1',
        variant=7,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd == [Decimal('2.0'), Decimal('5'), Decimal('0.3')]
    o = calculation_order_of_operations.sub_object(
        numbers_to_use=[2, 9, 50],
        variant=7,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] >= 0


def test_variant9():
    """Check variant9 in several problematic cases."""
    # a×b - c×d
    o = calculation_order_of_operations.sub_object(numbers_to_use=[2, 3, 4, 5],
                                                   variant=9,
                                                   subvariant='only_positive',
                                                   direct_test=True)
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] * o.abcd[3] > 0
    o = calculation_order_of_operations.sub_object(
        numbers_to_use=[Decimal('0.7'), 8, 4, 5],
        variant=9,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] * o.abcd[3] > 0


def test_variant10():
    """Check variant10 in a problematic case."""
    # a÷b + c×d
    o = calculation_order_of_operations.sub_object(
        numbers_to_use=[Decimal('0.8'), 5, 8, 9],
        variant=10,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert any(digits_nb(x) == 1 for x in [o.abcd[2], o.abcd[3]])
