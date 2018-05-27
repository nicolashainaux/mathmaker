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
from decimal import Decimal

from mathmakerlib.calculus import is_integer, move_fracdigits_to
from mathmakerlib.calculus import remove_fracdigits_from, fix_fracdigits
from mathmakerlib.calculus import Number

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.core.base_calculus import (Item, Sum, Product, Division,
                                              Expandable, Value)
from mathmaker.lib.core.calculus import Expression
from mathmaker.lib.document.content import component

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

# 100: (a + b)×c            # 104: (a - b)×c
# 101: (a + b)÷c            # 105: (a - b)÷c
# 102: a×(b + c)            # 106: a×(b - c)
# 103: a÷(b + c)            # 107: a÷(b - c)

# 108: a×(b + c)×d
# 109: a×(b + c)÷d
# 110: a÷(b + c)×d
# 111: a÷(b + c)÷d
# 112: a×(b - c)×d
# 113: a×(b - c)÷d
# 114: a÷(b - c)×d
# 115: a÷(b - c)÷d

# 116: a×(b + c×d)          # 120: a×(b - c×d)
# 117: (b + c×d)×a          # 121: (b - c×d)×a
# 118: a×(c×d + b)          # 122: a×(c×d - b)
# 119: (c×d + b)×a          # 123: (c×d - b)×a

# 124: a×(b + c÷d)          # 128: a×(b - c÷d)
# 125: (b + c÷d)×a          # 129: (b - c÷d)×a
# 126: a×(c÷d + b)          # 130: a×(c÷d - b)
# 127: (c÷d + b)×a          # 131: (c÷d - b)×a

# 132: a÷(b + c×d)
# 133: a÷(c×d + b)

# 134: a÷(b - c×d)
# 135: a÷(c×d - b)

# 136: (a×b + c)÷d
# 137: (c + a×b)÷d

# 138: (a×b - c)÷d
# 139: (c - a×b)÷d

# 140: a÷(b + c÷d)
# 141: a÷(c÷d + b)
# 142: a÷(b - c÷d)
# 143: a÷(c÷d - b)

# 144: (a÷b + c)÷d
# 145: (c + a÷b)÷d
# 146: (a÷b -c)÷d
# 147: (c - a÷b)÷d

# 148: (a + b)×(c + d)          # 152: (a - b)×(c + d)
# 149: (a + b)÷(c + d)          # 153: (a - b)÷(c + d)
# 150: (a + b)×(c - d)          # 154: (a - b)×(c - d)
# 151: (a + b)÷(c - d)          # 155: (a - b)÷(c - d)

# 156: a + b×(c + d)            # 160: a - b×(c + d)
# 157: a + b÷(c + d)            # 161: a - b÷(c + d)
# 158: a + b×(c - d)            # 162: a - b×(c - d)
# 159: a + b÷(c - d)            # 163: a - b÷(c - d)

# 164: a×(b + c) + d            # 168: a×(b - c) + d
# 165: a×(b + c) - d            # 169: a×(b - c) - d
# 166: a÷(b + c) + d            # 170: a÷(b - c) + d
# 167: a÷(b + c) - d            # 171: a÷(b - c) - d

# 172: (a + b)×c + d            # 176: (a - b)×c + d
# 173: (a + b)×c - d            # 177: (a - b)×c - d
# 174: (a + b)÷c + d            # 178: (a - b)÷c + d
# 175: (a + b)÷c - d            # 179: (a - b)÷c - d
# 180: a + (b + c)×d            # 184: a - (b + c)×d
# 181: a + (b + c)÷d            # 185: a - (b + c)÷d
# 182: a + (b - c)×d            # 186: a - (b - c)×d
# 183: a + (b - c)÷d            # 187: a - (b - c)÷d


