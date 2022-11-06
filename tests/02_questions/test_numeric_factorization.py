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

from mathmakerlib.calculus import Number

from mathmaker.lib.document.content.calculation import numeric_factorization


def test_numeric_factorization():
    """Check all normal cases are correctly handled."""
    o = numeric_factorization.sub_object(
        build_data=[2, 7], do_shuffle=False, nb_source='nnpairs:2-9')
    assert o.q() in [
        r'$ 0.1 \times 7 + 1.9 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.2 \times 7 + 1.8 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.3 \times 7 + 1.7 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.4 \times 7 + 1.6 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.5 \times 7 + 1.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.6 \times 7 + 1.4 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.7 \times 7 + 1.3 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.8 \times 7 + 1.2 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.9 \times 7 + 1.1 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.1 \times 7 + 0.9 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.2 \times 7 + 0.8 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.3 \times 7 + 0.7 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.4 \times 7 + 0.6 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.5 \times 7 + 0.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.6 \times 7 + 0.4 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.7 \times 7 + 0.3 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.8 \times 7 + 0.2 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.9 \times 7 + 0.1 \times 7 $ = \textcolor{BrickRed}{\text{?}}'
    ]
    assert o.a() == '14'
    assert o.js_a() == ['14']
    o = numeric_factorization.sub_object(
        build_data=[2, 7], do_shuffle=False, nb_source='nnpairs:2-9',
        split_as='quarters')
    assert o.q() in [
        r'$ 0.25 \times 7 + 1.75 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.75 \times 7 + 1.25 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.25 \times 7 + 0.75 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.75 \times 7 + 0.25 \times 7 $ = \textcolor{BrickRed}{\text{?}}'
    ]
    assert o.a() == '14'
    assert o.js_a() == ['14']
    o = numeric_factorization.sub_object(
        build_data=[2, 7], do_shuffle=False, nb_source='nnpairs:2-9',
        split_as='halves')
    assert o.a() == '14'
    assert o.js_a() == ['14']
    assert o.nb1 * o.nb2 + o.nb3 * o.nb4 == 14
    assert o.q() in [
        r'$ 0.5 \times 7 + 1.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.5 \times 7 + 0.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
    ]
    o = numeric_factorization.sub_object(
        build_data=[2, 7], do_shuffle=True, nb_source='nnpairs:2-9',
        split_as='halves')
    assert o.a() == '14'
    assert o.js_a() == ['14']
    assert o.nb1 * o.nb2 + o.nb3 * o.nb4 == 14
    assert o.q() in [
        r'$ 0.5 \times 7 + 1.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.5 \times 7 + 0.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 0.5 \times 7 + 7 \times 1.5 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1.5 \times 7 + 7 \times 0.5 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.5 + 7 \times 1.5 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.5 + 7 \times 0.5 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.5 + 1.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 1.5 + 0.5 \times 7 $ = \textcolor{BrickRed}{\text{?}}'
    ]
    o = numeric_factorization.sub_object(
        build_data=[16, 10], do_shuffle=False, nb_source='nnpairs:10×11-19',
        split_as='unit', nb_variant='decimal2')
    assert o.a() == '1.6'
    assert o.js_a() == ['1.6']
    assert o.nb1 * o.nb2 + o.nb3 * o.nb4 == Number('1.6')
    assert o.q() in [
        r'$ 9 \times 0.16 + 1 \times 0.16 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 8 \times 0.16 + 2 \times 0.16 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 7 \times 0.16 + 3 \times 0.16 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 6 \times 0.16 + 4 \times 0.16 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 5 \times 0.16 + 5 \times 0.16 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 4 \times 0.16 + 6 \times 0.16 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 3 \times 0.16 + 7 \times 0.16 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 2 \times 0.16 + 8 \times 0.16 $ = \textcolor{BrickRed}{\text{?}}',
        r'$ 1 \times 0.16 + 9 \times 0.16 $ = \textcolor{BrickRed}{\text{?}}'
    ]
