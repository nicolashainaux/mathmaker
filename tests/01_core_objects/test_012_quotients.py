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

from mathmaker.lib.core.base_calculus import Quotient, Fraction
from tools import wrap_nb


@pytest.fixture
def q1(): return Quotient(('+',
                           Fraction(('+', 8, 9)),
                           Fraction(('+', 7, 2)),
                           1,
                           'use_divide_symbol'))


@pytest.fixture
def q2(): return Quotient(('-',
                           Fraction(('+', 1, 2)),
                           Fraction(('+', 1, 3)),
                           1,
                           'use_divide_symbol'))


def test_q1_printed(q1):
    """Is this Quotient correctly printed?"""
    assert q1.printed == wrap_nb('\\frac{8}{9}\div \\frac{7}{2}')


def test_q1_next_step(q1):
    """Is this Quotient's calculation's next step correct?"""
    assert q1.calculate_next_step().printed == \
        wrap_nb('\\frac{8}{9}\\times \\frac{2}{7}')


def test_q1_next_step2(q1):
    """Is this Quotient's calculation's 2d next step correct?"""
    assert q1.calculate_next_step().calculate_next_step().printed == \
        wrap_nb('\\frac{8\\times 2}{9\\times 7}')


def test_q2_printed(q2):
    """Is this Quotient correctly printed?"""
    assert q2.printed == wrap_nb('-\\frac{1}{2}\div \\frac{1}{3}')


def test_q2_next_step(q2):
    """Is this Quotient's calculation's next step correct?"""
    assert q2.calculate_next_step().printed == \
        wrap_nb('-\\frac{1}{2}\\times \\frac{3}{1}')


def test_q2_next_step2(q2):
    """Is this Quotient's calculation's 2d next step correct?"""
    assert q2.calculate_next_step().calculate_next_step().printed == \
        wrap_nb('-\\frac{1\\times 3}{2\\times 1}')


def test_q2_next_step3(q2):
    """Is this Quotient's calculation's 3rd next step correct?"""
    assert q2.calculate_next_step().calculate_next_step()\
        .calculate_next_step().printed == \
        wrap_nb('-\\frac{3}{2}')
