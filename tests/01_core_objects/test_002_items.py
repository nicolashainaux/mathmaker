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

from mathmaker.lib.core.root_calculus import Exponented
from mathmaker.lib.core.base_calculus import Item, Sum, Product
from tools import wrap_nb


@pytest.fixture()
def pos6(): return Item(6)


@pytest.fixture()
def negneg1(): return Item(('-', -1))


@pytest.fixture()
def neg1_inside_exp2(): return Item(('+', -1, Item(2)))


@pytest.fixture()
def pos3_exp_2plus6(): return Item(('+', 3, Sum([-2, 6])))


@pytest.fixture()
def neg3_inside_exp_2plus5(): return Item(('+', -3, Sum([-2, 5])))


@pytest.fixture()
def neg5_inside_exp0(): return Item(('+', -5, 0))


@pytest.fixture()
def item_to_round(): return Item(6.548)


@pytest.fixture()
def item_with_unit(): return Item(19.5, unit='cm')


def test_isinstance_01():
    """Is Item correctly detected as an instance of Exponented?"""
    assert isinstance(Item(4), Exponented)


@pytest.fixture()
def neg2_inside_exp_sum_of_product_of_1plus1():
    return Item(('+', -2, Sum([Product([Sum([1, 1])])])))


def test_1_is_displayable_as_a_single_1():
    """Is Item(1) detected as displayable as a single 1?"""
    assert Item(1).is_displ_as_a_single_1()


def test_1_display():
    """Is Item(1) correctly printed?"""
    assert Item(1).printed == wrap_nb('1')


def test_6_is_not_displayable_as_a_single_1():
    """Is Item(6) detected as not displayable as a single 1?"""
    assert not Item(6).is_displ_as_a_single_1()


def test_6_is_not_None():
    """Is Item(6) detected as not None?"""
    assert Item(6) is not None


def test_couple_6_None_is_not_couple_None_None():
    """Is (Item(6), None) detected as not (None, None)?"""
    assert (Item(6), None) is not (None, None)


def test_6_is_item_6(pos6):
    """Is Item(6) detected as equal to itself?"""
    assert pos6 == Item(6)


def test_neg1_printed():
    """Is Item(-1) correctly printed?"""
    assert Item(-1).printed == wrap_nb('-1')


def test_negneg1_eval(negneg1):
    """Is Item('-', -1) correctly evaluated as 1?"""
    assert negneg1.evaluate() == 1


def test_negneg1_printed(negneg1):
    """Is Item(('-', -1)) correctly printed as -(-1)?"""
    assert negneg1.printed == wrap_nb('-(-1)')


def test_neg1_exp_negneg1_eval():
    """Is Item(('+', -1, Item(('-', -1)))) correctly evaluated as -1?"""
    assert Item(('+', -1, Item(('-', -1)))).evaluate() == -1


def test_neg1_exp_negneg1_printed():
    """Is Item(('+', -1, Item(('-', -1)))) correctly printed?"""
    assert Item(('+', -1, Item(('-', -1)))).printed == wrap_nb('-1^{-(-1)}')


def test_neg1_exp2_eval():
    """Is Item(('-', 1, Item(2))) correctly evaluated as -1?"""
    assert Item(('-', 1, Item(2))).evaluate() == -1


def test_neg1_exp2_printed():
    """Is Item(('-', 1, Item(2))) correctly printed?"""
    assert Item(('-', 1, Item(2))).printed == wrap_nb('-1^{2}')


def test_neg1_inside_exp2_negative_raw_value(neg1_inside_exp2):
    """Has (-1)^{2} a negative raw value?"""
    assert neg1_inside_exp2.raw_value < 0


def test_neg1_inside_exp2_requires_inner_brackets(neg1_inside_exp2):
    """Is (-1)^{2} correctly detected as requiring inner brackets?"""
    assert neg1_inside_exp2.requires_inner_brackets()


def test_neg1_inside_exp2_is_numeric(neg1_inside_exp2):
    """Is (-1)^{2} correctly detected as numeric?"""
    assert neg1_inside_exp2.is_numeric()


