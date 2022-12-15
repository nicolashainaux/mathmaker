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

import copy
import random

from intspan import intspan
from mathmakerlib.calculus import Number

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        """
        The first number of the IntspanProduct, if recognized in the result,
        will be placed at first position in build_data; the first number in
        build_data is the one to be split. The possible nb_variant will take
        effect on the second number only.

        nb_source must be a nnpairs:*

        Options: split_as=
        dig* (where * is a natural number);
        unit (to split at unit rank);
        int_as_halves, int_as_quarters, int_as_halves_or_quarters

        :param build_data: data used to build the question, in the form of a
        pair of numbers (a, b). Question will be "Calculate a1 × b + a2 × b"
        where a1 + a2 = a. Factors of each product may be swapped.
        :type build_data: tuple
        """
        # process build_data to put the first number of the IntspanProduct at
        # first position
        ip_1 = intspan(options['nb_source'].split(':')[1].split('×')[0])
        if build_data[1] in ip_1 and build_data[0] not in ip_1:
            build_data = (build_data[1], build_data[0])
        super().setup("minimal", **options)
        self.transduration = 30
        a, b = build_data
        a, b = Number(a), Number(b)
        # setup possible nb_variant on b only
        super().setup("numbers", nb=[b], shuffle_nbs=False, **options)
        super().setup("nb_variants", **options)
        # then retrieve b, after nb_variant has been applied to it
        b = copy.deepcopy(self.nb1)
        # and go on, preparing the numbers
        a1, a2 = a.split(**self.split_options)
        n1n2 = [a1, b]
        n3n4 = [a2, b]
        if options.get('do_shuffle', True):
            random.shuffle(n1n2)
            random.shuffle(n3n4)
        n1, n2 = n1n2
        n3, n4 = n3n4
        super().setup("numbers", nb=[n1, n2, n3, n4], shuffle_nbs=False,
                      **options)

        self.math_expr = r'{n1} \times {n2} + {n3} \times {n4}'\
            .format(n1=self.nb1.printed, n2=self.nb2.printed,
                    n3=self.nb3.printed, n4=self.nb4.printed)
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
