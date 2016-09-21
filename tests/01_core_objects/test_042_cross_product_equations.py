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
from mathmaker.lib.core.calculus import CrossProductEquation
from tools import wrap_nb


@pytest.fixture
def cpeq0():
    return CrossProductEquation((Item("AB"), Item(3),
                                 Item(4), Item(8)))


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
