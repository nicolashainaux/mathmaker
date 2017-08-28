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
from decimal import Decimal

from mathmaker.lib.core.base_geometry import Point, Segment


def test_divide_segment():
    """Check Points dividing Segment."""
    AB = Segment((Point('A', 0, 0), Point('B', 5, 0)))
    p = AB.dividing_points(n=4)
    assert p == [Point('a1', Decimal('1.25'), 0),
                 Point('a2', Decimal('2.5'), 0),
                 Point('a3', Decimal('3.75'), 0)]
    AB = Segment((Point('A', 0, 0), Point('B', 0, 5)))
    p = AB.dividing_points(n=4)
    assert p == [Point('a1', 0, Decimal('1.25')),
                 Point('a2', 0, Decimal('2.5')),
                 Point('a3', 0, Decimal('3.75'))]
    AB = Segment((Point('A', 0, 0), Point('B', 5, 5)))
    p = AB.dividing_points(n=4)
    assert p == [Point('a1', Decimal('1.25'), Decimal('1.25')),
                 Point('a2', Decimal('2.5'), Decimal('2.5')),
                 Point('a3', Decimal('3.75'), Decimal('3.75'))]
    p = AB.dividing_points(n=1)
    assert p == []
    with pytest.raises(TypeError):
        p = AB.dividing_points(n='4')
    with pytest.raises(ValueError):
        p = AB.dividing_points(n=0)
