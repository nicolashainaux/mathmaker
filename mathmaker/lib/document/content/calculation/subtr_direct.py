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

import os
import random

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.core.base_calculus import Sum
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import post_process


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        super().setup("numbers", nb=build_data, **options)
        super().setup("nb_variants", nb=build_data, **options)
        self.transduration = 8
        if (self.nb1 > 20 and self.nb2 > 20
            and abs(self.nb1 - self.nb2) > 10
            and abs(self.nb1 - self.nb2) % 10 != 0):
            self.transduration = 12
        elif abs(self.nb1 - self.nb2) % 1 != 0:
            self.transduration = 10

        if self.subvariant == 'only_positive':
            self.nb1, self.nb2 = max(self.nb1, self.nb2), min(self.nb1,
                                                              self.nb2)
        if (options.get('nb_source', 'default').startswith('complement')
            and self.nb_variant.startswith('decimal')):
            self.nb1 //= 10
        if (options.get('nb_source', 'default').startswith('complement')
            and random.choice([True, False])):
            self.nb2 = self.nb1 - self.nb2

        the_diff = Sum([self.nb1, -self.nb2])
        self.diff_str = the_diff.printed
        self.result = the_diff.evaluate()

        if self.context == 'mini_problem':
            self.transduration = 25
            super().setup('mini_problem_wording',
                          q_id=os.path.splitext(os.path.basename(__file__))[0],
                          **options)
        elif self.context.startswith('complement_wording'):
            self.transduration = 12
            super().setup('complement_wording',
                          q_id=os.path.splitext(os.path.basename(__file__))[0],
                          **options)

    def q(self, **options):
        if hasattr(self, 'wording'):
            return post_process(self.wording.format(**self.wording_format))
        else:
            self.substitutable_question_mark = True
            return _('{math_expr} = {q_mark}')\
                .format(
                math_expr=shared.machine.write_math_style2(self.diff_str),
                q_mark=COLORED_QUESTION_MARK)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        v = None
        if hasattr(self, 'hint'):
            v = Value(self.result, unit=self.hint)\
                .into_str(display_SI_unit=True)
        else:
            v = Value(self.result).into_str()
        return v

    def js_a(self, **kwargs):
        return [Value(self.result).jsprinted]
