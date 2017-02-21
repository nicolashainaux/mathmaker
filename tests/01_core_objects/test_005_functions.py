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
import math

from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.base_calculus import Function
from tools import wrap_nb


@pytest.fixture()
def f_x(): return Function()


@pytest.fixture()
def cos_x(): return Function(name='cos',
                             fct=lambda x: math.cos(math.radians(x)))


def test_f_x_printed(f_x):
    """Is f(x) correctly printed?"""
    assert f_x.printed == wrap_nb('f(x)')


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


def test_cos_x_evaluated0(cos_x):
    """Is cos(x) correctly printed?"""
    cos_x.num_val = Value(60)
    cos_x.set_numeric_mode()
    assert cos_x.printed == wrap_nb('cos(60)')
    assert Value(cos_x.evaluate()).round(4) == Value('0.5')
