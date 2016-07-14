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
import decimal

from mathmaker.lib.core.base_calculus import (Item, Sum, Product, Monomial,
                                              Fraction)
from tools import wrap_nb


@pytest.fixture
def one_by_one(): return Product([Item(1), Item(1)])


@pytest.fixture
def one_by_one_by_a(): return Product([Item(1), Item(1), Item('a')])


@pytest.fixture
def two_by_a_by_b(): return Product([Item(2), Item('a'), Item('b')])


@pytest.fixture
def one_by_negone(): return Product([Item(1), Item(-1)])


@pytest.fixture
def one_by_negb_by_1_by_4(): return Product([Item(1), Item('-b'),
                                             Item(1), Item(4)])


@pytest.fixture
def neg1_by_neg4(): return Product([Item(-1), Item(-4)])


@pytest.fixture
def neg1_by1by1by1(): return Product([Item(-1), Item(1), Item(1), Item(1)])


@pytest.fixture
def neg1_squared():
    p = Product(Item(-1))
    p.set_exponent(2)
    return p


@pytest.fixture
def neg3_by_neg5_exp_neg1_squared():
    p = Product([Item(-3), Item(-5)])
    p.set_exponent(Item(('+', -1, 2)))
    return p


@pytest.fixture
def complicated_product_01():
    p1 = Product([Item(-2), Item(7)])
    p1.set_exponent(2)
    return Product([Item(4), p1])


@pytest.fixture
def seven_by_sum_4_and_2():
    return Product([Item(7), Sum([Item(4), Item(2)])])


@pytest.fixture
def product_sum_3_plus_4_by_1():
    return Product([Sum([3, 4]), 1])


@pytest.fixture
def product_rubbish():
    return Product([Item(('+', 1, 1)), Item(('+', 'x', 1))])


@pytest.fixture
def product_1square():
    p = Product(Item(1))
    p.set_exponent(2)
    return p


@pytest.fixture
def big_product():
    s = Sum(['x', 3])
    s.set_exponent(3)
    p = Product(Monomial((1, 2)))
    p.set_exponent(3)
    p1 = Product([2, 3])
    p1.set_exponent(3)
    return Product([Monomial((2, 1)), Monomial((-4, 2)), s, Item(5), p,
                    Item(('+', -1, 2)), p1])


def test_nega_printed():
    """Is Product([Item("-a")]) correctly printed as -a?"""
    assert Product([Item("-a")]).printed == '-a'


def test_nega_is_not_reducible():
    """Is Product([Item("-a")]) correctly detected as not reducible?"""
    assert not Product([Item("-a")]).is_reducible()


def test_nega_bis_is_not_reducible():
    """
    Is Product([Item(('+', "-a", 1))]) correctly detected as not reducible?
    """
    assert not Product([Item(('+', "-a", 1))]).is_reducible()


def test_one_by_one_printed(one_by_one):
    """Is Product([Item(1), Item(1)]) correctly printed as 1?"""
    assert one_by_one.printed == wrap_nb('1')


def test_one_by_is_not_reducible(one_by_one):
    """Is Product([Item(1), Item(1)]) correctly detected as not reducible?"""
    assert not one_by_one.is_reducible()


def test_one_by_uncompact_printed(one_by_one):
    """
    Is Product([Item(1), Item(1)]) printed as 1\\times 1 when not compact?
    """
    one_by_one.set_compact_display(False)
    assert one_by_one.printed == wrap_nb('1\\times 1')


def test_one_by_one_by_a_printed(one_by_one_by_a):
    """Is Product([Item(1), Item(1), Item('a')]) correctly printed as a?"""
    assert one_by_one_by_a.printed == 'a'


def test_one_by_by_a_is_not_reducible(one_by_one_by_a):
    """Is Product([Item(1), Item(1), Item('a')]) detected as not reducible?"""
    assert not one_by_one_by_a.is_reducible()


