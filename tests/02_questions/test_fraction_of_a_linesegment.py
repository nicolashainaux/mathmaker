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

from mathmaker.lib.document.content.calculation \
    import fraction_of_a_linesegment


def test_instanciation_errors():
    """Check errors are raised as expected."""
    with pytest.raises(ValueError) as excinfo:
        fraction_of_a_linesegment.sub_object(build_data=[1, 1, 2, 2])
    assert str(excinfo.value) == 'Need either 2, or 3 numbers to build this ' \
        'question.'


def test_use_cases():
    """Check usage cases are correctly handled."""
    o = fraction_of_a_linesegment.sub_object(build_data=[2, 3])
    assert o.answer_wording == r'$ \dfrac{2}{3} $'

    o = fraction_of_a_linesegment.sub_object(build_data=[3, 2])
    assert o.answer_wording == r'$ \dfrac{2}{3} $'

    o = fraction_of_a_linesegment.sub_object(build_data=[1, 10])
    assert o.answer_wording == r'$ \dfrac{1}{10} $'
    assert o.transduration == 18

    o = fraction_of_a_linesegment.sub_object(build_data=[2, 2, 3])
    assert o.answer_wording == r'$ \dfrac{4}{6} $ (or $ \dfrac{2}{3} $)'

    o = fraction_of_a_linesegment.sub_object(build_data=[36, 56])
    assert o.answer_wording == r'$ \dfrac{36}{56} $ (or $ \dfrac{18}{28} $, ' \
        r'or $ \dfrac{9}{14} $)'

    o = fraction_of_a_linesegment.sub_object(build_data=[18, 24])
    assert o.answer_wording == r'$ \dfrac{18}{24} $ (or $ \dfrac{9}{12} $, ' \
        r'or $ \dfrac{6}{8} $, or $ \dfrac{3}{4} $)'

    o = fraction_of_a_linesegment.sub_object(build_data=[32, 40])
    assert o.answer_wording == r'$ \dfrac{32}{40} $ (or $ \dfrac{16}{20} $, ' \
        r'or $ \dfrac{8}{10} $...)'
    assert o.js_a() == ['4/5', 'any_fraction == 4/5']
