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

from mathmaker.lib.core.base_calculus import (Item, Sum, Monomial, Expandable,
                                              Product)
from mathmaker.lib.core.base_calculus import Polynomial, BinomialIdentity
from mathmaker.lib.core.calculus import Expression
from tests.tools import wrap_nb


@pytest.fixture
def expA():
    t = Expandable((Item(2), Sum([Item(1), Monomial((5, 1))])))
    return Expression("A", t)


@pytest.fixture
def expB():
    t = Expandable((Sum([Item(1), Monomial((-11, 1))]),
                    Sum([Item(11), Monomial((7, 1))])))
    return Expression("B", t)


@pytest.fixture
def expC():
    t = Sum([Monomial((3, 1)),
            Expandable((Item(-1),
                        Expandable((Sum([Item('x'), Item(3)]),
                                    Sum([Item(6), Monomial((2, 1))])))))])
    return Expression("C", t)


@pytest.fixture
def expD():
    t = Expandable((Item(-1), Sum([Monomial((3, 1)), Item(-2)])))
    return Expression("D", t)


@pytest.fixture
def expE():
    t = Sum([Product([Item(-3), Item(10)]),
             Product([Monomial(('-', 10, 1)), Monomial(('-', 9, 1))]),
             Product([Monomial(('+', 7, 1)), Monomial(('+', 8, 1))]),
             Product([Item(8), Item(10)])])
    return Expression("E", t)


@pytest.fixture
def expF():
    t = Sum([Product([Item(-2), Item(-6)]),
             Item(-1),
             Product([Item(3), Item(('-', "x", 1))]),
             Product([Monomial(('-', 8, 1)), Item(-3)])])
    return Expression("F", t)


@pytest.fixture
def expG():
    t = Sum([Monomial(('+', 5, 1)),
             Product([Monomial(('+', 7, 1)), Monomial(('+', 8, 1))]),
             Product([Monomial(('+', 5, 1)), Item(-1)]),
             Product([Item(7), Item(8)])])
    return Expression("G", t)


@pytest.fixture
def expH():
    t = Sum([Item(-30), Item(80), Monomial(('+', 1, 2))])
    return Expression("H", t)


@pytest.fixture
def expI():
    t = Sum([Monomial(('+', 4, 1)),
             Expandable((Monomial(('+', 1, 0)),
                         Polynomial([Monomial(('-', 15, 1)),
                                     Monomial(('+', 8, 0)),
                                     Monomial(('-', 5, 1))])))])
    return Expression("I", t)


@pytest.fixture
def expJ():
    t = BinomialIdentity((Item(3), Monomial(('+', 3, 1))),
                         squares_difference=True)
    return Expression("J", t)


@pytest.fixture
def expK():
    t = BinomialIdentity((Item(1), Monomial(('+', 10, 1))),
                         squares_difference=True)
    return Expression("K", t)


@pytest.fixture
def expL():
    t = Sum([Item(-2), Monomial(('-', 1, 1)),
             Monomial(('+', 8, 2)), Monomial(('+', 1, 1))])
    return Expression("L", t)


@pytest.fixture
def expM():
    t = Sum([Monomial((-15, 0)), Expandable((Item(1),
                                             Sum([Item(10),
                                                  Monomial((14, 1)),
                                                  Monomial(('-', 10, 2))])))])
    return Expression("M", t)


@pytest.fixture
def expN():
    t = Sum([Expandable((Monomial(('-', 1, 0)),
                         Expandable((Sum([Monomial((2, 1)),
                                          Monomial((9, 0))]),
                                     Sum([Monomial((-3, 1)),
                                          Monomial((-7, 0))]))))),
             Expandable((Monomial((4, 0)),
                         Sum([Monomial((-3, 1)),
                              Monomial((9, 0))]))),
             Monomial((13, 0))])
    return Expression("N", t)


@pytest.fixture
def expP():
    t = Sum([Expandable((Monomial(('+', 7, 0)),
                         Sum([Monomial(('-', 6, 1)),
                              Monomial((6, 0))]))),
             BinomialIdentity((Monomial(('-', 10, 1)),
                               Monomial(('-', 3, 0))),
                              difference_square='OK')])
    return Expression("P", t)


