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

from mathmaker.lib.core.base_geometry import Point


def test_p0x():
    """Check Point's abscissa."""
    assert Point('A', 0, 0).x == 0


def test_points_equalities():
    """Check Points' equality."""
    assert Point('A', 0, 0) == Point('A', 0, 0)
    assert Point('A', 0, 0) != Point('B', 0, 0)
    assert Point('A', 0, 0).xy == Point('B', 0, 0).xy
