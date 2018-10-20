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

import locale
import pytest
from decimal import Decimal

from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.constants import LOCALE_US, LOCALE_FR
from tests.tools import wrap_nb


@pytest.fixture()
def v0(): return Value(4)


@pytest.fixture()
def v1(): return Value(4.2)


@pytest.fixture()
def v2(): return Value(4.25)


@pytest.fixture()
def v3(): return Value(4.257)


@pytest.fixture()
def v4(): return Value(4.2571)


@pytest.fixture()
def negv(): return Value(-4.2)


@pytest.fixture()
def perfect_square(): return Value(16)


@pytest.fixture()
def perfect_decimal_square(): return Value(1.96)


@pytest.fixture()
def literal_value(): return Value('AB')


def test_0_display(v0):
    """Is the value correctly displayed?"""
    assert str(v0) == wrap_nb('4')


def test_1_display(v1):
    """Is the value correctly displayed?"""
    assert str(v1) == wrap_nb('4.2')


def test_negv_display(negv):
    """Is the value correctly displayed?"""
    assert str(negv) == wrap_nb('-4.2')


def test_0digit_numbers(v0):
    """Is an integer's number of digits detected as 0?"""
    assert v0.digits_number() == 0


def test_1digit_numbers(v1):
    """Is the number of digits detected right?"""
    assert v1.digits_number() == 1


def test_2digit_numbers(v2):
    """Is the number of digits detected right?"""
    assert v2.digits_number() == 2


def test_3digit_numbers(v3):
    """Is the number of digits detected right?"""
    assert v3.digits_number() == 3


def test_4digit_numbers(v4):
    """Is the number of digits detected right?"""
    assert v4.digits_number() == 4


def test_round_0digit_to_unit(v0):
    """Is the number correctly rounded?"""
    assert v0.rounded(0).raw_value == 4


def test_round_1digit_to_unit(v1):
    """Is the number correctly rounded?"""
    assert v1.rounded(0).raw_value == 4


def test_round_2digit_to_unit(v2):
    """Is the number correctly rounded?"""
    assert v2.rounded(0).raw_value == 4


def test_round_3digit_to_unit(v3):
    """Is the number correctly rounded?"""
    assert v3.rounded(0).raw_value == 4


def test_round_4digit_to_unit(v4):
    """Is the number correctly rounded?"""
    assert v4.rounded(0).raw_value == 4


def test_round_0digit_to_tenth(v0):
    """Is the number correctly rounded?"""
    assert v0.rounded(1).raw_value == 4


def test_round_1digit_to_tenth(v1):
    """Is the number correctly rounded?"""
    assert v1.rounded(1).raw_value == Decimal('4.2')


def test_round_2digit_to_tenth(v2):
    """Is the number correctly rounded?"""
    assert v2.rounded(1).raw_value == Decimal('4.3')


def test_round_3digit_to_tenth(v3):
    """Is the number correctly rounded?"""
    assert v3.rounded(1).raw_value == Decimal('4.3')


def test_round_4digit_to_tenth(v4):
    """Is the number correctly rounded?"""
    assert v4.rounded(1).raw_value == Decimal('4.3')


def test_round_0digit_to_hundredth(v0):
    """Is the number correctly rounded?"""
    assert v0.rounded(2).raw_value == 4


def test_round_1digit_to_hundredth(v1):
    """Is the number correctly rounded?"""
    assert v1.rounded(2).raw_value == Decimal('4.2')


def test_round_2digit_to_hundredth(v2):
    """Is the number correctly rounded?"""
    assert v2.rounded(2).raw_value == Decimal('4.25')


def test_round_3digit_to_hundredth(v3):
    """Is the number correctly rounded?"""
    assert v3.rounded(2).raw_value == Decimal('4.26')


def test_round_4digit_to_hundredth(v4):
    """Is the number correctly rounded?"""
    assert v4.rounded(2).raw_value == Decimal('4.26')


def test_round_0digit_to_thousandth(v0):
    """Is the number correctly rounded?"""
    assert v0.rounded(3).raw_value == 4


def test_round_1digit_to_thousandth(v1):
    """Is the number correctly rounded?"""
    assert v1.rounded(3).raw_value == Decimal('4.2')


def test_round_2digit_to_thousandth(v2):
    """Is the number correctly rounded?"""
    assert v2.rounded(3).raw_value == Decimal('4.25')


def test_round_3digit_to_thousandth(v3):
    """Is the number correctly rounded?"""
    assert v3.rounded(3).raw_value == Decimal('4.257')


def test_round_4digit_to_thousandth(v4):
    """Is the number correctly rounded?"""
    assert v4.rounded(3).raw_value == Decimal('4.257')


def test_round_0digit_to_tenthousandth(v0):
    """Is the number correctly rounded?"""
    assert v0.rounded(4).raw_value == 4


def test_round_1digit_to_tenthousandth(v1):
    """Is the number correctly rounded?"""
    assert v1.rounded(4).raw_value == Decimal('4.2')


def test_round_2digit_to_tenthousandth(v2):
    """Is the number correctly rounded?"""
    assert v2.rounded(4).raw_value == Decimal('4.25')