def test_exp0_next_step():
    """Is this Expression not expandable (returns None)?"""
    assert Product([Sum([Item(146)]), Item(('+', "x", 2))])\
        .expand_and_reduce_next_step() is None


def test_expA_auto_er(expA):
    """Is this Expression correctly expanded and reduced?"""
    assert expA.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{A}=2(1+5x)$\\newline \n'
                '$\\text{A}=2\\times 1+2\\times 5x$\\newline \n'
                '$\\text{A}=2+10x$\\newline \n')


def test_expB_auto_er(expB):
    """Is this Expression correctly expanded and reduced?"""
    assert expB.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{B}=(1-11x)(11+7x)$\\newline \n'
                '$\\text{B}=1\\times 11+1\\times 7x-11x\\times 11-11x'
                '\\times 7x$\\newline \n'
                '$\\text{B}=11+7x-121x-77x^{2}$\\newline \n'
                '$\\text{B}=11+(7-121)x-77x^{2}$\\newline \n'
                '$\\text{B}=11-114x-77x^{2}$\\newline \n')


def test_expC_auto_er(expC):
    """Is this Expression correctly expanded and reduced?"""
    assert expC.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{C}=3x-(x+3)(6+2x)$\\newline \n'
                '$\\text{C}=3x-(x\\times 6+x\\times 2x+3\\times 6+3'
                '\\times 2x)$\\newline \n'
                '$\\text{C}=3x-(6x+2x^{2}+18+6x)$\\newline \n'
                '$\\text{C}=3x-6x-2x^{2}-18-6x$\\newline \n'
                '$\\text{C}=(3-6-6)x-2x^{2}-18$\\newline \n'
                '$\\text{C}=-9x-2x^{2}-18$\\newline \n')


def test_expD_auto_er(expD):
    """Is this Expression correctly expanded and reduced?"""
    assert expD.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{D}=-(3x-2)$\\newline \n'
                '$\\text{D}=-3x+2$\\newline \n')


def test_expE_auto_er(expE):
    """Is this Expression correctly expanded and reduced?"""
    assert expE.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{E}=-3\\times 10-10x\\times (-9x)+7x\\times '
                '8x+8\\times 10$\\newline \n'
                '$\\text{E}=-30+90x^{2}+56x^{2}+80$\\newline \n'
                '$\\text{E}=-30+80+(90+56)x^{2}$\\newline \n'
                '$\\text{E}=50+146x^{2}$\\newline \n')


def test_expF_auto_er(expF):
    """Is this Expression correctly expanded and reduced?"""
    assert expF.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{F}=-2\\times (-6)-1+3\\times (-x)-8x\\times '
                '(-3)$\\newline \n'
                '$\\text{F}=12-1-3x+24x$\\newline \n'
                '$\\text{F}=11+(-3+24)x$\\newline \n'
                '$\\text{F}=11+21x$\\newline \n')


def test_expG_auto_er(expG):
    """Is this Expression correctly expanded and reduced?"""
    assert expG.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{G}=5x+7x\\times 8x+5x\\times (-1)+7\\times '
                '8$\\newline \n'
                '$\\text{G}=5x+56x^{2}-5x+56$\\newline \n'
                '$\\text{G}=(5-5)x+56x^{2}+56$\\newline \n'
                '$\\text{G}=0x+56x^{2}+56$\\newline \n'
                '$\\text{G}=56x^{2}+56$\\newline \n')


def test_expH_auto_er(expH):
    """Is this Expression correctly expanded and reduced?"""
    assert expH.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{H}=-30+80+x^{2}$\\newline \n'
                '$\\text{H}=50+x^{2}$\\newline \n')


def test_expI_auto_er(expI):
    """Is this Expression correctly expanded and reduced?"""
    assert expI.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{I}=4x+(-15x+8-5x)$\\newline \n'
                '$\\text{I}=4x-15x+8-5x$\\newline \n'
                '$\\text{I}=(4-15-5)x+8$\\newline \n'
                '$\\text{I}=-16x+8$\\newline \n')