def test_2_by_neg2_printed():
    """Is Product([Item(2), Item(-2)]) printed as 2\\times (-2)?"""
    assert Product([Item(2), Item(-2)]).printed == wrap_nb('2\\times (-2)')


def test_neg2_by_2_printed():
    """Is Product([Item(-2), Item(2)]) printed as -2\\times 2?"""
    assert Product([Item(-2), Item(2)]).printed == wrap_nb('-2\\times 2')


def test_mon_8_by_mon_neg6_printed():
    """
    Is Product([Monomial((8, 0)), Monomial((-6, 0))]) printed as 8\\times (-6)?
    """
    assert Product([Monomial((8, 0)), Monomial((-6, 0))]).printed == \
        wrap_nb('8\\times (-6)')


def test_two_by_a_by_b_printed():
    """Is Product([Item(2), Item('a'), Item('b')]) printed as 2ab?"""
    assert Product([Item(2), Item('a'), Item('b')]).printed == wrap_nb('2ab')


def test_two_by_a_by_b_not_reducible():
    """
    Is Product([Item(2), Item('a'), Item('b')]) detected as not reducible?
    """
    assert not Product([Item(2), Item('a'), Item('b')]).is_reducible()


def test_one_by_negone_printed(one_by_negone):
    """Is Product([Item(1), Item(-1)]) printed as -1?"""
    assert one_by_negone.printed == wrap_nb('-1')


def test_one_by_negone_uncompact_printed(one_by_negone):
    """
    Is Product([Item(1), Item(-1)]) printed as 1\\times (-1) when not compact?
    """
    one_by_negone.set_compact_display(False)
    assert one_by_negone.printed == wrap_nb('1\\times (-1)')


def test_1_by_negb_by_1_by_4_printed(one_by_negb_by_1_by_4):
    """Is this Product printed as -b\\times 4?"""
    assert one_by_negb_by_1_by_4.printed == wrap_nb('-b\\times 4')


def test_1_by_negb_by_1_by_4_not_reducible(one_by_negb_by_1_by_4):
    """Is this Product detected as reducible?"""
    assert one_by_negb_by_1_by_4.is_reducible()


def test_1_by_negb_by_1_by_4_uncompact_printed(one_by_negb_by_1_by_4):
    """Is this Product correctly printed when not compact?"""
    one_by_negb_by_1_by_4.set_compact_display(False)
    assert one_by_negb_by_1_by_4.printed == \
        wrap_nb('1\\times (-b)\\times 1\\times 4')


def test_neg1_by_neg4_printed(neg1_by_neg4):
    """Is this Product printed as -(-4)?"""
    assert neg1_by_neg4.printed == wrap_nb('-(-4)')


def test_neg1_by_neg4_is_reducible(neg1_by_neg4):
    """Is this Product detected as reducible?"""
    assert neg1_by_neg4.is_reducible()


def test_neg1_by_neg4_eval(neg1_by_neg4):
    """Is this Product evaluated as 4?"""
    assert neg1_by_neg4.evaluate() == 4


def test_neg1_by_4_printed():
    """Is Product([Item(-1), Item(4)]) printed as -4?"""
    assert Product([Item(-1), Item(4)]).printed == wrap_nb('-4')


def test_neg1_by1by1by1_printed(neg1_by1by1by1):
    """Is this Product printed as -1?"""
    assert neg1_by1by1by1.printed == wrap_nb('-1')


def test_neg1_by1by1by1_is_not_reducible(neg1_by1by1by1):
    """Is this Product not reducible?"""
    assert not neg1_by1by1by1.is_reducible()


def test_a_by_negb_printed():
    """Is this Product printed as a\\times (-b)?"""
    assert Product([Item('a'), (Item('-b'))]).printed == 'a\\times (-b)'


def test_a_by_negb_is_reducible():
    """Is this Product reducible?"""
    assert Product([Item('a'), (Item('-b'))]).is_reducible()


def test_a_by_negb_bis_printed():
    """Is this Product printed as a\\times (-b)?"""
    assert Product([Item('a'), Item(('+', "-b", 1))]).printed == \
        'a\\times (-b)'


