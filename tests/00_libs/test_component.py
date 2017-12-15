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
from mathmaker.lib.document.content import component


def test_setup_exceptions():
    """Check if exceptions are raised with an incorrect setup argument."""
    o = component.structure()
    with pytest.raises(TypeError) as excinfo:
        o.setup(8)
    assert str(excinfo.value) == 'arg must be a str'
    with pytest.raises(ValueError) as excinfo:
        o.setup('inexistent_module')
    assert str(excinfo.value) == 'There is no private method '\
        '_setup_inexistent_module() to handle setup of \'inexistent_module\'.'
