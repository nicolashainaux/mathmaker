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

# import pytest
from decimal import Decimal

from mathmakerlib.calculus.number import is_integer, Number

from mathmaker.lib.document.content.calculation \
    import order_of_operations


def test_variant1():
    """Check variant1 in several problematic cases."""
    # a + b÷c
    o = order_of_operations.sub_object(build_data=[10, 4, 5],
                                       nb_variant='decimal1',
                                       variant=1,
                                       subvariant='only_positive')
    assert not is_integer(o.abcd[0])
    assert o.abcd[1] == Decimal('20')
    assert o.abcd[2] in [Decimal('4'), Decimal('5')]
    o = order_of_operations.sub_object(build_data=[10, 10, 10],
                                       nb_variant='decimal1',
                                       variant=1,
                                       subvariant='only_positive')
    assert not is_integer(o.abcd[0])
    o = order_of_operations.sub_object(
        build_data=[10, 5, Decimal('0.4')],
        nb_variant='decimal1',
        variant=1,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[1] == Decimal('20')
    assert o.abcd[2] == Decimal('5')


def test_variant2():
    """Check variant2 in several problematic cases."""
    # a - b×c
    o = order_of_operations.sub_object(build_data=[1, 4, 5],
                                       variant=2,
                                       subvariant='only_positive')
    assert o.abcd[0] == Decimal('21')
    o = order_of_operations.sub_object(build_data=[10, 10, 10],
                                       nb_variant='decimal1',
                                       variant=2,
                                       subvariant='only_positive')
    assert o.abcd[0] - o.abcd[1] * o.abcd[2] > 0


def test_variant3():
    """Check variant3 in a problematic case."""
    # a - b÷c
    o = order_of_operations.sub_object(
        build_data=[1, 5, Decimal('0.4')],
        nb_variant='decimal1',
        variant=3,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] - o.abcd[1] / o.abcd[2] > 0
    assert any(Number(x).fracdigits_nb() == 1
               for x in [o.abcd[0], o.abcd[1]])


def test_variant5():
    """Check variant5 in a problematic case."""
    # a÷b + c
    o = order_of_operations.sub_object(
        build_data=[5, Decimal('0.4'), 1],
        nb_variant='decimal1',
        variant=5,
        subvariant='only_positive',
        direct_test=True)
    assert is_integer(o.abcd[1])
    assert any(Number(x).fracdigits_nb() == 1
               for x in [o.abcd[0], o.abcd[2]])


def test_variant6():
    """Check variant6 in several problematic cases."""
    # a×b - c
    o = order_of_operations.sub_object(build_data=[2, 4, 5],
                                       variant=6,
                                       subvariant='only_positive',
                                       direct_test=True)
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] >= 0
    o = order_of_operations.sub_object(
        build_data=[5, Decimal('0.4'), 10],
        nb_variant='decimal1',
        variant=6,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] >= 0
    assert o.abcd[0] != 1 and o.abcd[1] != 1


def test_variant7():
    """Check variant7 in several problematic cases."""
    # a÷b - c
    o = order_of_operations.sub_object(
        build_data=[5, Decimal('0.4'), 10],
        nb_variant='decimal1',
        variant=7,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] >= 0
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.4'), 5, 3],
        nb_variant='decimal1',
        variant=7,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd == [Decimal('2.0'), Decimal('5'), Decimal('0.3')]
    o = order_of_operations.sub_object(
        build_data=[2, 9, 50],
        variant=7,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] >= 0


def test_variant9():
    """Check variant9 in several problematic cases."""
    # a×b - c×d
    o = order_of_operations.sub_object(build_data=[2, 3, 4, 5],
                                       variant=9,
                                       subvariant='only_positive',
                                       direct_test=True)
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] * o.abcd[3] > 0
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.7'), 8, 4, 5],
        variant=9,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] * o.abcd[3] > 0


def test_variant10():
    """Check variant10 in a problematic case."""
    # a÷b + c×d
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.8'), 5, 8, 9],
        variant=10,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert any(Number(x).fracdigits_nb() == 1
               for x in [o.abcd[2], o.abcd[3]])


