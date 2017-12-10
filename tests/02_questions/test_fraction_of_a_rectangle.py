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
# from decimal import Decimal

from mathmaker.lib.document.content.calculation \
    import fraction_of_a_rectangle


def test_fraction_equal_to_1():
    """Check a Fraction equal to 1 is correctly handled."""
    o = fraction_of_a_rectangle.sub_object(build_data=[2, 2, 2, 2])
    assert o.answer_wording == \
        '$ \\dfrac{\\text{4}}{\\text{4}} $' \
        ' (or ' \
        '$ \\dfrac{\\text{2}}{\\text{2}} $' \
        ', or ' \
        '$ \\text{1} $' \
        ')'
    o = fraction_of_a_rectangle.sub_object(build_data=[2, 3, 2, 3])
    assert o.answer_wording == \
        '$ \\dfrac{\\text{6}}{\\text{6}} $' \
        ' (or ' \
        '$ \\dfrac{\\text{3}}{\\text{3}} $' \
        ', or ' \
        '$ \\dfrac{\\text{2}}{\\text{2}} $' \
        ', or ' \
        '$ \\text{1} $' \
        ')'


def test_fractions_reductions():
    """Check all normal cases are correctly handled."""
    o = fraction_of_a_rectangle.sub_object(build_data=[1, 2, 1, 3])
    assert o.answer_wording == '$ \\dfrac{\\text{2}}{\\text{3}} $'
    o = fraction_of_a_rectangle.sub_object(build_data=[3, 5, 9, 4])
    assert o.answer_wording == \
        '$ \\dfrac{\\text{15}}{\\text{36}} $' \
        ' (or ' \
        '$ \\dfrac{\\text{5}}{\\text{12}} $' \
        ')'
    o = fraction_of_a_rectangle.sub_object(build_data=[9, 4, 7, 8])
    assert o.answer_wording == \
        '$ \\dfrac{\\text{36}}{\\text{56}} $' \
        ' (or ' \
        '$ \\dfrac{\\text{18}}{\\text{28}} $' \
        ', or ' \
        '$ \\dfrac{\\text{9}}{\\text{14}} $' \
        ')'
    o = fraction_of_a_rectangle.sub_object(build_data=[3, 6, 4, 6])
    assert o.answer_wording == \
        '$ \\dfrac{\\text{18}}{\\text{24}} $' \
        ' (or ' \
        '$ \\dfrac{\\text{9}}{\\text{12}} $' \
        ', or ' \
        '$ \\dfrac{\\text{6}}{\\text{8}} $' \
        ', or ' \
        '$ \\dfrac{\\text{3}}{\\text{4}} $' \
        ')'
    o = fraction_of_a_rectangle.sub_object(build_data=[4, 8, 5, 8])
    assert o.answer_wording == \
        '$ \\dfrac{\\text{32}}{\\text{40}} $' \
        ' (or ' \
        '$ \\dfrac{\\text{16}}{\\text{20}} $' \
        ', or ' \
        '$ \\dfrac{\\text{8}}{\\text{10}} $' \
        '...)'
