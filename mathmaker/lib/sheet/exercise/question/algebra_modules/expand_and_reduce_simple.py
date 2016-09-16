# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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
from mathmaker.lib.core.base_calculus import Monomial, Polynomial, Expandable
from mathmaker.lib.core.calculus import Expression
from .. import submodule


class sub_object(submodule.structure):

    def __init__(self, numbers_to_use, **options):
        # We get 4 numbers, one of them being present twice.
        # First we should make a triplet, the first number being the one
        # found once in (nb1, nb2) and in (nb3, nb4):
        if numbers_to_use[0] == numbers_to_use[2]:
            numbers_to_use = numbers_to_use[0:2] + (numbers_to_use[3],)
        elif numbers_to_use[0] == numbers_to_use[3]:
            numbers_to_use = numbers_to_use[0:3]
        elif numbers_to_use[1] == numbers_to_use[2]:
            numbers_to_use = (numbers_to_use[1], numbers_to_use[0],
                              numbers_to_use[3])
        elif numbers_to_use[1] == numbers_to_use[3]:
            numbers_to_use = (numbers_to_use[1], numbers_to_use[0],
                              numbers_to_use[2])
        else:
            raise ValueError('Either the first or second number of this tuple '
                             'should have been equal to one of the two last '
                             'numbers: ' + str(numbers_to_use))
        super().setup("minimal", **options)
        super().setup("numbers", nb=numbers_to_use, shuffle_nbs=False,
                      **options)
        super().setup("nb_variants", nb=numbers_to_use, **options)

        degrees1 = [0, 1]
        degrees2 = [0, 1]
        random.shuffle(degrees1)
        random.shuffle(degrees2)

        weighted_signs = [('+', 16), ('-', 4)]
        weighted_signs = [val
                          for val, cnt in weighted_signs
                          for i in range(cnt)]
        signs = ['+', '-']

        self.expandable = Expandable((Monomial((random.choice(signs),
                                                self.nb1,
                                                degrees1.pop())),
                                      Polynomial([Monomial((random.choice(
                                                            weighted_signs),
                                                            self.nb2,
                                                            degrees2.pop())),
                                                  Monomial((random.choice(
                                                            signs),
                                                            self.nb3,
                                                            degrees2.pop()))])
                                      ))
        self.expression = Expression(shared.number_of_the_question,
                                     self.expandable)
        self.expression_str = self.expression.printed
        shared.number_of_the_question += 1

    def q(self, **options):
        return shared.machine.write_math_style2(self.expression_str)

    def a(self, **options):
        return shared.machine.write(
            self.expression.auto_expansion_and_reduction(**options))