def test_a_by_negb_bis_is_reducible():
    """Is this Product reducible?"""
    p = Product([Item('a'), Item(('+', "-b", 1))])
    p.set_compact_display(False)
    assert p.is_reducible()


def test_2_by_1_is_reducible():
    """Is Product([Item(2), (Item(1))]) reducible?"""
    p = Product([Item(2), (Item(1))])
    p.set_compact_display(False)
    assert p.is_reducible()


def test_1_by_7x_is_reducible():
    """Is Product([Item(1), (Monomial((7, 1)))]) reducible?"""
    p = Product([Item(1), (Monomial((7, 1)))])
    p.set_compact_display(False)
    assert p.is_reducible()


def test_neg1_squared_printed(neg1_squared):
    """Is this Product printed correctly?"""
    assert neg1_squared.printed == wrap_nb('(-1)^{2}')


def test_neg1_squared_not_displ_as_a_single_1(neg1_squared):
    """Is this Product not displayable as a single 1?"""
    assert not neg1_squared.is_displ_as_a_single_1()


def test_neg1_squared_not_displ_as_a_single_neg1(neg1_squared):
    """Is this Product not displayable as a single minus 1?"""
    assert not neg1_squared.is_displ_as_a_single_minus_1()


def test_neg1_squared_reducible(neg1_squared):
    """Is this Product reducible?"""
    assert neg1_squared.is_reducible()


def test_neg3_by_neg5_exp_neg1_squared_printed(neg3_by_neg5_exp_neg1_squared):
    """Is this Product correctly printed?"""
    assert neg3_by_neg5_exp_neg1_squared.printed == \
        wrap_nb('(-3\\times (-5))^{(-1)^{2}}')


def test_neg3_by_neg5_exp_neg1_squared_eval(neg3_by_neg5_exp_neg1_squared):
    """Is this Product correctly evaluated?"""
    assert neg3_by_neg5_exp_neg1_squared.evaluate() == 15


def test_4_by_neg2_by_7_printed():
    """Is this Product correctly printed?"""
    assert Product([Item(4), Product([Item(-2), Item(7)])]).printed == \
        wrap_nb('4\\times (-2)\\times 7')


def test_4_by_neg2_by_7_eval():
    """Is this Product correctly evaluated?"""
    assert Product([Item(4), Product([Item(-2), Item(7)])]).evaluate() == -56


def test_complicated_product_01_printed(complicated_product_01):
    """Is this Product correctly printed?"""
    assert complicated_product_01.printed == \
        wrap_nb('4\\times (-2\\times 7)^{2}')


def test_complicated_product_01_is_reducible(complicated_product_01):
    """Is this Product reducible?"""
    assert complicated_product_01.is_reducible()


def test_complicated_product_01_eval(complicated_product_01):
    """Is this Product correctly evaluated?"""
    assert complicated_product_01.evaluate() == 784


def test_7_by_sum_4_and_2_printed(seven_by_sum_4_and_2):
    """Is this Product correctly printed?"""
    assert seven_by_sum_4_and_2.printed == wrap_nb('7(4+2)')


def test_7_by_sum_4_and_2_notcompact_printed(seven_by_sum_4_and_2):
    """Is this Product correctly printed?"""
    seven_by_sum_4_and_2.set_compact_display(False)
    assert seven_by_sum_4_and_2.printed == wrap_nb('7\\times (4+2)')


def test_7_by_sum_4_and_2_eval(seven_by_sum_4_and_2):
    """Is this Product correctly evaluated?"""
    assert seven_by_sum_4_and_2.evaluate() == 42


def test_neg1_by_sum_4_and_2_printed():
    """Is this Product correctly printed?"""
    assert Product([Item(-1), Sum([Item(4), Item(2)])]).printed == \
        wrap_nb('-(4+2)')


