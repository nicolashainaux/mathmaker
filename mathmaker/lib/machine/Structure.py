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

from mathmaker.lib import error


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Structure
# @brief Not instanciable mother class of all machine objects.
class Structure(object):

    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined. Constructor.
    #   @warning Will raise an exception if not redefined
    #   @param **options Any options
    def __init__(self, language):
        raise error.NotInstanciableObject(self)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns a deep copy of the object
    def clone(self, language):
        result = object.__new__(type(self))
        result.__init__(language)
        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined.
    #   Write the complete header of the sheet to the output.
    #   @warning Will raise an exception if not redefined
    def write_document_header(self):
        raise error.MethodShouldBeRedefined(self, 'write_document_header')

    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the command to begin the document
    #   @warning Will raise an exception if not redefined
    def write_document_begins(self):
        raise error.MethodShouldBeRedefined(self, 'write_document_begins')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the command displaying an exercise's title plus
    #   its number
    #   @warning Will raise an exception if not redefined
    def write_exercise_number(self):
        raise error.MethodShouldBeRedefined(self, 'write_exercise_number')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the jump to next page command
    #   @warning Will raise an exception if not redefined
    def write_jump_to_next_page(self):
        raise error.MethodShouldBeRedefined(self, 'write_jump_to_next_page')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the exercises counter reinitializing command
    #   @warning Will raise an exception if not redefined
    def reset_exercises_counter(self):
        raise error.MethodShouldBeRedefined(self, 'reset_exercises_counter')

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the font_size_offset field
    def set_font_size_offset(self, arg):
        raise error.MethodShouldBeRedefined(self, 'set_font_size_offset')

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the redirect_output_to_str field to True or False
    def set_redirect_output_to_str(self, arg):
        raise error.MethodShouldBeRedefined(self, 'set_redirect_output_to_str')

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the value of redirect_output_to_str field
    def redirect_output_to_str(self):
        raise error.MethodShouldBeRedefined(self, 'redirect_output_to_str')

    ##
    #   @brief turn the size keyword in language matching keyword
    #   @warning if you chose a too low or too high value as font_size_offset,
    #   @warning then all the text will be either tiny or Huge.
    def translate_font_size(self, arg):
        raise error.MethodShouldBeRedefined(self, 'translate_font_size')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the end of document command
    #   @warning Will raise an exception if not redefined
    def write_document_ends(self):
        raise error.MethodShouldBeRedefined(self, 'write_document_ends')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the new line command
    #   @warning Will raise an exception if not redefined
    def write_new_line(self, **options):
        raise error.MethodShouldBeRedefined(self, 'write_new_line')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output two commands writing two new lines
    #   @warning Will raise an exception if not redefined
    def write_new_line_twice(self, **options):
        raise error.MethodShouldBeRedefined(self, 'write_new_line_twice')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the given string as a mathematical expression
    #   @warning Will raise an exception if not redefined
    def write_math_style2(self, given_string):
        raise error.MethodShouldBeRedefined(self, 'write_math_style2')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the given string as a math. expression (2d option)
    #   @warning Will raise an exception if not redefined
    def write_math_style1(self, given_string):
        raise error.MethodShouldBeRedefined(self, 'write_math_style1')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the given string
    #   @warning Will raise an exception if not redefined
    def write(self, given_string, **options):
        raise error.MethodShouldBeRedefined(self, 'write')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the given string
    #   @warning Will raise an exception if not redefined
    def write_out(self, given_string, **options):
        raise error.MethodShouldBeRedefined(self, 'write_out')

    ##
    #   @brief /!\ Must be redefined.
    #   Writes to the output the command setting the text size
    #   @warning Will raise an exception if not redefined
    def write_set_font_size_to(self, arg):
        raise error.MethodShouldBeRedefined(self, 'write_set_font_size_to')

    ##
    #   @brief Writes a table filled with the given [strings]
    #   @param size: (nb of columns, nb of lines)
    #   @param col_widths: [int]
    #   @param content: [strings]
    #   @options: borders=0|1|2|3... (not implemented yet)
    #   @options: unit='inch' etc. (check the possibilities...)
    def write_table(self, size, col_widths, content, **options):
        raise error.MethodShouldBeRedefined(self, 'write_table')

    ##
    #   @brief Writes content arranged like in a table (but can be written
    #   @brief without using a table)
    #   @param size: (nb of columns, nb of lines)
    #   @param col_widths: [int]
    #   @param content: [strings]
    #   @options: borders=0|1|2|3... (not implemented yet)
    #   @options: unit='inch' etc. (check the possibilities...)
    def write_layout(self, size, col_widths, content, **options):
        raise error.MethodShouldBeRedefined(self, 'write_layout')

    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined.
    #   Returns a string containing the object to be displayed, according to
    #   the desired output format (LaTeX etc.)
    #   @warning Will raise an exception if not redefined
    def type_string(self, objct, **options):
        raise error.MethodShouldBeRedefined(self, 'type_string')

    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined.
    #   Returns a string containing the object to be displayed, according to
    #   the desired output format (LaTeX etc.)
    #   @warning Will raise an exception if not redefined
    def insert_picture(self, drawable_arg, **options):
        raise error.MethodShouldBeRedefined(self, 'insert_picture')

    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined.
    #   Returns a string containing the object to be displayed, according to
    #   the desired output format (LaTeX etc.)
    #   @warning Will raise an exception if not redefined
    def insert_dashed_hline(self, **options):
        raise error.MethodShouldBeRedefined(self, 'insert_dashed_hline')

    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined.
    #   Returns a string containing the object to be displayed, according to
    #   the desired output format (LaTeX etc.)
    #   @warning Will raise an exception if not redefined
    def insert_vspace(self, **options):
        raise error.MethodShouldBeRedefined(self, 'insert_vspace')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns a non-breaking space
    def insert_nonbreaking_space(self, **options):
        raise error.MethodShouldBeRedefined(self, 'insert_nonbreaking_space')
