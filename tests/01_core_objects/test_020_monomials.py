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

from mathmaker.lib.core.base_calculus import Item, Monomial
from tests.tools import wrap_nb


def test_monom6_printed():
    """Is this Monomial printed correctly?"""
    m = Monomial(('+', 6, 0))
    m1 = m.throw_away_the_neutrals()
    assert m1.printed == wrap_nb('6')


def test_monom1_is_not_a_single_neutral_item0():
    """
    Is Monomial((1, 0)) not mistakenly considered as neutral for addition?
    """
    assert not Monomial((1, 0)).is_displ_as_a_single_neutral(Item(0))


def test_3x_squared_printed():
    """Is this squared Monomial printed correctly?"""
    m = Monomial(('+', 3, 1))
    m.set_exponent(2)
    assert m.printed == wrap_nb('(3x)^{2}')


def test_mon_deg0_5_squared_printed():
    """Is this squared Monomial printed correctly?"""
    m = Monomial(('+', 5, 0))
    m.set_exponent(2)
    assert m.printed == wrap_nb('5^{2}')
