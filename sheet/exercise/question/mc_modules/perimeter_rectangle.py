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

rectangles = recipes.rectangles

class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        rectangles.sub_object.__init__(self, numbers_to_use, **options)

        self.perimeter = Item(Product([Sum([self.w,self.l]),
                                       Item(2)]).evaluate(),
                              unit=self.unit_length)

        self.perimeter = self.perimeter.into_str(force_expression_begins=True,
                                                 display_unit=True)

    def q(self, M, **options):
        if self.context == "sketch":
            return M.write_layout((1, 2),
                                  [5, 8],
                                  [M.insert_picture(self.rectangle,
                                                    scale=0.75,
                                         vertical_alignment_in_a_tabular=True),
                                   _("Perimeter of this rectangle?")])
        else:
            return _(\
      "Perimeter of a rectangle whose width is {w} and length is {l}?")\
            .format(w=M.write_math_style2(self.w_str),
                    l=M.write_math_style2(self.l_str))

    def a(self, M, **options):
        return M.write_math_style2(self.perimeter)
