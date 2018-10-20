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

from mathmaker.lib.core.base_calculus import Item, Quotient, Fraction
from tests.tools import wrap_nb


@pytest.fixture
def fq0(): return Quotient(('+',
                            Fraction(('+', Item(9), Item(3))),
                            Fraction(('+', Item(1), Item(-3))),
                            1, 'use_divide_symbol'
                            ))


@pytest.fixture
def fq0_step1(fq0): return fq0.calculate_next_step()


@pytest.fixture
def fq0_step2(fq0_step1): return fq0_step1.calculate_next_step()


@pytest.fixture
def fq0_step3(fq0_step2): return fq0_step2.calculate_next_step()


@pytest.fixture
def fq0_step4(fq0_step3): return fq0_step3.calculate_next_step()


@pytest.fixture
def fq0_step5(fq0_step4): return fq0_step4.calculate_next_step()


def test_fq0_step1(fq0_step1):
    """Is this Quotient's calculation's 1st step correct?"""
    assert fq0_step1.printed == wrap_nb('\\frac{9}{3}\\times \\frac{-3}{1}')


def test_fq0_step2(fq0_step2):
    """Is this Quotient's calculation's 2d step correct?"""
    assert fq0_step2.printed == wrap_nb('-\\frac{9\\times 3}{3\\times 1}')


def test_fq0_step3(fq0_step3):
    """Is this Quotient's calculation's 3rd step correct?"""
    assert fq0_step3.printed == \
        wrap_nb('-\\frac{9\\times \\bcancel{3}}{\\bcancel{3}}')


def test_fq0_step4(fq0_step4):
    """Is this Quotient's calculation's 4th step correct?"""
    assert fq0_step4.printed == wrap_nb('-9')


def test_fq0_step5(fq0_step5):
    """Is this Quotient's calculation's 5th step correct?"""
    assert fq0_step5 is None
