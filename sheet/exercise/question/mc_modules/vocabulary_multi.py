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

# This module will add a question about the product of two numbers

from core.base_calculus import *
from lib.common.cst import *

class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        n1 = numbers_to_use[0]
        n2 = numbers_to_use[1]
        self.n1 = Item(n1).into_str(force_expression_begins=True)
        self.n2 = Item(n2).into_str(force_expression_begins=True)
        self.p = Item(Product([n1, n2]).evaluate()).\
                                        into_str(force_expression_begins=True)

    def q(self, M, **options):
        return _("How much is the product of {n1} and {n2}?").format(n1=self.n1,
                                                                     n2=self.n2)

    def a(self, M, **options):
        return M.write_math_style2(str(self.p))
