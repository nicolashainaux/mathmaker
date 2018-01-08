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
from mathmaker.lib.core.base_calculus import Product
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        if self.variant == 'with_a_decimal':
            second_couple = shared.mc_source.next('int_deci_clever_pairs')
        elif self.variant == 'integers_only':
            second_couple = shared.mc_source.next('intpairs_2to500',
                                                  clever_in=[4, 5])
        elif self.variant == 'fifths_series':
            second_couple = shared.mc_source.next('intpairs_2to500',
                                                  clever=5,
                                                  union={
                                                      'table_name':
                                                      'int_deci_clever_pairs',
                                                      'clever': 5})
        elif self.variant == 'quarters_series':
            second_couple = shared.mc_source.next('intpairs_2to500',
                                                  clever=4,
                                                  union={
                                                      'table_name':
                                                      'int_deci_clever_pairs',
                                                      'clever': 4})
        else:
            second_couple = shared.mc_source.next('intpairs_2to500',
                                                  clever_in=[4, 5, 10],
                                                  union={
                                                      'table_name':
                                                      'int_deci_clever_pairs'})

        # We shuffle the numbers in a special way
        if len(build_data) == 1:
            # There is only one number in addition to the 2 special ones
            # so either we put it in the first place, or in the middle
            # (not at the end, otherwise, the 2 special ones would be at the
            # two first places)
            special_ones = list(second_couple)
            random.shuffle(special_ones)
            all_nb = [list(build_data).pop(0), special_ones.pop(0)]
            random.shuffle(all_nb)
            all_nb += [special_ones.pop(0)]
        else:
            # It is assumed there are 2 build_data (so 4 altogether)
            # In order to avoid having the two "special" numbers in a row at
            # the two first places, we will shuffle all numbers in a special
            # way.
            if random.choice([True, False]):
                # In this case, the first number will NOT be from the "special"
                # ones, so no matter what follows
                nb_to_use = list(build_data)
                random.shuffle(nb_to_use)
                all_nb = [nb_to_use.pop(0)]
                remaining = nb_to_use + list(second_couple)
            else:
                # In this case, it will, so, at the second place we put a
                # number from the other source (the user specified one)
                first_couple = list(build_data)
                random.shuffle(first_couple)
                nb_to_use = list(second_couple)
                random.shuffle(nb_to_use)
                all_nb = [nb_to_use.pop(0), first_couple.pop(0)]
                remaining = nb_to_use + first_couple
            random.shuffle(remaining)
            all_nb += remaining

        super().setup("numbers", nb=all_nb, shuffle_nbs=False, **options)
        self.transduration = 15

        product = Product([getattr(self,
                                   'nb' + str(i + 1))
                           for i in range(self.nb_nb)])
        self.product_str = product.printed
        self.result = product.evaluate()

    def q(self, **options):
        self.substitutable_question_mark = True
        return _('{math_expr} = {q_mark}').format(
            math_expr=shared.machine.write_math_style2(self.product_str),
            q_mark=COLORED_QUESTION_MARK)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return Value(self.result).into_str()

    def js_a(self, **kwargs):
        return [Value(self.result).jsprinted]
