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

from mathmaker.lib.core.base_calculus import Item, Fraction
from mathmaker.lib.core.geometry import InterceptTheoremConfiguration
from tests.tools import wrap_nb


@pytest.fixture
def fig0():
    fig0 = InterceptTheoremConfiguration(sketch=False,
                                         rotate_around_isobarycenter=40)
    fig0.set_lengths([6, 12, 9], Fraction((Item(4), Item(3))))
    return fig0


@pytest.fixture
def fig0b():
    fig0b = InterceptTheoremConfiguration(sketch=False,
                                          rotate_around_isobarycenter=40)
    fig0b.set_lengths([6, 12, 9], Fraction((Item(4), Item(3))))
    fig0b.setup_labels(['?', True, False, True, True, True, False, False],
                       segments_list=[fig0b.u, fig0b.side[1], fig0b.v]
                       + fig0b.small + fig0b.chunk)
    return fig0b


@pytest.fixture
def fig1():
    fig1 = InterceptTheoremConfiguration(sketch=False,
                                         butterfly=True,
                                         rotate_around_isobarycenter=40)
    fig1.set_lengths([6, 12, 9], Fraction((Item(4), Item(3))))
    return fig1


def test_fig0_into_euk(fig0):
    """Check this figure's generated euk file."""
    fig0.setup_labels([True, True, True, True, True, True, True, True],
                      segments_list=[fig0.u, fig0.side[1], fig0.v]
                      + fig0.small + fig0.chunk)
    assert fig0.into_euk() == \
        'box -2.9, -2.13, 6.65, 4.27\n\n'\
        'A = point(1.58, -0.76)\n'\
        'B = point(5.41, 2.45)\n'\
        'C = point(-1.48, 3.67)\n'\
        'M = point(4.45, 1.65)\n'\
        'N = point(-0.72, 2.56)\n'\
        'U0 = point(2.22, -1.53)\n'\
        'U1 = point(6.05, 1.68)\n'\
        'V1 = point(-2.3, 3.1)\n'\
        'V0 = point(0.76, -1.33)\n'\
        'u = vector(U0, U1)\n'\
        'v = vector(V1, V0)\n\n'\
        'draw\n'\
        '  (A.B.C)\n'\
        '  M.N\n'\
        '  "A" A 262.2 deg, font("sffamily")\n'\
        '  "B" B 15 deg, font("sffamily")\n'\
        '  "C" C 147.4 deg, font("sffamily")\n'\
        '  "M" M 309.7 deg, font("sffamily")\n'\
        '  "N" N 214.8 deg, font("sffamily")\n'\
        '  u U0\n'\
        '  -u U1\n'\
        '  v V1\n'\
        '  -v V0\n'\
        '  $\\rotatebox{40}{\sffamily 6}$ A 40 - 7.8 deg 6\n'\
        '  $\\rotatebox{-10}{\sffamily 12}$ M 170 - 6.3 deg 8.4\n'\
        '  $\\rotatebox{305}{\sffamily 9}$ N 305 - 7.5 deg 6.5\n'\
        '  $\\rotatebox{40}{\sffamily 2}$ M 40 - 23.1 deg 2\n'\
        '  $\\rotatebox{304}{\sffamily 3}$ C 304 - 22.3 deg 2.2\n'\
        '  $\\rotatebox{40}{\sffamily 8}$ U0 40 - 6.5 deg 8\n'\
        '  $\\rotatebox{305}{\sffamily 12}$ V1 305 - 6.2 deg 8.7\n'\
        '  $\\rotatebox{-10}{\sffamily 16}$ B 170 - 5.2 deg 11.2\n'\
        'end\n'


