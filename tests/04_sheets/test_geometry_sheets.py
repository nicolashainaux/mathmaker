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
from mathmaker.lib.tools.xml import get_xml_sheets_paths
from mathmaker.lib.document.frames import Sheet

XML_SHEETS = get_xml_sheets_paths()


def test_intercept_theorem_triangles():
    """
    Checks if 'intercept_theorem_triangles' is generated without any error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['intercept_theorem_triangles'])),
        pdf_output=True)


def test_intercept_theorem_triangles_alt1():
    """
    Checks if 'intercept_theorem_triangles_alt1' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['intercept_theorem_triangles_alt1'])),
        pdf_output=True)


def test_intercept_theorem_triangles_alt2():
    """
    Checks if 'intercept_theorem_triangles_alt2' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['intercept_theorem_triangles_alt2'])),
        pdf_output=True)


def test_intercept_theorem_triangles_formulae():
    """
    Is 'intercept_theorem_triangles_formulae' generated with no error?
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['intercept_theorem_triangles_'
                                      'formulae'])),
        pdf_output=True)


def test_intercept_theorem_butterflies():
    """
    Checks if 'intercept_theorem_butterflies' is generated without any error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['intercept_theorem_butterflies'])),
        pdf_output=True)


def test_intercept_theorem_butterflies_alt1():
    """
    Checks if 'intercept_theorem_butterflies_alt1' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['intercept_theorem_butterflies_alt1'])),
        pdf_output=True)


def test_intercept_theorem_butterflies_alt2():
    """
    Checks if 'intercept_theorem_butterflies_alt2' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['intercept_theorem_butterflies_alt2'])),
        pdf_output=True)


def test_intercept_theorem_butterflies_formulae():
    """
    Is 'intercept_theorem_butterflies_formulae' generated with no error?
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['intercept_theorem_butterflies_'
                                      'formulae'])),
        pdf_output=True)


def test_intercept_theorem_converse():
    """
    Checks if 'intercept_theorem_converse' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['intercept_theorem_converse'])),
        pdf_output=True)


def test_intercept_theorem_converse_alt2():
    """
    Checks if 'intercept_theorem_converse_alt2' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['intercept_theorem_converse_alt2'])),
        pdf_output=True)


def test_trigonometry_cos_length():
    """
    Check if 'trigonometry_cos_length' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_cos_length'])),
        pdf_output=True)


def test_trigonometry_sin_length():
    """
    Check if 'trigonometry_sin_length' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_sin_length'])),
        pdf_output=True)


def test_trigonometry_tan_length():
    """
    Check if 'trigonometry_tan_length' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_tan_length'])),
        pdf_output=True)


def test_trigonometry_calculate_length():
    """
    Check if 'trigonometry_calculate_length' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_calculate_length'])),
        pdf_output=True)


def test_trigonometry_cos_angle():
    """
    Check if 'trigonometry_cos_angle' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_cos_angle'])),
        pdf_output=True)


def test_trigonometry_sin_angle():
    """
    Check if 'trigonometry_sin_angle' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_sin_angle'])),
        pdf_output=True)


def test_trigonometry_tan_angle():
    """
    Check if 'trigonometry_tan_angle' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_tan_angle'])),
        pdf_output=True)


def test_trigonometry_calculate_angle():
    """
    Check if 'trigonometry_calculate_angle' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_calculate_angle'])),
        pdf_output=True)


def test_trigonometry_cos_formulae():
    """
    Check if 'trigonometry_cos_formulae' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_cos_formulae'])),
        pdf_output=True)


def test_trigonometry_sin_formulae():
    """
    Check if 'trigonometry_sin_formulae' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_sin_formulae'])),
        pdf_output=True)


def test_trigonometry_tan_formulae():
    """
    Check if 'trigonometry_tan_formulae' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_tan_formulae'])),
        pdf_output=True)


def test_trigonometry_formulae():
    """
    Check if 'trigonometry_formulae' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_formulae'])),
        pdf_output=True)


def test_trigonometry_vocabulary():
    """
    Check if 'trigonometry_vocabulary' is generated with no error.
    """
    shared.machine.write_out(
        str(Sheet('', '', '',
                  filename=XML_SHEETS['trigonometry_vocabulary'])),
        pdf_output=True)
