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

from mathmaker.lib.core.base_calculus import Item, Sum, Fraction
from tools import wrap_nb


@pytest.fixture
def fs0(): return Sum([Fraction(('+', 2, 3)), Fraction(('+', 3, 4))])


@pytest.fixture
def fs0_step1(fs0): return fs0.calculate_next_step()


@pytest.fixture
def fs0_step2(fs0_step1): return fs0_step1.calculate_next_step()


@pytest.fixture
def fs0_step3(fs0_step2): return fs0_step2.calculate_next_step()


@pytest.fixture
def fs0_step4(fs0_step3): return fs0_step3.calculate_next_step()


@pytest.fixture
def fs0_step5(fs0_step4): return fs0_step4.calculate_next_step()


@pytest.fixture
def fs1(): return Sum([Fraction(('+', 1, 4)), Fraction(('+', 1, 8))])


@pytest.fixture
def fs1_step1(fs1): return fs1.calculate_next_step()


@pytest.fixture
def fs1_step2(fs1_step1): return fs1_step1.calculate_next_step()


@pytest.fixture
def fs1_step3(fs1_step2): return fs1_step2.calculate_next_step()


@pytest.fixture
def fs1_step4(fs1_step3): return fs1_step3.calculate_next_step()


@pytest.fixture
def fs1_step5(fs1_step4): return fs1_step4.calculate_next_step()


@pytest.fixture
def fs2(): return Sum([Fraction(('+', 1, 9)), Fraction(('+', 1, -12))])


@pytest.fixture
def fs2_step1(fs2): return fs2.calculate_next_step()


@pytest.fixture
def fs2_step2(fs2_step1): return fs2_step1.calculate_next_step()


@pytest.fixture
def fs2_step3(fs2_step2): return fs2_step2.calculate_next_step()


@pytest.fixture
def fs2_step4(fs2_step3): return fs2_step3.calculate_next_step()


@pytest.fixture
def fs2_step5(fs2_step4): return fs2_step4.calculate_next_step()


@pytest.fixture
def fs2_step6(fs2_step5): return fs2_step5.calculate_next_step()


@pytest.fixture
def fs3(): return Sum([Fraction(('+', -7, 10)), Fraction(('-', 11, -15))])


@pytest.fixture
def fs3_step1(fs3): return fs3.calculate_next_step()


@pytest.fixture
def fs3_step2(fs3_step1): return fs3_step1.calculate_next_step()


@pytest.fixture
def fs3_step3(fs3_step2): return fs3_step2.calculate_next_step()


@pytest.fixture
def fs3_step4(fs3_step3): return fs3_step3.calculate_next_step()


@pytest.fixture
def fs3_step5(fs3_step4): return fs3_step4.calculate_next_step()


@pytest.fixture
def fs3_step6(fs3_step5): return fs3_step5.calculate_next_step()


@pytest.fixture
def fs4(): return Sum([Fraction(('+', 3, 4)), Item(-5)])


@pytest.fixture
def fs4_step1(fs4): return fs4.calculate_next_step()


@pytest.fixture
def fs4_step2(fs4_step1): return fs4_step1.calculate_next_step()


@pytest.fixture
def fs4_step3(fs4_step2): return fs4_step2.calculate_next_step()


@pytest.fixture
def fs4_step4(fs4_step3): return fs4_step3.calculate_next_step()


@pytest.fixture
def fs4_step5(fs4_step4): return fs4_step4.calculate_next_step()


@pytest.fixture
def fs4_step6(fs4_step5): return fs4_step5.calculate_next_step()


@pytest.fixture
def fs5(): return Sum([Fraction(('+', 25, 10)), Fraction(('+', 1, 10))])


@pytest.fixture
def fs5_step1(fs5): return fs5.calculate_next_step()


@pytest.fixture
def fs5_step2(fs5_step1): return fs5_step1.calculate_next_step()


@pytest.fixture
def fs5_step3(fs5_step2): return fs5_step2.calculate_next_step()


@pytest.fixture
def fs5_step4(fs5_step3): return fs5_step3.calculate_next_step()


