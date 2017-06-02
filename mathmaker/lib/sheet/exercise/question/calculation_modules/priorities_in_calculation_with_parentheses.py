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
from mathmaker.lib.core.base_calculus import Item, Sum, Product, Quotient
from mathmaker.lib.core.calculus import Expression
from .. import submodule

# Possible variants are identified with a number:
# 100: (a + b)×c            # 104: (a - b)×c
# 101: (a + b)÷c            # 105: (a - b)÷c
# 102: a×(b + c)            # 106: a×(b - c)
# 103: a÷(b + c)            # 107: a÷(b - c)

# 108: a×(b + c)×d          # 116: a×(b + c×d)
# 109: a×(b + c)÷d          # 117: a×(b + c÷d)
# 110: a÷(b + c)×d          # 118: a÷(b + c×d)
# 111: a÷(b + c)÷d          # 119: a÷(b + c÷d)
# 112: a×(b - c)×d          # 120: a×(b - c×d)
# 113: a×(b - c)÷d          # 121: a×(b - c÷d)
# 114: a÷(b - c)×d          # 122: a÷(b - c×d)
# 115: a÷(b - c)÷d          # 123: a÷(b - c÷d)

# 124: (a×b + c)×d          # 132: (a + b)×(c + d)
# 125: (a÷b + c)×d          # 133: (a + b)÷(c + d)
# 126: (a×b + c)÷d          # 134: (a + b)×(c - d)
# 127: (a÷b + c)÷d          # 135: (a + b)÷(c - d)
# 128: (a×b - c)×d          # 136: (a - b)×(c + d)
# 129: (a÷b - c)×d          # 137: (a - b)÷(c + d)
# 130: (a×b - c)÷d          # 138: (a - b)×(c - d)
# 131: (a÷b - c)÷d          # 139: (a - b)÷(c - d)

# 140: a + b×(c + d)        # 148: (a + b)×c + d
# 141: a + b÷(c + d)        # 149: (a + b)×c - d
# 142: a + b×(c - d)        # 150: (a + b)÷c + d
# 143: a + b÷(c - d)        # 151: (a + b)÷c - d
# 144: a - b×(c + d)        # 152: (a - b)×c + d
# 145: a - b÷(c + d)        # 153: (a - b)×c - d
# 146: a - b×(c - d)        # 154: (a - b)÷c + d
# 147: a - b÷(c - d)        # 155: (a - b)÷c - d


def split_nb_into_sum(n, nb_variant, decimals_restricted_to, extra_digits):
    """
    Split n as a sum a + b = n

    Take the different constraints into account.
    """
    depth = 0  # default value, to keep integers
    if nb_variant.startswith('decimal'):
        if '+' in decimals_restricted_to or type(n) is not int:
            # e.g. 'decimal1_+-'
            # or 'decimalN' (where 1 <= N <= 9) and nb1 is no int
            depth = int(nb_variant[-1]) + extra_digits
    start, end = 0, int((n) * 10 ** depth - 1)
    if n < 0:
        start, end = end, start
    a = random.choice([(i + 1) / 10 ** depth
                       for i in range(start, end)])
    b = n - a
    return (a, b)


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
            if (100 <= self.variant <= 137) or (132 <= self.variant <= 139):
                self.nb1, self.nb2 = self.nb2, self.nb1
            elif (108 <= self.variant <= 115) or (140 <= self.variant <= 155):
                self.nb2, self.nb3 = self.nb3, self.nb2
            elif 116 <= self.variant <= 131:
                self.nb3, self.nb4 = self.nb4, self.nb3

        if self.subvariant == 'only_positive':
            pass  # to do YET for many variants... (the ones containing ÷)
            # see priorities_in_calculation_withOUT_parentheses

        self.expression = None
        self.obj = None
        if self.variant == 100:  # (a + b)×c
            c = self.nb2
            a, b = split_nb_into_sum(self.nb1, self.nb_variant,
                                     self.decimals_restricted_to,
                                     self.allow_extra_digits)
            self.obj = Product([Sum([Item(a), Item(b)]),
                                Item(c)])
        elif self.variant == 101:  # (a + b)÷c
            c = self.nb2
            self.nb1 = self.nb1 * self.nb2
            a, b = split_nb_into_sum(self.nb1, self.nb_variant,
                                     self.decimals_restricted_to,
                                     self.allow_extra_digits)
            self.obj = Quotient(('+', Sum([a, b]), c), use_divide_symbol=True)
        elif self.variant == 102:  # a×(b + c)
            a = self.nb1
            b, c = split_nb_into_sum(self.nb2, self.nb_variant,
                                     self.decimals_restricted_to,
                                     self.allow_extra_digits)
            self.obj = Product([Item(a),
                                Sum([Item(b), Item(c)])],
                               compact_display=False)

        # 104: (a - b)×c
        # 105: (a - b)÷c
        # 102:            # 106: a×(b - c)
        # 103: a÷(b + c)            # 107: a÷(b - c)

        # 108: a×(b + c)×d          # 116: a×(b + c×d)
        # 109: a×(b + c)÷d          # 117: a×(b + c÷d)
        # 110: a÷(b + c)×d          # 118: a÷(b + c×d)
        # 111: a÷(b + c)÷d          # 119: a÷(b + c÷d)
        # 112: a×(b - c)×d          # 120: a×(b - c×d)
        # 113: a×(b - c)÷d          # 121: a×(b - c÷d)
        # 114: a÷(b - c)×d          # 122: a÷(b - c×d)
        # 115: a÷(b - c)÷d          # 123: a÷(b - c÷d)

        # 124: (a×b + c)×d          # 132: (a + b)×(c + d)
        # 125: (a÷b + c)×d          # 133: (a + b)÷(c + d)
        # 126: (a×b + c)÷d          # 134: (a + b)×(c - d)
        # 127: (a÷b + c)÷d          # 135: (a + b)÷(c - d)
        # 128: (a×b - c)×d          # 136: (a - b)×(c + d)
        # 129: (a÷b - c)×d          # 137: (a - b)÷(c + d)
        # 130: (a×b - c)÷d          # 138: (a - b)×(c - d)
        # 131: (a÷b - c)÷d          # 139: (a - b)÷(c - d)

        # 140: a + b×(c + d)        # 148: (a + b)×c + d
        # 141: a + b÷(c + d)        # 149: (a + b)×c - d
        # 142: a + b×(c - d)        # 150: (a + b)÷c + d
        # 143: a + b÷(c - d)        # 151: (a + b)÷c - d
        # 144: a - b×(c + d)        # 152: (a - b)×c + d
        # 145: a - b÷(c + d)        # 153: (a - b)×c - d
        # 146: a - b×(c - d)        # 154: (a - b)÷c + d
        # 147: a - b÷(c - d)        # 155: (a - b)÷c - d
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
