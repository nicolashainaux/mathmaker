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
from decimal import Decimal

from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.base_geometry import Point
from mathmaker.lib.core.geometry import RectangleGrid


def test_exceptions():
    """Check exceptions are raised with wrong initialization data."""
    with pytest.raises(TypeError) as excinfo:
        RectangleGrid([Point('A', 0.5, 0.5), 4, 3, 'B', 'C', 'D'],
                      layout=4)
    assert 'layout keyword argument must be a str' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        RectangleGrid([Point('A', 0.5, 0.5), 4, 3, 'B', 'C', 'D'],
                      layout='4x4')
    assert 'no symbol × detected' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        RectangleGrid([Point('A', 0.5, 0.5), 4, 3, 'B', 'C', 'D'],
                      layout='a×4')
    assert 'row and col must be both integers' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        RectangleGrid([Point('A', 0.5, 0.5), 4, 3, 'B', 'C', 'D'],
                      layout='0×4')
    assert 'integers >= 1' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        RectangleGrid([Point('A', 0.5, 0.5), 4, 3, 'B', 'C', 'D'],
                      layout='4×0')
    assert 'integers >= 1' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        RectangleGrid([Point('A', 0.5, 0.5), 4, 3, 'B', 'C', 'D'],
                      layout='0×0')
    assert 'integers >= 1' in str(excinfo.value)


def test_grid1_into_euk():
    """Check RectangleGrid's generated euk file."""
    rg = RectangleGrid([Point('A', Decimal('0.5'), Decimal('0.5')),
                        Decimal('4'), Decimal('3'), 'B', 'C', 'D'],
                       layout='2×2')
    assert rg.into_euk() == \
        'box -0.1, -0.1, 5.1, 4.1\n\n'\
        'A = point(0.5, 0.5)\n'\
        'B = point(4.5, 0.5)\n'\
        'C = point(4.5, 3.5)\n'\
        'D = point(0.5, 3.5)\n'\
        '\n'\
        'draw\n'\
        '  (A.B.C.D)\n'\
        'end\n\n' \
        'a1 = point(2.5, 0.5)\n' \
        'b1 = point(2.5, 3.5)\n' \
        'c1 = point(4.5, 2)\n' \
        'd1 = point(0.5, 2)\n' \
        '\ndraw\n' \
        '  a1.b1\n' \
        '  c1.d1\n' \
        'end\n'
    ref = [[Point('A', Decimal('0.5'), Decimal('0.5')),
            Point('a1', Decimal('2.5'), Decimal('0.5')),
            Point('B', Decimal('4.5'), Decimal('0.5'))],
           [Point('d1', Decimal('0.5'), Decimal('2')),
            Point('i00', Decimal('2.5'), Decimal('2')),
            Point('c1', Decimal('4.5'), Decimal('2'))],
           [Point('D', Decimal('0.5'), Decimal('3.5')),
            Point('b1', Decimal('2.5'), Decimal('3.5')),
            Point('C', Decimal('4.5'), Decimal('3.5'))]
           ]
    for row_ref, row_rggrid in zip(ref, rg.grid):
        for p, q in zip(row_ref, row_rggrid):
            assert p == q

# def test_grid2_into_euk():
#     """Check RectangleGrid's generated euk file."""
#     rg = RectangleGrid([Point('A', 0.5, 0.5), 4, 3, 'B', 'C', 'D'],
#                        layout='3×6', fill='4×4')
#     print(rg.into_euk())
#     assert rg.into_euk() == \
#         'box -0.1, -0.1, 5.1, 4.1\n\n'\
#         'A = point(0.5, 0.5)\n'\
#         'B = point(4.5, 0.5)\n'\
#         'C = point(4.5, 3.5)\n'\
#         'D = point(0.5, 3.5)\n'\
#         '\n'\
#         'draw\n'\
#         '  (A.B.C.D)\n'\
#         'end\n\n' \
#         'a1 = point(2.5, 0.5)\n' \
#         'b1 = point(2.5, 3.5)\n' \
#         'c1 = point(4.5, 2)\n' \
#         'd1 = point(0.5, 2)\n' \
#         '\ndraw\n' \
#         '  a1.b1\n' \
#         '  c1.d1\n' \
#         'end\n'
