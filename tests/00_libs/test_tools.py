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

from mathmaker.lib.tools import check_unique_letters_words, rotate
from mathmaker.lib.tools import parse_layout_descriptor, ext_dict
from mathmaker.lib.tools import fix_math_style2_fontsize


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


def test_parse_layout_descriptor():
    """Test parse_layout_descriptor() in several cases."""
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor(4)
    assert 'The layout descriptor must be str' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', sep=[1])
    assert 'All items of the sep list must be str' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', sep=1)
    assert 'sep must be a str or a list' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', special_row_chars=4)
    assert 'special_row_char must be a list' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', special_row_chars=[4])
    assert 'All items of the special_row_chars list must be str' \
        in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', min_row='a')
    assert 'min_row and min_col must both be int' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', min_col='a')
    assert 'min_row and min_col must both be int' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', min_row=-2)
    assert 'min_row and min_col must both be positive' in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        parse_layout_descriptor('2×3', min_col=-2)
    assert 'min_row and min_col must both be positive' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×')
    assert 'The layout format must be a string like '\
        '\'row×col\', where × is your delimiter. ' \
        'Cannot find a row and a col in \'' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2x3')
    assert 'Cannot find a row and a col in \'' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2;')
    assert ' with any of the str from this list as delimiter: ' \
        in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×3', sep=['x'])
    assert ' with any of the str from this list as delimiter: ' \
        in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('a×3')
    assert 'Number of rows: \'a\' cannot be turned into int' \
        in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('3×a')
    assert 'Number of cols: \'a\' cannot be turned into int' \
        in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('?×3')
    assert 'Number of rows: \'?\' cannot be turned into int' \
        in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('0×3', min_row=1)
    assert 'nrow must be greater than 1' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('4×0', min_col=1)
    assert 'ncol must be greater than 1' in str(excinfo.value)

    assert parse_layout_descriptor('?×0', special_row_chars=['?'],
                                   min_row=1) == ('?', 0)
    assert parse_layout_descriptor('2×3', sep=['x', '×']) == (2, 3)
    assert parse_layout_descriptor('4×5') == (4, 5)
    assert parse_layout_descriptor('6×7', special_row_chars=['?']) == (6, 7)


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
