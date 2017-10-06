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


def test_02_white2_multiplications_hole():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '02_white2',
                                       'multiplications_hole',
                                       enable_js_form=True)))


def test_02_white2_multiplications_reversed():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '02_white2',
                                       'multiplications_reversed',
                                       enable_js_form=True)))


def test_02_white2_multiplications():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '02_white2',
                                       'multiplications',
                                       enable_js_form=True)))


def test_02_white2_addi_subtr():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '02_white2',
                                       'addi_subtr',
                                       enable_js_form=True)))


def test_02_white2_divisions():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '02_white2',
                                       'divisions',
                                       enable_js_form=True)))


def test_02_white2_fraction_of_a_rectangle():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '02_white2',
                                       'fraction_of_a_rectangle',
                                       enable_js_form=True)))


def test_02_white2_mini_problems():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '02_white2',
                                       'mini_problems',
                                       enable_js_form=True)))


def test_02_white2_multiplication_by_11():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '02_white2',
                                       'multiplication_by_11',
                                       enable_js_form=True)))


def test_02_white2_complements():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '02_white2',
                                       'complements',
                                       enable_js_form=True)))


def test_02_white2_exam():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '02_white2',
                                       'exam',
                                       enable_js_form=True)))