class sub_object(component.structure):

    def adjust_nb_for_variant_11(self, a, b, c, d):
        """
        Reorder the 4 numbers to ensure a÷b - c×d >= 0

        May (recursively if needed) change some values by multiplying them
        by 10 (if there's no other solution).
        """
        if a >= c * d:
            return (a, b, c, d)
        if b >= c * d:
            return (b, a, c, d)
        if c >= a * b:
            return (c, d, a, b)
        if d >= a * b:
            return (d, c, a, b)
        if 10 * a >= c * d:
            return (a * 10, b, c, d)
        if 10 * b >= c * d:
            return (b * 10, a, c, d)
        if 10 * c >= a * b:
            return (c * 10, d, a, b)
        if 10 * d >= a * b:
            return (d * 10, c, a, b)
        # No solution has been found, we'll recursively test with a * 10
        # (what will actually lead to test a * 100, then if necessary
        # a * 1000 etc. but that shouldn't go too far with the intended
        # numbers' range)
        return self.adjust_nb_for_variant_11(10 * max(a, b),
                                             min(a, b), c, d)

    def adjust_nb_for_variant_13(self, a, b, c, d):
        """
        Reorder the 4 numbers to ensure a×b - c÷d >= 0

        May (recursively if needed) change some values by multiplying them
        by 10 (if there's no other solution).
        """
        if a * b >= c:
            return (a, b, c, d)
        elif a * b >= d:
            return (a, b, d, c)
        else:
            # Necessarily, c * d >= a because a, b, c, d are all positive
            return (c, d, a, b)

    def adjust_depth(self, depth, n=None, **kwargs):
        """
        Return depth to use to split a number, depending on variant etc.

        This is to ensure a correct minimal value.

        :param depth: current depth (for instance, the default one, or the one
                      given by the user)
        :type depth: int
        :param n: the number to split
        :type n: a number (int or Decimal)
        :rtype: int
        """
        if Number(n).is_power_of_10() and depth == 0:
            depth = 1
        # mad stands for maximum added depth
        if self.nb_variant.startswith('decimal'):
            mad = int(self.nb_variant[-1]) - Number(n).fracdigits_nb()
        else:
            mad = 0
        mad = mad if mad > 0 else 0
        if self.variant in [100, 102, 104, 106]:
            # (a + b)×c  a×(b + c)  (a - b)×c  a×(b - c)
            return depth + random.choice([i for i in range(mad + 1)])
        elif self.variant in [101, 105]:  # (a ± b)÷c
            if (not self.allow_division_by_decimal
                and self.nb_variant == 'decimal1'
                and is_integer(n)):
                return max(depth, Number(n).fracdigits_nb() + 1)
        elif self.variant in [103, 107]:  # a÷(b + c) a÷(b - c)
            N = kwargs['N']
            return max(depth,
                       mad - Number(N).fracdigits_nb(),
                       random.choice([i for i in range(mad + 1)]))
        elif self.variant in [108, 112, 109, 113, 110, 114, 111, 115]:
            # a×(b ± c)×d   a×(b ± c)÷d  a÷(b ± c)×d  a÷(b ± c)÷d
            N, P = kwargs['N'], kwargs['P']
            return max(depth,
                       mad - Number(N).fracdigits_nb()
                       - Number(P).fracdigits_nb(),
                       random.choice([i for i in range(mad + 1)]))
        elif 148 <= self.variant <= 155:
            # (a±b)×(c±d) and (a±b)÷(c±d)
            last = kwargs.get('last', False)
            if (self.nb_variant.startswith('decimal')
                and is_integer(n)):
                if (n <= 1 or n <= 6
                    or (7 <= n <= 20 and random.choice([True, True, False]))
                    or (last and is_integer(kwargs['N'])
                        and is_integer(kwargs['P']))):
                    return max(depth, int(self.nb_variant[-1]))
                else:
                    return depth + random.choice([i for i in range(mad + 1)])
            else:
                return depth + random.choice([i for i in range(mad + 1)])
        elif 156 <= self.variant <= 187:
            # a ± b×(c ± d) and a ± b÷(c ± d) and symmetrics
            # (a ± b)×c ± d;    (a ± b)÷c ± d
            # and their symmetrics d ± (a ± b)×c;    d ± (a ± b)÷c
            if (self.nb_variant.startswith('decimal')
                and is_integer(n)
                and ((is_integer(kwargs['N']) and is_integer(kwargs['P']))
                     or n <= 6
                     or (7 <= n <= 20
                         and random.choice([True, True, False])))):
                return max(depth, int(self.nb_variant[-1]))
            else:
                return depth + random.choice([i for i in range(mad + 1)])
        return depth

    def adjust_numbers(self):
        # As the pairs for products and quotients should be shuffled, but as
        # the pairs can be either (self.nb1; self.nb2) or (self.nb2; self.nb3)
        # etc. depending on the exact variant, we have to do it here.
        if random.choice([True, False]):
            if (0 <= self.variant <= 3) or (16 <= self.variant <= 20):
                self.nb2, self.nb3 = self.nb3, self.nb2
            elif 4 <= self.variant <= 7:
                self.nb1, self.nb2 = self.nb2, self.nb1
            elif (100 <= self.variant <= 107) or (148 <= self.variant <= 155):
                self.nb1, self.nb2 = self.nb2, self.nb1
            elif (108 <= self.variant <= 115) or (156 <= self.variant <= 187):
                self.nb2, self.nb3 = self.nb3, self.nb2
            elif 116 <= self.variant <= 147:
                self.nb3, self.nb4 = self.nb4, self.nb3
        if 8 <= self.variant <= 15:
            if random.choice([True, False]):
                self.nb1, self.nb2 = self.nb2, self.nb1
            if random.choice([True, False]):
                self.nb3, self.nb4 = self.nb4, self.nb3

        if 116 <= self.variant <= 123:
            # In these cases, when self.nb2 is not integer, it gives quite
            # often "big" calculation with small numbers already. So most of
            # the time we try to avoid this.
            if (self.nb_variant.startswith('decimal')
                and not is_integer(self.nb2)
                and random.choice([True, True, True, False])):
                try:
                    self.nb2, self.nb1, self.nb3, self.nb4 =\
                        remove_fracdigits_from(self.nb2,
                                               to=[self.nb1, self.nb3,
                                                   self.nb4])
                except ValueError:
                    pass
        if not self.allow_division_by_decimal:
            if self.variant in [5, 7, 10, 11, 14, 15, ]:
                if not is_integer(self.nb2):
                    if is_integer(self.nb1):
                        self.nb1, self.nb2 = self.nb2, self.nb1
                    else:
                        self.nb2, self.nb1 = fix_fracdigits(self.nb2, self.nb1)
            if self.variant in [1, 3, 17, 21, 22, 23]:
                if not is_integer(self.nb3):
                    if is_integer(self.nb2):
                        self.nb2, self.nb3 = self.nb3, self.nb2
                    else:
                        self.nb3, self.nb2 = fix_fracdigits(self.nb3, self.nb2)
            if self.variant in [12, 13, 14, 15, ]:
                if not is_integer(self.nb4):
                    self.nb3, self.nb4 = self.nb4, self.nb3
            if self.variant in [101, 103, 105, 107, ]:
                if not is_integer(self.nb2):
                    if self.nb_variant == 'decimal1':
                        self.nb1, self.nb2 = self.nb2, self.nb1
                    else:
                        self.nb1, self.nb2 = \
                            move_fracdigits_to(self.nb1, from_nb=[self.nb2])
            if self.variant in [109, 110, 113, 114]:
                if not is_integer(self.nb3):
                    if self.nb_variant == 'decimal1':
                        self.nb2, self.nb3 = self.nb3, self.nb2
                    else:
                        self.nb2, self.nb3 = \
                            move_fracdigits_to(self.nb2, from_nb=[self.nb3])
            if self.variant in [111, 115]:
                self.nb1, self.nb2, self.nb3 = \
                    move_fracdigits_to(self.nb1, from_nb=[self.nb2, self.nb3])
            if 132 <= self.variant <= 135:
                if not is_integer(self.nb2):
                    if self.nb_variant == 'decimal1':
                        self.nb1, self.nb2 = self.nb2, self.nb1
                    else:
                        try:
                            self.nb2, self.nb1 = \
                                remove_fracdigits_from(self.nb2, to=[self.nb1])
                        except ValueError:
                            self.nb1 += random.choice([i for i in range(-4, 5)
                                                       if i != 0])
                            self.nb2, self.nb1 = \
                                remove_fracdigits_from(self.nb2, to=[self.nb1])
            if 124 <= self.variant <= 131 or 136 <= self.variant <= 139:
                if not is_integer(self.nb4):
                    if self.nb_variant == 'decimal1':
                        self.nb3, self.nb4 = self.nb4, self.nb3
                    else:
                        try:
                            self.nb4, self.nb3 = \
                                remove_fracdigits_from(self.nb4, to=[self.nb3])
                        except ValueError:
                            self.nb3 += random.choice([i for i in range(-4, 5)
                                                       if i != 0])
                            self.nb4, self.nb3 = \
                                remove_fracdigits_from(self.nb4, to=[self.nb3])
            if 140 <= self.variant <= 147:
                rnd = random.choice([i for i in range(-4, 5) if i != 0])
                if not is_integer(self.nb2):
                    try:
                        self.nb2, self.nb1, self.nb3 = remove_fracdigits_from(
                            self.nb2, to=[self.nb1, self.nb3])
                    except ValueError:
                        self.nb1 += rnd
                        self.nb2, self.nb1 = remove_fracdigits_from(
                            self.nb2, to=[self.nb1])
                if not is_integer(self.nb4):
                    try:
                        self.nb4, self.nb3, self.nb1 = remove_fracdigits_from(
                            self.nb4, to=[self.nb3, self.nb1])
                    except ValueError:
                        self.nb3 += rnd
                        self.nb4, self.nb3 = remove_fracdigits_from(
                            self.nb4, to=[self.nb3])
            if self.variant in [149, 151, 153, 155, 174, 175, 178, 179, 181,
                                183, 185, 187]:
                if not is_integer(self.nb2):
                    if is_integer(self.nb1):
                        self.nb1, self.nb2 = self.nb2, self.nb1
                    else:
                        self.nb2, self.nb1 = remove_fracdigits_from(
                            self.nb2, to=[self.nb1])
            if self.variant in [157, 159, 161, 163, 166, 170, 167, 171]:
                if not is_integer(self.nb3):
                    if is_integer(self.nb2):
                        self.nb2, self.nb3 = self.nb3, self.nb2
                    else:
                        self.nb3, self.nb1, self.nb2 = remove_fracdigits_from(
                            self.nb3, to=[self.nb1, self.nb2])
        if (self.variant in [14, 15]
            and self.nb_variant.startswith('decimal')
            and all(is_integer(x) for x in [self.nb1 * self.nb2,
                                            self.nb2,
                                            self.nb3 * self.nb4,
                                            self.nb4])):
            if not is_integer(self.nb1) and is_integer(self.nb1 * self.nb2):
                if not is_integer(self.nb3 * self.nb4 / 10):
                    self.nb1, self.nb3 = fix_fracdigits(self.nb1, self.nb3)
                else:
                    self.nb2 += random.choice([-1, 1])
            if not is_integer(self.nb3) and is_integer(self.nb3 * self.nb4):
                if not is_integer(self.nb1 * self.nb2 / 10):
                    self.nb3, self.nb1 = fix_fracdigits(self.nb3, self.nb1)
                else:
                    self.nb4 += random.choice([-1, 1])
        if self.variant in [17, 21, 22, 23]:
            if (self.nb_variant.startswith('decimal')
                and all(is_integer(x) for x in [self.nb1,
                                                self.nb2 * self.nb3,
                                                self.nb4])):
                if random.choice([True, False]):
                    self.nb2, self.nb1, self.nb4 = fix_fracdigits(self.nb2,
                                                                  self.nb1,
                                                                  self.nb4)
                else:
                    self.nb2, self.nb4, self.nb1 = fix_fracdigits(self.nb2,
                                                                  self.nb4,
                                                                  self.nb1)

    def _create_0to23(self):
        a, b, c = self.nb1, self.nb2, self.nb3
        if self.variant >= 8:
            d = self.nb4
        # 11 and 13: a÷b - c×d and a×b - c÷d
        if self.variant == 11:
            if (self.nb_variant.startswith('decimal')
                and not is_integer(a)
                and all(is_integer(x) for x in [a * b, c, d])):
                a, c, d = fix_fracdigits(a, c, d)
        elif self.variant == 13:
            if (self.nb_variant.startswith('decimal')
                and not is_integer(c)
                and all(is_integer(x) for x in [a, b, c * d])):
                c, a, b = fix_fracdigits(c, a, b)
        if (self.subvariant == 'only_positive'
            and self.variant == 11 and a - c * d < 0
            and self.nb_variant.startswith('decimal')):
            if not is_integer(a) and a * 10 - c * d / 10 >= 0:
                a, c, d = fix_fracdigits(a, c, d)
            else:
                self.variant = 13
                a, b, c, d = c, d, a, b
        elif (self.subvariant == 'only_positive'
              and self.variant == 13 and a * b - c < 0
              and self.nb_variant.startswith('decimal')):
            self.variant = 11
            a, b, c, d = c, d, a, b
        if self.variant == 0:  # a + b×c
            self.obj = Sum([a, Product([b, c])])
            self.watch('no negative; decimals distribution; '
                       'a isnt 0; b isnt 1; c isnt 1', a, b, c)
        elif self.variant == 1:  # a + b÷c
            if (self.nb_variant.startswith('decimal')
                and all(is_integer(x) for x in [a, b * c, c])):
                b, a = fix_fracdigits(b, a)
            b = b * c
            self.obj = Sum([a, Division(('+', b, c))])
            self.watch('no negative; decimals distribution; '
                       'a isnt 0; c isnt 0; c isnt 1; c isnt deci', a, b, c)
        elif self.variant == 2:  # a - b×c
            if self.subvariant == 'only_positive':
                if a < b * c:
                    a += b * c
            self.obj = Sum([a, Product([-b, c])])
            self.watch('no negative; decimals distribution; '
                       'a isnt 0; b isnt 1; c isnt 1', a, b, c)
        elif self.variant == 3:  # a - b÷c
            if (self.nb_variant.startswith('decimal')
                and all(is_integer(x) for x in [a, b * c, c])):
                b, a = fix_fracdigits(b, a)
            if self.subvariant == 'only_positive':
                if a < b:
                    a += b
            b = b * c
            self.obj = Sum([a, Division(('-', b, c))])
            self.watch('no negative; decimals distribution; '
                       'a isnt 0; c isnt 0; c isnt 1; c isnt deci', a, b, c)
        elif self.variant == 4:  # a×b + c
            self.obj = Sum([Product([a, b]), c])
            self.watch('no negative; decimals distribution; '
                       'c isnt 0; b isnt 1; a isnt 1', a, b, c)
        elif self.variant == 5:  # a÷b + c
            if (self.nb_variant.startswith('decimal')
                and all(is_integer(x) for x in [a * b, b, c])):
                a, c = fix_fracdigits(a, c)
            a = a * b
            self.obj = Sum([Division(('+', a, b)), c])
            self.watch('no negative; decimals distribution; '
                       'c isnt 0; b isnt 0; b isnt 1; b isnt deci', a, b, c)
        elif self.variant == 6:  # a×b - c
            if self.subvariant == 'only_positive' and a * b < c:
                depth = Number(a * b).fracdigits_nb()
                c = Decimal(str(random.choice(
                    [i + 1
                     for i in range(int(a * b * (10 ** depth)))]))) \
                    / Decimal((10 ** depth))
            self.obj = Sum([Product([a, b]), -c])
            self.watch('no negative; decimals distribution; '
                       'c isnt 0; b isnt 1; a isnt 1', a, b, c)
        elif self.variant == 7:  # a÷b - c
            if self.subvariant == 'only_positive' and a < c:
                if self.nb_variant.startswith('decimal'):
                    depth = int(self.nb_variant[-1]) + self.allow_extra_digits
                else:
                    depth = self.allow_extra_digits
                if self.nb_variant.startswith('decimal'):
                    for i in range(depth):
                        c = c / 10
                        if a >= c:
                            break
                    else:  # no break:
                        # We have divided c by 10 as much as allowed
                        # and yet a < c, so no other choice than
                        # randomly choose a new decimal value
                        c = Decimal(str(random.choice(
                            [i + 1
                             for i in range(int(min(a, b) * (10 ** depth)))]
                        ))) / Decimal(str((10 ** depth)))
                else:  # no choice but to randomly choose a new natural
                    if random.choice([True, True, False]):
                        a, b = max(a, b), min(a, b)
                        c = Decimal(str(
                            random.choice([i + 1
                                           for i in range(int(a) - 1)])))
                    else:
                        c = Decimal(str(
                            random.choice([i + 1
                                           for i in range(
                                               int(min(a, b)) - 1)])))

            a = a * b
            self.obj = Sum([Division(('+', a, b)), -c])
            self.watch('no negative; decimals distribution; '
                       'c isnt 0; b isnt 0; b isnt 1; b isnt deci', a, b, c)
        elif self.variant == 8:  # a×b + c×d
            self.obj = Sum([Product([a, b]), Product([c, d])])
            self.watch('no negative; decimals distribution; '
                       'a isnt 1; b isnt 1; c isnt 1; d isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 9:  # a×b - c×d
            if self.subvariant == 'only_positive' and a * b < c * d:
                a, b, c, d = c, d, a, b
            self.obj = Sum([Product([a, b]), Product([-c, d])])
            self.watch('no negative; decimals distribution; '
                       'a isnt 1; b isnt 1; c isnt 1; d isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 10:  # a÷b + c×d
            if (self.nb_variant.startswith('decimal')
                and all(is_integer(x) for x in [a * b, c, d])):
                a, c, d = fix_fracdigits(a, c, d)
            a = a * b
            self.obj = Sum([Division(('+', a, b)), Product([c, d])])
            self.watch('no negative; decimals distribution; '
                       'b isnt 1; c isnt 1; d isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 11:  # a÷b - c×d
            # Special case already managed at start of _create_0to23()
            if (self.subvariant == 'only_positive'
                and not self.nb_variant.startswith('decimal')):
                a, b, c, d = self.adjust_nb_for_variant_11(a, b, c, d)
            a = a * b
            self.obj = Sum([Division(('+', a, b)), Product([-c, d])])
            e = a / b - c * d
            self.watch('no negative; decimals distribution; '
                       'b isnt 1; c isnt 1; d isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
            self.watch('no negative', e, letters='e')
        elif self.variant == 12:  # a×b + c÷d
            if (self.nb_variant.startswith('decimal')
                and all(is_integer(x) for x in [a, b, c * d])):
                c, a, b = fix_fracdigits(c, a, b)
            c = c * d
            self.obj = Sum([Product([a, b]), Division(('+', c, d))])
            self.watch('no negative; decimals distribution; '
                       'a isnt 1; b isnt 1; d isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 13:  # a×b - c÷d
            # Special case already managed at start of _create_0to23()
            if (self.subvariant == 'only_positive'
                and not self.nb_variant.startswith('decimal')):
                a, b, c, d = self.adjust_nb_for_variant_13(a, b, c, d)
            c = c * d
            self.obj = Sum([Product([a, b]), Division(('-', c, d))])
            self.watch('no negative; decimals distribution; '
                       'a isnt 1; b isnt 1; d isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
            e = a * b - c / d
            self.watch('no negative', e, letters='e')
        elif self.variant == 14:  # a÷b + c÷d
            a, c = a * b, c * d
            self.obj = Sum([Division(('+', a, b)), Division(('+', c, d))])
            self.watch('no negative; decimals distribution; '
                       'b isnt 1; d isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 15:  # a÷b - c÷d
            if self.subvariant == 'only_positive' and a < c:
                a, b, c, d = c, d, a, b
            a, c = a * b, c * d
            self.obj = Sum([Division(('+', a, b)), Division(('-', c, d))])
            self.watch('no negative; decimals distribution; '
                       'b isnt 1; d isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 16:  # a + b×c + d
            self.obj = Sum([a, Product([b, c]), d])
            self.watch('no negative; decimals distribution; '
                       'b isnt 1; c isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 17:  # a + b÷c + d
            b = b * c
            self.obj = Sum([a, Division(('+', b, c)), d])
            self.watch('no negative; decimals distribution; '
                       'c isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 18:  # a - b×c + d
            if self.subvariant == 'only_positive':
                if a < b * c:
                    a += b * c
            self.obj = Sum([a, Product([-b, c]), d])
            self.watch('no negative; decimals distribution; '
                       'b isnt 1; c isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 19:  # a + b×c - d
            if self.subvariant == 'only_positive':
                if a + b * c < d:
                    a = a + d
            self.obj = Sum([a, Product([b, c]), -d])
            self.watch('no negative; decimals distribution; '
                       'b isnt 1; c isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 20:  # a - b×c - d
            if self.subvariant == 'only_positive':
                if d + b * c > a:
                    a = a + d + b * c
            self.obj = Sum([a, Product([-b, c]), -d])
            self.watch('no negative; decimals distribution; '
                       'b isnt 1; c isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 21:  # a - b÷c + d
            if self.subvariant == 'only_positive':
                if a < b:
                    a += b
            b = b * c
            self.obj = Sum([a, Division(('-', b, c)), d])
            self.watch('no negative; decimals distribution; '
                       'c isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 22:  # a + b÷c - d
            if self.subvariant == 'only_positive':
                if a + b < d:
                    a += d
                b = b * c
            self.obj = Sum([a, Division(('+', b, c)), -d])
            self.watch('no negative; decimals distribution; '
                       'c isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        elif self.variant == 23:  # a - b÷c - d
            if self.subvariant == 'only_positive':
                if a < b:
                    a += b
                    if a < b + d:
                        a += d
            b = b * c
            self.obj = Sum([a, Division(('-', b, c)), -d])
            self.watch('no negative; decimals distribution; '
                       'c isnt 1'
                       'a isnt 0; b isnt 0; c isnt 0; d isnt 0', a, b, c, d)
        abcd = [a, b, c]
        if self.variant >= 8:
            abcd.append(d)
        return abcd

    def _create_100_104(self):
        # (a + b)×c    (a - b)×c
        ops = '+' if self.variant == 100 else '-'
        opn = 1 if self.variant == 100 else -1
        c = self.nb2
        a, b = Number(self.nb1) \
            .split(operation=ops,
                   dig=self.adjust_depth(self.allow_extra_digits, n=self.nb1))
        self.obj = Product([Sum([Item(a), Item(opn * b)]),
                            Item(c)])
        self.watch('no negative; c isnt 1; decimals distribution', a, b, c)
        return [a, b, c]

    def _create_101_105(self):
        # (a + b)÷c     (a - b)÷c
        ops = '+' if self.variant == 101 else '-'
        opn = 1 if self.variant == 101 else -1
        c = self.nb2
        self.nb1 = self.nb1 * self.nb2
        a, b = Number(self.nb1) \
            .split(operation=ops,
                   dig=self.adjust_depth(self.allow_extra_digits, n=self.nb1))
        self.obj = Division(('+', Sum([a, opn * b]), c))
        self.watch('no negative; c isnt 1; c isnt deci; decimals distribution',
                   a, b, c)
        return [a, b, c]

    def _create_102_106(self):
        # a×(b + c)     a×(b - c)
        ops = '+' if self.variant == 101 else '-'
        opn = 1 if self.variant == 101 else -1
        a = self.nb1
        b, c = Number(self.nb2) \
            .split(operation=ops,
                   dig=self.adjust_depth(self.allow_extra_digits, n=self.nb2))
        self.obj = Product([Item(a),
                            Sum([Item(b), Item(opn * c)])],
                           compact_display=False)
        self.watch('no negative; a isnt 1; decimals distribution', a, b, c)
        return [a, b, c]

    def _create_103_107(self):
        # a÷(b + c)     a÷(b - c)
        ops = '+' if self.variant == 101 else '-'
        opn = 1 if self.variant == 101 else -1
        a = self.nb1 * self.nb2
        b, c = Number(self.nb2) \
            .split(operation=ops,
                   dig=self.adjust_depth(self.allow_extra_digits,
                                         n=self.nb2, N=a))
        self.obj = Division(('+', a, Sum([b, opn * c])))
        d = b + opn * c
        self.watch('no negative; d isnt deci; decimals distribution',
                   a, b, c, d)
        return [a, b, c]

    def _create_108_112(self):
        # a×(b ± c)×d
        ops = '+' if self.variant == 108 else '-'
        opn = 1 if self.variant == 108 else -1
        a = self.nb1
        d = self.nb3
        b, c = Number(self.nb2) \
            .split(operation=ops,
                   dig=self.adjust_depth(self.allow_extra_digits,
                                         n=self.nb2, N=a, P=d))
        self.obj = Product([Item(a),
                            Sum([Item(b), Item(opn * c)]),
                            Item(d)],
                           compact_display=False)
        self.watch('no negative; a isnt 1; d isnt 1; decimals distribution',
                   a, b, c, d)
        return [a, b, c, d]

    def _create_109_113(self):
        # a×(b ± c)÷d
        ops = '+' if self.variant == 109 else '-'
        opn = 1 if self.variant == 109 else -1
        a = self.nb1
        d = self.nb3
        nb2 = self.nb2
        self.nb2 = self.nb2 * self.nb3
        b, c = Number(self.nb2) \
            .split(operation=ops,
                   dig=self.adjust_depth(self.allow_extra_digits,
                                         n=self.nb2, N=a, P=d))
        if (all(is_integer(x) for x in [self.nb2, d, nb2])
            or (not is_integer(self.nb2) and not a % 10 == 0)):
            self.obj = Product([a, Division(('+', Sum([b, opn * c]), d))],
                               compact_display=False)
        else:
            self.obj = Division(('+',
                                 Product([a, Sum([b, opn * c])],
                                         compact_display=False),
                                 d))
        self.watch('no negative; a isnt 1; d isnt 1; d isnt deci; '
                   'decimals distribution', a, b, c, d)
        return [a, b, c, d]

    def _create_110_114(self):
        # a÷(b ± c)×d
        ops = '+' if self.variant == 110 else '-'
        opn = 1 if self.variant == 110 else -1
        a = self.nb2 * self.nb3
        d = self.nb1
        b, c = Number(self.nb3) \
            .split(operation=ops,
                   dig=self.adjust_depth(self.allow_extra_digits,
                                         n=self.nb3, N=a, P=d))
        self.obj = Product([Division(('+', a, Sum([b, opn * c]))),
                            d],
                           compact_display=False)
        e = self.nb3
        self.watch('no negative; d isnt 1; e isnt deci; '
                   'decimals distribution', a, b, c, d, e)
        return [a, b, c, d]

    def _create_111_115(self):
        # a÷(b ± c)÷d
        ops = '+' if self.variant == 111 else '-'
        opn = 1 if self.variant == 111 else -1
        a = self.nb1 * self.nb2 * self.nb3
        d = self.nb3
        b, c = Number(self.nb2) \
            .split(operation=ops,
                   dig=self.adjust_depth(self.allow_extra_digits,
                                         n=self.nb2, N=a, P=d))
        self.obj = Division(('+',
                             Division(('+', a, Sum([b, opn * c]))),
                             d))
        e = self.nb2
        self.watch('no negative; d isnt 1; d isnt deci; '
                   'e isnt deci; decimals distribution', a, b, c, d, e)
        return [a, b, c, d]

    def _create_116to123(self):
        # 116: a×(b + c×d)         117: (b + c×d)×a
        # 118: a×(c×d + b)         119: (c×d + b)×a (124)
        # 120: a×(b - c×d)         121: (b - c×d)×a
        # 122: a×(c×d - b)         123: (c×d - b)×a ((128))
        symmetrics = {120: 122, 122: 120, 121: 123, 123: 121}
        opn = 1 if 116 <= self.variant <= 119 else -1
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if 116 <= self.variant <= 119:
            if ((not self.subvariant == 'only_positive')
                or (self.subvariant == 'only_positive' and b - c * d > 0)):
                b = b - c * d
        if self.variant in [122, 123]:
            if self.subvariant == 'only_positive' and c * d - b < 0:
                self.variant = symmetrics[self.variant]
            elif c * d - b != 0:
                b = c * d - b
        if self.variant in [120, 121]:
            b = b + c * d
        if self.variant in [116, 120]:
            self.obj = Product([a,
                                Sum([b, Product([opn * c, d])])],
                               compact_display=False)
        elif self.variant in [117, 121]:
            self.obj = Product([Sum([b,
                                     Product([opn * c, d],
                                             compact_display=False)]),
                                a], compact_display=False)
        elif self.variant in [118, 122]:
            self.obj = Product([a,
                                Sum([Product([c, d],
                                     compact_display=False),
                                     opn * b])],
                               compact_display=False)
        elif self.variant in [119, 123]:
            self.obj = Product([Sum([Product([c, d],
                                     compact_display=False),
                                     opn * b]),
                                a], compact_display=False)
        self.watch('no negative; decimals distribution; a isnt 1; '
                   'c isnt 1; d isnt 1; b isnt 0', a, b, c, d)
        return [a, b, c, d]

    def _create_124to131(self):
        # 124: a×(b + c÷d)         125: (b + c÷d)×a
        # 126: a×(c÷d + b)         127: (c÷d + b)×a
        # 128: a×(b - c÷d)         129: (b - c÷d)×a
        # 130: a×(c÷d - b)         131: (c÷d - b)×a
        # We won't deal with only integers problems because they cannot show up
        # For instance if c÷d is 4÷5, then b being initially an integer, will
        # become decimal after addition or subtraction of c÷d
        symmetrics = {128: 130, 130: 128, 129: 131, 131: 129}
        ops = '+' if 124 <= self.variant <= 127 else '-'
        opn = 1 if 124 <= self.variant <= 127 else -1
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if 124 <= self.variant <= 127:
            if ((not self.subvariant == 'only_positive')
                or (self.subvariant == 'only_positive' and b - c > 0)):
                b = b - c
        elif self.variant in [130, 131]:
            if ((not self.subvariant == 'only_positive')
                or (self.subvariant == 'only_positive' and c - b > 0)):
                b = c - b
            elif self.subvariant == 'only_positive':
                # Here we have c - b <= 0
                self.variant = symmetrics[self.variant]
        if self.variant in [128, 129]:
            b = b + c
        c = c * d
        if self.variant in [124, 128]:
            self.obj = Product([a,
                                Sum([b, Division((ops, c, d))])],
                               compact_display=False)
        elif self.variant in [125, 129]:
            self.obj = Product([Sum([b,
                                     Division((ops, c, d))]),
                                a], compact_display=False)
        elif self.variant in [126, 130]:
            self.obj = Product([a,
                                Sum([Division(('+', c, d)),
                                     opn * b])],
                               compact_display=False)
        elif self.variant in [127, 131]:
            self.obj = Product([Sum([Division(('+', c, d)),
                                     opn * b]),
                                a], compact_display=False)
        # a×(b ± c÷d) and variants
        self.watch('no negative; decimals distribution; a isnt 1; d isnt 1; '
                   'd isnt deci; b isnt 0', a, b, c, d)
        return [a, b, c, d]

    def _create_132_133(self):
        # a÷(b + c×d)           a÷(c×d + b)
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and not is_integer(a)
            and all(is_integer(x) for x in [b, c, d, a * (b + c * d)])):
            try:
                a, b, c, d = remove_fracdigits_from(a, to=[b, c, d])
            except ValueError:
                rnd = random.choice([i for i in range(-4, 5) if i != 0])
                choice = random.choice([1, 2, 3])
                if choice is 1:
                    b += rnd
                elif choice is 2:
                    c += rnd
                else:
                    d += rnd
                a, b, c, d = remove_fracdigits_from(a, to=[b, c, d])
        if (not self.allow_division_by_decimal
            and self.nb_variant.startswith('decimal')
            and not is_integer(b + c * d)):
            if not is_integer(b):
                # For instance, b + c×d is 0.8 + 10×6
                try:
                    b, c, d = remove_fracdigits_from(b, to=[c, d])
                    # Now it is 8 + 10×0.6
                except ValueError:
                    # Bad luck, it was something like 0.8 + 50×10
                    # (and a = 20). We have to change c or d in order to
                    # ensure one of them at least can be turned into a
                    # decimal
                    rnd = random.choice([i
                                         for i in range(-4, 5)
                                         if i != 0])
                    if random.choice([True, False]):
                        c += rnd
                    else:
                        d += rnd
                    b, c, d = remove_fracdigits_from(b, to=[c, d])
            # Now it's sure b is an integer
            # this doesn't mean that b + c*d is
            if not is_integer(b + c * d):
                if ((not self.subvariant == 'only_positive')
                    or (self.subvariant == 'only_positive'
                        and b - c * d > 0)):
                    b = b - c * d
                else:
                    x = c * d
                    y = random.choice([n for n in range(int(b) + 1)])
                    b = Decimal(y) + 1 - (x - int(x))
        a = self.nb1 * (b + c * d)
        if self.variant == 132:
            self.obj = Division(('+', a, Sum([b, Product([c, d])])))
        elif self.variant == 133:
            self.obj = Division(('+', a, Sum([Product([c, d]), b])))
        # a÷(b + c×d)
        e = b + c * d
        self.watch('no negative; decimals distribution; c isnt 1; d isnt 1; '
                   'e isnt deci; e isnt 0; b isnt 0', a, b, c, d, e)
        return [a, b, c, d]

    def _create_134_135(self):
        # a÷(b - c×d)         a÷(c×d - b)
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and not is_integer(a)
            and all(is_integer(x) for x in [b, c, d, a * b])):
            try:
                a, c, d = remove_fracdigits_from(a, to=[c, d])
            except ValueError:
                rnd = random.choice([i for i in range(-4, 5) if i != 0])
                if random.choice([True, False]):
                    c += rnd
                else:
                    d += rnd
                a, c, d = remove_fracdigits_from(a, to=[c, d])
        if (not self.allow_division_by_decimal
            and self.nb_variant.startswith('decimal')
            and not is_integer(b)):
            try:
                b, c, d = remove_fracdigits_from(b, to=[c, d])
            except ValueError:
                rnd = random.choice([i for i in range(-4, 5) if i != 0])
                if random.choice([True, False]):
                    c += rnd
                else:
                    d += rnd
                b, c, d = remove_fracdigits_from(b, to=[c, d])
        if (self.variant == 135 and self.subvariant == 'only_positive'
            and c * d - b <= 0):
                self.variant = 134
        if self.variant == 134:
            b = b + c * d
        elif self.variant == 135:
            b = c * d - b
        a = self.nb1 * abs(b - c * d)
        if self.variant == 134:
            self.obj = Division(('+', a, Sum([b, Product([-c, d])])))
            e = b - c * d
        elif self.variant == 135:
            self.obj = Division(('+', a, Sum([Product([c, d]), -b])))
            e = c * d - b
        # a÷(b - c×d)
        self.watch('no negative; decimals distribution; c isnt 1; d isnt 1; '
                   'e isnt deci; b isnt 0; a isnt 0', a, b, c, d, e)
        return [a, b, c, d]

    def _create_136_137(self):
        # (a×b + c)÷d       (c + a×b)÷d
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and is_integer(c * d)
            and not is_integer(c)):
            if (a * b >= c * d
                or (a * b < c * d and self.subvariant != 'only_positive')):
                # if a*b == c*d then it's still ok to swap them
                # (this is in order to make the decimal visible)
                # and if a and b are decimals to (e.g. subvariant is
                # decimal2 or more), it doesn't hurt neither
                a, b, c, d = c, d, a, b
            else:
                # subvariant is only_positive
                # and it is not possible to swap a, b and c, d
                # (in order to move the decimal to the product a×b)
                try:
                    c, a, b = remove_fracdigits_from(c, to=[a, b])
                except ValueError:
                    rnd = random.choice([i for i in range(-4, 5) if i != 0])
                    if random.choice([True, False]):
                        a += rnd
                    else:
                        b += rnd
                    c, a, b = remove_fracdigits_from(c, to=[a, b])
        else:
            if (a * b > c * d and self.subvariant == 'only_positive'):
                if (all(is_integer(x) for x in [a, b])
                    or not is_integer(a * b)):
                    a, b, c, d = c, d, a, b
                else:
                    if not is_integer(b):
                        a, b = b, a
                    # Now, the decimal is in a, for sure
                    try:
                        a, c = remove_fracdigits_from(a, to=[c])
                    except ValueError:
                        c += random.choice([i + 1 for i in range(9)])
                        a, c = remove_fracdigits_from(a, to=[c])
                    a, b, c, d = c, d, a, b
        if not is_integer(d):
            c, d = d, c
        if a * b == c * d:
            c = c * d
        else:
            c = c * d - a * b
        if self.variant == 136:
            self.obj = Division(('+',
                                 Sum([Product([a, b],
                                              compact_display=False),
                                      c]),
                                 d))
        elif self.variant == 137:
            self.obj = Division(('+',
                                 Sum([c,
                                      Product([a, b],
                                              compact_display=False)]),
                                 d))
        # (a×b + c)÷d       (c + a×b)÷d
        self.watch('no negative; decimals distribution; d isnt 1; '
                   'd isnt deci; a isnt 1; b isnt 1; c isnt 0', a, b, c, d)
        return [a, b, c, d]

    def _create_138_139(self):
        # (a×b - c)÷d    (c - a×b)÷d
        symmetrics = {138: 139, 139: 138}
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant == 'decimal1'
            and is_integer(c * d)
            and not is_integer(c)):
            # It is enough to swap a,b and c,d in all cases.
            # If this would lead to a negative number, then it is possible
            # to create the symmetric expression (i.e. 139)
            a, b, c, d = c, d, a, b
        c = c * d
        if self.subvariant == 'only_positive':
            if ((self.variant == 138 and a * b - c < 0)
                or (self.variant == 139 and a * b - c > 0)):
                self.variant = symmetrics[self.variant]
        if self.variant == 138:
            if a * b != c:
                c = a * b - c
            first_factor = Sum([Product([a, b], compact_display=False), -c])
            self.obj = Division(('+', first_factor, d))
        elif self.variant == 139:
            if a * b != c:
                c = a * b + c
            first_factor = Sum([c, Product([-a, b], compact_display=False)])
            self.obj = Division(('+', first_factor, d))
        # (a×b - c)÷d    (c - a×b)÷d
        self.watch('no negative; decimals distribution; d isnt deci; c isnt 0',
                   a, b, c, d)
        return [a, b, c, d]

    def _create_140to147(self):
        # a ÷ (b + c÷d)   a ÷ (c÷d + b)
        # a ÷ (b - c÷d)   a ÷ (c÷d - b)
        # (a÷b + c)÷d    (c + a÷b)÷d
        # (a÷b - c)÷d    (c - a÷b)÷d
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        ops = '+' if self.variant in [140, 141, 144, 145] else '-'
        opn = 1 if self.variant in [140, 141, 144, 145] else -1
        if (self.nb_variant == 'decimal1'
            and is_integer(c * d)
            and not is_integer(c)):
            if not is_integer(a * b / 10):
                try:
                    c, a = remove_fracdigits_from(c, to=[a])
                except ValueError:
                    a += random.choice([i for i in range(-4, 5) if i != 0])
                    c, a = remove_fracdigits_from(c, to=[a])
            else:
                d += random.choice([-1, 1])
                if d == 1:
                    d = 3
        elif (self.nb_variant == 'decimal1'
              and is_integer(a * b)
              and not is_integer(a)):
            if not is_integer(c * d / 10):
                try:
                    a, c = remove_fracdigits_from(a, to=[c])
                except ValueError:
                    c += random.choice([i for i in range(-4, 5) if i != 0])
                    a, c = remove_fracdigits_from(a, to=[c])
            else:
                b += random.choice([-1, 1])
                if b == 1:
                    b = 3
        if 140 <= self.variant <= 143:
            if self.variant in [140, 141]:
                if b < c and self.subvariant == 'only_positive':
                    a, b, c, d = d, c, b, a
                    if (not self.allow_division_by_decimal
                        and not is_integer(d)):
                        try:
                            d, c = remove_fracdigits_from(d, to=[c])
                        except ValueError:
                            c += random.choice([i for i in range(-4, 5)
                                                if i != 0])
                            d, c = remove_fracdigits_from(d, to=[c])
                a = a * b
                if c != b:
                    b = b - c
            elif self.variant in [142, 143]:
                if self.variant == 142:
                    if b < c and self.subvariant == 'only_positive':
                        self.variant = 143
                elif self.variant == 143:
                    if c < b and self.subvariant == 'only_positive':
                        self.variant = 142
                a = a * b
                if b != c:
                    if self.variant == 142:
                        b = b + c
                    else:
                        b = c - b
            c = c * d
        else:
            if self.variant in [144, 145]:
                if a > c * d and self.subvariant == 'only_positive':
                    a, b, c, d = c, d, a, b
                if c * d != a:
                    c = c * d - a
                else:
                    # Do not forget the case c * d == a:
                    c = c * d
            elif self.variant in [146, 147]:
                if self.variant == 146:
                    if a <= c * d and self.subvariant == 'only_positive':
                        self.variant = 147
                elif self.variant == 147:
                    if c * d <= a and self.subvariant == 'only_positive':
                        self.variant = 146
                if self.variant == 146:
                    c = a - c * d
                else:
                    c = c * d + a
            a = a * b
        if self.variant in [140, 142]:
            self.obj = Division(('+',
                                 a,
                                 Sum([b,
                                      Division((ops, c, d))])))
        elif self.variant in [141, 143]:
            self.obj = Division(('+',
                                 a,
                                 Sum([Division(('+', c, d)),
                                      opn * b])))
        elif self.variant in [144, 146]:
            self.obj = Division(('+',
                                 Sum([Division(('+', a, b)), opn * c]),
                                 d))
        elif self.variant in [145, 147]:
            self.obj = Division(('+',
                                 Sum([c, Division((ops, a, b))]),
                                 d))
        # a ÷ (b ± c÷d)   a ÷ (c÷d ± b)
        # (a÷b ± c)÷d    (c ± a÷b)÷d
        watch_rules = 'no negative; decimals distribution; d isnt 1; ' \
            + 'd isnt deci'
        if 140 <= self.variant <= 143:
            if self.variant in [140, 141]:
                e = b + c / d
            elif self.variant == 142:
                e = b - c / d
            elif self.variant == 143:
                e = c / d - b
            watch_rules += '; e isnt deci; e inst 0; b isnt 0'
            self.watch(watch_rules, a, b, c, d, e)
        # (a÷b + c)÷d
        else:
            watch_rules += '; b isnt 1; b isnt deci; c isnt 0'
            self.watch(watch_rules, a, b, c, d)
        return [a, b, c, d]

    def _create_148to155(self):
        # 148: (a + b)×(c + d)          # 152: (a - b)×(c + d)
        # 149: (a + b)÷(c + d)          # 153: (a - b)÷(c + d)
        # 150: (a + b)×(c - d)          # 154: (a - b)×(c - d)
        # 151: (a + b)÷(c - d)          # 155: (a - b)÷(c - d)
        ab_signs = dict.fromkeys([148, 149, 150, 151], '+')
        ab_signs.update(dict.fromkeys([152, 153, 154, 155], '-'))
        cd_signs = dict.fromkeys([148, 149, 152, 153], '+')
        cd_signs.update(dict.fromkeys([150, 151, 154, 155], '-'))
        opn_signs = {'+': 1, '-': -1}
        if self.variant in [148, 150, 152, 154]:
            a, b = Number(self.nb1) \
                .split(operation=ab_signs[self.variant],
                       dig=self.adjust_depth(self.allow_extra_digits,
                                             n=self.nb1))
        else:
            a, b = Number(self.nb1 * self.nb2) \
                .split(operation=ab_signs[self.variant],
                       dig=self.adjust_depth(self.allow_extra_digits,
                                             n=self.nb1 * self.nb2))
        c, d = Number(self.nb2) \
            .split(operation=cd_signs[self.variant],
                   dig=self.adjust_depth(self.allow_extra_digits,
                                         n=self.nb2, last=True, N=a, P=b))
        nabs = opn_signs[ab_signs[self.variant]]
        ncds = opn_signs[cd_signs[self.variant]]
        if self.variant in [148, 150, 152, 154]:
            self.obj = Product([Sum([a, nabs * b]),
                                Sum([c, ncds * d])],
                               compact_display=False)
        else:
            self.obj = Division(('+',
                                 Sum([a, nabs * b]),
                                 Sum([c, ncds * d])))
        # 148: (a + b)×(c + d)          # 152: (a - b)×(c + d)
        # 149: (a + b)÷(c + d)          # 153: (a - b)÷(c + d)
        # 150: (a + b)×(c - d)          # 154: (a - b)×(c - d)
        # 151: (a + b)÷(c - d)          # 155: (a - b)÷(c - d)
        e = c + ncds * d
        watch_rules = 'no negative; decimals distribution'
        if self.variant in [149, 151, 153, 155]:
            watch_rules += '; e isnt deci; e isnt 0'
        self.watch(watch_rules, a, b, c, d, e)
        return [a, b, c, d]

    def _create_156to171(self):
        # 156: a + b×(c + d)            # 160: a - b×(c + d)
        # 157: a + b÷(c + d)            # 161: a - b÷(c + d)
        # 158: a + b×(c - d)            # 162: a - b×(c - d)
        # 159: a + b÷(c - d)            # 163: a - b÷(c - d)
        # 164: a×(b + c) + d            # 168: a×(b - c) + d
        # 165: a×(b + c) - d            # 169: a×(b - c) - d
        # 166: a÷(b + c) + d            # 170: a÷(b - c) + d
        # 167: a÷(b + c) - d            # 171: a÷(b - c) - d
        symmetric = {156: 164, 164: 156, 157: 166, 166: 157,
                     158: 168, 168: 158, 159: 170, 170: 159,
                     160: 165, 165: 160, 161: 167, 167: 161,
                     162: 169, 169: 162, 163: 171, 171: 163}
        b_signs = dict.fromkeys([156, 157, 158, 159, 164, 166, 168, 170], '+')
        b_signs.update(
            dict.fromkeys([160, 161, 162, 163, 165, 167, 169, 171], '-'))
        cd_signs = dict.fromkeys([156, 157, 160, 161, 164, 166, 165, 167], '+')
        cd_signs.update(
            dict.fromkeys([158, 159, 162, 163, 168, 170, 169, 171], '-'))
        opn_signs = {'+': 1, '-': -1}
        nbs = opn_signs[b_signs[self.variant]]
        ncds = opn_signs[cd_signs[self.variant]]
        a, b = self.nb1, self.nb2
        if self.subvariant == 'only_positive':
            if self.variant in [165, 169]:
                if b * self.nb3 - a < 0:
                    self.variant = symmetric[self.variant]
            elif self.variant in [167, 171]:
                if b - a < 0:
                    self.variant = symmetric[self.variant]
            if self.variant in [160, 162]:
                if a - b * self.nb3 < 0:
                    a += b * self.nb3
            elif self.variant in [161, 163]:
                if a - b < 0:
                    a += b
        if self.variant in [157, 159, 161, 163, 166, 170, 167, 171]:
            b = self.nb2 * self.nb3
        c, d = Number(self.nb3) \
            .split(operation=cd_signs[self.variant],
                   dig=self.adjust_depth(self.allow_extra_digits,
                                         n=self.nb3, N=a, P=b))
        if self.variant in [156, 158, 160, 162]:
            self.obj = Sum([a,
                            Product([nbs * b,
                                     Sum([c, ncds * d])],
                                    compact_display=False)])
        elif self.variant in [164, 168, 165, 169]:
            self.obj = Sum([Product([b,
                                     Sum([c, ncds * d])],
                                    compact_display=False),
                            nbs * a])
        elif self.variant in [157, 159, 161, 163]:
            self.obj = Sum([a,
                            Division((b_signs[self.variant],
                                      b,
                                      Sum([c, ncds * d])))])
        elif self.variant in [166, 167, 170, 171]:
            self.obj = Sum([Division(('+',
                                      b,
                                      Sum([c, ncds * d]))),
                            nbs * a])
        # 156: a + b×(c + d)            # 160: a - b×(c + d)
        # 157: a + b÷(c + d)            # 161: a - b÷(c + d)
        # 158: a + b×(c - d)            # 162: a - b×(c - d)
        # 159: a + b÷(c - d)            # 163: a - b÷(c - d)
        # 164: a×(b + c) + d            # 168: a×(b - c) + d
        # 165: a×(b + c) - d            # 169: a×(b - c) - d
        # 166: a÷(b + c) + d            # 170: a÷(b - c) + d
        # 167: a÷(b + c) - d            # 171: a÷(b - c) - d
        watch_rules = 'no negative; decimals distribution'
        if self.variant in [156, 158, 160, 162, 164, 168, 165, 169]:
            watch_rules += '; b isnt 1'
        self.watch(watch_rules, a, b, c, d)
        if self.variant in [157, 159, 161, 163, 166, 170, 167, 171]:
            e = self.nb3
            self.watch('e isnt deci', e, letters='e')
        if 160 <= self.variant <= 163 or self.variant in [165, 167, 169, 171]:
            if self.variant in [161, 163]:
                f = a - self.nb2
            elif self.variant in [167, 171]:
                f = self.nb2 - a
            elif self.variant in [160, 162]:
                f = a - b * self.nb3
            elif self.variant in [165, 169]:
                f = b * self.nb3 - a
            self.watch('no negative', f, letters='f')
        return [a, b, c, d]

    def _create_172to187(self):
        # (a ± b)×c ± d;    (a ± b)÷c ± d
        # and their symmetrics d ± (a ± b)×c;    d ± (a ± b)÷c
        symmetric = {172: 180, 180: 172, 173: 184, 184: 173,
                     174: 181, 181: 174, 175: 185, 185: 175,
                     176: 182, 182: 176, 177: 186, 186: 177,
                     178: 183, 183: 178, 179: 187, 187: 179}
        b_signs = dict.fromkeys([172, 173, 174, 175, 180, 181, 184, 185], '+')
        b_signs.update(
            dict.fromkeys([176, 177, 178, 179, 182, 183, 186, 187], '-'))
        d_signs = dict.fromkeys([172, 174, 176, 178, 180, 181, 182, 183], '+')
        d_signs.update(
            dict.fromkeys([173, 175, 177, 179, 184, 185, 186, 187], '-'))
        opn_signs = {'+': 1, '-': -1}
        nbs = opn_signs[b_signs[self.variant]]
        nds = opn_signs[d_signs[self.variant]]
        if (self.nb_variant.startswith('decimal')
            and self.variant in [174, 175, 178, 179, 181, 183, 185, 187]
            and not is_integer(self.nb1)
            and is_integer(self.nb1 * self.nb2)):
            try:
                remove_fracdigits_from(self.nb1, to=[self.nb3])
            except ValueError:
                self.nb3 += random.choice([i for i in range(-4, 5) if i != 0])
                remove_fracdigits_from(self.nb1, to=[self.nb3])
        c, d = self.nb2, self.nb3
        op = b_signs[self.variant]
        if self.variant in [172, 173, 176, 177, 180, 182, 184, 186]:
            nb_to_split = self.nb1
            dig_level = self.adjust_depth(self.allow_extra_digits,
                                          n=self.nb1, N=c, P=d)
        else:
            nb_to_split = self.nb1 * self.nb2
            dig_level = self.adjust_depth(self.allow_extra_digits,
                                          n=self.nb1 * self.nb2, N=c, P=d)
        a, b = Number(nb_to_split).split(operation=op, dig=dig_level)
        if self.subvariant == 'only_positive':
            if ((self.variant in [173, 177] and self.nb1 * self.nb2 < self.nb3)
                or (self.variant in [175, 179] and self.nb1 < self.nb3)
                or (self.variant in [184, 186]
                    and self.nb1 * self.nb2 > self.nb3)
                or (self.variant in [185, 187] and self.nb1 > self.nb3)):
                self.variant = symmetric[self.variant]
        if self.variant in [172, 173, 176, 177]:
            self.obj = Sum([Product([Sum([a, nbs * b]), c],
                                    compact_display=False),
                            nds * d])
        elif self.variant in [180, 182, 184, 186]:
            self.obj = Sum([d,
                            Product([Expandable((Item(nds),
                                                 Sum([a, nbs * b]))),
                                     c], compact_display=False)])
        elif self.variant in [174, 175, 178, 179]:
            self.obj = Sum([Division(('+',
                                      Sum([a, nbs * b]),
                                      c)),
                            nds * d])
        elif self.variant in [181, 183, 185, 187]:
                self.obj = Sum([d,
                                Division((d_signs[self.variant],
                                          Sum([a, nbs * b]),
                                          c))])
        watch_rules = 'no negative; decimals distribution; c isnt 1'
        if self.variant in [174, 175, 178, 179, 181, 183, 185, 187]:
            watch_rules += '; c isnt deci'
        self.watch(watch_rules, a, b, c, d)
        if self.variant in [173, 175, 177, 179, 184, 185, 186, 187]:
            if self.variant in [173, 177]:
                f = (a + nbs * b) * c - d
            elif self.variant in [175, 179]:
                f = (a + nbs * b) / c - d
            elif self.variant in [184, 186]:
                f = d - (a + nbs * b) * c
            elif self.variant in [185, 187]:
                f = d - (a + nbs * b) / c
            self.watch('no negative', f, letters='f')
        return [a, b, c, d]

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        super().setup("numbers", nb=build_data, shuffle_nbs=False,
                      **options)
        direct_test = options.get('direct_test', False)
        if not direct_test:
            super().setup("nb_variants", **options)
            super().setup('logging', **options)

        self.adjust_numbers()
        self.expression = None
        self.obj = None

        catalog = dict.fromkeys([i for i in range(24)],
                                self._create_0to23)
        catalog.update(dict.fromkeys([100, 104], self._create_100_104))
        catalog.update(dict.fromkeys([101, 105], self._create_101_105))
        catalog.update(dict.fromkeys([102, 106], self._create_102_106))
        catalog.update(dict.fromkeys([103, 107], self._create_103_107))
        catalog.update(dict.fromkeys([108, 112], self._create_108_112))
        catalog.update(dict.fromkeys([109, 113], self._create_109_113))
        catalog.update(dict.fromkeys([110, 114], self._create_110_114))
        catalog.update(dict.fromkeys([111, 115], self._create_111_115))
        catalog.update(dict.fromkeys([116 + i for i in range(8)],
                                     self._create_116to123))
        catalog.update(dict.fromkeys([124 + i for i in range(8)],
                                     self._create_124to131))
        catalog.update(dict.fromkeys([132, 133], self._create_132_133))
        catalog.update(dict.fromkeys([134, 135], self._create_134_135))
        catalog.update(dict.fromkeys([136, 137], self._create_136_137))
        catalog.update(dict.fromkeys([138, 139], self._create_138_139))
        catalog.update(dict.fromkeys([140 + i for i in range(8)],
                                     self._create_140to147))
        catalog.update(dict.fromkeys([148 + i for i in range(8)],
                                     self._create_148to155))
        catalog.update(dict.fromkeys([156 + i for i in range(16)],
                                     self._create_156to171))
        catalog.update(dict.fromkeys([172 + i for i in range(16)],
                                     self._create_172to187))

        try:
            self.abcd = catalog[self.variant]()
        except KeyError:
            raise ValueError('Unknown variant identifier for '
                             'order_of_operations: {}'
                             .format(str(self.variant)))

        self.expression = Expression(shared.number_of_the_question,
                                     self.obj)
        self.expression_str = self.expression.printed
        shared.number_of_the_question += 1
        self.transduration = 18

    def q(self, **options):
        if self.x_layout_variant == 'tabular' or self.slideshow:
            self.substitutable_question_mark = True
            return _('{math_expr} = {q_mark}').format(
                math_expr=shared.machine.write_math_style2(self.obj.printed),
                q_mark=COLORED_QUESTION_MARK)
        else:
            return shared.machine.write_math_style2(self.expression_str)

    def a(self, **options):
        if self.x_layout_variant == 'tabular' or self.slideshow:
            return Value(self.expression.right_hand_side.evaluate()).printed
        else:
            return shared.machine.write(
                self.expression.auto_expansion_and_reduction(**options))

    def js_a(self, **kwargs):
        return [Value(self.expression.right_hand_side.evaluate()).jsprinted]