def test_neg1_inside_exp2_eval(neg1_inside_exp2):
    """Is  Item(('+', -1, Item(2))) evaluated as 1?"""
    assert neg1_inside_exp2.evaluate() == 1


def test_neg1_inside_exp2_printed(neg1_inside_exp2):
    """Is  Item(('+', -1, Item(2))) correctly printed?"""
    assert neg1_inside_exp2.printed == wrap_nb('(-1)^{2}')


def test_neg5_inside_exp0_printed(neg5_inside_exp0):
    """Is (-5)^{0} correctly printed as 1?"""
    assert neg5_inside_exp0.printed == wrap_nb('1')


def test_neg5_inside_exp0_printed_bis(neg5_inside_exp0):
    """Is (-5)^{0} correctly printed as (-5)^{0} when explicitely desired?"""
    assert neg5_inside_exp0.into_str(force_display_exponent_0='OK',
                                     force_expression_begins=True) == \
        wrap_nb('(-5)^{0}')


def test_pos3_exp_2plus6_eval(pos3_exp_2plus6):
    """Is Item(('+', 3, Sum([-2, 6]))) evaluated to 81?"""
    assert pos3_exp_2plus6.evaluate() == 81


def test_pos3_exp_2plus6_printed(pos3_exp_2plus6):
    """Is Item(('+', 3, Sum([-2, 6]))) evaluated to 81?"""
    assert pos3_exp_2plus6.printed == wrap_nb('3^{-2+6}')


def test_a_printed():
    """Is Item('a') correctly printed?"""
    assert Item('a').printed == 'a'


def test_nega_printed():
    """Is Item('-a') correctly printed?"""
    assert Item('-a').printed == '-a'


def test_negnega_printed():
    """Is Item(('-', '-a')) correctly printed?"""
    assert Item(('-', '-a')).printed == '-(-a)'


def test_neg3_inside_exp_2plus5_eval(neg3_inside_exp_2plus5):
    """Is Item(('+', -3, Sum([-2, 5]))) correctly printed?"""
    assert neg3_inside_exp_2plus5.evaluate() == -27


def test_neg3_inside_exp_2plus5_printed(neg3_inside_exp_2plus5):
    """Is Item(('+', -3, Sum([-2, 5]))) correctly printed?"""
    assert neg3_inside_exp_2plus5.printed == wrap_nb('(-3)^{-2+5}')


def test_pos2_exp_neg2_inside_exp4_printed():
    """Is Item(('+', 2, Item(('+', -2, 4)))) correctly printed?"""
    assert Item(('+', 2, Item(('+', -2, 4)))).printed == \
        wrap_nb('2^{(-2)^{4}}')


def test_pos2_exp_sum_neg2_inside_exp4_printed():
    """Is Item(('+', 2, Sum([Item(('+', -2, 4))]))) correctly printed?"""
    assert Item(('+', 2, Sum([Item(('+', -2, 4))]))).printed == \
        wrap_nb('2^{(-2)^{4}}')


def test_neg2_inside_exp_1plus0_printed():
    """Is Item(('+', -2, Sum([1, 0]))) correctly printed?"""
    assert Item(('+', -2, Sum([1, 0]))).printed == wrap_nb('-2')


def test_neg2_inside_exp_sum_of_product_of_1plus0_printed():
    """Is Item(('+', -2, Sum([Product([Sum([1, 0])])]))) correctly printed?"""
    assert Item(('+', -2, Sum([Product([Sum([1, 0])])]))).printed == \
        wrap_nb('-2')


def test_neg2_inside_exp_sum_of_product_of_1plus1_printed(
        neg2_inside_exp_sum_of_product_of_1plus1):
    """Is Item(('+', -2, Sum([Product([Sum([1, 1])])]))) correctly printed?"""
    assert neg2_inside_exp_sum_of_product_of_1plus1.printed == \
        wrap_nb('(-2)^{1+1}')


def test_neg2_inside_exp_sum_of_product_of_1plus1_printed_bis(
        neg2_inside_exp_sum_of_product_of_1plus1):
    """
    Is Item(('+', -2, Sum([Product([Sum([1, 1])])]))) still correctly printed
    if the 'embedded' Product is not set to compact display?
    """
    neg2_inside_exp_sum_of_product_of_1plus1.exponent\
                                            .term[0]\
                                            .set_compact_display(False)
    assert neg2_inside_exp_sum_of_product_of_1plus1.printed == \
        wrap_nb('(-2)^{1+1}')


