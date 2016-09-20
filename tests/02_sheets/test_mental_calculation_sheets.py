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


def test_tables2_9():
    """Checks if 'table_2_9' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['tables2_9'])))


def test_divisions():
    """Checks if 'divisions' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['divisions'])))


def test_mini_problems():
    """Checks if 'mini_problems' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['mini_problems'])))


def test_multi_11_15_25():
    """Checks if 'multi_11_15_25' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['multi_11_15_25'])))


def test_multi_decimal():
    """Checks if 'multi_decimal' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['multi_decimal'])))


def test_multi_divi_10_100_1000():
    """Checks if 'multi_divi_10_100_1000' is generated without any error."""
    shared.machine.write_out(
        str(S_Generic(XML_SHEETS['multi_divi_10_100_1000'])))


def test_multi_hole_any_nb():
    """Checks if 'multi_hole_any_nb' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['multi_hole_any_nb'])))


def test_multi_hole_tables2_9():
    """Checks if 'multi_hole_tables2_9' is generated without any error."""
    shared.machine.write_out(
        str(S_Generic(XML_SHEETS['multi_hole_tables2_9'])))


def test_multi_reversed():
    """Checks if 'multi_reversed' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['multi_reversed'])))


def test_operations_vocabulary():
    """Checks if 'operations_vocabulary' is generated without any error."""
    shared.machine.write_out(
        str(S_Generic(XML_SHEETS['operations_vocabulary'])))


def test_ranks():
    """Checks if 'ranks' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['ranks'])))


def test_rectangles():
    """Checks if 'rectangles' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['rectangles'])))


def test_test_11_1():
    """Checks if 'test_11_1' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['test_11_1'])))


def test_test_11_2():
    """Checks if 'test_11_2' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['test_11_2'])))


def test_test_multi_clever():
    """Checks if 'multi_clever' is generated without any error."""
    shared.machine.write_out(str(S_Generic(XML_SHEETS['multi_clever'])))
