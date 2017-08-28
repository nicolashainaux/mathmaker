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

from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.base_geometry import Point
from mathmaker.lib.core.geometry import Rectangle


def test_r1_into_euk():
    """Check Rectangle's generated euk file."""
    r1 = Rectangle([Point('A', 0.5, 0.5), 4, 3, 'B', 'C', 'D'])
    r1.side[2].label = Value(4, unit='cm')
    r1.side[3].label = Value(3, unit='cm')
    assert r1.into_euk() == \
        'box -0.1, -0.1, 5.1, 4.1\n\n'\
        'A = point(0.5, 0.5)\n'\
        'B = point(4.5, 0.5)\n'\
        'C = point(4.5, 3.5)\n'\
        'D = point(0.5, 3.5)\n'\
        '\n'\
        'draw\n'\
        '  (A.B.C.D)\n'\
        '  $\\rotatebox{0}{\sffamily 4~cm}$ C 180 - 7.5 deg 6.4\n'\
        '  $\\rotatebox{90}{\sffamily 3~cm}$ D 270 - 9 deg 4.9\n'\
        '  "A" A 225 deg, font("sffamily")\n'\
        '  "B" B 315 deg, font("sffamily")\n'\
        '  "C" C 45 deg, font("sffamily")\n'\
        '  "D" D 135 deg, font("sffamily")\n'\
        'end\n\n'\
        'label\n'\
        '  B, A, D right\n'\
        '  C, B, A right\n'\
        '  D, C, B right\n'\
        '  A, D, C right\n'\
        'end\n'
