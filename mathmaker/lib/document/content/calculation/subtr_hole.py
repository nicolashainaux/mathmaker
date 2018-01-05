# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

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

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.core.base_calculus import Sum, Item
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, hidden=None,
                 swap_complement=None, **options):
        if hidden is None:
            hidden = random.choice([1, 2])
        else:
            hidden = int(hidden)
        if swap_complement is None:
            swap_complement = random.choice([True, False])
        super().setup("minimal", **options)
        super().setup("numbers", nb=build_data, **options)
        super().setup("nb_variants", nb=build_data, **options)
        self.transduration = 12
        if (self.nb1 > 20 and self.nb2 > 20
            and abs(self.nb1 - self.nb2) > 10
            and abs(self.nb1 - self.nb2) % 10 != 0):
            self.transduration = 16

        if self.subvariant == 'only_positive':
            self.nb1, self.nb2 = (max(self.nb1, self.nb2),
                                  min(self.nb1, self.nb2))
        if (options.get('nb_source', 'default').startswith('complement')
            and self.nb_variant.startswith('decimal')):
            self.nb1 //= 10
        if (options.get('nb_source', 'default').startswith('complement')
            and swap_complement):
            self.nb2 = self.nb1 - self.nb2
        if self.subvariant == 'only_positive':
            self.nb1, self.nb2 = (max(self.nb1, self.nb2),
                                  min(self.nb1, self.nb2))
        self.result = Item(self.nb1 - self.nb2).printed
        if hidden == 1:
            self.hidden_one = Item(self.nb1)
            self.nb2 = Item(('-', self.nb2, 1))
            self.nb1 = Item(Value(COLORED_QUESTION_MARK))
        else:
            self.hidden_one = Item(self.nb2)
            self.nb2 = Item(('-', COLORED_QUESTION_MARK, 1))
            self.nb1 = Item(self.nb1)
        self.substitutable_question_mark = True
        self.holed_diff_str = Sum([self.nb1, self.nb2]).printed

    def q(self, **options):
        return shared.machine.write_math_style2(
            '{holed_diff} = {result}'.format(holed_diff=self.holed_diff_str,
                                             result=self.result))

    def a(self, **options):
        return shared.machine.write_math_style2(self.hidden_one.printed)

    def js_a(self, **kwargs):
        return [self.hidden_one.jsprinted]
