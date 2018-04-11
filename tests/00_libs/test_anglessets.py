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

from mathmaker.lib.tools.generators.anglessets import AnglesSetGenerator


@pytest.fixture()
def AG(): return AnglesSetGenerator()


def test_AnglesSetGenerator(AG):
    """Check normal use cases."""
    AG.generate(codename='2_1', name='FLUOR',
                labels=[(1, 36), (2, 40)], variant=0)


def test_1_1(AG):
    """Check 1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        AG._1_1()
    assert str(excinfo.value) == 'variant must be 0 (not \'None\')'
    AG._1_1(variant=0, labels=[(1, 27), (1, 37)], name='FIVE',
            subvariant_nb=1)
    AG._1_1(variant=0, labels=[(1, 27), (1, 37)], name='FIVE',
            subvariant_nb=2)
    AG._1_1(variant=0, labels=[(1, 27), (1, 37)], name='FIVE',
            subvariant_nb=3)


def test_1_1r(AG):
    """Check 1_1r generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        AG._1_1r()
    assert str(excinfo.value) == 'variant must be 0 or 1 (not \'None\')'
    AG._1_1r(variant=0, labels=[(1, 27), (1, 90)], name='FIVE',
             subvariant_nb=1)
    AG._1_1r(variant=0, labels=[(1, 27), (1, 90)], name='FIVE',
             subvariant_nb=2)
    AG._1_1r(variant=0, labels=[(1, 27), (1, 90)], name='FIVE',
             subvariant_nb=3)
    AG._1_1r(variant=1, labels=[(1, 27), (1, 90)], name='FIVE',
             subvariant_nb=1)
    AG._1_1r(variant=1, labels=[(1, 27), (1, 90)], name='FIVE',
             subvariant_nb=2)
    AG._1_1r(variant=1, labels=[(1, 27), (1, 90)], name='FIVE',
             subvariant_nb=3)
    AG._1_1r(variant=1, labels=[(1, 27), (1, 90)], name='FIVE',
             subvariant_nb=1, subtr_shapes=True)
    AG._1_1r(variant=1, labels=[(1, 27), (1, 90)], name='FIVE',
             subvariant_nb=2, subtr_shapes=True)
    AG._1_1r(variant=1, labels=[(1, 27), (1, 90)], name='FIVE',
             subvariant_nb=3, subtr_shapes=True)


def test_2(AG):
    """Check 2 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        AG._2()
    assert str(excinfo.value) == 'variant must be 0 (not \'None\')'
    AG._2(variant=0, labels=[(2, 27)], name='FIVE', subvariant_nb=1)
    AG._2(variant=0, labels=[(2, 27)], name='FIVE', subvariant_nb=2)
    AG._2(variant=0, labels=[(2, 27)], name='FIVE', subvariant_nb=3)


def test_1_1_1(AG):
    """Check 1_1_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        AG._1_1_1()
    assert str(excinfo.value) == 'variant must be 0 (not \'None\')'
    AG._1_1_1(variant=0, labels=[(1, 27), (1, 37), (1, 46)], name='FLUOR',
              subvariant_nb=1)
    AG._1_1_1(variant=0, labels=[(1, 27), (1, 37), (1, 46)], name='FLUOR',
              subvariant_nb=2)
    AG._1_1_1(variant=0, labels=[(1, 27), (1, 37), (1, 46)], name='FLUOR',
              subvariant_nb=3)


def test_1_1_1r(AG):
    """Check 1_1_1r generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        AG._1_1_1r()
    assert str(excinfo.value) == "variant must be in [0, 1, 2] (found 'None')"
    AG._1_1_1r(variant=0, labels=[(1, 27), (1, 37), (1, 90)], name='FLUOR',
               subvariant_nb=1)
    AG._1_1_1r(variant=1, labels=[(1, 27), (1, 37), (1, 90)], name='FLUOR',
               subvariant_nb=1)
    AG._1_1_1r(variant=2, labels=[(1, 27), (1, 37), (1, 90)], name='FLUOR',
               subvariant_nb=1)


def test_2_1(AG):
    """Check 2_1 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        AG._2_1()
    assert str(excinfo.value) == "variant must be in [0, 1, 2] (found 'None')"
    AG._2_1(variant=0, labels=[(2, 27), (1, 37)], name='FLUOR',
            subvariant_nb=1)
    AG._2_1(variant=1, labels=[(2, 27), (1, 37)], name='FLUOR',
            subvariant_nb=1)
    AG._2_1(variant=2, labels=[(2, 27), (1, 37)], name='FLUOR',
            subvariant_nb=1)


def test_2_1r(AG):
    """Check 2_1r generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        AG._2_1r()
    assert str(excinfo.value) == "variant must be in [0, 1, 2] (found 'None')"
    AG._2_1r(variant=0, labels=[(2, 27), (1, 90)], name='FLUOR',
             subvariant_nb=1)
    AG._2_1r(variant=1, labels=[(2, 27), (1, 90)], name='FLUOR',
             subvariant_nb=1)
    AG._2_1r(variant=2, labels=[(2, 27), (1, 90)], name='FLUOR',
             subvariant_nb=1)


def test_3(AG):
    """Check 3 generation proceeds as expected."""
    with pytest.raises(ValueError) as excinfo:
        AG._3()
    assert str(excinfo.value) == 'variant must be 0 (not \'None\')'
    AG._3(variant=0, labels=[(3, 27)], name='FLOPS', subvariant_nb=1)
    AG._3(variant=0, labels=[(3, 27)], name='FLOPS', subvariant_nb=2)
    AG._3(variant=0, labels=[(3, 27)], name='FLOPS', subvariant_nb=3)
