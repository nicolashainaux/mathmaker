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


from mathmaker.lib import shared
from mathmaker.lib.document.frames import Sheet


def test_01_white1_multiplications():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'multiplications')))


def test_01_white1_positional_notation():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'positional_notation')))


def test_01_white1_exam():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'exam')))


def test_01_white1_W01a():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'W01a')))


def test_01_white1_W01b():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'W01b')))


def test_01_white1_W01c():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'W01c')))


def test_01_white1_W01d():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'W01d')))


def test_01_white1_W02a():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'W02a')))


def test_01_white1_W02b():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'W02b')))


def test_01_white1_W02c():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'W02c')))


def test_01_white1_W02d():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '01_white1',
                                       'W02d')))
