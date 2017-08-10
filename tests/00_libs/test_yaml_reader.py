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

# TODO: add yaml validation tests (per json schema?)

import pytest
from collections import OrderedDict

from ruamel.yaml.compat import ordereddict
from ruamel.yaml.comments import CommentedOrderedMap

from mathmaker.lib.tools.yaml_reader import load_sheet


def test_load_sheet_exceptions():
    """Test wrong theme, subtheme, sheet name do raise an exception."""
    with pytest.raises(IOError) as excinfo:
        load_sheet('dumbtheme', '', '')
    assert str(excinfo.value) == 'Could not find the provided theme ' \
        '(dumbtheme) among the frameworks.'
    with pytest.raises(IOError) as excinfo:
        load_sheet('algebra', 'dumbsubtheme', '')
    assert str(excinfo.value) == 'Could not find the provided subtheme ' \
        '(dumbsubtheme) in the provided theme (algebra).'
    with pytest.raises(ValueError) as excinfo:
        load_sheet('algebra', 'expand', 'dumbsheetname')
    assert str(excinfo.value) == 'No sheet of this name (dumbsheetname) in ' \
        'the provided theme and subtheme (algebra, expand).'


def test_load_sheet():
    """Test right theme, subtheme, sheet name return the right data."""
    d = load_sheet('algebra', 'expand', 'double')
    assert isinstance(d, OrderedDict)
    assert isinstance(d, ordereddict)
    assert isinstance(d, CommentedOrderedMap)
    assert d == ordereddict([
        ('title',
         'Algebra: expand and reduce double brackets'),
        ('answers_title', 'Answers'),
        ('exercise',
         ordereddict([('details_level', 'medium'),
                      ('text_exc',
                       'Expand and reduce the following '
                       'expressions:'),
                      ('text_ans',
                       'Example of detailed solutions:'),
                      ('questions',
                       'expand double -> intpairs_2to9;;intpairs_2to9 (5)')
                      ]))])
