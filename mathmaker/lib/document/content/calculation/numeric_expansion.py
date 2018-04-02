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
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        """
        :param build_data: data used to build the question, in the form of a
        triple of numbers (a, b, c). Question will be "Calculate a × N"
        (or N × a) where N = 10×b + c.
        :type build_data: tuple
        """
        super().setup("minimal", **options)
        super().setup("numbers", nb=build_data, **options)
        # super().setup("nb_variants", nb=build_data, **options)
        self.transduration = 30

        n1 = self.nb1
        n2 = 10 * self.nb2 + self.nb3
        factors = [n1, n2]
        random.shuffle(factors)
        self.product_str = r' \times '.join([factors.pop().printed,
                                             factors.pop().printed])
        self.answer = n1 * n2

    def q(self, **options):
        self.substitutable_question_mark = True
        return _('{math_expr} = {q_mark}').format(
            math_expr=shared.machine.write_math_style2(self.product_str),
            q_mark=COLORED_QUESTION_MARK)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.answer.printed

    def js_a(self, **kwargs):
        return [self.answer.uiprinted]
