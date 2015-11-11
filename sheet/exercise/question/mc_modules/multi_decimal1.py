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

# This module will ask to calculate a multiplication where one of the factors
# is a decimal number having one decimal digit.

from core.base_calculus import *
from lib import randomly

class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        nb_list = list(numbers_to_use)
        nb1 = nb_list[randomly.pop([0, 1])]
        nb2 = nb_list[0]
        nb1 = nb1 / 10
        nb_list = [nb1, nb2]
        self.nb1 = randomly.pop(nb_list)
        self.nb2 = randomly.pop(nb_list)

    def q(self, M, **options):
        return _("Calculate:") + " "\
               + M.write_math_style2(Product([self.nb1,
                                              self.nb2]).into_str(\
                                                    force_expression_begins=True
                                                                 )
                                    )

    def a(self, M, **options):
        return M.write_math_style2(Item(Product([self.nb1,
                                                 self.nb2]).evaluate())\
                                         .into_str(\
                                              force_expression_begins=True
                                                  )
                                  )
