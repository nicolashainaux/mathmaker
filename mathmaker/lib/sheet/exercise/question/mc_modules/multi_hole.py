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

from mathmaker.lib import shared
from lib.core.base_calculus import *
from lib.core.root_calculus import *


class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        nb_list = list(numbers_to_use)
        hole = Item(Value('...'))
        self.hidden_one = None
        visible_one = None
        self.product = Value(Product([nb_list[0], nb_list[1]]).evaluate())

        if isinstance(nb_list[1], Fraction):
            self.hidden_one = nb_list[1]
            visible_one = nb_list[0]
        else:
            nb1 = randomly.pop(nb_list)
            nb2 = randomly.pop(nb_list)
            nb_list = [nb1, nb2]
            self.hidden_one = Item(randomly.pop(nb_list))
            visible_one = randomly.pop(nb_list)

        factors = [visible_one, hole]
        self.holed_product = Product([randomly.pop(factors),
                                      randomly.pop(factors)])
        self.holed_product.set_compact_display(False)

    def q(self, **options):
        return _("Which number can fill the hole in") \
               + " "\
               + shared.machine.write_math_style2(\
               self.holed_product.printed) \
               + " = " \
               + self.product.into_str() \
               + " ?"

    def a(self, **options):
        return shared.machine.write_math_style2(self.hidden_one.printed)
