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

from mathmaker.lib.document.content.calculation import subtr_hole
from tests.tools import wrap_nb


def test_subtr_hole():
    """Check all normal cases are correctly handled."""
    o = subtr_hole.sub_object(build_data=[5, 7], hidden=1)
    assert '?' in o.nb1.printed
    o = subtr_hole.sub_object(build_data=[5, 7], hidden=2)
    assert '?' in o.nb2.printed
    o = subtr_hole.sub_object(build_data=[21, 71])
    assert o.transduration == 12
    o = subtr_hole.sub_object(build_data=[21, 70])
    assert o.transduration == 16
    o = subtr_hole.sub_object(build_data=[10, 2],
                              nb_source='complements_to_10',
                              swap_complement=False,
                              subvariant='only_positive')
    assert o.result == wrap_nb('8')
    o = subtr_hole.sub_object(build_data=[10, 2],
                              nb_source='complements_to_10',
                              swap_complement=True,
                              subvariant='only_positive')
    assert o.result == wrap_nb('2')