def test_variant11_naturals():
    """Check variant11 in several problematic cases."""
    # a÷b - c×d
    o = order_of_operations.sub_object(
        build_data=[2, 3, 8, 9],
        variant=11,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] * o.abcd[3] > 0
    assert o.abcd[0] == 72
    o = order_of_operations.sub_object(
        build_data=[2, 3, 9, 8],
        variant=11,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] * o.abcd[3] > 0
    assert o.abcd[0] == 72
    o = order_of_operations.sub_object(
        build_data=[9, 8, 2, 3],
        variant=11,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] * o.abcd[3] > 0
    assert o.abcd[0] == 72
    o = order_of_operations.sub_object(
        build_data=[4, 7, 2, 3],
        variant=11,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] * o.abcd[3] > 0
    assert (o.abcd[0], o.abcd[1]) == (28, 4)
    o = order_of_operations.sub_object(
        build_data=[3, 3, 3, 3],
        variant=11,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] * o.abcd[3] > 0
    assert (o.abcd[0], o.abcd[1]) == (90, 3)
    o = order_of_operations.sub_object(
        build_data=[2, 3, 5, 5],
        variant=11,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd == [Decimal('60'), Decimal('2'), Decimal('5'), Decimal('5')]
    o = order_of_operations.sub_object(
        build_data=[2, 4, 6, 7],
        variant=11,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] == Decimal('420')
    o = order_of_operations.sub_object(
        build_data=[2, 31, 6, 52],
        variant=11,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[:2] == [Decimal('3120'), Decimal('6')]
    o = order_of_operations.sub_object(
        build_data=[4, 66, 26, 26],
        variant=11,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd == [Decimal('26400'), Decimal('4'),
                      Decimal('26'), Decimal('26')]


def test_variant11_decimals():
    """Check variant11 in several problematic cases."""
    # a÷b - c×d
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.4'), 15, 3, 2],
        variant=11,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.variant == 11
    assert is_integer(o.abcd[1])
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] * o.abcd[3] > 0
    assert o.abcd[:2] == [Decimal('60'), Decimal('15')]
    assert any([not is_integer(x) for x in o.abcd[-2:]])
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.4'), 12, 3, 2],
        variant=11,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.variant == 11
    assert o.abcd[:2] == [Decimal('48'), Decimal('12')]
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.2'), 6, 7, 3],
        variant=11,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.variant == 13
    assert o.abcd[-2:] == [Decimal('1.2'), Decimal('6')]


def test_variant13_naturals():
    """Check variant13 in several problematic cases."""
    # a×b - c÷d
    o = order_of_operations.sub_object(
        build_data=[2, 3, 8, 9],
        variant=13,
        subvariant='only_positive',
        direct_test=True)
    assert set(o.abcd[0:2]) == {8, 9}
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] / o.abcd[3] > 0
    assert o.abcd[2] == 6
    o = order_of_operations.sub_object(
        build_data=[2, 3, 9, 8],
        variant=13,
        subvariant='only_positive',
        direct_test=True)
    assert set(o.abcd[0:2]) == {8, 9}
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] / o.abcd[3] > 0
    assert o.abcd[2] == 6
    o = order_of_operations.sub_object(
        build_data=[9, 8, 2, 3],
        variant=13,
        subvariant='only_positive',
        direct_test=True)
    assert set(o.abcd[0:2]) == {8, 9}
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] / o.abcd[3] > 0
    assert o.abcd[2] == 6
    o = order_of_operations.sub_object(
        build_data=[2, 3, 7, 7],
        variant=13,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0:3] == [Decimal('7'), Decimal('7'), Decimal('6')]
    o = order_of_operations.sub_object(
        build_data=[3, 3, 3, 3],
        variant=13,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd == [Decimal('3'), Decimal('3'), Decimal('9'), Decimal('3')]
    o = order_of_operations.sub_object(
        build_data=[2, 2, 5, 2],
        variant=13,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd == [Decimal('2'), Decimal('2'), Decimal('10'), Decimal('5')]
    o = order_of_operations.sub_object(
        build_data=[2, 2, 5, 5],
        variant=13,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd == [Decimal('5'), Decimal('5'), Decimal('4'), Decimal('2')]


def test_variant13_decimals():
    """Check variant13 in several problematic cases."""
    # a×b - c÷d
    o = order_of_operations.sub_object(
        build_data=[3, 2, 15, Decimal('0.4')],
        variant=13,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.variant == 11
    assert is_integer(o.abcd[1])
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] * o.abcd[3] > 0
    o = order_of_operations.sub_object(
        build_data=[7, 7, 15, Decimal('0.4')],
        variant=13,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.variant == 13
    assert is_integer(o.abcd[3])
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] / o.abcd[3] > 0
    assert any([not is_integer(x) for x in o.abcd])
    o = order_of_operations.sub_object(
        build_data=[10, 10, Decimal('0.4'), 15],
        variant=13,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.variant == 13
    assert is_integer(o.abcd[3])
    assert o.abcd[0] * o.abcd[1] - o.abcd[2] / o.abcd[3] > 0
    assert any([not is_integer(x) for x in o.abcd])


def test_variant14():
    """Check variant14 in some problematic cases."""
    # a÷b + c÷d
    o = order_of_operations.sub_object(
        build_data=[2, 9, 15, Decimal('0.4')],
        variant=14,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert is_integer(o.abcd[1])
    assert is_integer(o.abcd[3])
    assert any(not is_integer(x) for x in [o.abcd[0], o.abcd[2]])
    o = order_of_operations.sub_object(
        build_data=[15, Decimal('0.4'), 2, 9],
        variant=14,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert is_integer(o.abcd[1])
    assert is_integer(o.abcd[3])
    assert any(not is_integer(x) for x in [o.abcd[0], o.abcd[2]])
    o = order_of_operations.sub_object(
        build_data=[2, 5, 15, Decimal('0.4')],
        variant=14,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert is_integer(o.abcd[1])
    assert is_integer(o.abcd[3])
    assert any(not is_integer(x) for x in [o.abcd[0], o.abcd[2]])


def test_variant15():
    """Check variant15 in a problematic case."""
    # a÷b - c÷d
    o = order_of_operations.sub_object(
        build_data=[2, 9, Decimal('0.4'), 15],
        variant=15,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert is_integer(o.abcd[1])
    assert is_integer(o.abcd[3])
    assert any(not is_integer(x) for x in [o.abcd[0], o.abcd[2]])
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.4'), 15, 9, 2],
        variant=15,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert any(not is_integer(x) for x in o.abcd)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] / o.abcd[3] > 0
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.3'), 15, 9, 2],
        variant=15,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert any(not is_integer(x) for x in o.abcd)
    assert o.abcd[0] / o.abcd[1] - o.abcd[2] / o.abcd[3] > 0


def test_variant17():
    """Check variant17 in a problematic case."""
    # a + b÷c + d
    o = order_of_operations.sub_object(
        build_data=[5, 15, Decimal('0.4'), 3],
        variant=17,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert is_integer(o.abcd[2])
    assert any(not is_integer(x) for x in o.abcd)


def test_variant18():
    """Check variant18 in a problematic case."""
    # a - b×c + d
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.4'), 3, 5, 15],
        variant=18,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] > o.abcd[1] * o.abcd[2]


def test_variant19():
    """Check variant19 in a problematic case."""
    # a + b×c - d
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.3'), 2, 5, 15],
        variant=19,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] + o.abcd[1] * o.abcd[2] > o.abcd[3]


def test_variant20():
    """Check variant20 in a problematic case."""
    # a - b×c - d
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.3'), 6, 3, 12],
        variant=20,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] > o.abcd[1] * o.abcd[2] + o.abcd[3]


def test_variant21():
    """Check variant21 in two problematic cases."""
    # a - b÷c + d
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.3'), 6, 3, 12],
        variant=21,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] > o.abcd[1] / o.abcd[2]
    o = order_of_operations.sub_object(
        build_data=[10, 15, Decimal('0.4'), 10],
        variant=21,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert is_integer(o.abcd[2])
    assert any(not is_integer(x) for x in o.abcd)
    assert o.abcd[0] > o.abcd[1] / o.abcd[2]


def test_variant22():
    """Check variant22 in two problematic cases."""
    # a + b÷c - d
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.3'), 6, 3, 49],
        variant=22,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] + o.abcd[1] / o.abcd[2] > o.abcd[3]
    o = order_of_operations.sub_object(
        build_data=[10, 15, Decimal('0.4'), 10],
        variant=22,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert is_integer(o.abcd[2])
    assert any(not is_integer(x) for x in o.abcd)
    assert o.abcd[0] + o.abcd[1] / o.abcd[2] > o.abcd[3]


def test_variant23():
    """Check variant23 in two problematic cases."""
    # a - b÷c - d
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.3'), 6, 3, 49],
        variant=23,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] > o.abcd[1] / o.abcd[2]
    assert o.abcd[0] > o.abcd[1] / o.abcd[2] + o.abcd[3]
    o = order_of_operations.sub_object(
        build_data=[Decimal('0.3'), 6, 3, 1],
        variant=23,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] > o.abcd[1] / o.abcd[2]
    assert o.abcd[0] > o.abcd[1] / o.abcd[2] + o.abcd[3]
    o = order_of_operations.sub_object(
        build_data=[10, 15, Decimal('0.4'), 10],
        variant=23,
        nb_variant='decimal1',
        subvariant='only_positive',
        direct_test=True)
    assert is_integer(o.abcd[2])
    assert any(not is_integer(x) for x in o.abcd)
    assert o.abcd[0] > o.abcd[1] / o.abcd[2]
    assert o.abcd[0] > o.abcd[1] / o.abcd[2] + o.abcd[3]


def test_variant109():
    """Check variant109 in problematic cases."""
    # a×(b + c)÷d
    o = order_of_operations.sub_object(
        build_data=[7, 2, 5],
        variant=109,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[1] + o.abcd[2] == 10


def test_variant113():
    """Check variant113 in problematic cases."""
    # a×(b - c)÷d
    o = order_of_operations.sub_object(
        build_data=[7, 2, 5],
        variant=113,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[1] - o.abcd[2] == 10


def test_variant176():
    """Check variant176 in problematic cases."""
    # (a - b)×c + d
    o = order_of_operations.sub_object(
        build_data=[10, 3, 8],
        variant=176,
        subvariant='only_positive',
        direct_test=True)
    assert o.abcd[0] - o.abcd[1] == 10
