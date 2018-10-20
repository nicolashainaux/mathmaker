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

from mathmaker.lib.core.base_calculus import (Item, Monomial, Sum, Fraction,
                                              SquareRoot, Function)
from mathmaker.lib.core.base_calculus import Expandable
from mathmaker.lib.core.base_calculus import Polynomial
from mathmaker.lib.core.calculus import Equation
from tests.tools import wrap_nb


@pytest.fixture
def eq24():
    return Equation((Monomial(('+', 1, 1)),
                     Sum([Item(('+', 4, 2)), Item(('+', 5, 2))])),
                    number=1)


@pytest.fixture
def eq30():
    return Equation((Item("AB"), Sum([Item(('+', 3, 2)), Item(('+', 4, 2))])),
                    number=1, variable_letter_name="AB")


@pytest.fixture
def eq33():
    return Equation((Monomial(('+', 1, 2)), (Item(16))))


@pytest.fixture
def eq34():
    return Equation((Monomial(('+', 1, 2)), (Item(5))))


@pytest.fixture
def eq40():
    return Equation((Item(2), Item(2)), number=1)


@pytest.fixture
def eq41():
    f_1 = Function()
    f_1.set_numeric_mode()
    return Equation((Item('CU'), f_1))


@pytest.fixture
def eq42():
    return Equation((Monomial(('+', 4, 1)),
                     Fraction(('+', Item(11), Item(60)))), number=1)


def test_eq0_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Polynomial([Monomial(('+', 1, 1)), Monomial(('+', 7, 0))]),
                   Item(3)),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[x+7=3\]'
                                           '\[x=3-7\]'
                                           '\[x=-4\]')


def test_eq1_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Polynomial([Monomial(('-', 8, 0)),
                               Monomial(('+', 1, 1))]),
                   Item(-2)),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[-8+x=-2\]'
                                           '\[x=-2+8\]'
                                           '\[x=6\]')


def test_eq2_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Item(-5),
                   Polynomial([Monomial(('+', 1, 1)), Monomial(('+', 3, 0))])),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[-5=x+3\]'
                                           '\[x=-5-3\]'
                                           '\[x=-8\]')


def test_eq3_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Item(-6), Monomial(('+', 5, 1))), number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[-6=5x\]'
                                           '\[x=-\\frac{6}{5}\]')


def test_eq4_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Monomial(('+', 8, 1)), Item(1)), number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[8x=1\]'
                                           '\[x=\\frac{1}{8}\]')


def test_eq5_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Monomial(('+', 12, 1)), Item(8)), number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[12x=8\]'
                                           '\[x=\\frac{8}{12}\]'
                                           '\[x=\\frac{\\bcancel{4}\\times 2}'
                                           '{\\bcancel{4}\\times 3}\]'
                                           '\[x=\\frac{2}{3}\]')


def test_eq6_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Polynomial([Monomial(('+', 2, 1)), Monomial(('+', 3, 0))]),
                   Item(8)),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[2x+3=8\]'
                                           '\[2x=8-3\]'
                                           '\[2x=5\]'
                                           '\[x=\\frac{5}{2}\]')


def test_eq7_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Polynomial([Monomial(('+', 19, 0)), Monomial(('+', 3, 1))]),
                   Monomial(('+', 2, 1))),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[19+3x=2x\]'
                                           '\[3x-2x=-19\]'
                                           '\[(3-2)x=-19\]'
                                           '\[x=-19\]')


def test_eq8_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Polynomial([Monomial(('+', 4, 1)), Monomial(('+', 2, 0))]),
                   Polynomial([Monomial(('-', 3, 0)), Monomial(('+', 2, 1))])),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[4x+2=-3+2x\]'
                                           '\[4x-2x=-3-2\]'
                                           '\[(4-2)x=-5\]'
                                           '\[2x=-5\]'
                                           '\[x=-\\frac{5}{2}\]')


def test_eq9_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Polynomial([Monomial(('-', 2, 1)), Monomial(('+', 5, 0))]),
                   Polynomial([Monomial(('+', 3, 1)), Monomial(('-', 4, 0))])),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[-2x+5=3x-4\]'
                                           '\[-2x-3x=-4-5\]'
                                           '\[(-2-3)x=-9\]'
                                           '\[-5x=-9\]'
                                           '\[x=\\frac{-9}{-5}\]'
                                           '\[x=\\frac{9}{5}\]')


