# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

import random

from core.base_calculus import *
from . import recipes
from . import divi_direct

rectangles = recipes.rectangles
minimal_setup = recipes.minimal_setup
units = recipes.units

class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        minimal_setup.sub_object.__init__(self, **options)

        if self.context == "from_area":
            del options['context']
            options['context'] = "area_width_length_rectangle"
            divi_direct.sub_object.__init__(self, numbers_to_use, **options)

        elif self.context == "from_perimeter":
            minimal_setup.sub_object.__init__(self, **options)
            units.sub_object.__init__(self, **options)
            rectangles.sub_object.__init__(self, numbers_to_use, **options)

            self.q_context = random.choice(["w", "l"])

            self.w_str = self.rectangle.width.into_str(\
                                                  force_expression_begins=True,
                                                  display_unit=True)
            self.l_str = self.rectangle.length.into_str(\
                                                   force_expression_begins=True,
                                                   display_unit=True)
            self.perimeter_str = self.rectangle.perimeter.into_str(\
                                                   force_expression_begins=True,
                                                   display_unit=True)
            if self.q_context == "w":
                self.rectangle.setup_labels([False, False, True, "?"])
            else:
                self.rectangle.setup_labels([False, False, "?", True])
        else:
            raise error.ImpossibleAction("Create this question without any "\
                                         + "context.")



    def q(self, M, **options):
        if self.context == "area_width_length_rectangle":
            return divi_direct.sub_object.q(self, M, **options)
        elif self.context == "from_perimeter":
            self.q_text = { "w": \
_("What is the width of a rectangle whose perimeter is {p} and length is {l}?")\
.format(p=M.write_math_style2(self.perimeter_str),
        l=M.write_math_style2(self.l_str)),

                            "l": \
_("What is the length of a rectangle whose perimeter is {p} and width is {w}?")\
.format(p=M.write_math_style2(self.perimeter_str),
        w=M.write_math_style2(self.w_str))
                          }

            if self.picture:
                return M.write_layout((1, 2),
                                      [3.5, 9.5],
                                      [M.insert_picture(self.rectangle,
                                                        scale=0.75,
                                         vertical_alignment_in_a_tabular=True),
                                       self.q_text[self.q_context]])
            else:
                return self.q_text[self.q_context]

    def h(self, M, **options):
        return M.write_math_style2("........................ " \
                                   + self.unit_length.into_str())

    def a(self, M, **options):
        if self.context == "area_width_length_rectangle":
            return divi_direct.sub_object.a(self, M, **options)
        elif self.context == "from_perimeter":
            answer = {"w": self.w_str, "l": self.l_str}
            return M.write_math_style2(answer[self.q_context])