def test_expJ_auto_er(expJ):
    """Is this Expression correctly expanded and reduced?"""
    assert expJ.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{J}=(3+3x)(3-3x)$\\newline \n'
                '$\\text{J}=3^{2}-(3x)^{2}$\\newline \n'
                '$\\text{J}=9-9x^{2}$\\newline \n')


def test_expK_auto_er(expK):
    """Is this Expression correctly expanded and reduced?"""
    assert expK.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{K}=(1+10x)(1-10x)$\\newline \n'
                '$\\text{K}=1^{2}-(10x)^{2}$\\newline \n'
                '$\\text{K}=1-100x^{2}$\\newline \n')


def test_expL_auto_er(expL):
    """Is this Expression correctly expanded and reduced?"""
    assert expL.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{L}=-2-x+8x^{2}+x$\\newline \n'
                '$\\text{L}=-2+(-1+1)x+8x^{2}$\\newline \n'
                '$\\text{L}=-2+0x+8x^{2}$\\newline \n'
                '$\\text{L}=-2+8x^{2}$\\newline \n')


def test_expM_auto_er(expM):
    """Is this Expression correctly expanded and reduced?"""
    assert expM.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{M}=-15+(10+14x-10x^{2})$\\newline \n'
                '$\\text{M}=-15+10+14x-10x^{2}$\\newline \n'
                '$\\text{M}=-5+14x-10x^{2}$\\newline \n')


def test_expN_auto_er(expN):
    """Is this Expression correctly expanded and reduced?"""
    assert expN.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{N}=-(2x+9)(-3x-7)+4(-3x+9)+13$\\newline \n'
                '$\\text{N}=-(2x\\times (-3x)+2x\\times (-7)+9\\times '
                '(-3x)+9\\times (-7))+4\\times (-3x)+4\\times 9'
                '+13$\\newline \n'
                '$\\text{N}=-(-6x^{2}-14x-27x-63)-12x+36+13$\\newline \n'
                '$\\text{N}=6x^{2}+14x+27x+63-12x+49$\\newline \n'
                '$\\text{N}=6x^{2}+(14+27-12)x+63+49$\\newline \n'
                '$\\text{N}=6x^{2}+29x+112$\\newline \n')


def test_expP_auto_er(expP):
    """Is this Expression correctly expanded and reduced?"""
    assert expP.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{P}=7(-6x+6)+(-10x-3)^{2}$\\newline \n'
                '$\\text{P}=7\\times (-6x)+7\\times 6+(-10x)^{2}-2'
                '\\times (-10x)\\times 3+3^{2}$\\newline \n'
                '$\\text{P}=-42x+42+100x^{2}+60x+9$\\newline \n'
                '$\\text{P}=(-42+60)x+42+9+100x^{2}$\\newline \n'
                '$\\text{P}=18x+51+100x^{2}$\\newline \n')


def test_expQ_auto_er():
    """No redundant lines in expansion and reduction of 9-(0.4+0.4)×5?"""
    temp = Sum([9, Product([Expandable((Item(-1),
                                        Sum([Decimal('0.4'),
                                             Decimal('0.4')]))),
                            Item(5)], compact_display=False)])
    expQ = Expression("Q", temp)
    assert expQ.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{Q}=9-(0.4+0.4)\\times 5$\\newline \n'
                '$\\text{Q}=9-0.8\\times 5$\\newline \n'
                '$\\text{Q}=9-4$\\newline \n'
                '$\\text{Q}=5$\\newline \n')


def test_expR_auto_er():
    """No extraneous parentheses or lines in exp. and red. of 2+(7.5-6.7)×6?"""
    temp = Sum([Item(2), Product([Expandable((Item(1),
                                              Sum([Decimal('7.5'),
                                                   -Decimal('6.7')]))),
                                  Item(6)], compact_display=False)])
    expR = Expression("R", temp)
    assert expR.auto_expansion_and_reduction() == \
        wrap_nb('$\\text{R}=2+(7.5-6.7)\\times 6$\\newline \n'
                '$\\text{R}=2+0.8\\times 6$\\newline \n'
                '$\\text{R}=2+4.8$\\newline \n'
                '$\\text{R}=6.8$\\newline \n')