@pytest.fixture
def fs5_step5(fs5_step4): return fs5_step4.calculate_next_step()


@pytest.fixture
def fs6(): return Sum([Fraction(('-', 18, 5)), Fraction(('-', 2, 5))])


@pytest.fixture
def fs6_step1(fs6): return fs6.calculate_next_step()


@pytest.fixture
def fs6_step2(fs6_step1): return fs6_step1.calculate_next_step()


@pytest.fixture
def fs6_step3(fs6_step2): return fs6_step2.calculate_next_step()


@pytest.fixture
def fs6_step4(fs6_step3): return fs6_step3.calculate_next_step()


@pytest.fixture
def fs6_step5(fs6_step4): return fs6_step4.calculate_next_step()


@pytest.fixture
def fs7(): return Sum([Item(4), Fraction((25, 10)),
                       Item(-7), Fraction((1, 10))])


@pytest.fixture
def fs7_step1(fs7): return fs7.calculate_next_step()


@pytest.fixture
def fs7_step2(fs7_step1): return fs7_step1.calculate_next_step()


@pytest.fixture
def fs7_step3(fs7_step2): return fs7_step2.calculate_next_step()


@pytest.fixture
def fs7_step4(fs7_step3): return fs7_step3.calculate_next_step()


@pytest.fixture
def fs7_step5(fs7_step4): return fs7_step4.calculate_next_step()


@pytest.fixture
def fs7_step6(fs7_step5): return fs7_step5.calculate_next_step()


@pytest.fixture
def fs7_step7(fs7_step6): return fs7_step6.calculate_next_step()


def test_fs0_printed(fs0):
    """Is this Sum correctly printed?"""
    assert fs0.printed == wrap_nb('\\frac{2}{3}+\\frac{3}{4}')


def test_fs0_step1(fs0_step1):
    """Is this Sum's calculation's 1st step correct?"""
    assert fs0_step1.printed == wrap_nb('\\frac{2\\times 4}{3\\times 4}'
                                        '+\\frac{3\\times 3}{4\\times 3}')


def test_fs0_step2(fs0_step2):
    """Is this Sum's calculation's 2d step correct?"""
    assert fs0_step2.printed == wrap_nb('\\frac{8}{12}+\\frac{9}{12}')


def test_fs0_step3(fs0_step3):
    """Is this Sum's calculation's 3rd step correct?"""
    assert fs0_step3.printed == wrap_nb('\\frac{8+9}{12}')


def test_fs0_step4(fs0_step4):
    """Is this Sum's calculation's 4th step correct?"""
    assert fs0_step4.printed == wrap_nb('\\frac{17}{12}')


def test_fs0_step5(fs0_step5):
    """Is this Sum's calculation's 5th step correct?"""
    assert fs0_step5 is None


def test_fs1_printed(fs1):
    """Is this Sum correctly printed?"""
    assert fs1.printed == wrap_nb('\\frac{1}{4}+\\frac{1}{8}')


def test_fs1_step1(fs1_step1):
    """Is this Sum's calculation's 1st step correct?"""
    assert fs1_step1.printed == wrap_nb('\\frac{1\\times 2}{4\\times 2}'
                                        '+\\frac{1}{8}')


def test_fs1_step2(fs1_step2):
    """Is this Sum's calculation's 2d step correct?"""
    assert fs1_step2.printed == \
        wrap_nb('\\frac{2}{8}+\\frac{1}{8}')


def test_fs1_step3(fs1_step3):
    """Is this Sum's calculation's 3rd step correct?"""
    assert fs1_step3.printed == wrap_nb('\\frac{2+1}{8}')


def test_fs1_step4(fs1_step4):
    """Is this Sum's calculation's 4th step correct?"""
    assert fs1_step4.printed == wrap_nb('\\frac{3}{8}')


def test_fs1_step5(fs1_step5):
    """Is this Sum's calculation's 5th step correct?"""
    assert fs1_step5 is None


