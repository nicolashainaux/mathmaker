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

from abc import ABCMeta, abstractmethod


class Structure(object, metaclass=ABCMeta):
    """Abstract mother class of machine objects."""

    @abstractmethod
    def __init__(self, language):
        """Initialization"""

    @abstractmethod
    def write_preamble(self):
        """Write the LaTeX document's preamble."""

    @abstractmethod
    def write_document_begins(self):
        """Write "document begins" markup."""

    @abstractmethod
    def write_exercise_number(self):
        """Write the command displaying "Exercise n°..."."""

    @abstractmethod
    def write_jump_to_next_page(self):
        """Write the "jump to next page" command."""

    @abstractmethod
    def reset_exercises_counter(self):
        """Write command reinitializing the exercises counter."""

    @abstractmethod
    def set_font_size_offset(self, arg):
        """Set the font_size_offset field"""

    @abstractmethod
    def set_redirect_output_to_str(self, arg):
        """Set the redirect_output_to_str field to True or False"""

    @abstractmethod
    def translate_font_size(self, arg):
        """Turn the size keyword in markup language matching keyword."""

    @abstractmethod
    def write_document_ends(self):
        """Write the "end of document" command."""

    @abstractmethod
    def write_frame(self, content, uncovered=False, only=False,
                    duration=None, numbering=''):
        """Write a frame to the output."""

    @abstractmethod
    def write_new_line(self, **options):
        """Write the "new line" command."""

    @abstractmethod
    def write_new_line_twice(self, **options):
        """Write the "new line" command twice."""

    @abstractmethod
    def write_math_style2(self, given_string):
        """Write the given string as a mathematical expression."""

    @abstractmethod
    def write_math_style1(self, given_string):
        """Write the given string as a math. expression (2d option)"""

    @abstractmethod
    def write(self, given_string, **options):
        """Write the given string."""

    @abstractmethod
    def write_out(self, given_string, **options):
        """Write to the current output."""

    @abstractmethod
    def write_set_font_size_to(self, arg):
        """Write the command to set font size."""

    @abstractmethod
    def create_table(self, size, content, **options):
        """Write a table filled with the given content."""

    @abstractmethod
    def write_layout(self, size, col_widths, content, **options):
        """Writes content arranged like in a table.

        :param: size: (nb of columns, nb of lines)
        :param col_widths: list of int
        :param content: list of str
        """

    @abstractmethod
    def type_string(self, objct, **options):
        """Get the str version of objct. (Should be __str__())"""

    @abstractmethod
    def insert_picture(self, drawable_arg, **options):
        """Draw and insert the picture of the drawable_arg."""

    @abstractmethod
    def insert_dashed_hline(self, **options):
        """Draw a horizontal dashed line."""

    @abstractmethod
    def insert_vspace(self, **options):
        """Insert a vertical space (default height: 1 cm)."""

    @abstractmethod
    def insert_nonbreaking_space(self, **options):
        """Insert a non-breaking space."""