def test_fig0b_into_euk2(fig0b):
    """Check this figure's generated euk file (less labels to display)."""
    assert fig0b.into_euk() == \
        'box -2.08, -2.13, 6.65, 4.27\n\n'\
        'A = point(1.58, -0.76)\n'\
        'B = point(5.41, 2.45)\n'\
        'C = point(-1.48, 3.67)\n'\
        'M = point(4.45, 1.65)\n'\
        'N = point(-0.72, 2.56)\n'\
        'U0 = point(2.22, -1.53)\n'\
        'U1 = point(6.05, 1.68)\n'\
        'V1 = point(-2.3, 3.1)\n'\
        'V0 = point(0.76, -1.33)\n'\
        'u = vector(U0, U1)\n'\
        'v = vector(V1, V0)\n\n'\
        'draw\n'\
        '  (A.B.C)\n'\
        '  M.N\n'\
        '  "A" A 262.2 deg, font("sffamily")\n'\
        '  "B" B 15 deg, font("sffamily")\n'\
        '  "C" C 147.4 deg, font("sffamily")\n'\
        '  "M" M 309.7 deg, font("sffamily")\n'\
        '  "N" N 214.8 deg, font("sffamily")\n'\
        '  u U0\n'\
        '  -u U1\n'\
        '  $\\rotatebox{40}{\sffamily 6}$ A 40 - 7.8 deg 6\n'\
        '  $\\rotatebox{-10}{\sffamily 12}$ M 170 - 6.3 deg 8.4\n'\
        '  $\\rotatebox{305}{\sffamily 9}$ N 305 - 7.5 deg 6.5\n'\
        '  $\\rotatebox{40}{\sffamily ?}$ U0 40 - 6.5 deg 8\n'\
        '  $\\rotatebox{-10}{\sffamily 16}$ B 170 - 5.2 deg 11.2\n'\
        'end\n'


def test_fig0_ratios_equalities(fig0):
    assert fig0.ratios_equalities().into_str() == \
        '\\frac{\\text{AM}}{\\text{AB}}='\
        '\\frac{\\text{MN}}{\\text{BC}}='\
        '\\frac{\\text{NA}}{\\text{CA}}'


def test_fig0b_ratios_equalities_substituted(fig0b):
    assert fig0b.ratios_equalities_substituted()\
        .into_str() == wrap_nb(
            '\\frac{6}{\\text{AB}}='
            '\\frac{12}{16}='
            '\\frac{9}{\\text{CA}}')


def test_fig0b_cross_product_equation1(fig0b):
    assert fig0b.ratios_equalities_substituted()\
        .into_crossproduct_equation(Item('AB')).printed == wrap_nb(
            '\\frac{6}{\\text{AB}}=\\frac{12}{16}')


def test_fig0b_cross_product_equation2(fig0b):
    assert fig0b.ratios_equalities_substituted()\
        .into_crossproduct_equation(Item('CA')).printed == wrap_nb(
            '\\frac{12}{16}=\\frac{9}{\\text{CA}}')


def test_fig1_into_euk(fig1):
    """Check this figure's generated euk file."""
    fig1.setup_labels([True, True, True, True, True, True],
                      segments_list=fig1.side + fig1.small)
    assert fig1.into_euk() == \
        'box -2.08, -4.68, 6.01, 4.27\n\n'\
        'C = point(1.58, -0.76)\n'\
        'D = point(5.41, 2.45)\n'\
        'E = point(-1.48, 3.67)\n'\
        'B = point(-1.3, -3.17)\n'\
        'A = point(3.87, -4.08)\n\n'\
        'draw\n'\
        '  (C.D.E)\n'\
        '  (C.B.A)\n\n'\
        '  "C" C 352.2 deg, font("sffamily")\n'\
        '  "D" D 15 deg, font("sffamily")\n'\
        '  "E" E 147.4 deg, font("sffamily")\n'\
        '  "B" B 214.8 deg, font("sffamily")\n'\
        '  "A" A 309.7 deg, font("sffamily")\n'\
        '  $\\rotatebox{40}{\sffamily 6}$ C 220 - 7.8 deg 6.1\n'\
        '  $\\rotatebox{350}{\sffamily 12}$ B 350 - 6.3 deg 8.4\n'\
        '  $\\rotatebox{-55}{\sffamily 9}$ A 125 - 7.5 deg 6.5\n'\
        '  $\\rotatebox{40}{\sffamily 8}$ C 40 - 6.5 deg 8\n'\
        '  $\\rotatebox{-10}{\sffamily 16}$ D 170 - 5.2 deg 11.2\n'\
        '  $\\rotatebox{305}{\sffamily 12}$ E 305 - 6.2 deg 8.7\n'\
        'end\n'
