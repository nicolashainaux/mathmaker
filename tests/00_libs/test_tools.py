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

from mathmakerlib.calculus import Number, Fraction

from mathmaker.lib.tools import check_unique_letters_words, rotate
from mathmaker.lib.tools import ext_dict
from mathmaker.lib.tools import fix_math_style2_fontsize, deci_and_frac_repr
from mathmaker.lib.tools import closest_nn_outside_data, divisors


def test_recursive_update():
    """Check recursive_update()"""
    d1 = ext_dict({'a': 1, 'b': 2,
                   'c': {'z': 26, 'y': 25, 'x': {1: 'a', 2: 'b'}}})
    d2 = ext_dict({'a': 11, 'c': {'y': 24, 'x': {2: 'f', 3: 'g'}, 'w': 23}})
    d1.recursive_update(d2)
    assert d1 == {'a': 11, 'b': 2,
                  'c': {'z': 26, 'y': 24, 'w': 23,
                        'x': {1: 'a', 2: 'f', 3: 'g'}}}


def test_flat():
    """Check flat()"""
    d = ext_dict({'a': 1, 'b': 2,
                  'c': {'z': 26, 'y': 25, 'x': {1: 'a', 2: 64}}})
    assert d.flat() == {'a': 1, 'b': 2,
                        'c.z': 26, 'c.y': 25, 'c.x.1': 'a', 'c.x.2': 64}


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


def test_divisors():
    assert divisors(60) == [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]


def test_fix_math_style2_fontsize():
    """Test fix_math_style2_fontsize() in several cases."""
    assert fix_math_style2_fontsize('$ \\frac{\\text{6}}{\\text{20}} $ '
                                    '(or $ \\frac{\\text{3}}{\\text{10}} $) ')\
        == '$ \\dfrac{\\text{6}}{\\text{20}} $' \
           ' (or $ \\dfrac{\\text{3}}{\\text{10}} $) '
    assert fix_math_style2_fontsize(
        '$ \\frac{\\text{18}}{\\text{24}} $ '
        '(or $ \\frac{\\text{9}}{\\text{12}} $, '
        'or $ \\frac{\\text{6}}{\\text{8}} $, '
        'or $ \\frac{\\text{3}}{\\text{4}} $)') == \
        '$ \\dfrac{\\text{18}}{\\text{24}} $' \
        ' (or ' \
        '$ \\dfrac{\\text{9}}{\\text{12}} $' \
        ', or ' \
        '$ \\dfrac{\\text{6}}{\\text{8}} $' \
        ', or ' \
        '$ \\dfrac{\\text{3}}{\\text{4}} $' \
        ')'


def test_deci_and_frac_repr():
    f = Fraction(3, 4)
    assert deci_and_frac_repr(f) == r"$\dfrac{3}{4}$ (or 0.75)"
    assert deci_and_frac_repr(f, output='js') == [
        '3/4', '0.75', 'any_fraction == 3/4']
    n = Number('0.75')
    assert deci_and_frac_repr(n) == r"0.75 (or $\dfrac{3}{4}$)"
    assert deci_and_frac_repr(n, output='js') == [
        '0.75', '3/4', 'any_fraction == 3/4']
    f = Fraction(3, 7)
    assert deci_and_frac_repr(f) == r"$\dfrac{3}{7}$"
    assert deci_and_frac_repr(f, output='js') == [
        '3/7', 'any_fraction == 3/7']
    n = Number('1.21')
    assert deci_and_frac_repr(n) == r"1.21"
    assert deci_and_frac_repr(n, output='js') == ['1.21']
    n = Number('5')
    assert deci_and_frac_repr(n) == r"5"
    assert deci_and_frac_repr(n, output='js') == ['5']
    n = Number('5.00')
    assert deci_and_frac_repr(n) == r"5"
    assert deci_and_frac_repr(n, output='js') == ['5']


def test_closest_nn_outside_data():
    line = [2, 3, 7]
    assert closest_nn_outside_data(line, 0) == 1
    assert closest_nn_outside_data(line, 1) == 4
    assert closest_nn_outside_data(line, 2) == 8
    line = [2, 3, 7, 8]
    assert closest_nn_outside_data(line, 2) == 6
    line = [1, 3, 7]
    assert closest_nn_outside_data(line, 0) == 2
