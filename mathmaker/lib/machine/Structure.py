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

from abc import ABCMeta, abstractmethod


class Structure(object, metaclass=ABCMeta):
    """Abstract mother class of machine objects."""

    # --------------------------------------------------------------------------
    ##
    #   @warning Will raise an exception if not redefined
    @abstractmethod
    def __init__(self, language):
        pass

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns a deep copy of the object
    def clone(self, language):
        result = object.__new__(type(self))
        result.__init__(language)
        return result

    # --------------------------------------------------------------------------
    ##
    #   Write the complete header of the sheet to the output.
    @abstractmethod
    def write_document_header(self):
        pass

    # --------------------------------------------------------------------------
    ##
    #   Writes to the output the command to begin the document
    @abstractmethod
    def write_document_begins(self):
        pass

    ##
    #   Writes to the output the command displaying an exercise's title plus
    #   its number
    @abstractmethod
    def write_exercise_number(self):
        pass

    ##
    #   Writes to the output the jump to next page command
    @abstractmethod
    def write_jump_to_next_page(self):
        pass

    ##
    #   Writes to the output the exercises counter reinitializing command
    @abstractmethod
    def reset_exercises_counter(self):
        pass

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the font_size_offset field
    @abstractmethod
    def set_font_size_offset(self, arg):
        pass

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the redirect_output_to_str field to True or False
    @abstractmethod
    def set_redirect_output_to_str(self, arg):
        pass

    ##
    #   @brief turn the size keyword in language matching keyword
    #   @warning if you chose a too low or too high value as font_size_offset,
    #   @warning then all the text will be either tiny or Huge.
    @abstractmethod
    def translate_font_size(self, arg):
        pass

    ##
    #   Writes to the output the end of document command
    @abstractmethod
    def write_document_ends(self):
        pass

    @abstractmethod
    def write_frame(self, content, uncovered=False, only=False,
                    duration=None, numbering=''):
        """Write frame to the output"""
        pass

    ##
    #   Writes to the output the new line command
    @abstractmethod
    def write_new_line(self, **options):
        pass

    ##
    #   Writes to the output two commands writing two new lines
    @abstractmethod
    def write_new_line_twice(self, **options):
        pass

    ##
    #   Writes to the output the given string as a mathematical expression
    @abstractmethod
    def write_math_style2(self, given_string):
        pass

    ##
    #   Writes to the output the given string as a math. expression (2d option)
    @abstractmethod
    def write_math_style1(self, given_string):
        pass

    ##
    #   Writes to the output the given string
    @abstractmethod
    def write(self, given_string, **options):
        pass

    @abstractmethod
    def write_out(self, given_string, **options):
        pass

    @abstractmethod
    def write_set_font_size_to(self, arg):
        pass

    ##
    #   @brief Writes a table filled with the given [strings]
    #   @param size: (nb of columns, nb of lines)
    #   @param col_widths: [int]
    #   @param content: [strings]
    #   @options: borders=0|1|2|3... (not implemented yet)
    #   @options: unit='inch' etc. (check the possibilities...)
    @abstractmethod
    def create_table(self, size, content, **options):
        pass

    ##
    #   @brief Writes content arranged like in a table (but can be written
    #   @brief without using a table)
    #   @param size: (nb of columns, nb of lines)
    #   @param col_widths: [int]
    #   @param content: [strings]
    #   @options: borders=0|1|2|3... (not implemented yet)
    #   @options: unit='inch' etc. (check the possibilities...)
    @abstractmethod
    def write_layout(self, size, col_widths, content, **options):
        pass

    @abstractmethod
    def type_string(self, objct, **options):
        pass

    @abstractmethod
    def insert_picture(self, drawable_arg, **options):
        pass

    @abstractmethod
    def insert_dashed_hline(self, **options):
        pass

    @abstractmethod
    def insert_vspace(self, **options):
        pass

    @abstractmethod
    def insert_nonbreaking_space(self, **options):
        pass
