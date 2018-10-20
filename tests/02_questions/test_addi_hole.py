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

# import pytest

from mathmakerlib.calculus.number import is_number, is_integer

from mathmaker.lib.document.content.calculation import addi_hole
from tests.tools import wrap_nb


def test_addi_hole():
    """Check all normal cases are correctly handled."""
    o = addi_hole.sub_object(build_data=[10, 2],
                             nb_source='complements_to_10')
    assert o.result == wrap_nb('10')
    o = addi_hole.sub_object(build_data=[21, 21])
    assert o.transduration == 16
    o = addi_hole.sub_object(build_data=[5, 7], hidden=1)
    assert '?' in o.nb1.printed
    o = addi_hole.sub_object(build_data=[5, 7], hidden=2)
    assert '?' in o.nb2.printed
    o = addi_hole.sub_object(build_data=[10, 20], nb_variant='decimal1')
    assert ((is_number(o.nb1) and not is_integer(o.nb1))
            or (is_number(o.nb2) and not is_integer(o.nb2))
            or (is_number(o.result_nb) and not is_integer(o.result_nb)))