def test_neg2_inside_exp_sum_of_sum_of_1plus1_printed():
    """Is Item(('+', -2, Sum([Sum([Sum([1, 1])])]))) correctly printed?"""
    assert Item(('+', -2, Sum([Sum([Sum([1, 1])])]))).printed == \
        wrap_nb('(-2)^{1+1}')


def test_neg2_inside_exp_sum_of_sum_of_2times2_printed():
    """Is Item(('+', -2, Sum([Sum([Product([2, 2])])]))) correctly printed?"""
    assert Item(('+', -2, Sum([Sum([Product([2, 2])])]))).printed == \
        wrap_nb('(-2)^{2\\times 2}')


def test_neg2_inside_exp_sum_of_product_of_sum_of_2_printed():
    """Is Item(('+', -2, Sum([Product([Sum([2])])]))) correctly printed?"""
    assert Item(('+', -2, Sum([Product([Sum([2])])]))).printed == \
        wrap_nb('(-2)^{2}')


def test_order_a_b():
    """Is Item('a') not greater than Item('b')?"""
    assert not Item('a') > Item('b')


def test_order_b_a():
    """Is Item('b') greater than Item('a')?"""
    assert Item('b') > Item('a')


def test_sort_b_a():
    assert sorted([Item('b'), Item('a')],
                  key=lambda item: item.get_first_letter()) == \
        [Item('a'), Item('b')]


def test_item_to_round_digits_number(item_to_round):
    """Is the number of digits of Item(6.548) correctly detected as 3?"""
    assert item_to_round.digits_number() == 3


def test_item_to_round_needs_to_get_rounded_0(item_to_round):
    """Is Item(6.548) detected as needed to get rounded to the unit?"""
    assert item_to_round.needs_to_get_rounded(0)


def test_item_to_round_needs_to_get_rounded_1(item_to_round):
    """Is Item(6.548) detected as needed to get rounded to the tenth?"""
    assert item_to_round.needs_to_get_rounded(1)


def test_item_to_round_needs_to_get_rounded_2(item_to_round):
    """Is Item(6.548) detected as needed to get rounded to the hundredth?"""
    assert item_to_round.needs_to_get_rounded(2)


def test_item_to_round_needs_to_get_rounded_3(item_to_round):
    """
    Is Item(6.548) detected as not needed to get rounded to the thousandth?
    """
    assert not item_to_round.needs_to_get_rounded(3)


def test_item_to_round_needs_to_get_rounded_4(item_to_round):
    """
    Is Item(6.548) detected as not needed to get rounded to the tenthousandth?
    """
    assert not item_to_round.needs_to_get_rounded(4)


def test_item_to_round_round_to_unit(item_to_round):
    """Is Item(6.548) correctly rounded (to unit) to Item(7)?"""
    assert item_to_round.round(0) == Item(7)


def test_item_to_round_round_to_tenth(item_to_round):
    """Is Item(6.548) correctly rounded (to tenth) to Item(6.5)?"""
    assert item_to_round.round(1) == Item(6.5)


def test_item_to_round_round_to_hundredth(item_to_round):
    """Is Item(6.548) correctly rounded (to hundredth) to Item(6.55)?"""
    assert item_to_round.round(2) == Item(6.55)


def test_item_to_round_round_to_thousandth(item_to_round):
    """Is Item(6.548) correctly rounded (to thousandth) to Item(6.548)?"""
    assert item_to_round.round(3) == Item(6.548)


def test_item_with_unit_printed(item_with_unit):
    """Is Item(19.5, unit='cm') correctly printed?"""
    assert item_with_unit.into_str(display_unit=True,
                                   graphic_display=True,
                                   force_expression_begins=True) == '19.5~cm'


def test_item_eval():
    """Is Item.evaluate() a decimal.Decimal instance?"""
    assert isinstance(Item(2.5).evaluate(), decimal.Decimal)