def test_neg1_by_sum_4_and_2_eval():
    """Is this Product correctly evaluated?"""
    assert Product([Item(-1), Sum([Item(4), Item(2)])]).evaluate() == -6


def test_product_sum_1_and_2_printed():
    """Is this Product correctly printed?"""
    assert Product([Sum([1, 2])]).printed == wrap_nb('1+2')


def test_one_by_sum_3_and_4_printed():
    """Is this Product correctly printed?"""
    assert Product([1, Sum([3, 4])]).printed == wrap_nb('3+4')


def test_product_sum_3_plus_4_by_1_printed(product_sum_3_plus_4_by_1):
    """Is this Product correctly printed?"""
    assert product_sum_3_plus_4_by_1.printed == wrap_nb('3+4')


def test_product_sum_3_plus_4_by_1_is_not_reducible(product_sum_3_plus_4_by_1):
    """Is this Product not reducible?"""
    assert not product_sum_3_plus_4_by_1.is_reducible()


def test_product_rubbish_printed(product_rubbish):
    """Is this Product correctly printed?"""
    assert product_rubbish.printed == 'x'


def test_product_rubbish_not_reducible(product_rubbish):
    """Is this Product not reducible?"""
    assert not product_rubbish.is_reducible()


def test_product_mon_deg0_notcompact_printed():
    """Is this Product correctly printed?"""
    assert Product([Monomial((7, 0)), (Monomial((8, 0)))]).printed == \
        wrap_nb('7\\times 8')


def test_product_sum_by_mon_printed():
    """Is this Product correctly printed?"""
    assert Product([Sum([Item(3), Item(4)]), Monomial((-8, 1))]).printed == \
        wrap_nb('(3+4)\\times (-8x)')


def test_4x_by_neg3x_printed():
    """Is this Product correctly printed?"""
    assert Product([Monomial((4, 1)), Monomial((-3, 1))]).printed == \
        wrap_nb('4x\\times (-3x)')


def test_mon_deg0_by_mon_deg0_notcompact_printed():
    """Is this Product correctly printed?"""
    p = Product([Monomial((4, 0)), Monomial((-3, 0))])
    p.set_compact_display(False)
    assert p.printed == wrap_nb('4\\times (-3)')


def test_square_product_mon0_printed():
    """Is this Product correctly printed?"""
    p = Product(Monomial(('+', 6, 0)))
    p.set_exponent(2)
    assert p.printed == wrap_nb('6^{2}')


def test_square_product_square_item_6_printed():
    """Is this Product correctly printed?"""
    p = Product(Item(('+', 6, 2)))
    p.set_exponent(2)
    assert p.printed == wrap_nb('(6^{2})^{2}')


def test_square_product_monom_x_printed():
    """Is this Product correctly printed?"""
    p = Product(Monomial(('+', 1, 1)))
    p.set_exponent(2)
    assert p.printed == wrap_nb('x^{2}')


def test_square_product_square_item_x_printed():
    """Is this Product correctly printed?"""
    p = Product(Item(('+', 'x', 2)))
    p.set_exponent(2)
    assert p.printed == wrap_nb('(x^{2})^{2}')


def test_product_minus1_fraction_2over3_fraction_3over4_printed():
    """Is this Product correctly printed?"""
    p = Product([Item(-1), Fraction(('+', 2, 3)), Fraction(('+', 3, 4))])
    assert p.printed == wrap_nb('-\\frac{2}{3}\\times \\frac{3}{4}')


def test_product_fraction_6over2_times_fraction_8overminus5_printed():
    """Is this Product correctly printed?"""
    p = Product([Fraction(('+', 6, 2)), Fraction(('+', 8, -5))])
    assert p.printed == wrap_nb('\\frac{6}{2}\\times \\frac{8}{-5}')


def test_fractions_product_next_step_01():
    """Is the next calculation's step of this Product correct?"""
    p = Product([Fraction(('+', -3, -2)), Fraction(('+', -1, 5))])
    assert p.calculate_next_step().printed == \
        wrap_nb('-\\frac{3\\times 1}{2\\times 5}')