def test_round_3digit_to_tenthousandth(v3):
    """Is the number correctly rounded?"""
    assert v3.rounded(4).raw_value == Decimal('4.257')


def test_round_4digit_to_tenthousandth(v4):
    """Is the number correctly rounded?"""
    assert v4.rounded(4).raw_value == Decimal('4.2571')


def test_needs_to_get_rounded_0digit_to_unit(v0):
    """Is the number correctly detected as needing to get rounded?"""
    assert not v0.needs_to_get_rounded(0)


def test_needs_to_get_rounded_0digit_to_tenth(v0):
    """Is the number correctly detected as needing to get rounded?"""
    assert not v0.needs_to_get_rounded(1)


def test_needs_to_get_rounded_1digit_to_unit(v1):
    """Is the number correctly detected as needing to get rounded?"""
    assert v1.needs_to_get_rounded(0)


def test_needs_to_get_rounded_1digit_to_tenth(v1):
    """Is the number correctly detected as needing to get rounded?"""
    assert not v1.needs_to_get_rounded(1)


def test_needs_to_get_rounded_1digit_to_hundredth(v1):
    """Is the number correctly detected as needing to get rounded?"""
    assert not v1.needs_to_get_rounded(2)


def test_needs_to_get_rounded_2digit_to_unit(v2):
    """Is the number correctly detected as needing to get rounded?"""
    assert v2.needs_to_get_rounded(0)


def test_needs_to_get_rounded_2digit_to_tenth(v2):
    """Is the number correctly detected as needing to get rounded?"""
    assert v2.needs_to_get_rounded(1)


def test_needs_to_get_rounded_2digit_to_hundredth(v2):
    """Is the number correctly detected as needing to get rounded?"""
    assert not v2.needs_to_get_rounded(2)


def test_needs_to_get_rounded_3digit_to_unit(v3):
    """Is the number correctly detected as needing to get rounded?"""
    assert v3.needs_to_get_rounded(0)


def test_needs_to_get_rounded_3digit_to_tenth(v3):
    """Is the number correctly detected as needing to get rounded?"""
    assert v3.needs_to_get_rounded(1)


def test_needs_to_get_rounded_3digit_to_hundredth(v3):
    """Is the number correctly detected as needing to get rounded?"""
    assert v3.needs_to_get_rounded(2)


def test_needs_to_get_rounded_3digit_to_thousandth(v3):
    """Is the number correctly detected as needing to get rounded?"""
    assert not v3.needs_to_get_rounded(3)


def test_needs_to_get_rounded_4digit_to_unit(v4):
    """Is the number correctly detected as needing to get rounded?"""
    assert v4.needs_to_get_rounded(0)


def test_needs_to_get_rounded_4digit_to_tenth(v4):
    """Is the number correctly detected as needing to get rounded?"""
    assert v4.needs_to_get_rounded(1)


def test_needs_to_get_rounded_4digit_to_hundredth(v4):
    """Is the number correctly detected as needing to get rounded?"""
    assert v4.needs_to_get_rounded(2)


def test_needs_to_get_rounded_4digit_to_thousandth(v4):
    """Is the number correctly detected as needing to get rounded?"""
    assert v4.needs_to_get_rounded(3)


def test_needs_to_get_rounded_4digit_to_tenthousandth(v4):
    """Is the number correctly detected as needing to get rounded?"""
    assert not v4.needs_to_get_rounded(4)


def test_is_a_perfect_square_sq(perfect_square):
    """Is the number detected as a perfect square?"""
    assert perfect_square.is_a_perfect_square()


def test_is_a_perfect_square_dsq(perfect_decimal_square):
    """Is the number detected as a perfect square?"""
    assert perfect_decimal_square.is_a_perfect_square()


def test_is_a_perfect_square_v2(v2):
    """Is the number detected as a perfect square?"""
    assert not v2.is_a_perfect_square()


def test_sqrt_sq_01(perfect_square):
    """Does the squared root of a perfect square have no digits?"""
    assert perfect_square.sqrt().digits_number() == 0


def test_is_integer_v0(v0):
    """Is a no-digit Value an integer?"""
    assert v0.is_an_integer()


def test_is_integer_v1(v1):
    """Is a one-digit Value not an integer?"""
    assert not v1.is_an_integer()


def test_literal_value_substituted(literal_value):
    """Is this Value correctly substituted?"""
    literal_value.substitute({Value('AB'): 11, Value('CD'): 10})
    assert literal_value.printed == wrap_nb('11')


def test_js_repr():
    """Is the "js" representation correct?"""
    assert Value(4).into_str(js_repr=True) == '4'
    assert Value('a').into_str(js_repr=True) == 'a'
    assert Value('units').into_str(js_repr=True) == 'units'
    assert Value(-4).into_str(js_repr=True) == '-4'
    locale.setlocale(locale.LC_NUMERIC, locale=LOCALE_FR)
    assert Value(Decimal('4.5')).into_str(js_repr=True) == '4.5'
    locale.setlocale(locale.LC_NUMERIC, locale=LOCALE_US)
