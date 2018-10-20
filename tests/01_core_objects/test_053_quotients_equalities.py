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
import math

from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.core.base_calculus import Item, Function  # , AngleItem
from mathmaker.lib.core.base_geometry import Point, Angle
from mathmaker.lib.core.calculus import QuotientsEquality
# from tests.tools import wrap_nb


@pytest.fixture()
def ABC(): return Angle((Point('A', 1, 0),
                         Point('B', 0, 0),
                         Point('C', 0.5, 0.75)))


@pytest.fixture()
def cos_ABC(ABC): return Function(name='cos',
                                  var=ABC,
                                  fct=lambda x: math.cos(math.radians(x)),
                                  inv_fct=lambda x: math.degrees(
                                      math.acos(x)))


@pytest.fixture
def qe0():
    return QuotientsEquality([[cos_ABC(ABC()), Item('BC')],
                              [Item((1)), Item('BA')]],
                             subst_dict={Value('BC'): Value(10),
                                         Value('BA'): Value(15)})


def test_qe0_autoresolution0(qe0, ABC):
    """Is this Quotients' Equality correctly auto-resolved?"""
    assert qe0.auto_resolution(dont_display_equations_name=True,
                               skip_fraction_simplification=True,
                               decimal_result=0,
                               unit='\\textdegree') == \
        '\[cos(\widehat{\\text{ABC}})=\\frac{\\text{BC}}{\\text{BA}}\]'\
        '\[cos(\widehat{\\text{ABC}})=\\frac{\\text{10}}{\\text{15}}\]'\
        '\[\widehat{\\text{ABC}}\simeq\\text{48}\\text{ \\textdegree}\]'
