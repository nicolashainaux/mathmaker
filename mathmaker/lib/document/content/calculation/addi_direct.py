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

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.core.base_calculus import Sum
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import post_process


class sub_object(component.structure):

    def __init__(self, numbers_to_use, **options):
        super().setup("minimal", **options)
        if self.nb_source.startswith('complement'):
            maxi, mini = max(numbers_to_use), min(numbers_to_use)
            numbers_to_use = [mini, maxi - mini]
        super().setup("numbers", nb=numbers_to_use,
                      shuffle_nbs=(self.nb_source != 'decimalfractionssums'),
                      **options)
        super().setup("nb_variants", nb=numbers_to_use, **options)
        self.transduration = 8
        if (self.nb1 > 20 and self.nb2 > 20
            and not self.nb1 % 10 == 0 and not self.nb2 % 10 == 0):
            self.transduration = 12
        if self.nb_source.startswith('decimalfractionssums'):
            self.transduration = 15

        the_sum = Sum(self.nb_list)
        self.sum_str = the_sum.printed
        self.result = the_sum.evaluate(stop_recursion=True)

        if self.context == 'mini_problem':
            self.transduration = 25
            super().setup('mini_problem_wording',
                          q_id=os.path.splitext(os.path.basename(__file__))[0],
                          **options)
        elif self.context.startswith('ask:'):
            super().setup('ask_question',
                          q_key=self.context.split(sep=':')[1],
                          values=[
                              shared.machine.write_math_style2(self.sum_str)],
                          fix_math_style2_fontsize=True)

    def q(self, **options):
        if self.context == 'mini_problem':
            return post_process(self.wording.format(**self.wording_format))
        elif self.context.startswith('ask:'):
            return self.wording
        else:
            self.substitutable_question_mark = True
            return _('{math_expr} = {q_mark}').format(
                math_expr=shared.machine.write_math_style2(self.sum_str),
                q_mark=COLORED_QUESTION_MARK)

    def a(self, **options):
        v = None
        if hasattr(self, 'hint'):
            v = Value(self.result, unit=self.hint)\
                .into_str(display_SI_unit=True)
        else:
            v = Value(self.result).into_str()
        return v

    def js_a(self, **kwargs):
        return [Value(self.result).jsprinted]