def test_eq10_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Polynomial([Monomial(('+', 5, 0)), Monomial(('+', 4, 1))]),
                   Polynomial([Monomial(('-', 20, 1)),
                               Monomial(('+', 3, 0))])),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[5+4x=-20x+3\]'
                                           '\[4x+20x=3-5\]'
                                           '\[(4+20)x=-2\]'
                                           '\[24x=-2\]'
                                           '\[x=-\\frac{2}{24}\]'
                                           '\[x=-\\frac{\\bcancel{2}}'
                                           '{\\bcancel{2}\\times 12}\]'
                                           '\[x=-\\frac{1}{12}\]')


def test_eq11_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Polynomial([Monomial(('+', 5, 0)), Monomial(('-', 1, 1))]),
                   Polynomial([Monomial(('+', 5, 1))])),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[5-x=5x\]'
                                           '\[-x-5x=-5\]'
                                           '\[(-1-5)x=-5\]'
                                           '\[-6x=-5\]'
                                           '\[x=\\frac{-5}{-6}\]'
                                           '\[x=\\frac{5}{6}\]')


def test_eq12_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Polynomial([Monomial(('+', 2, 1)), Monomial(('+', 1, 0))]),
                   Item(1)),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[2x+1=1\]'
                                           '\[2x=1-1\]'
                                           '\[2x=0\]'
                                           '\[x=0\]')


def test_eq13_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Polynomial([Monomial(('+', 1, 1)), Monomial(('+', 5, 0))]),
                   Polynomial([Monomial(('+', 1, 1)), Monomial(('+', 2, 0))])),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[x+5=x+2\]'
                                           '\[x-x=2-5\]'
                                           '\[(1-1)x=-3\]'
                                           '\[0x=-3\]'
                                           '\[0=-3\]'
                                           'This equation has no solution.'
                                           '\\newline ')


def test_eq14_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Sum([Monomial(('+', 3, 0)), Monomial(('+', 10, 1))]),
                   Monomial(('+', 10, 1))))
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}): $'
                                           '\[3+10x=10x\]'
                                           '\[10x-10x=-3\]'
                                           '\[(10-10)x=-3\]'
                                           '\[0x=-3\]'
                                           '\[0=-3\]'
                                           'This equation has no solution.'
                                           '\\newline ')


def test_eq15_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Item(1), Item(2)), number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[1=2\]'
                                           'This equation has no solution.'
                                           '\\newline ')


def test_eq16_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Sum([Monomial(('+', 9, 1)),
                        Expandable((Monomial(('+', 9, 0)),
                                    Sum([Monomial(('-', 4, 0)),
                                         Monomial(('-', 1, 1))])))]),
                   Item(8)),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[9x+9(-4-x)=8\]'
                                           '\[9x+9\\times (-4)+9\\times '
                                           '(-x)=8\]'
                                           '\[9x-36-9x=8\]'
                                           '\[(9-9)x-36=8\]'
                                           '\[0x-36=8\]'
                                           '\[-36=8\]'
                                           'This equation has no solution.'
                                           '\\newline ')


def test_eq17_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Expandable((Item(-1),
                               Sum([Monomial((-11, 1)), Item(-10)]))),
                   Sum([Expandable((Item(1),
                                    Sum([Item(-15), Monomial((12, 1))]))),
                        Item(-1)])),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[-(-11x-10)=(-15+12x)-1\]'
                                           '\[11x+10=-15+12x-1\]'
                                           '\[11x+10=-15-1+12x\]'
                                           '\[11x+10=-16+12x\]'
                                           '\[11x-12x=-16-10\]'
                                           '\[(11-12)x=-26\]'
                                           '\[-x=-26\]'
                                           '\[x=26\]')


