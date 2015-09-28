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
from core.root_calculus import *


class sub_object(object):

    def __init__(self, numbers_to_use):
        nb_list = list(numbers_to_use)
        nb1 = randomly.pop(nb_list)
        nb2 = randomly.pop(nb_list)
        self.product = Product([nb1, nb2]).evaluate()
        nb_list = [nb1, nb2]
        self.hidden_one = randomly.pop(nb_list)
        ##
        #   @todo   Cases when the result is not randomly one the two first
        #           numbers (e.g. the numbers to use are not in the tables
        #           from 2 to 9)
        visible_one = randomly.pop(nb_list)
        hole = Item(Value('...'))
        factors = [visible_one, hole]
        f1 = randomly.pop(factors)
        f2 = randomly.pop(factors)
        self.holed_product = Product([f1, f2])
        self.holed_product.set_compact_display(False)

    def q(self, M, **options):
        return _("Which number can fill the hole in") \
               + " "\
               + M.write_math_style2(\
               self.holed_product.into_str(force_expression_begins=True)) \
               + " = " \
               + M.write_math_style2(str(self.product)) \
               + " ?"


    def a(self, M, **options):
        return M.write_math_style2(str(self.hidden_one))