def test_fs2_printed(fs2):
    """Is this Sum correctly printed?"""
    assert fs2.printed == wrap_nb('\\frac{1}{9}+\\frac{1}{-12}')


def test_fs2_step1(fs2_step1):
    """Is this Sum's calculation's 1st step correct?"""
    assert fs2_step1.printed == wrap_nb('\\frac{1}{9}-\\frac{1}{12}')


def test_fs2_step2(fs2_step2):
    """Is this Sum's calculation's 2d step correct?"""
    assert fs2_step2.printed == wrap_nb('\\frac{1\\times 4}{9\\times 4}'
                                        '-\\frac{1\\times 3}{12\\times 3}')


def test_fs2_step3(fs2_step3):
    """Is this Sum's calculation's 3rd step correct?"""
    assert fs2_step3.printed == wrap_nb('\\frac{4}{36}-\\frac{3}{36}')


def test_fs2_step4(fs2_step4):
    """Is this Sum's calculation's 4th step correct?"""
    assert fs2_step4.printed == wrap_nb('\\frac{4-3}{36}')


def test_fs2_step5(fs2_step5):
    """Is this Sum's calculation's 5th step correct?"""
    assert fs2_step5.printed == wrap_nb('\\frac{1}{36}')


def test_fs2_step6(fs2_step6):
    """Is this Sum's calculation's 6th step correct?"""
    assert fs2_step6 is None


def test_fs3_printed(fs3):
    """Is this Sum correctly printed?"""
    assert fs3.printed == wrap_nb('\\frac{-7}{10}-\\frac{11}{-15}')


def test_fs3_step1(fs3_step1):
    """Is this Sum's calculation's 1st step correct?"""
    assert fs3_step1.printed == wrap_nb('-\\frac{7}{10}+\\frac{11}{15}')


def test_fs3_step2(fs3_step2):
    """Is this Sum's calculation's 2d step correct?"""
    assert fs3_step2.printed == wrap_nb('-\\frac{7\\times 3}{10\\times 3}'
                                        '+\\frac{11\\times 2}{15\\times 2}')


def test_fs3_step3(fs3_step3):
    """Is this Sum's calculation's 3rd step correct?"""
    assert fs3_step3.printed == wrap_nb('-\\frac{21}{30}+\\frac{22}{30}')


def test_fs3_step4(fs3_step4):
    """Is this Sum's calculation's 4th step correct?"""
    assert fs3_step4.printed == wrap_nb('\\frac{-21+22}{30}')


def test_fs3_step5(fs3_step5):
    """Is this Sum's calculation's 5th step correct?"""
    assert fs3_step5.printed == wrap_nb('\\frac{1}{30}')


def test_fs3_step6(fs3_step6):
    """Is this Sum's calculation's 6th step correct?"""
    assert fs3_step6 is None


def test_fs4_printed(fs4):
    """Is this Sum correctly printed?"""
    assert fs4.printed == wrap_nb('\\frac{3}{4}-5')


def test_fs4_step1(fs4_step1):
    """Is this Sum's calculation's 1st step correct?"""
    assert fs4_step1.printed == wrap_nb('\\frac{3}{4}-\\frac{5}{1}')


def test_fs4_step2(fs4_step2):
    """Is this Sum's calculation's 2d step correct?"""
    assert fs4_step2.printed == wrap_nb('\\frac{3}{4}-\\frac{5\\times 4}'
                                        '{1\\times 4}')


def test_fs4_step3(fs4_step3):
    """Is this Sum's calculation's 3rd step correct?"""
    assert fs4_step3.printed == wrap_nb('\\frac{3}{4}-\\frac{20}{4}')


def test_fs4_step4(fs4_step4):
    """Is this Sum's calculation's 4th step correct?"""
    assert fs4_step4.printed == wrap_nb('\\frac{3-20}{4}')


def test_fs4_step5(fs4_step5):
    """Is this Sum's calculation's 5th step correct?"""
    assert fs4_step5.printed == wrap_nb('-\\frac{17}{4}')


def test_fs4_step6(fs4_step6):
    """Is this Sum's calculation's 6th step correct?"""
    assert fs4_step6 is None


