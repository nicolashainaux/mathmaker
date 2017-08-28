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

# from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.base_geometry import Point
from mathmaker.lib.core.geometry import RectangleGrid


def test_exceptions():
    """Check RectangleGrid's exceptions."""
    with pytest.raises(TypeError) as excinfo:
        RectangleGrid([Point('A', Decimal('0.5'), Decimal('0.5')),
                       Decimal('4'), Decimal('3'), 'B', 'C', 'D'],
                      startvertex='1')
    assert str(excinfo.value) == 'startvertex must be int'
    with pytest.raises(ValueError) as excinfo:
        RectangleGrid([Point('A', Decimal('0.5'), Decimal('0.5')),
                       Decimal('4'), Decimal('3'), 'B', 'C', 'D'],
                      startvertex=4)
    assert str(excinfo.value) == 'startvertex must be 0, 1, 2 or 3'


def test_grids():
    """Check RectangleGrid's generated euk file."""
    rg = RectangleGrid([Point('A', Decimal('0.5'), Decimal('0.5')),
                        Decimal('4'), Decimal('3'), 'B', 'C', 'D'],
                       layout='2×2')
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
    rg = RectangleGrid([Point('A', Decimal('0.5'), Decimal('0.5')),
                        Decimal('4'), Decimal('3'), 'B', 'C', 'D'],
                       layout='1×1')
    ref = [[Point('A', Decimal('0.5'), Decimal('0.5')),
            Point('B', Decimal('4.5'), Decimal('0.5'))],
           [Point('D', Decimal('0.5'), Decimal('3.5')),
            Point('C', Decimal('4.5'), Decimal('3.5'))]
           ]
    for row_ref, row_rggrid in zip(ref, rg.grid):
        for p, q in zip(row_ref, row_rggrid):
            assert p == q
    rg = RectangleGrid([Point('A', Decimal('0.5'), Decimal('0.5')),
                        Decimal('4'), Decimal('3'), 'B', 'C', 'D'],
                       layout='1×2')
    ref = [[Point('A', Decimal('0.5'), Decimal('0.5')),
            Point('a1', Decimal('2.5'), Decimal('0.5')),
            Point('B', Decimal('4.5'), Decimal('0.5'))],
           [Point('D', Decimal('0.5'), Decimal('3.5')),
            Point('b1', Decimal('2.5'), Decimal('3.5')),
            Point('C', Decimal('4.5'), Decimal('3.5'))]
           ]
    for row_ref, row_rggrid in zip(ref, rg.grid):
        for p, q in zip(row_ref, row_rggrid):
            assert p == q
    rg = RectangleGrid([Point('A', Decimal('0.5'), Decimal('0.5')),
                        Decimal('4'), Decimal('3'), 'B', 'C', 'D'],
                       layout='2×1', autofit=False)
    ref = [[Point('A', Decimal('0.5'), Decimal('0.5')),
            Point('B', Decimal('4.5'), Decimal('0.5'))],
           [Point('d1', Decimal('0.5'), Decimal('2')),
            Point('c1', Decimal('4.5'), Decimal('2'))],
           [Point('D', Decimal('0.5'), Decimal('3.5')),
            Point('C', Decimal('4.5'), Decimal('3.5'))]
           ]
    for row_ref, row_rggrid in zip(ref, rg.grid):
        for p, q in zip(row_ref, row_rggrid):
            assert p == q
    rg = RectangleGrid([Point('A', Decimal('0.5'), Decimal('0.5')),
                        Decimal('4'), Decimal('3'), 'B', 'C', 'D'],
                       layout='2×1', autofit=True)  # i.e. same as layout '1×2'
    ref = [[Point('A', Decimal('0.5'), Decimal('0.5')),
            Point('a1', Decimal('2.5'), Decimal('0.5')),
            Point('B', Decimal('4.5'), Decimal('0.5'))],
           [Point('D', Decimal('0.5'), Decimal('3.5')),
            Point('b1', Decimal('2.5'), Decimal('3.5')),
            Point('C', Decimal('4.5'), Decimal('3.5'))]
           ]
    for row_ref, row_rggrid in zip(ref, rg.grid):
        for p, q in zip(row_ref, row_rggrid):
            assert p == q
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('10'), Decimal('3'), 'B', 'C', 'D'],
                       layout='3×5')
    ref = [[Point('A', 0, 0), Point('a1', 2, 0), Point('a2', 4, 0),
            Point('a3', 6, 0), Point('a4', 8, 0), Point('B', 10, 0)],
           [Point('d1', 0, 1), Point('i00', 2, 1), Point('i01', 4, 1),
            Point('i02', 6, 1), Point('i03', 8, 1), Point('c1', 10, 1)],
           [Point('d2', 0, 2), Point('i10', 2, 2), Point('i11', 4, 2),
            Point('i12', 6, 2), Point('i13', 8, 2), Point('c2', 10, 2)],
           [Point('D', 0, 3), Point('b1', 2, 3), Point('b2', 4, 3),
            Point('b3', 6, 3), Point('b4', 8, 3), Point('C', 10, 3)]
           ]
    for row_ref, row_rggrid in zip(ref, rg.grid):
        for p, q in zip(row_ref, row_rggrid):
            assert p == q


