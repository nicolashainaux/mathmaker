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

from mathmaker.lib.core.base_calculus import (Item, Sum, Product, Monomial,
                                              Polynomial)
from mathmaker.lib.core.base_calculus import BinomialIdentity, Expandable
from tools import wrap_nb


@pytest.fixture
def sum_of_squared_numbers(): return Sum([Item(('+', 4, 2)),
                                          Item(('+', 5, 2))])


@pytest.fixture
def complicated_sum_to_reduce():
    return Sum([Monomial(('+', 3, 1)),
                Item(4),
                Sum([Monomial(('+', 3, 1)),
                     Monomial(('+', 5, 2)),
                     Product([Item(-7), Item('a'), Item('b')])]),
                Product([Item('-a'), Item('b')]),
                Monomial(('+', 5, 2)),
                Item(2),
                Monomial(('-', 2, 1)),
                Product([Item(2), Item('a'), Item('b')])])


@pytest.fixture
def rubbish_polynomial():
    return Polynomial([Monomial(('+', 1, 2)), Monomial(('+', 7, 1)),
                       Monomial(('-', 10, 2)), Monomial(('-', 9, 1)),
                       Monomial(('+', 9, 2))])


def test_sum_of_sums():
    """
    Is Sum([Sum(['a', 'b']), Sum(['a', 'b'])]) correctly printed as a+b+a+b?
    """
    assert Sum([Sum(['a', 'b']), Sum(['a', 'b'])]).printed == 'a+b+a+b'


def test_sum_neg1plusx():
    """Is this Sum correctly printed as -1+x?"""
    assert Sum([Monomial(('-', 1, 0)), Monomial(('+', 1, 1))]).printed == \
        wrap_nb('-1+x')


def test_sum_neg1plusx_bis():
    """Is this Sum correctly printed as -1+x?"""
    assert Sum([Product(Item(-1)), Item('x')]).printed == wrap_nb('-1+x')


def test_sum_1plusx():
    """Is this Sum correctly printed as 1+x?"""
    assert Sum([Product(Item(1)), Item('x')]).printed == wrap_nb('1+x')


def test_sum_3squareplus5():
    """Is this Sum correctly printed as 3^{2}+5?"""
    p = Product([Item(3)])
    p.set_exponent(2)
    assert Sum([p, Item(5)]).printed == wrap_nb('3^{2}+5')


def test_complicated_sum_01():
    """Is this Sum correctly printed as 2-10x^{2}+9?"""
    assert Sum([Item(2),
                Product([Polynomial([Monomial(('-', 10, 2)),
                                     Monomial(('+', 9, 0))])])]).printed == \
        wrap_nb('2-10x^{2}+9')


def test_complicated_sum_02():
    """Is this Sum correctly printed as (6+x)^{2}+12(2+11x)?"""
    assert Sum([BinomialIdentity((Monomial(('+', 6, 0)),
                                  Monomial(('+', 1, 1)))),
                Expandable((Monomial(('+', 12, 0)),
                            Sum([Polynomial([Monomial(('+', 2, 0)),
                                             Monomial(('+', 11, 1))])])
                            ))]).printed == wrap_nb('(6+x)^{2}+12(2+11x)')


def test_complicated_sum_03():
    """Is this Sum correctly printed as (6+x)^{2}+1?"""
    assert Sum([BinomialIdentity((Monomial(('+', 6, 0)),
                                  Monomial(('+', 1, 1)))),
                Item(1)]).printed == wrap_nb('(6+x)^{2}+1')


def test_sum_of_sum_plus_1():
    """Is this Sum correctly printed as 5+7+1?"""
    assert Sum([Sum([Item(5), Item(7)]), Item(1)]).printed == wrap_nb('5+7+1')


def test_sum_of_squared_numbers(sum_of_squared_numbers):
    """Is this Sum correctly printed as 4^{2}+5^{2}?"""
    assert sum_of_squared_numbers.printed == wrap_nb('4^{2}+5^{2}')


def test_sum_of_squared_numbers_calculate(sum_of_squared_numbers):
    """Is the next calculation step of this Sum equal to 16+25?"""
    assert sum_of_squared_numbers.calculate_next_step() == Sum([Item(16),
                                                                Item(25)])


def test_complicated_sum_to_reduce(complicated_sum_to_reduce):
    """Is this Sum printed as 3x+4+3x+5x^{2}-7ab-ab+5x^{2}+2-2x+2ab?"""
    assert complicated_sum_to_reduce.printed == \
        wrap_nb('3x+4+3x+5x^{2}-7ab-ab+5x^{2}+2-2x+2ab')


def test_complicated_sum_to_reduce_inter_line(complicated_sum_to_reduce):
    """Is this Sum's intermediate line (3+3-2)x+4+2+(5+5)x^{2}+(-7-1+2)ab?"""
    assert complicated_sum_to_reduce.intermediate_reduction_line().printed ==\
        wrap_nb('(3+3-2)x+4+2+(5+5)x^{2}+(-7-1+2)ab')


def test_complicated_sum_to_reduce_reduced(complicated_sum_to_reduce):
    """Is this Sum reduced as 4x+6+10x^{2}-6ab?"""
    assert complicated_sum_to_reduce.reduce_().printed ==\
        wrap_nb('4x+6+10x^{2}-6ab')


def test_rubbish_polynomial(rubbish_polynomial):
    """Is this Polynomial printed as x^{2}+7x-10x^{2}-9x+9x^{2}?"""
    assert rubbish_polynomial.printed == wrap_nb('x^{2}+7x-10x^{2}-9x+9x^{2}')


def test_rubbish_polynomial_inter_line(rubbish_polynomial):
    """Is this Polynomial inter line as (1-10+9)x^{2}+(7-9)x?"""
    assert rubbish_polynomial.intermediate_reduction_line().printed ==\
        wrap_nb('(1-10+9)x^{2}+(7-9)x')


def test_rubbish_polynomial_reduced(rubbish_polynomial):
    """Is this Polynomial reduced as -2x?"""
    assert rubbish_polynomial.reduce_().printed == wrap_nb('-2x')
