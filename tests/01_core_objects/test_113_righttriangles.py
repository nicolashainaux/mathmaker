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

from mathmaker.lib.common.cst import HUNDREDTH
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.calculus import Equation
from mathmaker.lib.core.geometry import RightTriangle
from mathmaker.lib.common import pythagorean
from tools import wrap_nb


@pytest.fixture
def t4():
    t4 = RightTriangle((("L", "O", "P"),
                        {'leg0': 2, 'leg1': 7}),
                       rotate_around_isobarycenter=140)
    t4.leg[0].label = Value(1.5, unit='cm')
    t4.leg[1].label = Value("")
    t4.hypotenuse.label = Value(7, unit='cm')
    t4.angle[0].mark = "back"
    t4.angle[2].mark = "dotted"
    t4.angle[0].label = Value(30, unit="\\textdegree")
    return t4


def test_t1_into_euk():
    """Check RightTriangle's generated euk file."""
    t1 = RightTriangle((("A", "B", "C"),
                        {'leg0': 4, 'leg1': 3}),
                       rotate_around_isobarycenter='no')
    t1.leg[0].label = Value(4, unit='cm')
    t1.leg[1].label = Value(3, unit='cm')
    t1.hypotenuse.label = Value(5, unit='cm')
    assert t1.into_euk() == ''\
        'box -0.6, -0.6, 4.6, 3.6\n\n'\
        'A = point(0, 0)\n'\
        'B = point(4, 0)\n'\
        'C = point(4, 3)\n'\
        '\n'\
        'draw\n'\
        '  (A.B.C)\n'\
        '  $\\rotatebox{0}{\sffamily 4~cm}$ A 0 - 7.5 deg 6.4\n'\
        '  $\\rotatebox{-90}{\sffamily 3~cm}$ B 90 - 9 deg 4.9\n'\
        '  $\\rotatebox{37}{\sffamily 5~cm}$ C 217 - 6.5 deg 8\n'\
        '  "A" A 198.4 deg, font("sffamily")\n'\
        '  "B" B 315 deg, font("sffamily")\n'\
        '  "C" C 63.4 deg, font("sffamily")\n'\
        'end\n\n'\
        'label\n'\
        '  C, B, A right\n'\
        'end'


def test_t2_into_euk():
    """Check RightTriangle's generated euk file."""
    t2 = RightTriangle((("Y", "E", "P"),
                        {'leg0': 4, 'leg1': 3}),
                       rotate_around_isobarycenter=30)
    t2.leg[0].label = Value(4, unit='cm')
    t2.leg[1].label = Value(3, unit='cm')
    t2.hypotenuse.label = Value(5, unit='cm')
    assert t2.into_euk() == ''\
        'box 0.26, -1.8, 4.92, 4.0\n\n'\
        'Y = point(0.86, -1.2)\n'\
        'E = point(4.32, 0.8)\n'\
        'P = point(2.82, 3.4)\n'\
        '\n'\
        'draw\n'\
        '  (Y.E.P)\n'\
        '  $\\rotatebox{30}{\sffamily 4~cm}$ Y 30 - 7.5 deg 6.4\n'\
        '  $\\rotatebox{-60}{\sffamily 3~cm}$ E 120 - 8.9 deg 4.9\n'\
        '  $\\rotatebox{67}{\sffamily 5~cm}$ P 247 - 6.5 deg 8.1\n'\
        '  "Y" Y 228.4 deg, font("sffamily")\n'\
        '  "E" E 344.9 deg, font("sffamily")\n'\
        '  "P" P 93.5 deg, font("sffamily")\n'\
        'end\n\n'\
        'label\n'\
        '  P, E, Y right\n'\
        'end'


def test_t3_into_euk():
    """Check RightTriangle's generated euk file."""
    t3 = RightTriangle((("Z", "A", "K"),
                        {'leg0': 3, 'leg1': 4}),
                       rotate_around_isobarycenter=75)
    t3.leg[0].label = Value(3.2, unit='cm')
    t3.leg[1].label = Value(4.5, unit='cm')
    t3.hypotenuse.label = Value("")
    assert t3.into_euk() == ''\
        'box -0.92, -1.54, 4.15, 3.59\n\n'\
        'Z = point(2.77, -0.94)\n'\
        'A = point(3.55, 1.95)\n'\
        'K = point(-0.32, 2.99)\n'\
        '\n'\
        'draw\n'\
        '  (Z.A.K)\n'\
        '  $\\rotatebox{75}{\sffamily 3.2~cm}$ Z 75 - 9.1 deg 4.8\n'\
        '  $\\rotatebox{-15}{\sffamily 4.5~cm}$ A 165 - 7.5 deg 6.5\n'\
        '  "Z" Z 281.6 deg, font("sffamily")\n'\
        '  "A" A 30 deg, font("sffamily")\n'\
        '  "K" K 146.6 deg, font("sffamily")\n'\
        'end\n\n'\
        'label\n'\
        '  K, A, Z right\n'\
        'end'