def test_eq18_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Sum([Monomial(('-', 8, 0)),
                        Monomial(('+', 9, 0)),
                        Monomial(('-', 1, 0))]),
                   Expandable((Item(10),
                               Sum([Item(-2), Monomial((-12, 1))])))),
                  number=1)
    assert eq.auto_resolution() == \
        wrap_nb('$(\\text{E}_{1}): $'
                '\[-8+9-1=10(-2-12x)\]'
                '\[0=10\\times (-2)+10\\times (-12x)\]'
                '\[0=-20-120x\]'
                '\[120x=-20\]'
                '\[x=-\\frac{20}{120}\]'
                '\[x=-\\frac{\\bcancel{10}\\times'
                ' 2}{\\bcancel{10}\\times 12}\]'
                '\[x=-\\frac{\\bcancel{2}}'
                '{\\bcancel{2}\\times 6}\]'
                '\[x=-\\frac{1}{6}\]')


def test_eq19_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Sum([Monomial(('-', 1, 1)),
                        Monomial(('-', 2, 1)),
                        Monomial(('+', 7, 0))]),
                   Expandable((Item(1), Sum([Monomial(('+', 7, 1)),
                                             Monomial(('+', 5, 0))])))),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[-x-2x+7=(7x+5)\]'
                                           '\[(-1-2)x+7=7x+5\]'
                                           '\[-3x+7=7x+5\]'
                                           '\[-3x-7x=5-7\]'
                                           '\[(-3-7)x=-2\]'
                                           '\[-10x=-2\]'
                                           '\[x=\\frac{-2}{-10}\]'
                                           '\[x=\\frac{+\\bcancel{2}}'
                                           '{+\\bcancel{2}\\times 5}\]'
                                           '\[x=\\frac{1}{5}\]')


def test_eq20_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Sum([Monomial(('+', 5, 1))]),
                   Sum([Expandable((Item(1), Sum([Monomial(('+', 2, 0)),
                                                  Monomial(('-', 5, 1))]))),
                        Monomial(('-', 2, 0))])),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[5x=(2-5x)-2\]'
                                           '\[5x=2-5x-2\]'
                                           '\[5x=2-2-5x\]'
                                           '\[5x=-5x\]'
                                           '\[5x+5x=0\]'
                                           '\[(5+5)x=0\]'
                                           '\[10x=0\]'
                                           '\[x=0\]')


def test_eq21_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Sum([Monomial(('-', 1, 0)),
                        Monomial(('-', 4, 1))]),
                   Monomial(('-', 9, 0))))
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}): $'
                                           '\[-1-4x=-9\]'
                                           '\[-4x=-9+1\]'
                                           '\[-4x=-8\]'
                                           '\[x=\\frac{-8}{-4}\]'
                                           '\[x=\\frac{+\\bcancel{4}\\times 2}'
                                           '{+\\bcancel{4}}\]'
                                           '\[x=2\]')


def test_eq22_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Sum([Expandable((Item(3),
                                    Sum([Monomial(('-', 9, 0)),
                                         Monomial(('+', 6, 1))]))),
                        Item(-8)]),
                   Sum([Item(9)])),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[3(-9+6x)-8=9\]'
                                           '\[3\\times (-9)+3\\times 6x-8=9\]'
                                           '\[-27+18x-8=9\]'
                                           '\[-27-8+18x=9\]'
                                           '\[-35+18x=9\]'
                                           '\[18x=9+35\]'
                                           '\[18x=44\]'
                                           '\[x=\\frac{44}{18}\]'
                                           '\[x=\\frac{\\bcancel{2}\\times 22}'
                                           '{\\bcancel{2}\\times 9}\]'
                                           '\[x=\\frac{22}{9}\]')


def test_eq23_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Item(5), Sum([Expandable((Item(1),
                                             Sum([Monomial(('+', 1, 1)),
                                                  Monomial(('-', 2, 0))]))),
                                 Item(7)])),
                  number=1)
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[5=(x-2)+7\]'
                                           '\[5=x-2+7\]'
                                           '\[5=x+5\]'
                                           '\[x=5-5\]'
                                           '\[x=0\]')


def test_eq24_autoresolution(eq24):
    """Is this Equation correctly auto-resolved?"""
    eq = eq24
    assert eq.auto_resolution() == wrap_nb('$(\\text{E}_{1}): $'
                                           '\[x=4^{2}+5^{2}\]'
                                           '\[x=16+25\]'
                                           '\[x=41\]')


