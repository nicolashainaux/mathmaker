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

from mathmaker.lib.core.base_calculus import Item, Product, Fraction
from tests.tools import wrap_nb


@pytest.fixture
def f1(): return Fraction(('+', 92, 76))


@pytest.fixture
def f2(): return Fraction(('+',
                           Product([Item(10), Item(6)]),
                           Product([Item(7), Item(2)])))


def test_f1_printed(f1):
    """Is this Fraction correctly printed?"""
    assert f1.printed == wrap_nb('\\frac{92}{76}')


def test_f1_next_step(f1):
    """Is this Fraction's calculation's next step correct?"""
    assert f1.calculate_next_step().printed == \
        wrap_nb('\\frac{\\bcancel{2}\\times 46}{\\bcancel{2}\\times 38}')


def test_f1_next_step2(f1):
    """Is this Fraction's calculation's 2d next step correct?"""
    assert f1.calculate_next_step().calculate_next_step().printed == \
        wrap_nb('\\frac{\\bcancel{2}\\times 23}{\\bcancel{2}\\times 19}')


def test_f1_simplified(f1):
    """Is this Fraction's simplification's next step correct?"""
    assert f1.simplified().printed == wrap_nb('\\frac{46}{38}')


def test_f1_simplification_line_simplified(f1):
    """Is this Fraction's simplification's next step correct?"""
    assert f1.simplification_line().simplified().printed == \
        wrap_nb('\\frac{46}{38}')


def test_f2_is_reducible(f2):
    """Is this Fraction reducible?"""
    assert f2.is_reducible()


def test_f2_next_step(f2):
    """Is this Fraction's calculation's next step correct?"""
    assert f2.calculate_next_step().printed == \
        wrap_nb('\\frac{\\bcancel{2}\\times 5\\times 6}'
                '{7\\times \\bcancel{2}}')


def test_f3_simplification_line():
    """Is this Fraction's simplification line correct?"""
    assert Fraction(('+',
                     Product([Item(7), Item(6)]),
                     Product([Item(3), Item(3)])))\
        .simplification_line().printed == \
        wrap_nb('\\frac{7\\times \\bcancel{3}\\times 2}'
                '{\\bcancel{3}\\times 3}')


def test_f4_next_step():
    """Is this Fraction's calculation's next step correct?"""
    assert Fraction(('+',
                     Product([Item(3), Item(7)]),
                     Product([Item(10), Item(4)])))\
        .calculate_next_step().printed == wrap_nb('\\frac{21}{40}')


def test_f5_simplification_line():
    """Is this Fraction's simplification line correct?"""
    assert Fraction(('+',
                     Product([Item(8), Item(3)]),
                     Product([Item(5), Item(6)])))\
        .simplification_line().printed == \
        wrap_nb('\\frac{\\bcancel{2}\\times 4\\times \\bcancel{3}}{5\\times'
                ' \\bcancel{2}\\times \\bcancel{3}}')


def test_f6_simplification_line():
    """Is this Fraction's simplification line correct?"""
    assert Fraction(('+',
                     Product([Item(10), Item(5)]),
                     Product([Item(5), Item(9)])))\
        .simplification_line().printed == \
        wrap_nb('\\frac{10\\times \\bcancel{5}}{\\bcancel{5}\\times 9}')


def test_f7_reduced():
    """Is this Fraction's simplification correct?"""
    assert Fraction(('+', 3, 7)).completely_reduced().printed == \
        wrap_nb('\\frac{3}{7}')


def test_f7_is_not_decimal():
    """Is this Fraction not decimal?"""
    assert not Fraction(('+', 3, 7)).is_a_decimal_number()


def test_f8_is_not_decimal():
    """Is this Fraction not decimal?"""
    assert not Fraction(('+', 9, 700)).is_a_decimal_number()


def test_f9_is_decimal():
    """Is this Fraction not decimal?"""
    assert Fraction(('+', 9, 2500)).is_a_decimal_number()


def test_f10_is_decimal():
    """Is this Fraction not decimal?"""
    assert Fraction(('+', 7, 700)).is_a_decimal_number()


def test_f11_eval():
    """Is this Fraction correctly evaluated?"""
    assert Fraction((Item(3), Item(8))).evaluate() == Decimal('0.375')


def test_f12_eval():
    """Is this Fraction correctly evaluated?"""
    assert Fraction((Item(3), Item(7))).evaluate() == \
        Decimal('0.4285714285714285714285714286')


def test_f12_eval2():
    """Is this Fraction correctly evaluated?"""
    assert Fraction((Item(3), Item(7)))\
        .evaluate(keep_not_decimal_nb_as_fractions=True).printed == \
        wrap_nb('\\frac{3}{7}')


def test_fraction_evaluation():
    """Check fractions are correctly evaluated."""
    assert Fraction(Decimal('0.4')).evaluate() == Decimal('0.4')


def test_fraction_from_decimal():
    """Are decimal fractions created correctly from decimals?"""
    assert Fraction(Decimal('0.56')).printed == wrap_nb('\\frac{56}{100}')
    assert Fraction(Decimal('0.938')).printed == wrap_nb('\\frac{938}{1000}')
    assert Fraction(Decimal('0.4')).printed == wrap_nb('\\frac{4}{10}')
    assert Fraction(Decimal('2.17')).printed == wrap_nb('\\frac{217}{100}')
    assert Fraction(Decimal('4')).printed == wrap_nb('\\frac{40}{10}')


def test_fractions_comparisons():
    """Check fractions compare correctly to other numbers."""
    assert Fraction(Decimal('0.56')) > Fraction(Decimal('0.31'))
    assert Fraction(Decimal('0.31')) < Fraction(Decimal('0.56'))
    assert Fraction(Decimal('0.56')) >= Fraction(Decimal('0.31'))
    assert Fraction(Decimal('0.31')) <= Fraction(Decimal('0.56'))
    assert Fraction(Decimal('0.56')) > Decimal('0.31')
    assert Fraction(Decimal('0.31')) < Decimal('0.56')
    assert Fraction(Decimal('0.56')) >= Decimal('0.31')
    assert Fraction(Decimal('0.31')) <= Decimal('0.56')
    assert Decimal('0.56') > Fraction(Decimal('0.31'))
    assert Decimal('0.31') < Fraction(Decimal('0.56'))
    assert Decimal('0.56') >= Fraction(Decimal('0.31'))
    assert Decimal('0.31') <= Fraction(Decimal('0.56'))
    assert 2 <= Fraction(Decimal('4.56'))
    assert 2.9 < Fraction(Decimal('4.56'))