def test_t4_into_euk(t4):
    """Check RightTriangle's generated euk file."""
    assert t4.into_euk() == ''\
        'box -2.78, -1.41, 4.45, 5.15\n\n'\
        'L = point(3.85, 3.26)\n'\
        'O = point(2.32, 4.55)\n'\
        'P = point(-2.18, -0.81)\n'\
        '\n'\
        'draw\n'\
        '  (L.O.P)\n'\
        '  $\\rotatebox{-40}{\sffamily 1.5~cm}$ L 140 - 17 deg 3.3\n'\
        '  $\\rotatebox{34}{\sffamily 7~cm}$ P 34 - 5.1 deg 11.7\n'\
        '  $\\rotatebox{-2.9}{\sffamily 30\\textdegree}$ L 177.1 deg 2.7\n'\
        '  "L" L 357.1 deg, font("sffamily")\n'\
        '  "O" O 94.9 deg, font("sffamily")\n'\
        '  "P" P 222.1 deg, font("sffamily")\n'\
        'end\n\n'\
        'label\n'\
        '  O, L, P back\n'\
        '  P, O, L right\n'\
        '  L, P, O dotted\n'\
        'end'


def test_t4_pyth_eq(t4):
    """Check the pythagorean equality created from t4."""
    assert t4.pythagorean_substequality().into_str() == \
        wrap_nb('\\text{OP}^{2}=\\text{PL}^{2}-\\text{LO}^{2}')


def test_t4_pyth_eq_substituted(t4):
    """Check the pythagorean equality created from t4, once substituted."""
    assert t4.pythagorean_substequality().substitute().into_str() == \
        wrap_nb('\\text{OP}^{2}=7^{2}-1.5^{2}')


def test_t4_pyth_eq_autoresolution(t4):
    """
    Check the auto-resolution of the pythagorean equation created from t4.
    """
    eq_t4 = Equation(t4.pythagorean_substequality().substitute())
    assert eq_t4.auto_resolution(dont_display_equations_name=True,
                                 decimal_result=HUNDREDTH,
                                 pythagorean_mode=True,
                                 unit='cm') == \
        wrap_nb('\[\\text{OP}^{2}=7^{2}-1.5^{2}\]'
                '\[\\text{OP}^{2}=49-2.25\]'
                '\[\\text{OP}^{2}=46.75\]'
                '\[\\text{OP}=\\sqrt{\mathstrut 46.75}'
                '\\text{ because \\text{OP} is positive.}\]'
                '\[\\text{OP}\\simeq6.84\\text{ cm}\]')


def test_t5_into_euk():
    """Check RightTriangle's generated euk file."""
    t5 = RightTriangle((("P", "A", "X"),
                        {'leg0': 1, 'leg1': 8}),
                       rotate_around_isobarycenter=0)
    t5.leg[0].label = Value(1, unit='cm')
    t5.leg[1].label = Value(8, unit='cm')
    t5.hypotenuse.label = Value("?")
    t5.angle[0].mark = "simple"
    t5.angle[2].mark = "double"
    t5.angle[0].label = Value(64, unit="\\textdegree")
    t5.angle[2].label = Value(80, unit="\\textdegree")
    assert t5.into_euk() == ''\
        'box -0.6, -0.6, 1.6, 8.6\n\n'\
        'P = point(0, 0)\n'\
        'A = point(1, 0)\n'\
        'X = point(1, 8)\n'\
        '\n'\
        'draw\n'\
        '  (P.A.X)\n'\
        '  $\\rotatebox{0}{\sffamily 1~cm}$ P 0 - 25 deg 1.6\n'\
        '  $\\rotatebox{-90}{\sffamily 8~cm}$ A 90 - 4.7 deg 12.8\n'\
        '  $\\rotatebox{83}{\sffamily ?}$ X 263 - 4.7 deg 12.9\n'\
        '  $\\rotatebox{41.5}{\sffamily 64\\textdegree}$ P 41.5 deg 2.7\n'\
        '  $\\rotatebox{86.5}{\sffamily 80\\textdegree}$ X 266.5 deg 7.92\n'\
        '  "P" P 221.5 deg, font("sffamily")\n'\
        '  "A" A 315 deg, font("sffamily")\n'\
        '  "X" X 86.5 deg, font("sffamily")\n'\
        'end\n\n'\
        'label\n'\
        '  A, P, X simple\n'\
        '  X, A, P right\n'\
        '  P, X, A double\n'\
        'end'


def test_legmatching_65():
    """Check if the legs matching an hypotenuse of 65 are correct."""
    assert pythagorean.get_legs_matching_given_hypotenuse(65) == \
        [16, 63, 25, 60, 33, 56, 39, 52]


def test_hypmatching_36():
    """Check if the hypotenuses matching a leg of 36 are correct."""
    assert pythagorean.get_legs_matching_given_leg(36) == \
        [15, 27, 48, 77, 105, 160]
