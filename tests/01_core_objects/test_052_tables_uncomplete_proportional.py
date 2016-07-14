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

from mathmaker.lib.core.base_calculus import Item
from mathmaker.lib.core.calculus import Table_UP
from tools import wrap_nb


@pytest.fixture
def AB(): return Item('AB')


@pytest.fixture
def CD(): return Item('CD')


@pytest.fixture
def EF(): return Item('EF')


@pytest.fixture
def GH(): return Item('GH')


@pytest.fixture
def MN(): return Item('MN')


@pytest.fixture
def tup0(AB, MN):
    return Table_UP(1.7, [Item(2), Item(5), Item(6)],
                         [None, (AB, None), (None, MN)])


@pytest.fixture
def tup1(AB, CD, EF, GH):
    return Table_UP(1.25, [Item(2), None, Item(3), Item(4)],
                          [None, (AB, CD), (EF, None), (None, GH)])


@pytest.fixture
def tup2(AB, MN):
    return Table_UP(0.8, [Item(3), Item(4), Item(9)],
                         [(AB, None), (None, None), (None, MN)])


def test_tup0_printed(tup0):
    """Is this table correctly printed?"""
    assert tup0.printed == \
        wrap_nb('\\begin{tabular}{|c|c|c|}\n\hline \n'
                '2&\n\\text{AB}&\n6\\\\\n\\hline \n'
                '3.4&\n8.5&\n\\text{MN}\\\\\n\\hline \n'
                '\end{tabular}\n')


def test_tup0_crossproducts_AB(tup0, AB):
    """Check one of the crossproducts of this table."""
    assert tup0.crossproducts_info[AB] == (1, 0)


def test_tup0_crossproduct_MN(tup0, MN):
    """Check one of the crossproducts of this table."""
    assert tup0.crossproducts_info[MN] == (2, 0)


def test_tup0_crossproduct_eq_AB(tup0, AB):
    """Check one of the crossproducts equations of this table."""
    assert tup0.into_crossproduct_equation(AB).printed == \
        wrap_nb('\\frac{2}{3.4}=\\frac{\\text{AB}}{8.5}')


def test_tup0_crossproduct_eq_MN(tup0, MN):
    """Check one of the crossproducts equations of this table."""
    assert tup0.into_crossproduct_equation(MN).printed == \
        wrap_nb('\\frac{2}{3.4}=\\frac{6}{\\text{MN}}')


def test_tup1_printed(tup1):
    """Is this table correctly printed?"""
    assert tup1.printed == \
        wrap_nb('\\begin{tabular}{|c|c|c|c|}\n\hline \n'
                '2&\n\\text{AB}&\n\\text{EF}&\n4\\\\\n\\hline \n'
                '2.5&\n\\text{CD}&\n3.75&\n\\text{GH}\\\\\n\\hline \n'
                '\end{tabular}\n')


def test_tup1_crossproducts_EF(tup1, EF):
    """Check one of the crossproducts of this table."""
    assert tup1.crossproducts_info[EF] == (2, 0)


def test_tup1_crossproduct_GH(tup1, GH):
    """Check one of the crossproducts of this table."""
    assert tup1.crossproducts_info[GH] == (3, 0)


def test_tup1_crossproduct_eq_GH(tup1, GH):
    """Check one of the crossproducts equations of this table."""
    assert tup1.into_crossproduct_equation(GH).printed == \
        wrap_nb('\\frac{2}{2.5}=\\frac{4}{\\text{GH}}')


def test_tup2_printed(tup2):
    """Is this table correctly printed?"""
    assert tup2.printed == \
        wrap_nb('\\begin{tabular}{|c|c|c|}\n\hline \n'
                '\\text{AB}&\n4&\n9\\\\\n\\hline \n'
                '2.4&\n3.2&\n\\text{MN}\\\\\n\\hline \n'
                '\end{tabular}\n')


def test_tup2_crossproduct_eq_AB(tup2, AB):
    """Check one of the crossproducts equations of this table."""
    assert tup2.into_crossproduct_equation(AB).printed == \
        wrap_nb('\\frac{\\text{AB}}{2.4}=\\frac{4}{3.2}')


def test_tup2_crossproduct_eq_MN(tup2, MN):
    """Check one of the crossproducts equations of this table."""
    assert tup2.into_crossproduct_equation(MN).printed == \
        wrap_nb('\\frac{4}{3.2}=\\frac{9}{\\text{MN}}')
