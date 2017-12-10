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
# from decimal import Decimal

from mathmaker.lib.document.content.calculation import subtr_direct


def test_subtr_direct_exceptions():
    """Check a wrong context raises an exception."""
    with pytest.raises(ValueError) as excinfo:
        subtr_direct.sub_object(build_data=[10, 2],
                                context='complement_wordingnuts1')
    assert str(excinfo.value).startswith('Cannot recognize context: ')


def test_subtr_direct():
    """Check all normal cases are correctly handled."""
    o = subtr_direct.sub_object(build_data=[10, 2],
                                context='complement_wording')
    assert o.context in ['complement_wording1', 'complement_wording2']
