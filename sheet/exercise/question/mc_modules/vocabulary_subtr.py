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

# This module will add a question about the sum of two numbers

from core.base_calculus import *
from lib.common.cst import *

class sub_object(object):

    def __init__(self, M, numbers_to_use, **options):
        nb_list = list(numbers_to_use)
        n1 = randomly.pop(nb_list)
        n2 = randomly.pop(nb_list)
        self.n1 = Item(n1).into_str(force_expression_begins=True)
        self.n2 = Item(n2).into_str(force_expression_begins=True)
        m = -min(n1, n2)
        M = max(n1, n2)
        self.d = Item(Sum([M, m]).evaluate()).\
                                        into_str(force_expression_begins=True)

    def q(self, M, **options):
        return _("How much is the difference between {n1} and {n2}?")\
                                                            .format(n1=self.n1,
                                                                    n2=self.n2)

    def a(self, M, **options):
        return str(self.d)