def test_into_euk0():
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
        'a1 = point(2.5, 0.5)\n' \
        'b1 = point(2.5, 3.5)\n' \
        'c1 = point(4.5, 2)\n' \
        'd1 = point(0.5, 2)\n' \
        '\ndraw\n' \
        '  a1.b1\n' \
        '  c1.d1\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk1():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('10'), Decimal('3'), 'B', 'C', 'D'],
                       layout='3×5')
    assert rg.into_euk() == \
        'box -0.6, -0.6, 10.6, 3.6\n\n'\
        'A = point(0, 0)\n'\
        'B = point(10, 0)\n'\
        'C = point(10, 3)\n'\
        'D = point(0, 3)\n'\
        '\n'\
        'a1 = point(2, 0)\n' \
        'b1 = point(2, 3)\n' \
        'a2 = point(4, 0)\n' \
        'b2 = point(4, 3)\n' \
        'a3 = point(6, 0)\n' \
        'b3 = point(6, 3)\n' \
        'a4 = point(8, 0)\n' \
        'b4 = point(8, 3)\n' \
        'c1 = point(10, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(10, 2)\n' \
        'd2 = point(0, 2)\n' \
        '\ndraw\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk2():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='3×6', startvertex=0)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i22 = point(3, 3)\n' \
        '\n' \
        'draw\n' \
        '  [A.B.c3.i22.b3.D] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk3():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='3×6', startvertex=1)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i10 = point(1, 2)\n' \
        '\n' \
        'draw\n' \
        '  [B.C.b1.i10.d2.A] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk4():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='3×6', startvertex=2)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i01 = point(2, 1)\n' \
        '\n' \
        'draw\n' \
        '  [D.C.B.a2.i01.d1] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk5():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='3×6', startvertex=3)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i13 = point(4, 2)\n' \
        '\n' \
        'draw\n' \
        '  [D.A.a4.i13.c2.C] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk6():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='5×5')
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        '\n' \
        'draw\n' \
        '  [A.B.C.D] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk7():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='3×4', startvertex=0)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i23 = point(4, 3)\n' \
        '\n' \
        'draw\n' \
        '  [A.a4.i23.d3] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk8():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='3×4', startvertex=1)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i20 = point(1, 3)\n' \
        '\n' \
        'draw\n' \
        '  [a1.B.c3.i20] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk9():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='3×4', startvertex=2)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i00 = point(1, 1)\n' \
        '\n' \
        'draw\n' \
        '  [i00.c1.C.b1] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk10():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='3×4', startvertex=3)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i03 = point(4, 1)\n' \
        '\n' \
        'draw\n' \
        '  [d1.i03.b4.D] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk11():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='2×3', startvertex=0)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i12 = point(3, 2)\n' \
        '\n' \
        'draw\n' \
        '  [A.a3.i12.d2] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk12():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='3×2', startvertex=0)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i21 = point(2, 3)\n' \
        '\n' \
        'draw\n' \
        '  [A.a2.i21.d3] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk13():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='1×13', startvertex=0)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i12 = point(3, 2)\n' \
        'i22 = point(3, 3)\n' \
        '\n' \
        'draw\n' \
        '  [A.B.c2.i12.i22.d3] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk14():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='1×13', startvertex=1)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i00 = point(1, 1)\n' \
        'i01 = point(2, 1)\n' \
        '\n' \
        'draw\n' \
        '  [B.C.b2.i01.i00.a1] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk15():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='1×13', startvertex=2)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i01 = point(2, 1)\n' \
        'i11 = point(2, 2)\n' \
        '\n' \
        'draw\n' \
        '  [D.C.c1.i01.i11.d2] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk16():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('5'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×5', fill='1×13', startvertex=3)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 5.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(5, 0)\n' \
        'C = point(5, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 4)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 4)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 4)\n' \
        'a4 = point(4, 0)\n' \
        'b4 = point(4, 4)\n' \
        'c1 = point(5, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(5, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(5, 3)\n' \
        'd3 = point(0, 3)\n' \
        'i22 = point(3, 3)\n' \
        'i23 = point(4, 3)\n' \
        '\n' \
        'draw\n' \
        '  [D.A.a3.i22.i23.b4] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  a4.b4\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk17():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('4'), Decimal('1'), 'B', 'C', 'D'],
                       layout='1×4', fill='1×3', startvertex=0)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 4.6, 1.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(4, 0)\n' \
        'C = point(4, 1)\n' \
        'D = point(0, 1)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 1)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 1)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 1)\n' \
        '\n' \
        'draw\n' \
        '  [A.a3.b3.D] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk18():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('4'), Decimal('1'), 'B', 'C', 'D'],
                       layout='1×4', fill='1×3', startvertex=1)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 4.6, 1.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(4, 0)\n' \
        'C = point(4, 1)\n' \
        'D = point(0, 1)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 1)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 1)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 1)\n' \
        '\n' \
        'draw\n' \
        '  [a1.B.C.b1] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk19():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('4'), Decimal('1'), 'B', 'C', 'D'],
                       layout='1×4', fill='1×3', startvertex=2)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 4.6, 1.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(4, 0)\n' \
        'C = point(4, 1)\n' \
        'D = point(0, 1)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 1)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 1)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 1)\n' \
        '\n' \
        'draw\n' \
        '  [a1.B.C.b1] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk20():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('4'), Decimal('1'), 'B', 'C', 'D'],
                       layout='1×4', fill='1×3', startvertex=3)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 4.6, 1.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(4, 0)\n' \
        'C = point(4, 1)\n' \
        'D = point(0, 1)\n' \
        '\n' \
        'a1 = point(1, 0)\n' \
        'b1 = point(1, 1)\n' \
        'a2 = point(2, 0)\n' \
        'b2 = point(2, 1)\n' \
        'a3 = point(3, 0)\n' \
        'b3 = point(3, 1)\n' \
        '\n' \
        'draw\n' \
        '  [A.a3.b3.D] lightgray\n' \
        '  a1.b1\n' \
        '  a2.b2\n' \
        '  a3.b3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk21():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('1'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×1', fill='3×1', startvertex=0)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 1.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(1, 0)\n' \
        'C = point(1, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'c1 = point(1, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(1, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(1, 3)\n' \
        'd3 = point(0, 3)\n' \
        '\n' \
        'draw\n' \
        '  [A.B.c3.d3] lightgray\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk22():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('1'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×1', fill='3×1', startvertex=1)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 1.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(1, 0)\n' \
        'C = point(1, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'c1 = point(1, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(1, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(1, 3)\n' \
        'd3 = point(0, 3)\n' \
        '\n' \
        'draw\n' \
        '  [A.B.c3.d3] lightgray\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk23():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('1'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×1', fill='3×1', startvertex=2)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 1.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(1, 0)\n' \
        'C = point(1, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'c1 = point(1, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(1, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(1, 3)\n' \
        'd3 = point(0, 3)\n' \
        '\n' \
        'draw\n' \
        '  [d1.c1.C.D] lightgray\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'


def test_into_euk24():
    rg = RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                        Decimal('1'), Decimal('4'), 'B', 'C', 'D'],
                       layout='4×1', fill='3×1', startvertex=3)
    assert rg.into_euk() == \
        'box -0.6, -0.6, 1.6, 4.6\n' \
        '\n' \
        'A = point(0, 0)\n' \
        'B = point(1, 0)\n' \
        'C = point(1, 4)\n' \
        'D = point(0, 4)\n' \
        '\n' \
        'c1 = point(1, 1)\n' \
        'd1 = point(0, 1)\n' \
        'c2 = point(1, 2)\n' \
        'd2 = point(0, 2)\n' \
        'c3 = point(1, 3)\n' \
        'd3 = point(0, 3)\n' \
        '\n' \
        'draw\n' \
        '  [d1.c1.C.D] lightgray\n' \
        '  c1.d1\n' \
        '  c2.d2\n' \
        '  c3.d3\n' \
        '  (A.B.C.D)\n' \
        'end\n'
