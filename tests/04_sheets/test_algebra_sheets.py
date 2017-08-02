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


from mathmaker.lib import shared
from mathmaker.lib.tools.xml_sheet import get_xml_sheets_paths
from mathmaker.lib.sheet import S_Generic

XML_SHEETS = get_xml_sheets_paths()


def test_double_expansion():
    """Checks if 'double_expansion' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['double_expansion'])))


def test_double_expansion_detailed_solutions():
    """Checks generation of 'double_expansion_detailed_solutions'."""
    shared.machine.write_out(
        str(S_Generic(XML_SHEETS['double_expansion_detailed_solutions'])))


def test_simple_expansion():
    """Checks if 'simple_expansion' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['simple_expansion'])))


def test_simple_expansion_detailed_solutions():
    """Checks generation of 'simple_expansion_detailed_solutions'."""
    shared.machine.write_out(
        str(S_Generic(XML_SHEETS['simple_expansion_detailed_solutions'])))
