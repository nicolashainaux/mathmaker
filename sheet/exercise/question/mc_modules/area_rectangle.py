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

import copy, sys

from core.base_calculus import *
from lib.common.cst import *
from . import multi_direct

class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        units = copy.deepcopy(COMMON_LENGTH_UNITS)
        unit = randomly.pop(units)
        unit_area = LENGTH_TO_AREA[unit]
        multi_direct.sub_object.__init__(self, numbers_to_use, **options)
        nb_list = [self.nb1, self.nb2]
        self.w = min(nb_list)
        self.l = max(nb_list)
        self.w_str = Item(self.w)
        self.w_str.set_unit(unit)
        self.w_str = self.w_str.into_str(force_expression_begins=True,
                                         display_unit=True)
        self.l_str = Item(self.l)
        self.l_str.set_unit(unit)
        self.l_str = self.l_str.into_str(force_expression_begins=True,
                                         display_unit=True)
        self.product = Item(Product([self.w,self.l]).evaluate())
        self.product.set_unit(unit_area)
        self.product = self.product.into_str(force_expression_begins=True,
                                             display_unit=True)

    def q(self, M, **options):
        return _(\
  "Area of a rectangle whose width is {w} and length is {l}?")\
        .format(w=self.w_str, l=self.l_str)

    def a(self, M, **options):
        return M.write_math_style2(self.product)
