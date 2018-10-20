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
import math

from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.base_calculus import Item, Function, AngleItem
from mathmaker.lib.core.base_geometry import Point, Angle
from mathmaker.lib.core.calculus import Table
from tests.tools import wrap_nb


@pytest.fixture()
def ABC(): return Angle((Point('A', 1, 0),
                         Point('B', 0, 0),
                         Point('C', 0.5, 0.75)))


@pytest.fixture()
def cos_x(): return Function(name='cos',
                             fct=lambda x: math.cos(math.radians(x)))


@pytest.fixture()
def cos_ABC(ABC): return Function(name='cos',
                                  var=ABC,
                                  fct=lambda x: math.cos(math.radians(x)))


@pytest.fixture
def t0():
    return Table([[Item((2)), Item((5)), Item((6)), Item((7))],
                  [Item((4)), Item((10)), Item((12)), Item((14))]])


@pytest.fixture
def t1():
    return Table([[cos_x(), Item(('BC'))],
                  [Item((1)), Item(('BA'))]],
                 displ_as_qe=True)


@pytest.fixture
def t2():
    return Table([[cos_ABC(ABC()), Item(('EG'))],
                  [Item((1)), Item(('EF'))]],
                 displ_as_qe=True)


def test_t0_length(t0):
    """Is this Table's length correct?"""
    assert len(t0) == 4


def test_t0_is_numeric(t0):
    """Is this Table numeric?"""
    assert t0.is_numeric()


def test_t0_into_str(t0):
    """Is this Table correctly turned into a string?"""
    assert t0.into_str() == wrap_nb('\\begin{tabular}{|c|c|c|c|}\n\hline \n'
                                    '2&\n5&\n6&\n7\\\\\n\\hline \n'
                                    '4&\n10&\n12&\n14\\\\\n\\hline \n'
                                    '\end{tabular}\n')


def test_t0_into_str_bis(t0):
    """Is this Table correctly turned into a string?"""
    assert t0.into_str(as_a_quotients_equality=True,
                       ignore_1_denominator=True) == \
        wrap_nb('\\frac{2}{4}=\\frac{5}{10}=\\frac{6}{12}=\\frac{7}{14}')


def test_t0_as_cross_product_1(t0):
    """Is this Table correctly turned into a cross product?"""
    assert t0.cross_product((0, 1), 0).printed == \
        wrap_nb('\\frac{5\\times 4}{10}')


def test_t0_as_cross_product_2(t0):
    """Is this Table correctly turned into a cross product?"""
    assert t0.cross_product((0, 1), 1).printed == \
        wrap_nb('\\frac{2\\times 10}{4}')


def test_t0_as_cross_product_3(t0):
    """Is this Table correctly turned into a cross product?"""
    assert t0.cross_product((0, 1), 2).printed == \
        wrap_nb('\\frac{5\\times 4}{2}')


def test_t0_as_cross_product_4(t0):
    """Is this Table correctly turned into a cross product?"""
    assert t0.cross_product((0, 1), 3).printed == \
        wrap_nb('\\frac{2\\times 10}{5}')


def test_t1_into_str_as_QE(t1):
    """Is this Table correctly turned into a string?"""
    assert t1.printed == \
        wrap_nb('cos(x)=\\frac{\\text{BC}}{\\text{BA}}')


def test_t1_substituted(t1):
    """Are the literals in this table correctly substituted?"""
    t1.substitute({Value('x'): Value(35),
                   Value('BA'): Value(10)})
    assert t1.printed == \
        wrap_nb('cos(35)=\\frac{\\text{BC}}{10}')


def test_t2_into_str_as_QE(t2):
    """Is this Table correctly turned into a string?"""
    assert t2.printed == \
        wrap_nb('cos(\widehat{\\text{ABC}})=\\frac{\\text{EG}}{\\text{EF}}')


def test_t2_substituted(t2, ABC):
    """Are the literals in this table correctly substituted?"""
    t2.substitute({AngleItem(from_this_angle=ABC): Value(27),
                   Value('EF'): Value(5)})
    assert t2.printed == \
        wrap_nb('cos(27)=\\frac{\\text{EG}}{5}')


def test_t2_into_crossproduct_eq(t2, ABC):
    """Are the literals in this table correctly substituted?"""
    t2.substitute({AngleItem(from_this_angle=ABC): Value(32),
                   Value('EF'): Value(9)})
    assert t2.printed == \
        wrap_nb('cos(32)=\\frac{\\text{EG}}{9}')
    assert t2.into_crossproduct_equation().printed == \
        wrap_nb('cos(32)=\\frac{\\text{EG}}{9}')
