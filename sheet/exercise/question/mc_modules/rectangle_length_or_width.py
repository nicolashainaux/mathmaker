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
from . import mc_module
from lib.tools.wordings_handling import reformat, setup_wording_format_of
from lib.common import shared

class sub_object(mc_module.structure):

    def __init__(self, M, numbers_to_use, **options):
        super().setup(M, "minimal", **options)
        super().setup(M, "length_units", **options)

        if self.context == "from_area":
            super().setup(M, "division", nb=numbers_to_use, **options)
            self.nb1, self.nb2 = self.dividend, self.divisor
            super().setup(M, "rectangle", **options)
            if self.picture:
                self.rectangle.rename(next(shared.four_letters_words_source))
            wordings = {'w': _("A rectangle has an area of {a} <area_unit> \
and a length of {x} <length_unit>. What is its width? |hint:length_unit|"),
                        'l': _("A rectangle has an area of {a} <area_unit> \
and a width of {x} <length_unit>. What is its length? |hint:length_unit|")
                       }
            self.wording = reformat(wordings[self.subcontext]\
                           .format(a=M.write_math_style2(self.dividend_str),
                                   x=M.write_math_style2(self.divisor_str)))
            setup_wording_format_of(self, M)

        elif self.context == "from_perimeter":
            super().setup(M, "nb_variants", nb=numbers_to_use, **options)
            super().setup(M, "rectangle", **options)
            if self.picture:
                self.rectangle.rename(next(shared.four_letters_words_source))
            self.subcontext = random.choice(['w', 'l'])
            self.w_str = self.rectangle.width.into_str(\
                                                  force_expression_begins=True)
            self.l_str = self.rectangle.length.into_str(\
                                                   force_expression_begins=True)
            self.perimeter_str = self.rectangle.perimeter.into_str(\
                                                   force_expression_begins=True)
            self.x = self.w_str if self.subcontext == 'l' else self.l_str
            wordings = { 'w': _("What is the width of a rectangle whose \
perimeter is {p} <length_unit> and length is {x} <length_unit>? \
|hint:length_unit|"),
                         'l': _("What is the length of a rectangle whose \
perimeter is {p} <length_unit> and width is {x} <length_unit>? \
|hint:length_unit|")
                       }
            self.wording = reformat(wordings[self.subcontext]\
                           .format(p=M.write_math_style2(self.perimeter_str),
                                   x=M.write_math_style2(self.x)))
            setup_wording_format_of(self, M)

        else:
            raise error.ImpossibleAction("Create this question without any "\
                                         + "context.")

        if self.subcontext == "w":
            self.rectangle.setup_labels([False, False, True, "?"])
        elif self.subcontext == "l":
            self.rectangle.setup_labels([False, False, "?", True])

    def q(self, M, **options):
        if self.picture:
            return M.write_layout((1, 2),
                                  [3.5, 9.5],
                                  [M.insert_picture(self.rectangle,
                                                    scale=0.75,
                                     vertical_alignment_in_a_tabular=True),
                                   self.wording.format(**self.wording_format)])
        else:
            return self.wording.format(**self.wording_format)

    def a(self, M, **options):
        u = ""
        if hasattr(self, 'hint'):
            u = M.insert_nonbreaking_space() + self.hint
        if self.context == "from_area":
            return M.write_math_style2(self.result_str) + u
        elif self.context == "from_perimeter":
            answer = {"w": self.w_str, "l": self.l_str}
            return M.write_math_style2(answer[self.subcontext]) + u
