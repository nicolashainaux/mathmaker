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
import copy
import warnings
from decimal import Decimal

from mathmaker.lib import shared
from mathmaker.lib.tools.auxiliary_functions import is_integer
from mathmaker.lib.core.base_calculus import Item, Sum, Product, Division
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


def remove_division_by_decimal(N, numbers=None):
    """
    Turn N into decimal instead of the numbers of the list.

    This is useful for the case division by a decimal is unwanted.
    """
    if numbers is None:
        raise ValueError('A list of numbers must be given as argument '
                         '\'numbers\'.')
    if all([is_integer(n) for n in numbers]):
        return [N, ] + [n for n in numbers]
    numbers_copy = copy.deepcopy(numbers)
    for i, n in enumerate(numbers):
        if not is_integer(n):
            numbers_copy[i] = n * 10
            return remove_division_by_decimal(N / 10, numbers=numbers_copy)
    return [N, ] + [n for n in numbers]


def split_nb_into(operation, n, nb_variant,
                  decimals_restricted_to, extra_digits):
    """
    Split n as a sum, like a + b = n; or a difference, like a - b = n

    Take the different constraints into account.
    """
    if operation not in ['sum', 'difference']:
        raise ValueError('Argument "operation" should be either \'sum\' or '
                         '\'difference\'.')
    depth = 0  # default value, to keep integers
    if nb_variant.startswith('decimal'):
        if (not is_integer(n)
            or ('+' in decimals_restricted_to and operation is 'sum')
            or ('-' in decimals_restricted_to and operation is 'difference')):
            # e.g. decimals_restricted_to contains '+-'
            # or nb_variant is 'decimalN' (where 1 <= N <= 9) and nb1 is no int
            depth = int(nb_variant[-1]) + extra_digits
    if operation is 'sum':
        if not (nb_variant.startswith('decimal') and depth >= 1) and n == 1:
            # This case is impossible: write 1 as a sum of two natural
            # numbers bigger than 1, so we replace arbitrarily replace 1 by
            # a random number between 2 and 10
            warnings.warn('mathmaker is asked to split 1 as a sum of two '
                          'naturals bigger than 1. As this is impossible, '
                          '1 will be replaced by a random natural between '
                          '2 and 10.')
            n = random.choice([i + 2 for i in range(8)])
        amplitude = n
    elif operation is 'difference':
        amplitude = max(10, n)
    start, end = 0, int((amplitude) * 10 ** depth - 1)
    if start > end:
        start, end = end, start
    if nb_variant.startswith('decimal') and depth >= 1:
        seq = [(Decimal(i) + 1) / Decimal(10) ** Decimal(depth)
               for i in range(start, end)
               if not is_integer((Decimal(i) + 1)
                                 / Decimal(10) ** Decimal(depth))]
    else:  # default: integers
        seq = [(Decimal(i) + 1) / Decimal(10) ** Decimal(depth)
               for i in range(start, end)]
    if operation == 'sum':
        a = random.choice(seq)
        b = n - a
    elif operation == 'difference':
        b = random.choice(seq)
        a = n + b
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
            if (100 <= self.variant <= 107) or (132 <= self.variant <= 139):
                self.nb1, self.nb2 = self.nb2, self.nb1
            elif (108 <= self.variant <= 115) or (140 <= self.variant <= 155):
                self.nb2, self.nb3 = self.nb3, self.nb2
            elif 116 <= self.variant <= 131:
                self.nb3, self.nb4 = self.nb4, self.nb3

        if not self.allow_division_by_decimal:
            if self.variant in [101, 103, 105, 107, ]:
                if not is_integer(self.nb2):
                    self.nb1, self.nb2 = self.nb2, self.nb1
            if self.variant in [109, 110, 113, 114]:
                if not is_integer(self.nb3):
                    self.nb2, self.nb3 = self.nb3, self.nb2
            if self.variant in [111, 115]:
                self.nb1, self.nb2, self.nb3 = \
                    remove_division_by_decimal(self.nb1, numbers=[self.nb2,
                                                                  self.nb3])
            if self.variant in [117, 119, 121, 123]:
                self.nb3, self.nb4 = \
                    remove_division_by_decimal(self.nb3, numbers=[self.nb4, ])
            if self.variant == 118:
                # allow_division_by_decimal is still False,
                # self.nb_variant does start with 'decimal'
                # The idea is to modify self.nb2 in order to have
                # self.nb2 + self.nb3 * self.nb4 being an integer
                if not is_integer(self.nb2 + self.nb3 * self.nb4):
                    self.nb2 += int(self.nb2 + self.nb3 * self.nb4) + 1 \
                        - (self.nb2 + self.nb3 * self.nb4)
            if self.variant == 119:
                if not is_integer(self.nb2) and is_integer(self.nb3):
                    if self.nb3 % 10 == 0 or random.choice([True, False]):
                        self.nb1, self.nb2 = remove_division_by_decimal(
                            self.nb1, numbers=[self.nb2, ])
                    else:
                        self.nb3, self.nb2 = remove_division_by_decimal(
                            self.nb3, numbers=[self.nb2, ])
                if is_integer(self.nb2) and not is_integer(self.nb3):
                    self.nb2 += int(self.nb2 + self.nb3 + 1) \
                        - (self.nb2 + self.nb3)

        if self.subvariant == 'only_positive':
            if self.variant in [120, 122]:
                if self.nb2 < self.nb3 * self.nb4:
                    if not is_integer(self.nb2):
                        if self.nb3 != 10:
                            self.nb3, self.nb2 = remove_division_by_decimal(
                                N=self.nb3, numbers=[self.nb2, ])
                        else:
                            self.nb4, self.nb2 = remove_division_by_decimal(
                                N=self.nb4, numbers=[self.nb2, ])
                    if self.nb2 < self.nb3 * self.nb4:
                        self.nb2 += self.nb3 * self.nb4
                if (self.nb_variant.startswith('decimal')
                    and not self.allow_division_by_decimal):
                    if not is_integer(self.nb2 - self.nb3 * self.nb4):
                        # Same idea as for variant 118 somewhat above
                        self.nb2 += int(self.nb2 - self.nb3 * self.nb4) + 1 \
                            - (self.nb2 - self.nb3 * self.nb4)
                if self.nb2 - self.nb3 * self.nb4 == 0:
                    self.nb2 += random.choice([i + 1 for i in range(9)])
            elif self.variant in [121, 123]:
                if self.nb2 < self.nb3:
                    self.nb2 += self.nb3
                if self.variant == 123:
                    if (not is_integer(self.nb2 - self.nb3)
                        and not self.allow_division_by_decimal):
                        self.nb2 += int(self.nb2 - self.nb3) + 1 \
                            - (self.nb2 - self.nb3)
                        if self.nb2 - self.nb3 == 1:
                            self.nb2 += \
                                random.choice([i for i in range(10)])
        self.expression = None
        self.obj = None
        if self.variant == 100:  # (a + b)×c
            c = self.nb2
            a, b = split_nb_into('sum', self.nb1, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            if any([n < 0 for n in [a, b, c]]):
                raise RuntimeError('100: Negative number detected!')
            if all([is_integer(n) for n in [a, b, c]]):
                raise RuntimeError('100: only integers!')
            if c == 1:
                raise RuntimeError('100: c == 1!')
            self.obj = Product([Sum([Item(a), Item(b)]),
                                Item(c)])
        elif self.variant == 101:  # (a + b)÷c
            c = self.nb2
            self.nb1 = self.nb1 * self.nb2
            a, b = split_nb_into('sum', self.nb1, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            self.obj = Division(('+', Sum([a, b]), c))
            if all([is_integer(n) for n in [a, b, c]]):
                raise RuntimeError('101: only integers!')
            if any([n < 0 for n in [a, b, c]]):
                raise RuntimeError('101: Negative number detected!')
            if c == 1:
                raise RuntimeError('101: c == 1!')
        elif self.variant == 102:  # a×(b + c)
            a = self.nb1
            b, c = split_nb_into('sum', self.nb2, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            self.obj = Product([Item(a),
                                Sum([Item(b), Item(c)])],
                               compact_display=False)
            if any([n < 0 for n in [a, b, c]]):
                raise RuntimeError('102: Negative number detected: (a, b, c) ='
                                   ' ({}, {}, {})'.format(a, b, c))
        elif self.variant == 103:  # a÷(b + c)
            a = self.nb1 * self.nb2
            b, c = split_nb_into('sum', self.nb2, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            if any([n < 0 for n in [a, b, c]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Division(('+', a, Sum([b, c])))
        elif self.variant == 104:  # (a - b)×c
            c = self.nb2
            a, b = split_nb_into('difference', self.nb1, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            if any([n < 0 for n in [a, b, c]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Product([Sum([Item(a), Item(-b)]),
                                Item(c)])
        elif self.variant == 105:  # (a - b)÷c
            c = self.nb2
            self.nb1 = self.nb1 * self.nb2
            a, b = split_nb_into('difference', self.nb1, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            if any([n < 0 for n in [a, b, c]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Division(('+', Sum([a, -b]), c))
        elif self.variant == 106:  # a×(b - c)
            a = self.nb1
            b, c = split_nb_into('difference', self.nb2, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            if any([n < 0 for n in [a, b, c]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Product([Item(a),
                                Sum([Item(b), Item(-c)])],
                               compact_display=False)
        elif self.variant == 107:  # a÷(b - c)
            a = self.nb1 * self.nb2
            b, c = split_nb_into('difference', self.nb2, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            if any([n < 0 for n in [a, b, c]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Division(('+', a, Sum([b, -c])))
        elif self.variant in [108, 112]:  # a×(b ± c)×d
            op = 'sum' if self.variant == 108 else 'difference'
            opn = 1 if self.variant == 108 else -1
            a = self.nb1
            b, c = split_nb_into(op, self.nb2, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            d = self.nb3
            if any([n < 0 for n in [a, b, c, d]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Product([Item(a),
                                Sum([Item(b), Item(opn * c)]),
                                Item(d)],
                               compact_display=False)
        elif self.variant in [109, 113]:  # a×(b ± c)÷d
            op = 'sum' if self.variant == 109 else 'difference'
            opn = 1 if self.variant == 109 else -1
            a = self.nb1
            self.nb2 = self.nb2 * self.nb3
            b, c = split_nb_into(op, self.nb2, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            d = self.nb3
            if any([n < 0 for n in [a, b, c, d]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Division(('+',
                                 Product([a, Sum([b, opn * c])],
                                         compact_display=False),
                                 d))
        elif self.variant in [110, 114]:  # a÷(b ± c)×d
            op = 'sum' if self.variant == 110 else 'difference'
            opn = 1 if self.variant == 110 else -1
            a = self.nb2 * self.nb3
            b, c = split_nb_into(op, self.nb3, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            d = self.nb1
            if any([n < 0 for n in [a, b, c, d]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Product([Division(('+', a, Sum([b, opn * c]))),
                                d],
                               compact_display=False)
        elif self.variant in [111, 115]:  # a÷(b ± c)÷d
            op = 'sum' if self.variant == 111 else 'difference'
            opn = 1 if self.variant == 111 else -1
            a = self.nb1 * self.nb2 * self.nb3
            b, c = split_nb_into(op, self.nb2, self.nb_variant,
                                 self.decimals_restricted_to,
                                 self.allow_extra_digits)
            d = self.nb3
            if any([n < 0 for n in [a, b, c, d]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Division(('+',
                                 Division(('+', a, Sum([b, opn * c]))),
                                 d))
        elif self.variant in [116, 120]:  # a×(b ± c×d)
            opn = 1 if self.variant == 116 else -1
            a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
            self.obj = Product([a,
                                Sum([b, Product([opn * c, d])])],
                               compact_display=False)
            if any([n < 0 for n in [a, b, c, d]]):
                raise RuntimeError('Negative number detected!')
        elif self.variant in [117, 121]:  # a×(b ± c÷d)
            ops = '+' if self.variant == 117 else '-'
            opn = 1 if self.variant == 117 else -1
            a, b, c, d = self.nb1, self.nb2, self.nb3 * self.nb4, self.nb4
            if (self.variant == 117
                and self.nb_variant.startswith('decimal')
                and all(is_integer(n) for n in [a, b, c, d])):
                c = c * 10
                if a % 10 == 0:
                    a += Decimal('0.1') \
                        * random.choice([i + 1 for i in range(-6, 5)])
                else:
                    a = a / 10
            if any([n < 0 for n in [a, b, c, d]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Product([a,
                                Sum([b,
                                     Division((ops, c, d))])],
                               compact_display=False)
        elif self.variant in [118, 122]:  # a÷(b ± c×d)
            ops = '+' if self.variant == 118 else '-'
            opn = 1 if self.variant == 118 else -1
            if self.variant == 118 and self.nb2 == 1:
                self.nb2 += random.choice([i for i in range(10)])
            a = self.nb1 * (self.nb2 + opn * self.nb3 * self.nb4)
            b, c, d = self.nb2, self.nb3, self.nb4
            if any([n < 0 for n in [a, b, c, d]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Division(('+',
                                 a,
                                 Sum([b, Product([opn * c, d])])))
        elif self.variant in [119, 123]:  # a÷(b ± c÷d)
            ops = '+' if self.variant == 119 else '-'
            opn = 1 if self.variant == 119 else -1
            if self.variant == 119 and self.nb2 == 1:
                self.nb2 += random.choice([i for i in range(10)])
            a = self.nb1 * (self.nb2 + opn * self.nb3)
            b, c, d = self.nb2, self.nb3 * self.nb4, self.nb4
            if (self.variant == 119
                and self.nb_variant.startswith('decimal')
                and all(is_integer(n) for n in [a, b, c, d])):
                # if (self.nb2 + self.nb3) % 10 == 0,
                # then adding 0.1 to self.nb1 won't introduce any decimal
                # in a, b, c or d
                ranks = [i + 1 for i in range(-6, 5)]
                random.shuffle(ranks)
                if (self.nb2 + self.nb3) % 10 == 0:
                    for r in ranks:
                        new_nb2 = b + Decimal('0.1') * r
                        new_a = self.nb1 * (new_nb2 + opn * self.nb3)
                        if new_a > 0 and not is_integer(new_a):
                            self.nb2 = new_nb2
                            break
                else:
                    for r in ranks:
                        new_nb1 = self.nb1 + Decimal('0.1') * r
                        new_a = new_nb1 * (self.nb2 + opn * self.nb3)
                        if new_a > 0 and not is_integer(new_a):
                            self.nb1 = new_nb1
                            break
                a = self.nb1 * (self.nb2 + opn * self.nb3)
            if any([n < 0 for n in [a, b, c, d]]):
                raise RuntimeError('Negative number detected!')
            self.obj = Division(('+',
                                 a,
                                 Sum([b,
                                      Division((ops, c, d))])))

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
