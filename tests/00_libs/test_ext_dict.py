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


from mathmaker.lib.tools.ext_dict import ext_dict


def test_recursive_update():
    """Checks recursive_update()"""
    d1 = ext_dict({'a': 1, 'b': 2,
                   'c': {'z': 26, 'y': 25, 'x': {1: 'a', 2: 'b'}}})
    d2 = ext_dict({'a': 11, 'c': {'y': 24, 'x': {2: 'f', 3: 'g'}, 'w': 23}})
    d1.recursive_update(d2)
    assert d1 == {'a': 11, 'b': 2,
                  'c': {'z': 26, 'y': 24, 'w': 23,
                        'x': {1: 'a', 2: 'f', 3: 'g'}}}


def test_flat():
    """Checks flat()"""
    d = ext_dict({'a': 1, 'b': 2,
                  'c': {'z': 26, 'y': 25, 'x': {1: 'a', 2: 64}}})
    assert d.flat() == {'a': 1, 'b': 2,
                        'c.z': 26, 'c.y': 25, 'c.x.1': 'a', 'c.x.2': 64}