def test_3_by_negx_printed():
    """Is this Product correctly printed?"""
    assert Product([Item(3), Item(('-', 'x'))]).printed == \
        wrap_nb('3\\times (-x)')


def test_3_by_negx_reducible():
    """Is this Product detected as reducible?"""
    assert Product([Item(3), Item(('-', 'x'))]).is_reducible()


def test_0_by_x_printed():
    """Is this Product correctly printed?"""
    assert Product([Item(0), Item('x')]).printed == wrap_nb('0x')


def test_0_by_x_is_reducible():
    """Is this Product detected as reducible?"""
    assert Product([Item(0), Item('x')]).is_reducible()


def test_product_1square_is_not_displ_as_a_single1(product_1square):
    """Is this Product not displayable as a single 1?"""
    assert not product_1square.is_displ_as_a_single_1()


def test_product_1square_is_reducible(product_1square):
    """Is this Product reducible?"""
    assert product_1square.is_reducible()


def test_product_monom_minus1_times_minus7x_printed():
    """Is this Product correctly printed?"""
    p = Product([Item(-1), Product([Monomial(('-', 7, 1))])])
    p.set_compact_display(False)
    assert p.printed == wrap_nb('-1\\times (-7x)')


def test_7_times_product_minusa_minusb_printed():
    """Is this Product correctly printed?"""
    p = Product([Item(7), Product([Item(('-', "a")), Item(('+', "b"))])])
    assert p.printed == wrap_nb('7\\times (-ab)')


def test_7_times_product_minusa_minusb_bis_printed():
    """Is this Product correctly printed?"""
    p1 = Product([Item(('-', "a")), Item(('+', "b"))])
    p1.set_compact_display(False)
    p = Product([Item(7), p1])
    assert p.printed == wrap_nb('7\\times (-a)\\times b')


def test_product_9_times_minus2_times_7ab_printed():
    """Is this Product correctly printed?"""
    assert Product([Item(9),
                    Product([Item(-2),
                             Item(7),
                             Item('a'),
                             Item('b')])])\
        .printed == wrap_nb('9\\times (-2)\\times 7ab')


def test_product_9_times_minus2_times_7ab_bis_printed():
    """Is this Product correctly printed?"""
    p1 = Product([Item(-2), Item(7), Item('a'), Item('b')])
    p1.set_compact_display(False)
    assert Product([Item(9), p1]).printed == \
        wrap_nb('9\\times (-2)\\times 7\\times a\\times b')


def test_product_9_times_minus2a_times_4b_printed():
    """Is this Product correctly printed?"""
    p1 = Product([Item(-2), Item('a'), Item(4), Item('b')])
    assert Product([Item(9), p1]).printed == \
        wrap_nb('9\\times (-2a)\\times 4b')


def test_product_9_times_minus2a_times_4b_bis_printed():
    """Is this Product correctly printed?"""
    p1 = Product([Item(-2), Item('a'), Item(4), Item('b')])
    p1.set_compact_display(False)
    assert Product([Item(9), p1]).printed == \
        wrap_nb('9\\times (-2)\\times a\\times 4\\times b')


def test_product_sum_minus1_plus_4_times_x_printed():
    """Is this Product correctly printed?"""
    assert Product([Sum([Item(-1), Item(3)]), Item('x')]).printed == \
        wrap_nb('(-1+3)x')


def test_product_9_times_Monomial_minusx_printed():
    """Is this Product correctly printed?"""
    assert Product([Item(9), Monomial(('-', 1, 1))]).printed == \
        wrap_nb('9\\times (-x)')


def test_product_10_times_minusminus4_printed():
    """Is this Product correctly printed?"""
    assert Product([Item(10), Product([Item(-1), Item(-4)])]).printed == \
        wrap_nb('10\\times (-(-4))')


