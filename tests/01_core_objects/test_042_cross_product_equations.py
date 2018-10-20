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
from mathmaker.lib.core.base_calculus import (Item, Function)
from mathmaker.lib.core.calculus import CrossProductEquation
from mathmaker.lib.core.base_geometry import Point, Angle
from tests.tools import wrap_nb


@pytest.fixture()
def ABC(): return Angle((Point('A', 1, 0),
                         Point('B', 0, 0),
                         Point('C', 0.5, 0.75)))


@pytest.fixture()
def cos_ABC(ABC): return Function(name='cos',
                                  var=ABC,
                                  fct=lambda x: math.cos(math.radians(x)),
                                  inv_fct=lambda x: math.degrees(math.acos(x)))


@pytest.fixture()
def cos_40():
    return Function(name='cos',
                    fct=lambda x: math.cos(math.radians(x)),
                    num_val=Value(40),
                    display_mode='numeric')


@pytest.fixture
def cpeq0():
    return CrossProductEquation((Item('AB'), Item(3),
                                 Item(4), Item(8)))


@pytest.fixture
def cpeq2():
    return CrossProductEquation((cos_40(), Item('AB'),
                                 Item(1), Item(8)))


@pytest.fixture
def cpeq3(ABC):
    return CrossProductEquation((cos_ABC(ABC), Item(3),
                                 Item(1), Item(8)))


def test_cpeq0_printed(cpeq0):
    """Is this Equation correctly printed?"""
    assert cpeq0.printed == wrap_nb('\\frac{\\text{AB}}{4}=\\frac{3}{8}')


def test_cpeq0_autoresolution(cpeq0):
    """Is this Equation correctly auto-resolved?"""
    assert cpeq0.auto_resolution(dont_display_equations_name=True) == \
        wrap_nb('\[\\frac{\\text{AB}}{4}=\\frac{3}{8}\]'
                '\[\\text{AB}=\\frac{3\\times 4}{8}\]'
                '\[\\text{AB}=\\frac{3\\times \\bcancel{4}}'
                '{\\bcancel{4}\\times 2}\]'
                '\[\\text{AB}=\\frac{3}{2}\]')


def test_cpeq0_autoresolution_bis(cpeq0):
    """Is this Equation correctly auto-resolved?"""
    assert cpeq0.auto_resolution(dont_display_equations_name=True,
                                 skip_fraction_simplification=True,
                                 decimal_result=2) == \
        wrap_nb('\[\\frac{\\text{AB}}{4}=\\frac{3}{8}\]'
                '\[\\text{AB}=\\frac{3\\times 4}{8}\]'
                '\[\\text{AB}=1.5\]')


def test_cpeq0_autoresolution_ter(cpeq0):
    """Is this Equation correctly auto-resolved?"""
    assert cpeq0.auto_resolution(dont_display_equations_name=True,
                                 skip_fraction_simplification=True) == \
        wrap_nb('\[\\frac{\\text{AB}}{4}=\\frac{3}{8}\]'
                '\[\\text{AB}=\\frac{3\\times 4}{8}\]'
                '\[\\text{AB}=\\frac{3}{2}\]')


def test_cpeq1_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = CrossProductEquation((Item(6), Item(1.4),
                               Item(1.5), Item("AB")))
    assert eq.auto_resolution(dont_display_equations_name=True,
                              skip_fraction_simplification=True,
                              decimal_result=2) == \
        wrap_nb('\[\\frac{6}{1.5}=\\frac{1.4}{\\text{AB}}\]'
                '\[\\text{AB}=\\frac{1.4\\times 1.5}{6}\]'
                '\[\\text{AB}=0.35\]')


def test_cpeq2_printed(cpeq2):
    """Is this Equation correctly printed?"""
    assert cpeq2.printed == wrap_nb('cos(40)=\\frac{\\text{AB}}{8}')


def test_cpeq2_autoresolution(cpeq2):
    """Is this Equation correctly auto-resolved?"""
    assert cpeq2.auto_resolution(dont_display_equations_name=True,
                                 skip_fraction_simplification=True,
                                 decimal_result=2) == \
        wrap_nb('\[cos(40)=\\frac{\\text{AB}}{8}\]'
                '\[\\text{AB}=cos(40)\\times 8\]'
                '\[\\text{AB}\\simeq6.13\]')


def test_cpeq3_autoresolution(cpeq3):
    """Is this Equation correctly auto-resolved?"""
    assert cpeq3.auto_resolution(dont_display_equations_name=True,
                                 skip_fraction_simplification=True,
                                 decimal_result=0,
                                 unit='\\textdegree') == \
        '\[cos(\widehat{\\text{ABC}})=\\frac{\\text{3}}{\\text{8}}\]'\
        '\[\widehat{\\text{ABC}}\\simeq\\text{68}\\text{ \\textdegree}\]'
