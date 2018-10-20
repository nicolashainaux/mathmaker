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
from tests.tools import wrap_nb


@pytest.fixture()
def ABC(): return Angle((Point('A', 1, 0),
                         Point('B', 0, 0),
                         Point('C', 0.5, 0.75)))


@pytest.fixture()
def f_x(): return Function()


@pytest.fixture()
def cos_x(): return Function(name='cos',
                             fct=lambda x: math.cos(math.radians(x)))


@pytest.fixture()
def cos_ABC(ABC): return Function(name='cos',
                                  var=ABC,
                                  fct=lambda x: math.cos(math.radians(x)))


def test_f_x_printed(f_x):
    """Is f(x) correctly printed?"""
    assert f_x.printed == wrap_nb('f(x)')


def test_f_x_cloned(f_x):
    """Is f(x) correctly cloned?"""
    g_x = f_x.clone()
    assert f_x == g_x


def test_f_1_printed(f_x):
    """Is f(1) correctly printed?"""
    f_x.set_numeric_mode()
    assert f_x.printed == wrap_nb('f(1)')


def test_set_num_val_0(f_x):
    """Is f_x.num_val = 4 raising an exception?"""
    with pytest.raises(TypeError):
        f_x.num_val = 4


def test_set_num_val_1(f_x):
    """Is f_x.num_val = 'x' raising an exception?"""
    with pytest.raises(TypeError):
        f_x.num_val = 'x'


def test_set_num_val_2(f_x):
    """Does f_x.num_val = Value(4) correctly assign Value(4)?"""
    f_x.num_val = Value(4)
    f_x.set_numeric_mode()
    assert f_x.printed == wrap_nb('f(4)')


def test_cos_x_printed(cos_x):
    """Is cos(x) correctly printed?"""
    assert cos_x.printed == wrap_nb('cos(x)')


def test_cos_x_inv_fct_undefined(cos_x):
    """Is a call to an undefined inv fct raising a RuntimeError?"""
    with pytest.raises(RuntimeError):
        cos_x.inv_fct(0.5)


def test_cos_x_value_substituted(cos_x):
    """Is cos(x) correctly substituted?"""
    cos_x.substitute({Value('x'): Value(75)})
    assert cos_x.printed == wrap_nb('cos(75)')


def test_cos_x_item_substituted(cos_x):
    """Is cos(x) correctly substituted?"""
    cos_x.substitute({Item('x'): Value(75)})
    assert cos_x.printed == wrap_nb('cos(75)')


def test_cos_x_evaluated0(cos_x):
    """Is cos(x) correctly printed?"""
    cos_x.num_val = Value(60)
    cos_x.set_numeric_mode()
    assert cos_x.printed == wrap_nb('cos(60)')
    assert Value(cos_x.evaluate()).rounded(4) == Value('0.5')


def test_cos_ABC_printed(cos_ABC):
    """Is cos(ABC) correctly printed?"""
    assert cos_ABC.printed == wrap_nb('cos(\widehat{\\text{ABC}})')


def test_cos_ABC_substituted(cos_ABC, ABC):
    """Is cos(ABC) correctly substituted?"""
    cos_ABC.substitute({AngleItem(from_this_angle=ABC): Value(25)})
    assert cos_ABC.printed == wrap_nb('cos(25)')
