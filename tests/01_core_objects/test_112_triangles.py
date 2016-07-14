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

from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.geometry import Triangle


def test_t1_into_euk():
    """Check Triangle's generated euk file."""
    t1 = Triangle((("Z", "E", "P"),
                   {'side0': 4, 'angle1': 64, 'side1': 5}),
                  rotate_around_isobarycenter=115)
    t1.side[0].label = Value(4, unit='cm')
    t1.side[1].label = Value(5, unit='cm')
    t1.side[2].label = Value(4.84, unit='cm')
    t1.angle[0].label = Value('?')
    t1.angle[1].label = Value(64, unit='\\textdegree')
    t1.angle[2].label = Value(35, unit='\\textdegree')
    t1.angle[0].mark = 'simple'
    t1.angle[1].mark = 'double'
    t1.angle[2].mark = 'dotted'
    assert t1.into_euk() == \
        'box -1.32, -0.48, 4.71, 4.6\n\n'\
        'Z = point(4.11, 0.37)\n'\
        'E = point(2.42, 4)\n'\
        'P = point(-0.72, 0.12)\n'\
        '\n'\
        'draw\n'\
        '  (Z.E.P)\n'\
        '  $\\rotatebox{-65}{\sffamily 4~cm}$ Z 115 - 7.5 deg 6.5\n'\
        '  $\\rotatebox{51}{\sffamily 5~cm}$ E 231 - 6.5 deg 8\n'\
        '  $\\rotatebox{3}{\sffamily 4.84~cm}$ P 3 - 6.7 deg 7.8\n'\
        '  $\\rotatebox{-31.2}{\sffamily ?}$ Z 148.8 deg 2.7\n'\
        '  $\\rotatebox{82.9}{\sffamily 64\\textdegree}$ E 262.9 deg 2.7\n'\
        '  $\\rotatebox{27}{\sffamily 35\\textdegree}$ P 27 deg 2.7\n'\
        '  "Z" Z 328.8 deg, font("sffamily")\n'\
        '  "E" E 82.9 deg, font("sffamily")\n'\
        '  "P" P 207 deg, font("sffamily")\n'\
        'end\n\n'\
        'label\n'\
        '  E, Z, P simple\n'\
        '  P, E, Z double\n'\
        '  Z, P, E dotted\n'\
        'end'
