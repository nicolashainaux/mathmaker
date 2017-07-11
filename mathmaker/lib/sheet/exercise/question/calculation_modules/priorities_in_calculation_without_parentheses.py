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
from mathmaker.lib.tools.auxiliary_functions import is_integer
from mathmaker.lib.core.base_calculus import Item, Sum, Product, Division
from mathmaker.lib.core.calculus import Expression
from .. import submodule

# Possible variants are identified with a number:
# 0: a + b×c            # 4: a×b + c
# 1: a + b÷c            # 5: a÷b + c
# 2: a - b×c            # 6: a×b - c
# 3: a - b÷c            # 7: a÷b - c

# 8: a×b + c×d          # 16: a + b×c + d
# 9: a×b - c×d          # 17: a + b÷c + d
# 10: a÷b + c×d         # 18: a - b×c + d
# 11: a÷b - c×d         # 19: a + b×c - d
# 12: a×b + c÷d         # 20: a - b×c - d
# 13: a×b - c÷d         # 21: a - b÷c + d
# 14: a÷b + c÷d         # 22: a + b÷c - d
# 15: a÷b - c÷d         # 23: a - b÷c - d


def adjust_nb_for_variant_11(n1, n2, n3, n4):
    """
    Reorder the 4 numbers to ensure a÷b - c×d >= 0

    May (recursively if needed) change some values by multiplying them
    by 10 (if there's no other solution).
    """
    if n1 >= n3 * n4:
        return (n1, n2, n3, n4)
    if n2 >= n3 * n4:
        return (n2, n1, n3, n4)
    if 10 * n1 >= n3 * n4:
        return (n1 * 10, n2, n3, n4)
    if 10 * n2 >= n3 * n4:
        return (n2 * 10, n1, n3, n4)
    if 10 * n3 >= n1 * n2:
        return (n3 * 10, n4, n1, n2)
    if 10 * n4 >= n1 * n2:
        return (n4 * 10, n3, n1, n2)
    # No solution has been found, we'll recursively test with n1 * 10
    # (what will actually lead to test n1 * 100, then if necessary n1 * 1000
    # etc. but that shouldn't go too far with the intended numbers' range)
    return adjust_nb_for_variant_11(10 * max(n1, n2), min(n1, n2), n3, n4)


def adjust_nb_for_variant_13(n1, n2, n3, n4):
    """
    Reorder the 4 numbers to ensure a×b - c÷d >= 0

    May (recursively if needed) change some values by multiplying them
    by 10 (if there's no other solution).
    """
    if n1 * n2 >= n3:
        return (n1, n2, n3, n4)
    if n1 * n2 >= n4:
        return (n1, n2, n4, n3)
    if n3 * n4 >= n1:
        return (n3, n4, n1, n2)
    if n3 * n4 >= n1:
        return (n3, n4, n2, n1)
    return adjust_nb_for_variant_13(10 * max(n1, n2), min(n1, n2), n3, n4)


def adjust_nb_for_variant_15(n1, n2, n3, n4):
    """
    Reorder the 4 numbers to ensure a÷b - c÷d >= 0

    May (recursively if needed) change some values by multiplying them
    by 10 (if there's no other solution).
    """
    if n1 >= n3:
        return (n1, n2, n3, n4)
    if n1 >= n4:
        return (n1, n2, n4, n3)
    if n2 >= n3:
        return (n2, n1, n3, n4)
    if n2 >= n4:
        return (n2, n1, n4, n3)
    return adjust_nb_for_variant_15(10 * max(n1, n2), min(n1, n2), n3, n4)