def test_product_15_times_Monomial_3x_printed():
    """Is this Product correctly printed?"""
    assert Product([Item(15), Sum([Item(0),
                                   Monomial(('+', 3, 1))])]).printed == \
        wrap_nb('15\\times 3x')


def test_product_sum_2_3x_times_sum_minus4_6x_is_not_reducible():
    """Is this Product not reducible?"""
    p = Product([Sum([Item(2), Monomial(('+', 3, 1))]),
                 Sum([Item(-4), Monomial(('+', 6, 1))])])
    assert not p.is_reducible()


def test_product_neg10x_printed():
    """Is this Product correctly printed?"""
    p = Product([Monomial(('-', 10, 1))])
    p.set_exponent(2)
    assert p.printed == wrap_nb('(-10x)^{2}')


def test_product_neg10x_next_step():
    """Is this Product's calculation's next step correct?"""
    p = Product([Monomial(('-', 10, 1))])
    p.set_exponent(2)
    assert p.calculate_next_step().printed == wrap_nb('100x^{2}')


def test_fraction_by_item_01_next_step():
    """Is this Product's calculation's next step correct?"""
    p = Product([Fraction((Item(5), Item(7))), Item(8)])
    assert p.calculate_next_step().printed == wrap_nb('\\frac{5\\times 8}{7}')


def test_fraction_by_item_02_next_step():
    """Is this Product's calculation's next step correct?"""
    p = Product([Item(8), Fraction((Item(5), Item(7)))])
    assert p.calculate_next_step().printed == wrap_nb('\\frac{8\\times 5}{7}')


def test_fractions_by_items_01_next_step():
    """Is this Product's calculation's next step correct?"""
    p = Product([Fraction((Item(3), Item(5))),
                 Item(8),
                 Fraction((Item(7), Item(11))),
                 Item(4),
                 Fraction((Item(13), Item(17)))])
    assert p.calculate_next_step().printed == \
        wrap_nb('\\frac{3\\times 8\\times 7\\times 4\\times 13}{5\\times 11'
                '\\times 17}')


def test_items_product_eval():
    """Is Product.evaluate() an instance of decimal.Decimal?"""
    assert isinstance(Product([Item(2.5), Item(3.5)]).evaluate(),
                      decimal.Decimal)


def test_items_product_eval_bis():
    """Is this Product correctly evaluated?"""
    assert Product([Item(2.5), Item(3.5)]).evaluate() == \
        decimal.Decimal('8.75')


def test_fractions_product_eval_01():
    """Is this Product correctly evaluated?"""
    assert Product([Fraction((Item(3), Item(7))),
                    Fraction((Item(7), Item(4)))]).evaluate() == \
        decimal.Decimal('0.75')


def test_fractions_product_eval_01bis():
    """Is this Product correctly evaluated?"""
    assert Product([Fraction((Item(3), Item(7))),
                    Fraction((Item(7), Item(4)))])\
        .evaluate(keep_not_decimal_nb_as_fractions=True) == \
        decimal.Decimal('0.75')


def test_fractions_product_eval_01ter():
    """Is this Product correctly evaluated?"""
    assert Product([Item(6), Fraction((Item(5), Item(3)))]).evaluate() == \
        decimal.Decimal('10')


def test_big_product_printed(big_product):
    """Is this Product correctly printed?"""
    assert big_product.printed == \
        wrap_nb('2x\\times (-4x^{2})(x+3)^{3}\\times 5\\times (x^{2})^{3}\\'
                'times (-1)^{2}\\times (2\\times 3)^{3}')


def test_big_product_ordered(big_product):
    """Is this Product correctly ordered?"""
    assert big_product.order().printed == \
        wrap_nb('2\\times (-4)\\times 5\\times (-1)^{2}\\times '
                '2^{3}\\times 3^{3}x\\times x^{2}x^{6}(x+3)^{3}')


def test_big_product_reduced(big_product):
    """Is this Product correctly reduced?"""
    assert big_product.reduce_().printed == wrap_nb('-8640x^{9}(x+3)^{3}')
