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

import os

from core.base_calculus import *
from . import mc_module
from lib.wordings_handling_tools import post_process

class sub_object(mc_module.structure):

    def __init__(self, M, numbers_to_use, **options):
        super().setup(M, "minimal", **options)
        super().setup(M, "nb_variants", nb=numbers_to_use, **options)

        product = Product([self.nb1, self.nb2])
        self.product_str = product.into_str(force_expression_begins=True)
        self.result_str = Item(product.evaluate())\
                          .into_str(force_expression_begins=True)

        if self.context == 'mini_problem':
            super().setup(M, "mini_problem_wording",
                          q_id=os.path.splitext(os.path.basename(__file__))[0],
                          **options)

    def q(self, M, **options):
        if self.context == 'mini_problem':
            return post_process(self.wording.format(**self.wording_format))
        else:
            return _("Calculate: {math_expr}").format(\
                                math_expr=M.write_math_style2(self.product_str))

    def a(self, M, **options):
        u = ""
        if hasattr(self, 'hint'):
            u = M.insert_nonbreaking_space() + self.hint
        return M.write_math_style2(self.result_str) + u
