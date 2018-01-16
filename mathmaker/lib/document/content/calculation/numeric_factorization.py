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

from mathmakerlib.calculus import Number, is_integer

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        """
        :param build_data: data used to build the question, in the form of a
        pair of numbers (a, b). Question will be "Calculate a1 × b + a2 × b"
        where a1 + a2 = a. Factors of each product may be swapped.
        :type build_data: tuple
        """
        super().setup("minimal", **options)
        # super().setup("nb_variants", nb=build_data, **options)
        self.transduration = 21
        if not is_integer(build_data[1]):
            self.transduration = 30
        split_as = options.get('split_as', 'dig1')
        split_options = {'int_as_halves': False,
                         'int_as_quarters': False,
                         'int_as_halves_or_quarters': False}
        if split_as in ['halves', 'quarters', 'halves_or_quarters']:
            split_options.update({'int_as_' + split_as: True})
        elif split_as == 'dig1':
            split_options.update({'dig': 1})
        a, b = build_data
        a, b = Number(a), Number(b)
        a1, a2 = a.split(**split_options)
        n1n2 = [a1, b]
        n3n4 = [a2, b]
        if options.get('do_shuffle', True):
            random.shuffle(n1n2)
            random.shuffle(n3n4)
        n1, n2 = n1n2.pop(), n1n2.pop()
        n3, n4 = n3n4.pop(), n3n4.pop()
        super().setup("numbers", nb=[n1, n2, n3, n4], shuffle_nbs=False,
                      **options)

        self.math_expr = r'{} \times {} + {} \times {}'\
            .format(self.nb1.printed, self.nb2.printed, self.nb3.printed,
                    self.nb4.printed)
        self.answer = (a * b).standardized()

    def q(self, **options):
        self.substitutable_question_mark = True
        return _('{math_expr} = {q_mark}').format(
            math_expr=shared.machine.write_math_style2(self.math_expr),
            q_mark=COLORED_QUESTION_MARK)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.answer.printed

    def js_a(self, **kwargs):
        return [self.answer.uiprinted]
