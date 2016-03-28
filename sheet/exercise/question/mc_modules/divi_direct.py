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

from core.base_calculus import *
from . import recipes

units = recipes.units
minimal_setup = recipes.minimal_setup
rectangles = recipes.rectangles

class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        minimal_setup.sub_object.__init__(self, **options)

        nb_list = list(numbers_to_use)
        self.divisor = 0
        self.result = 0
        self.dividend = 0
        self.result_str = ""
        self.quotient_str = ""
        self.a_text = {}
        self.q_context = "default"

        if '10_100_1000' in options and options['10_100_1000']:
            self.divisor = nb_list[0]
            self.dividend = nb_list[1]
            self.result = Quotient(('+', self.dividend, self.divisor))\
                          .evaluate()
        else:
            self.divisor = randomly.pop(nb_list)
            self.result = randomly.pop(nb_list)
            if self.variant[:-1] == 'decimal':
                self.result /= 10
            self.dividend = Product([self.divisor, self.result]).evaluate()

        if self.context == 'area_width_length_rectangle':
            units.sub_object.__init__(self, **options)
            self.q_context = "w" if self.result < self.divisor else "l"
            self.dividend_str = Item(self.dividend, unit=self.unit_area)\
                                .into_str(force_expression_begins=True,
                                          display_unit=True)
            self.divisor_str = Item(self.divisor, unit=self.unit_length)\
                               .into_str(force_expression_begins=True,
                                         display_unit=True)
            self.result_str = Item(self.result, unit=self.unit_length)\
                              .into_str(force_expression_begins=True,
                                        display_unit=True)
            if self.picture:
                rectangles.sub_object.__init__(self, numbers_to_use, **options)
                if self.q_context == "w":
                    self.rectangle.side[3].label = Value("?")
                else:
                    self.rectangle.side[2].label = Value("?")
                self.q_context += "_pic"

        else:
            self.dividend_str = Item(self.dividend)\
                                .into_str(force_expression_begins=True)
            self.divisor_str = Item(self.divisor)\
                                .into_str(force_expression_begins=True)
            self.result_str = Item(self.result)\
                                .into_str(force_expression_begins=True)

        self.quotient = Quotient(('+', self.dividend, self.divisor),
                                 use_divide_symbol=True)
        self.quotient_str = self.quotient.into_str(force_expression_begins=True)

    def q(self, M, **options):
        if self.q_context == "w_pic":
            return M.write_layout((1, 2),
                                  [3.7, 9.3],
                                  [M.insert_picture(self.rectangle,
                                                    scale=0.75,
                                   vertical_alignment_in_a_tabular=True),
    _("A rectangle has an area of {a} and a length of {l}. What is its width?")\
    .format(a=M.write_math_style2(self.dividend_str),
            l=M.write_math_style2(self.divisor_str)) ] )

        elif self.q_context == "l_pic":
            return M.write_layout((1, 2),
                                  [3.7, 9.3],
                                  [M.insert_picture(self.rectangle,
                                                    scale=0.75,
                                   vertical_alignment_in_a_tabular=True),
    _("A rectangle has an area of {a} and a width of {w}. What is its length?")\
    .format(a=M.write_math_style2(self.dividend_str),
            w=M.write_math_style2(self.divisor_str)) ] )

        elif self.q_context == "default":
            return _("Calculate: {quotient}").format(quotient=\
                                      M.write_math_style2(self.quotient_str))

        elif self.q_context == "w":
            return _(\
      "A rectangle has an area of {a} and a length of {l}. What is its width?")\
            .format(a=M.write_math_style2(self.dividend_str),
                    l=M.write_math_style2(self.divisor_str))

        elif self.q_context == "l":
            return _(\
      "A rectangle has an area of {a} and a width of {w}. What is its length?")\
            .format(a=M.write_math_style2(self.dividend_str),
                    w=M.write_math_style2(self.divisor_str))

    def h(self, M, **options):
        if hasattr(self, "unit_length"):
            return M.write_math_style2("........................ " \
                                   + self.unit_length.into_str())
        else:
            return ""

    def a(self, M, **options):
        return M.write_math_style2(self.result_str)