def test_eq24_autoresolution_bis(eq24):
    """Is this Equation correctly auto-resolved?"""
    eq = eq24
    assert eq.auto_resolution(decimal_result=2) == \
        wrap_nb('$(\\text{E}_{1}): $'
                '\[x=4^{2}+5^{2}\]'
                '\[x=16+25\]'
                '\[x=41\]')


def test_eq25_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Item(('+', 5, 2)),
                   Sum([Item(('+', 4, 2)), Monomial(('+', 1, 1))])),
                  number=1)
    assert eq.auto_resolution(dont_display_equations_name=True) == \
        wrap_nb('\[5^{2}=4^{2}+x\]'
                '\[25=16+x\]'
                '\[x=25-16\]'
                '\[x=9\]')


def test_eq26_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Monomial(('+', 2, 1)), Item(1)), number=1)
    assert eq.auto_resolution(decimal_result=2) == \
        wrap_nb('$(\\text{E}_{1}): $'
                '\[2x=1\]'
                '\[x=\\frac{1}{2}\]'
                '\[x=0.5\]')


def test_eq27_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Monomial(('+', 3, 1)), Item(1)), number=1)
    assert eq.auto_resolution(decimal_result=2) == \
        wrap_nb('$(\\text{E}_{1}): $'
                '\[3x=1\]'
                '\[x=\\frac{1}{3}\]'
                '\[x\\simeq0.33\]')


def test_eq28_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Monomial(('+', 8, 1)), Item(6)), number=1)
    assert eq.auto_resolution(decimal_result=2) == \
        wrap_nb('$(\\text{E}_{1}): $'
                '\[8x=6\]'
                '\[x=\\frac{6}{8}\]'
                '\[x=0.75\]')


def test_eq29_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Monomial(('+', 1, 1)), Sum([Fraction((Item(1), Item(4))),
                                               Fraction((Item(1), Item(8)))])),
                  number=1)
    assert eq.auto_resolution(decimal_result=2) == \
        wrap_nb('$(\\text{E}_{1}): $'
                '\[x=\\frac{1}{4}+\\frac{1}{8}\]'
                '\[x=\\frac{1\\times 2}{4\\times 2}'
                '+\\frac{1}{8}\]'
                '\[x=\\frac{2}{8}+\\frac{1}{8}\]'
                '\[x=\\frac{2+1}{8}\]'
                '\[x=\\frac{3}{8}\]'
                '\[x\\simeq0.38\]')


def test_eq30_autoresolution(eq30):
    """Is this Equation correctly auto-resolved?"""
    eq = eq30
    assert eq.auto_resolution(dont_display_equations_name=True,
                              decimal_result=0) == \
        wrap_nb('\[\\text{AB}=3^{2}+4^{2}\]'
                '\[\\text{AB}=9+16\]'
                '\[\\text{AB}=25\]')


def test_eq30_autoresolution_bis(eq30):
    """Is this Equation correctly auto-resolved?"""
    eq = eq30
    assert eq.auto_resolution(dont_display_equations_name=True,
                              decimal_result=1) == \
        wrap_nb('\[\\text{AB}=3^{2}+4^{2}\]'
                '\[\\text{AB}=9+16\]'
                '\[\\text{AB}=25\]')


def test_eq31_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Monomial(('+', 1, 1)), SquareRoot(Item(5))))
    assert eq.auto_resolution(dont_display_equations_name=True,
                              decimal_result=2) == \
        wrap_nb('\[x=\\sqrt{\mathstrut 5}\]'
                '\[x\\simeq2.24\]')


def test_eq32_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Monomial(('+', 1, 1)), SquareRoot(Item(16))))
    assert eq.auto_resolution(dont_display_equations_name=True,
                              decimal_result=2) == \
        wrap_nb('\[x=\\sqrt{\mathstrut 16}\]'
                '\[x=4\]')


def test_eq33_autoresolution(eq33):
    """Is this Equation correctly auto-resolved?"""
    eq = eq33
    assert eq.auto_resolution(dont_display_equations_name=True,
                              decimal_result=2) == \
        wrap_nb('\[x^{2}=16\]'
                '\[x=\\sqrt{\mathstrut 16} '
                'or x=-\\sqrt{\mathstrut 16}\]'
                '\[x=4 or x=-4\]')


