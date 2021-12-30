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

from mathmakerlib.calculus import is_integer

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.core.base_calculus import Product
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import post_process


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        super().setup("numbers", nb=build_data, **options)
        super().setup("nb_variants", nb=build_data, **options)
        self.transduration = 8
        if (not is_integer(self.nb1) or not is_integer(self.nb2)
            or self.nb1 > 10 or self.nb2 > 10):
            self.transduration = 15
        if hasattr(self, 'nb3'):
            self.transduration = 30

        product = Product([self.nb1, self.nb2])
        if hasattr(self, 'nb3'):
            product = Product([self.nb1, self.nb2, self.nb3])
        self.product_str = product.printed
        self.result = product.evaluate()

        if self.context == 'mini_problem':
            self.transduration = 25
            super().setup('mini_problem_wording',
                          q_id=os.path.splitext(os.path.basename(__file__))[0],
                          **options)

    def q(self, **options):
        if self.context == 'mini_problem':
            return post_process(self.wording.format(**self.wording_format))
        else:
            self.substitutable_question_mark = True
            return _('{math_expr} = {q_mark}').format(
                math_expr=shared.machine.write_math_style2(self.product_str),
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
