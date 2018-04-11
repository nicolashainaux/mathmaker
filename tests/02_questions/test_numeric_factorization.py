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

from mathmaker.lib.document.content.calculation import numeric_factorization


def test_numeric_factorization():
    """Check all normal cases are correctly handled."""
    o = numeric_factorization.sub_object(build_data=[2, 7], do_shuffle=False)
    assert o.q() in [
        r'$ 7 \times 0.1 + 7 \times 1.9 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.2 + 7 \times 1.8 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.3 + 7 \times 1.7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.4 + 7 \times 1.6 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.5 + 7 \times 1.5 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.6 + 7 \times 1.4 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.7 + 7 \times 1.3 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.8 + 7 \times 1.2 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.9 + 7 \times 1.1 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.1 + 7 \times 0.9 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.2 + 7 \times 0.8 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.3 + 7 \times 0.7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.4 + 7 \times 0.6 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.5 + 7 \times 0.5 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.6 + 7 \times 0.4 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.7 + 7 \times 0.3 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.8 + 7 \times 0.2 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.9 + 7 \times 0.1 $ = \textcolor{BrickRed}{\text{?}}'
    ]
    assert o.a() == '14'
    assert o.js_a() == ['14']
    o = numeric_factorization.sub_object(build_data=[2, 7], do_shuffle=False,
                                         split_as='quarters')
    assert o.q() in [
        r'$ 7 \times 0.25 + 7 \times 1.75 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.75 + 7 \times 1.25 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.25 + 7 \times 0.75 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.75 + 7 \times 0.25 $ = \textcolor{BrickRed}{\text{?}}'
    ]
    assert o.a() == '14'
    assert o.js_a() == ['14']
    o = numeric_factorization.sub_object(build_data=[2, 7], split_as='halves')
    assert o.a() == '14'
    assert o.js_a() == ['14']
    assert o.nb1 * o.nb2 + o.nb3 * o.nb4 == 14
    assert o.q() in [
        r'$ 7 \times 0.5 + 7 \times 1.5 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.5 + 1.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.5 \times 7 + 7 \times 1.5 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.5 \times 7 + 1.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.5 + 7 \times 0.5 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.5 + 0.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.5 \times 7 + 7 \times 0.5 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.5 \times 7 + 0.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
    ]
