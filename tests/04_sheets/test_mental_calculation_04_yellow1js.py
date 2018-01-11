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


def test_04_yellow1_fraction_of_a_linesegment():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'fraction_of_a_linesegment',
                                       enable_js_form=True)))


def test_04_yellow1_percentages():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'percentages',
                                       enable_js_form=True)))


def test_04_yellow1_multi_hole():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'multi_hole',
                                       enable_js_form=True)))


def test_04_yellow1_addi_subtr_hole():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'addi_subtr_hole',
                                       enable_js_form=True)))


def test_04_yellow1_euclidean_divisions():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'euclidean_divisions',
                                       enable_js_form=True)))


def test_04_yellow1_rectangles():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'rectangles',
                                       enable_js_form=True)))


def test_04_yellow1_perimeter_of_a_polygon():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'perimeter_of_a_polygon',
                                       enable_js_form=True)))


def test_04_yellow1_multi_divi_10_100_1000():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'multi_divi_10_100_1000',
                                       enable_js_form=True)))


def test_04_yellow1_multi_clever():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'multi_clever',
                                       enable_js_form=True)))


def test_04_yellow1_multi_decimal():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'multi_decimal',
                                       enable_js_form=True)))


def test_04_yellow1_proportionality_problems():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'proportionality_problems',
                                       enable_js_form=True)))


def test_04_yellow1_exam():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'exam',
                                       enable_js_form=True)))


def test_04_yellow1_challenge():
    """Check this sheet is generated without any error."""
    shared.machine.write_out(str(Sheet('mental_calculation',
                                       '04_yellow1',
                                       'challenge',
                                       enable_js_form=True)))