def test_eq33_autoresolution_bis(eq33):
    """Is this Equation correctly auto-resolved?"""
    eq = eq33
    assert eq.auto_resolution(dont_display_equations_name=True) == \
        wrap_nb('\[x^{2}=16\]'
                '\[x=\\sqrt{\mathstrut 16} '
                'or x=-\\sqrt{\mathstrut 16}\]'
                '\[x=4 or x=-4\]')


def test_eq34_autoresolution(eq34):
    """Is this Equation correctly auto-resolved?"""
    eq = eq34
    assert eq.auto_resolution(dont_display_equations_name=True) == \
        wrap_nb('\[x^{2}=5\]'
                '\[x=\\sqrt{\mathstrut 5} '
                'or x=-\\sqrt{\mathstrut 5}\]')


def test_eq34_autoresolution_bis(eq34):
    """Is this Equation correctly auto-resolved?"""
    eq = eq34
    assert eq.auto_resolution(dont_display_equations_name=True,
                              decimal_result=2) == \
        wrap_nb('\[x^{2}=5\]'
                '\[x=\\sqrt{\mathstrut 5} '
                'or x=-\\sqrt{\mathstrut 5}\]'
                '\[x\\simeq2.24 or x\\simeq-2.24\]')


def test_eq34_autoresolution_ter(eq34):
    """Is this Equation correctly auto-resolved?"""
    eq = eq34
    assert eq.auto_resolution(dont_display_equations_name=True,
                              decimal_result=2,
                              pythagorean_mode=True) == \
        wrap_nb('\[x^{2}=5\]'
                '\[x=\\sqrt{\mathstrut 5}'
                '\\text{ because x is positive.}\]'
                '\[x\\simeq2.24\]')


def test_eq35_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Item(('+', 73, 2)),
                   Sum([Item(('+', 48, 2)), Item(('+', "AB", 2))])),
                  number=1, variable_letter_name="AB")
    assert eq.auto_resolution(dont_display_equations_name=True,
                              decimal_result=2,
                              pythagorean_mode=True) == \
        wrap_nb('\[73^{2}=48^{2}+\\text{AB}^{2}\]'
                '\[5329=2304+\\text{AB}^{2}\]'
                '\[\\text{AB}^{2}=5329-2304\]'
                '\[\\text{AB}^{2}=3025\]'
                '\[\\text{AB}='
                '\\sqrt{\mathstrut 3025}'
                '\\text{ because \\text{AB} '
                'is positive.}\]'
                '\[\\text{AB}=55\]')


def test_eq36_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Item(('+', "EF", 2)),
                   Sum([Item(('+', 60, 2)), Item(('+', 91, 2))])),
                  number=1, variable_letter_name="AB")
    assert eq.auto_resolution(dont_display_equations_name=True,
                              pythagorean_mode=True,
                              unit='cm') == \
        wrap_nb('\[\\text{EF}^{2}=60^{2}+91^{2}\]'
                '\[\\text{EF}^{2}=3600+8281\]'
                '\[\\text{EF}^{2}=11881\]'
                '\[\\text{EF}='
                '\\sqrt{\mathstrut 11881}'
                '\\text{ because \\text{EF} '
                'is positive.}\]'
                '\[\\text{EF}=109\\text{ cm}\]')


def test_eq37_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Monomial((Fraction((Item(2), Item(3))), 1)),
                   Fraction((Item(4), Item(5)))))
    assert eq.auto_resolution(dont_display_equations_name=True) == \
        wrap_nb('\[\\frac{2}{3}x=\\frac{4}{5}\]'
                '\[x=\\frac{4}{5}\div \\frac{2}{3}\]'
                '\[x=\\frac{4}{5}\\times \\frac{3}{2}\]'
                '\[x=\\frac{4\\times 3}{5\\times 2}\]'
                '\[x=\\frac{\\bcancel{2}\\times 2\\times 3}'
                '{5\\times \\bcancel{2}}\]'
                '\[x=\\frac{6}{5}\]')