class sub_object(submodule.structure):

    def __init__(self, numbers_to_use, **options):
        super().setup("minimal", **options)
        super().setup("numbers", nb=numbers_to_use, shuffle_nbs=False,
                      **options)
        super().setup("nb_variants", nb=numbers_to_use, **options)

        # As the pairs for products and quotients should be shuffled, but as
        # the pairs can be either (self.nb1; self.nb2) or (self.nb2; self.nb3)
        # etc. depending on the exact variant, we have to do it here.
        if random.choice([True, False]):
            if (0 <= self.variant <= 3) or (16 <= self.variant <= 20):
                self.nb2, self.nb3 = self.nb3, self.nb2
            elif 4 <= self.variant <= 7:
                self.nb1, self.nb2 = self.nb2, self.nb1
        if 8 <= self.variant <= 15:
            if random.choice([True, False]):
                self.nb1, self.nb2 = self.nb2, self.nb1
            if random.choice([True, False]):
                self.nb3, self.nb4 = self.nb4, self.nb3

        if self.subvariant == 'only_positive':
            if self.variant == 11:
                self.nb1, self.nb2, self.nb3, self.nb4 = \
                    adjust_nb_for_variant_11(self.nb1, self.nb2,
                                             self.nb3, self.nb4)
            elif self.variant == 13:
                self.nb1, self.nb2, self.nb3, self.nb4 = \
                    adjust_nb_for_variant_13(self.nb1, self.nb2,
                                             self.nb3, self.nb4)
            elif self.variant == 15:
                self.nb1, self.nb2, self.nb3, self.nb4 = \
                    adjust_nb_for_variant_15(self.nb1, self.nb2,
                                             self.nb3, self.nb4)

        if not self.allow_division_by_decimal:
            if self.variant in [5, 7, 10, 11, 14, 15, ]:
                if not is_integer(self.nb2):
                    self.nb1, self.nb2 = self.nb2, self.nb1
            if self.variant in [1, 3, 17, 21, 22, 23]:
                if not is_integer(self.nb3):
                    self.nb2, self.nb3 = self.nb3, self.nb2
            if self.variant in [12, 13, 14, 15, ]:
                if not is_integer(self.nb4):
                    self.nb3, self.nb4 = self.nb4, self.nb3

        if self.subvariant == 'only_positive':
            if self.variant in [2, 18]:
                if (Item(Product([self.nb2, self.nb3]).evaluate())
                    > Item(self.nb1)):
                    self.nb1 = self.nb1 + self.nb2 * self.nb3
            if self.variant in [3, 21]:
                if self.nb2 > self.nb1:
                    self.nb1 += self.nb2

        self.expression = None
        self.obj = None
        if self.variant == 0:  # a + b×c
            self.obj = Sum([self.nb1, Product([self.nb2, self.nb3])])
        elif self.variant == 1:  # a + b÷c
            self.obj = Sum([self.nb1, Division(('+',
                                                self.nb2 * self.nb3,
                                                self.nb3))])
        elif self.variant == 2:  # a - b×c
            if self.subvariant == 'only_positive':
                if self.nb1 < self.nb2:
                    self.nb1 += self.nb2
            self.obj = Sum([self.nb1, Product([-self.nb2, self.nb3])])
        elif self.variant == 3:  # a - b÷c
            if self.subvariant == 'only_positive':
                if self.nb1 < self.nb2 * self.nb3:
                    self.nb1 += self.nb2 * self.nb3
            self.obj = Sum([self.nb1,
                            Division(('-', self.nb2 * self.nb3, self.nb3))])
        elif self.variant == 4:  # a×b + c
            self.obj = Sum([Product([self.nb1, self.nb2]),
                            self.nb3])
        elif self.variant == 5:  # a÷b + c
            self.obj = Sum([Division(('+', self.nb1 * self.nb2, self.nb2)),
                            self.nb3])
        elif self.variant == 6:  # a×b - c
            if (self.subvariant == 'only_positive'
                and self.nb1 * self.nb2 < self.nb3):
                self.nb3 = self.nb3 % (self.nb1 * self.nb2)
            self.obj = Sum([Product([self.nb1, self.nb2]),
                            -self.nb3])
        elif self.variant == 7:  # a÷b - c
            if self.subvariant == 'only_positive' and self.nb1 < self.nb3:
                if self.nb_variant.startswith('decimal'):
                    depth = int(self.nb_variant[-1]) + self.allow_extra_digits
                else:
                    depth = self.allow_extra_digits
                if self.nb_variant.startswith('decimal'):
                    for i in range(depth):
                        self.nb3 = self.nb3 / 10
                        if self.nb1 >= self.nb3:
                            break
                    else:  # no break:
                        # We have divided self.nb3 by 10 as much as allowed
                        # and yet self.nb1 < self.nb3, so no other choice than
                        # randomly choose a new decimal value
                        self.nb3 = random.choice(
                            [i + 1
                             for i in range(int(min(self.nb1, self.nb2)
                                            * (10 ** depth)))]) / (10 ** depth)
                else:  # no choice but to randomly choose a new natural
                    self.nb3 = random.choice(
                        [i + 1
                         for i in range(int(min(self.nb1, self.nb2)) - 1)])
            self.obj = Sum([Division(('+', self.nb1 * self.nb2, self.nb2)),
                            -self.nb3])
        elif self.variant == 8:  # a×b + c×d
            self.obj = Sum([Product([self.nb1, self.nb2]),
                            Product([self.nb3, self.nb4])])
        elif self.variant == 9:  # a×b - c×d
            if (self.subvariant == 'only_positive'
                and self.nb1 * self.nb2 < self.nb3 * self.nb4):
                self.nb1, self.nb2, self.nb3, self.nb4 = \
                    self.nb3, self.nb4, self.nb1, self.nb2
            self.obj = Sum([Product([self.nb1, self.nb2]),
                            Product([-self.nb3, self.nb4])])
        elif self.variant == 10:  # a÷b + c×d
            self.obj = Sum([Division(('+', self.nb1 * self.nb2, self.nb2)),
                            Product([self.nb3, self.nb4])])
        elif self.variant == 11:  # a÷b - c×d
            self.obj = Sum([Division(('+', self.nb1 * self.nb2, self.nb2)),
                            Product([-self.nb3, self.nb4])])
        elif self.variant == 12:  # a×b + c÷d
            self.obj = Sum([Product([self.nb1, self.nb2]),
                            Division(('+', self.nb3 * self.nb4, self.nb4))])
        elif self.variant == 13:  # a×b - c÷d
            self.obj = Sum([Product([self.nb1, self.nb2]),
                            Division(('-', self.nb3 * self.nb4, self.nb4))])
        elif self.variant == 14:  # a÷b + c÷d
            self.obj = Sum([Division(('+', self.nb1 * self.nb2, self.nb2)),
                            Division(('+', self.nb3 * self.nb4, self.nb4))])
        elif self.variant == 15:  # a÷b - c÷d
            self.obj = Sum([Division(('+', self.nb1 * self.nb2, self.nb2)),
                            Division(('-', self.nb3 * self.nb4, self.nb4))])
        elif self.variant == 16:  # a + b×c + d
            self.obj = Sum([self.nb1,
                            Product([self.nb2, self.nb3]),
                            self.nb4])
        elif self.variant == 17:  # a + b÷c + d
            self.obj = Sum([self.nb1,
                            Division(('+', self.nb2 * self.nb3, self.nb3)),
                            self.nb4])
        elif self.variant == 18:  # a - b×c + d
            self.obj = Sum([self.nb1,
                            Product([-self.nb2, self.nb3]),
                            self.nb4])
        elif self.variant == 19:  # a + b×c - d
            if self.subvariant == 'only_positive':
                if self.nb1 + self.nb2 * self.nb3 < self.nb4:
                    self.nb1 = self.nb1 + self.nb4
            self.obj = Sum([self.nb1,
                            Product([self.nb2, self.nb3]),
                            -self.nb4])
        elif self.variant == 20:  # a - b×c - d
            if self.subvariant == 'only_positive':
                if self.nb4 + self.nb2 * self.nb3 > self.nb1:
                    self.nb1 = self.nb1 + self.nb4 + self.nb2 * self.nb3
            self.obj = Sum([self.nb1,
                            Product([-self.nb2, self.nb3]),
                            -self.nb4])
        elif self.variant == 21:  # a - b÷c + d
            self.obj = Sum([self.nb1,
                            Division(('-', self.nb2 * self.nb3, self.nb3))])
        elif self.variant == 22:  # a + b÷c - d
            if self.subvariant == 'only_positive':
                if self.nb1 + self.nb2 < self.nb4:
                    self.nb1 += self.nb4
            self.obj = Sum([self.nb1,
                            Division(('+', self.nb2 * self.nb3, self.nb3)),
                            -self.nb4])
        elif self.variant == 23:  # a - b÷c - d
            if self.subvariant == 'only_positive':
                if self.nb1 < self.nb2:
                    self.nb1 += self.nb2
                    if self.nb1 < self.nb2 + self.nb4:
                        self.nb1 += self.nb4
            self.obj = Sum([self.nb1,
                            Division(('-', self.nb2 * self.nb3, self.nb3)),
                            -self.nb4])
        else:
            raise ValueError('Unknown variant identifier for priorities_in'
                             '_calculation_without_parentheses: {}'
                             .format(str(self.variant)))

        self.expression = Expression(shared.number_of_the_question,
                                     self.obj)
        self.expression_str = self.expression.printed
        shared.number_of_the_question += 1

    def q(self, **options):
        return shared.machine.write_math_style2(self.expression_str)

    def a(self, **options):
        return shared.machine.write(
            self.expression.auto_expansion_and_reduction(**options))
