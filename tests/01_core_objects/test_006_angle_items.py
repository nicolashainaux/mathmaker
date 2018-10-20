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

from mathmaker.lib.core.base_calculus import Item, AngleItem
from mathmaker.lib.core.base_geometry import Point, Angle
from tests.tools import wrap_nb


@pytest.fixture()
def ABC(): return Angle((Point('A', 1, 0),
                         Point('B', 0, 0),
                         Point('C', 0.5, 0.75)))


def test_empty_init():
    """Does an empty __init__() call trigger the correct Error?"""
    with pytest.raises(ValueError):
        AngleItem()


def test_wrong_init0():
    """Does a wrong __init__() call trigger the correct Error?"""
    with pytest.raises(TypeError):
        AngleItem(copy_this=Item(30))


def test_wrong_init1():
    """Does a wrong __init__() call trigger the correct Error?"""
    with pytest.raises(TypeError):
        AngleItem(from_this_angle='ABC')


def test_30degrees_printed():
    """Is a angle of 30° correctly printed?"""
    assert AngleItem(raw_value=30).printed == '\\text{30}'


def test_ABC_printed(ABC):
    """Is AngleItem ABC correctly printed?"""
    assert AngleItem(from_this_angle=ABC).printed == \
        wrap_nb('\widehat{\\text{ABC}}')


def test_ABC_raw_value(ABC):
    """Is AngleItem ABC's raw value correct?"""
    assert AngleItem(from_this_angle=ABC).raw_value == 'ABC'