def test_eq38_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Sum([Monomial((Fraction((Item(1), Item(4))), 1)),
                        Fraction((Item(1), Item(7)))]),
                   Fraction(('-', Item(3), Item(14)))))
    assert eq.auto_resolution(dont_display_equations_name=True) == \
        wrap_nb('\[\\frac{1}{4}x+\\frac{1}{7}=-\\frac{3}{14}\]'
                '\[\\frac{1}{4}x=-\\frac{3}{14}-\\frac{1}{7}\]'
                '\[\\frac{1}{4}x=-\\frac{3}{14}-\\frac{1\\times 2}'
                '{7\\times 2}\]'
                '\[\\frac{1}{4}x=-\\frac{3}{14}-\\frac{2}{14}\]'
                '\[\\frac{1}{4}x=\\frac{-3-2}{14}\]'
                '\[\\frac{1}{4}x=-\\frac{5}{14}\]'
                '\[x=-\\frac{5}{14}\div \\frac{1}{4}\]'
                '\[x=-\\frac{5}{14}\\times \\frac{4}{1}\]'
                '\[x=-\\frac{5\\times 4}{14\\times 1}\]'
                '\[x=-\\frac{5\\times \\bcancel{2}\\times 2}'
                '{\\bcancel{2}\\times 7}\]'
                '\[x=-\\frac{10}{7}\]')


def test_eq39_autoresolution():
    """Is this Equation correctly auto-resolved?"""
    eq = Equation((Sum([Monomial((Fraction((Item(2),
                                            Item(1))).simplified(), 1)),
                        Fraction((Item(1), Item(5)))]),
                   Fraction(('-', Item(4), Item(5)))))
    assert eq.auto_resolution(dont_display_equations_name=True) == \
        wrap_nb('\[2x+\\frac{1}{5}=-\\frac{4}{5}\]'
                '\[2x=-\\frac{4}{5}-\\frac{1}{5}\]'
                '\[2x=\\frac{-4-1}{5}\]'
                '\[2x=-\\frac{5}{5}\]'
                '\[2x=-\\frac{\\bcancel{5}}{\\bcancel{5}}\]'
                '\[2x=-1\]'
                '\[x=-\\frac{1}{2}\]')


def test_eq40_printed(eq40):
    """Is this Equation correctly printed?"""
    assert eq40.printed == wrap_nb('2=2')


def test_eq40_nextstep(eq40):
    """Is this Equation's next step correct?"""
    assert eq40.solve_next_step() == \
        wrap_nb('Any value of {x} is solution of the equation.'
                .format(x=eq40.variable_letter))


def test_eq41_autoresolution(eq41):
    """Is this Equation correctly auto-resolved?"""
    assert eq41.auto_resolution(dont_display_equations_name=True,
                                decimal_result=2) == \
        wrap_nb('\[\\text{CU}=f(1)\]'
                '\[\\text{CU}=1\]')


def test_eq42_autoresolution(eq42):
    """Is 4x = 11/60 correctly auto-resolved?"""
    assert eq42.auto_resolution(dont_display_equations_name=True) == wrap_nb(
        '\[4x=\\frac{11}{60}\]'
        '\[x=\\frac{11}{60}\div 4\]'
        '\[x=\\frac{11}{60}\\times \\frac{1}{4}\]'
        '\[x=\\frac{11\\times 1}{60\\times 4}\]'
        '\[x=\\frac{11}{240}\]')


def test_eq42_autoresolution2(eq42):
    """Is 4x = 11/60 correctly auto-resolved?"""
    assert eq42.auto_resolution(dont_display_equations_name=True,
                                details_level='medium') == wrap_nb(
        '\[4x=\\frac{11}{60}\]'
        '\[x=\\frac{11}{60}\div 4\]'
        '\[x=\\frac{11}{60\\times 4}\]'
        '\[x=\\frac{11}{240}\]')


def test_eq42_autoresolution3(eq42):
    """Is 4x = 11/60 correctly auto-resolved?"""
    assert eq42.auto_resolution(dont_display_equations_name=True,
                                details_level='none') == wrap_nb(
        '\[4x=\\frac{11}{60}\]'
        '\[x=\\frac{11}{60}\div 4\]'
        '\[x=\\frac{11}{240}\]')