def test_fs5_printed(fs5):
    """Is this Sum correctly printed?"""
    assert fs5.printed == wrap_nb('\\frac{25}{10}+\\frac{1}{10}')


def test_fs5_step1(fs5_step1):
    """Is this Sum's calculation's 1st step correct?"""
    assert fs5_step1.printed == wrap_nb('\\frac{25+1}{10}')


def test_fs5_step2(fs5_step2):
    """Is this Sum's calculation's 2d step correct?"""
    assert fs5_step2.printed == wrap_nb('\\frac{26}{10}')


def test_fs5_step3(fs5_step3):
    """Is this Sum's calculation's 3rd step correct?"""
    assert fs5_step3.printed == wrap_nb('\\frac{\\bcancel{2}\\times 13}'
                                        '{\\bcancel{2}\\times 5}')


def test_fs5_step4(fs5_step4):
    """Is this Sum's calculation's 4th step correct?"""
    assert fs5_step4.printed == wrap_nb('\\frac{13}{5}')


def test_fs5_step5(fs5_step5):
    """Is this Sum's calculation's 5th step correct?"""
    assert fs5_step5 is None


def test_fs6_printed(fs6):
    """Is this Sum correctly printed?"""
    assert fs6.printed == wrap_nb('-\\frac{18}{5}-\\frac{2}{5}')


def test_fs6_step1(fs6_step1):
    """Is this Sum's calculation's 1st step correct?"""
    assert fs6_step1.printed == wrap_nb('\\frac{-18-2}{5}')


def test_fs6_step2(fs6_step2):
    """Is this Sum's calculation's 2d step correct?"""
    assert fs6_step2.printed == wrap_nb('-\\frac{20}{5}')


def test_fs6_step3(fs6_step3):
    """Is this Sum's calculation's 3rd step correct?"""
    assert fs6_step3.printed == wrap_nb('-\\frac{\\bcancel{5}\\times 4}'
                                        '{\\bcancel{5}}')


def test_fs6_step4(fs6_step4):
    """Is this Sum's calculation's 4th step correct?"""
    assert fs6_step4.printed == wrap_nb('-4')


def test_fs6_step5(fs6_step5):
    """Is this Sum's calculation's 5th step correct?"""
    assert fs6_step5 is None


def test_fs7_printed(fs7):
    """Is this Sum correctly printed?"""
    assert fs7.printed == wrap_nb('4+\\frac{25}{10}-7+\\frac{1}{10}')


def test_fs7_step1(fs7_step1):
    """Is this Sum's calculation's 1st step correct?"""
    assert fs7_step1.printed == wrap_nb('4-7+\\frac{25+1}{10}')


def test_fs7_step2(fs7_step2):
    """Is this Sum's calculation's 2d step correct?"""
    assert fs7_step2.printed == wrap_nb('-3+\\frac{26}{10}')


def test_fs7_step3(fs7_step3):
    """Is this Sum's calculation's 3rd step correct?"""
    assert fs7_step3.printed == wrap_nb('-3+\\frac{\\bcancel{2}\\times 13}'
                                        '{\\bcancel{2}\\times 5}')


def test_fs7_step4(fs7_step4):
    """Is this Sum's calculation's 4th step correct?"""
    assert fs7_step4.printed == wrap_nb('-3+\\frac{13}{5}')


def test_fs7_step5(fs7_step5):
    """Is this Sum's calculation's 5th step correct?"""
    assert fs7_step5.printed == wrap_nb('-\\frac{3}{1}+\\frac{13}{5}')


def test_fs7_step6(fs7_step6):
    """Is this Sum's calculation's 6th step correct?"""
    assert fs7_step6.printed == wrap_nb('-\\frac{3\\times 5}{1\\times 5}'
                                        '+\\frac{13}{5}')


def test_fs7_step7(fs7_step7):
    """Is this Sum's calculation's 7th step correct?"""
    assert fs7_step7.printed == wrap_nb('-\\frac{15}{5}+\\frac{13}{5}')
