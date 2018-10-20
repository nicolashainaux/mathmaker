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

from mathmaker.lib.core.base_calculus import Product, Fraction
from tests.tools import wrap_nb


@pytest.fixture
def fp0(): return Product([Fraction((5, 4)), Fraction((5, 5))])


@pytest.fixture
def fp0_step1(fp0): return fp0.calculate_next_step()


@pytest.fixture
def fp0_step2(fp0_step1): return fp0_step1.calculate_next_step()


@pytest.fixture
def fp0_step3(fp0_step2): return fp0_step2.calculate_next_step()


@pytest.fixture
def fp0_step4(fp0_step3): return fp0_step3.calculate_next_step()


@pytest.fixture
def fp1(): return Product([Fraction((14, 7)), Fraction((12, 12))])


@pytest.fixture
def fp1_step1(fp1): return fp1.calculate_next_step()


@pytest.fixture
def fp1_step2(fp1_step1): return fp1_step1.calculate_next_step()


@pytest.fixture
def fp1_step3(fp1_step2): return fp1_step2.calculate_next_step()


@pytest.fixture
def fp1_step4(fp1_step3): return fp1_step3.calculate_next_step()


@pytest.fixture
def fp2(): return Product([Fraction((9, -2)), Fraction((-8, 10))])


@pytest.fixture
def fp2_step1(fp2): return fp2.calculate_next_step()


@pytest.fixture
def fp2_step2(fp2_step1): return fp2_step1.calculate_next_step()


@pytest.fixture
def fp2_step3(fp2_step2): return fp2_step2.calculate_next_step()


@pytest.fixture
def fp2_step4(fp2_step3): return fp2_step3.calculate_next_step()


def test_fp0_printed(fp0):
    """Is this Product correctly printed?"""
    assert fp0.printed == wrap_nb('\\frac{5}{4}\\times \\frac{5}{5}')


def test_fp0_step1(fp0_step1):
    """Is this Product's calculation's 1st step correct?"""
    assert fp0_step1.printed == wrap_nb('\\frac{5\\times 5}{4\\times 5}')


def test_fp0_step2(fp0_step2):
    """Is this Product's calculation's 2d step correct?"""
    assert fp0_step2.printed == \
        wrap_nb('\\frac{\\bcancel{5}\\times 5}{4\\times \\bcancel{5}}')


def test_fp0_step3(fp0_step3):
    """Is this Product's calculation's 3rd step correct?"""
    assert fp0_step3.printed == wrap_nb('\\frac{5}{4}')


def test_fp0_step4(fp0_step4):
    """Is this Product's calculation's 4th step correct?"""
    assert fp0_step4 is None


def test_fp1_printed(fp1):
    """Is this Product correctly printed?"""
    assert fp1.printed == wrap_nb('\\frac{14}{7}\\times \\frac{12}{12}')


def test_fp1_step1(fp1_step1):
    """Is this Product's calculation's 1st step correct?"""
    assert fp1_step1.printed == wrap_nb('\\frac{14\\times 12}{7\\times 12}')


def test_fp1_step2(fp1_step2):
    """Is this Product's calculation's 2d step correct?"""
    assert fp1_step2.printed == \
        wrap_nb('\\frac{\\bcancel{7}\\times 2\\times \\bcancel{12}}'
                '{\\bcancel{7}\\times \\bcancel{12}}')


def test_fp1_step3(fp1_step3):
    """Is this Product's calculation's 3rd step correct?"""
    assert fp1_step3.printed == wrap_nb('2')


def test_fp1_step4(fp1_step4):
    """Is this Product's calculation's 4th step correct?"""
    assert fp1_step4 is None


def test_fp2_printed(fp2):
    """Is this Product correctly printed?"""
    assert fp2.printed == wrap_nb('\\frac{9}{-2}\\times \\frac{-8}{10}')


def test_fp2_step1(fp2_step1):
    """Is this Product's calculation's 1st step correct?"""
    assert fp2_step1.printed == wrap_nb('\\frac{9\\times 8}{2\\times 10}')


def test_fp2_step2(fp2_step2):
    """Is this Product's calculation's 2d step correct?"""
    assert fp2_step2.printed == wrap_nb('\\frac{9\\times \\bcancel{2}'
                                        '\\times 4}{\\bcancel{2}\\times 10}')


def test_fp2_step3(fp2_step3):
    """Is this Product's calculation's 3rd step correct?"""
    assert fp2_step3.printed == wrap_nb('\\frac{9\\times \\bcancel{2}'
                                        '\\times 2}{\\bcancel{2}\\times 5}')


def test_fp2_step4(fp2_step4):
    """Is this Product's calculation's 4th step correct?"""
    assert fp2_step4.printed == wrap_nb('\\frac{18}{5}')
