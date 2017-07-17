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
from decimal import Decimal

from mathmaker.lib import shared
from mathmaker.lib.tools.auxiliary_functions \
    import (is_integer, move_digits_to, split_nb, digits_nb,
            remove_digits_from)
from mathmaker.lib.core.base_calculus import (Item, Sum, Product, Division,
                                              Expandable)
from mathmaker.lib.core.calculus import Expression
from .. import submodule

# Possible variants are identified with a number:

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


class sub_object(submodule.structure):

    def adjust_depth(self, depth, n=None, **kwargs):
        """
        Return depth to use to split a number, depending on variant etc.

        This is to ensure a correct minimal value. For instance, if
        self.deci_restriction is '+-', it certainly requires to be at least 1.

        :param depth: current depth (for instance, the default one, or the one
                      given by the user)
        :type depth: int
        :param n: the number to split
        :type n: a number (int or Decimal)
        :rtype: int
        """
        # mad stands for maximum added depth
        if self.nb_variant.startswith('decimal'):
            mad = int(self.nb_variant[-1]) - digits_nb(n)
        else:
            mad = 0
        mad = mad if mad > 0 else 0
        if (self.nb_variant.startswith('decimal')
            and self.deci_restriction == '+-'):
            return max(depth, digits_nb(n) + 1)
        if self.variant in [100, 102, 104, 106]:
            # (a + b)×c  a×(b + c)  (a - b)×c  a×(b - c)
            return depth + random.choice([i for i in range(mad + 1)])
        elif self.variant in [101, 105]:  # (a ± b)÷c
            if (not self.allow_division_by_decimal
                and self.nb_variant == 'decimal1'
                and is_integer(n)):
                return max(depth, digits_nb(n) + 1)
        elif self.variant in [103, 107]:  # a÷(b + c) a÷(b - c)
            N = kwargs['N']
            return max(depth,
                       mad - digits_nb(N),
                       random.choice([i for i in range(mad + 1)]))
        elif self.variant in [108, 112, 109, 113, 110, 114, 111, 115]:
            # a×(b ± c)×d   a×(b ± c)÷d  a÷(b ± c)×d  a÷(b ± c)÷d
            N, P = kwargs['N'], kwargs['P']
            return max(depth,
                       mad - digits_nb(N) - digits_nb(P),
                       random.choice([i for i in range(mad + 1)]))
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
            if (100 <= self.variant <= 107) or (148 <= self.variant <= 155):
                self.nb1, self.nb2 = self.nb2, self.nb1
            elif (108 <= self.variant <= 115) or (156 <= self.variant <= 187):
                self.nb2, self.nb3 = self.nb3, self.nb2
            elif 116 <= self.variant <= 147:
                self.nb3, self.nb4 = self.nb4, self.nb3
        if not self.allow_division_by_decimal:
            if self.variant in [101, 103, 105, 107, ]:
                if not is_integer(self.nb2):
                    if self.variant == 'decimal1':
                        self.nb1, self.nb2 = self.nb2, self.nb1
                    else:
                        self.nb1, self.nb2 = move_digits_to(self.nb1,
                                                            from_nb=[self.nb2])
            if self.variant in [109, 110, 113, 114]:
                if not is_integer(self.nb3):
                    if self.variant == 'decimal1':
                        self.nb2, self.nb3 = self.nb3, self.nb2
                    else:
                        self.nb2, self.nb3 = move_digits_to(self.nb2,
                                                            from_nb=[self.nb3])
            if self.variant in [111, 115]:
                self.nb1, self.nb2, self.nb3 = \
                    move_digits_to(self.nb1, from_nb=[self.nb2, self.nb3])
            if self.variant in [174, 175, 178, 179, 181, 183, 185, 187]:
                if not is_integer(self.nb2):
                    if is_integer(self.nb1):
                        self.nb1, self.nb2 = self.nb2, self.nb1
                    else:
                        self.nb2, self.nb1 = remove_digits_from(
                            self.nb2, to=[self.nb1])
            if self.variant in [157, 159, 161, 163, 166, 170, 167, 171]:
                if not is_integer(self.nb3):
                    if is_integer(self.nb2):
                        self.nb2, self.nb3 = self.nb3, self.nb2
                    else:
                        self.nb3, self.nb1, self.nb2 = remove_digits_from(
                            self.nb3, to=[self.nb1, self.nb2])

    def _create_100_104(self):
        # (a + b)×c    (a - b)×c
        ops = '+' if self.variant == 100 else '-'
        opn = 1 if self.variant == 100 else -1
        c = self.nb2
        a, b = split_nb(self.nb1, operation=ops,
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb1))
        self.obj = Product([Sum([Item(a), Item(opn * b)]),
                            Item(c)])
        self.watch('no negative; c isnt 1; decimals distribution', a, b, c)

    def _create_101_105(self):
        # (a + b)÷c     (a - b)÷c
        ops = '+' if self.variant == 101 else '-'
        opn = 1 if self.variant == 101 else -1
        c = self.nb2
        self.nb1 = self.nb1 * self.nb2
        a, b = split_nb(self.nb1, operation=ops,
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb1))
        self.obj = Division(('+', Sum([a, opn * b]), c))
        self.watch('no negative; c isnt 1; c isnt deci; decimals distribution',
                   a, b, c)

    def _create_102_106(self):
        # a×(b + c)     a×(b - c)
        ops = '+' if self.variant == 101 else '-'
        opn = 1 if self.variant == 101 else -1
        a = self.nb1
        b, c = split_nb(self.nb2, operation=ops,
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb2))
        self.obj = Product([Item(a),
                            Sum([Item(b), Item(opn * c)])],
                           compact_display=False)
        self.watch('no negative; a isnt 1; decimals distribution', a, b, c)

    def _create_103_107(self):
        # a÷(b + c)     a÷(b - c)
        ops = '+' if self.variant == 101 else '-'
        opn = 1 if self.variant == 101 else -1
        a = self.nb1 * self.nb2
        b, c = split_nb(self.nb2, operation=ops,
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb2, N=a))
        self.obj = Division(('+', a, Sum([b, opn * c])))
        d = b + opn * c
        self.watch('no negative; d isnt deci; decimals distribution',
                   a, b, c, d)

    def _create_108_112(self):
        # a×(b ± c)×d
        ops = '+' if self.variant == 108 else '-'
        opn = 1 if self.variant == 108 else -1
        a = self.nb1
        d = self.nb3
        b, c = split_nb(self.nb2, operation=ops,
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb2, N=a, P=d))
        self.obj = Product([Item(a),
                            Sum([Item(b), Item(opn * c)]),
                            Item(d)],
                           compact_display=False)
        self.watch('no negative; a isnt 1; d isnt 1; decimals distribution',
                   a, b, c, d)

    def _create_109_113(self):
        # a×(b ± c)÷d
        ops = '+' if self.variant == 109 else '-'
        opn = 1 if self.variant == 109 else -1
        a = self.nb1
        d = self.nb3
        nb2 = self.nb2
        self.nb2 = self.nb2 * self.nb3
        b, c = split_nb(self.nb2, operation=ops,
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

    def _create_110_114(self):
        # a÷(b ± c)×d
        ops = '+' if self.variant == 110 else '-'
        opn = 1 if self.variant == 110 else -1
        a = self.nb2 * self.nb3
        d = self.nb1
        b, c = split_nb(self.nb3, operation=ops,
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb3, N=a, P=d))
        self.obj = Product([Division(('+', a, Sum([b, opn * c]))),
                            d],
                           compact_display=False)
        e = self.nb3
        self.watch('no negative; d isnt 1; e isnt deci; '
                   'decimals distribution', a, b, c, d, e)

    def _create_111_115(self):
        # a÷(b ± c)÷d
        ops = '+' if self.variant == 111 else '-'
        opn = 1 if self.variant == 111 else -1
        a = self.nb1 * self.nb2 * self.nb3
        d = self.nb3
        b, c = split_nb(self.nb2, operation=ops,
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb2, N=a, P=d))
        self.obj = Division(('+',
                             Division(('+', a, Sum([b, opn * c]))),
                             d))
        e = self.nb2
        self.watch('no negative; d isnt 1; d isnt deci; '
                   'e isnt deci; decimals distribution', a, b, c, d, e)

    def _create_156to171(self):
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
        c, d = split_nb(self.nb3, operation=cd_signs[self.variant],
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
                remove_digits_from(self.nb1, to=[self.nb3])
            except ValueError:
                self.nb3 += random.choice([i for i in range(-4, 5) if i != 0])
                remove_digits_from(self.nb1, to=[self.nb3])
        c, d = self.nb2, self.nb3
        if self.variant in [172, 173, 176, 177, 180, 182, 184, 186]:
            a, b = split_nb(self.nb1, operation=b_signs[self.variant],
                            dig=self.adjust_depth(self.allow_extra_digits,
                                                  n=self.nb1, N=c, P=d))
        else:
            a, b = split_nb(self.nb1 * self.nb2,
                            operation=b_signs[self.variant],
                            dig=self.adjust_depth(self.allow_extra_digits,
                                                  n=self.nb1 * self.nb2,
                                                  N=c, P=d))
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

    def __init__(self, numbers_to_use, **options):
        super().setup("minimal", **options)
        super().setup("numbers", nb=numbers_to_use, shuffle_nbs=False,
                      **options)
        super().setup("nb_variants", **options)
        super().setup('logging', **options)

        self.adjust_numbers()
        self.expression = None
        self.obj = None

        catalog = dict.fromkeys([100, 104], self._create_100_104)
        catalog.update(dict.fromkeys([101, 105], self._create_101_105))
        catalog.update(dict.fromkeys([102, 106], self._create_102_106))
        catalog.update(dict.fromkeys([103, 107], self._create_103_107))
        catalog.update(dict.fromkeys([108, 112], self._create_108_112))
        catalog.update(dict.fromkeys([109, 113], self._create_109_113))
        catalog.update(dict.fromkeys([110, 114], self._create_110_114))
        catalog.update(dict.fromkeys([111, 115], self._create_111_115))

        catalog.update(dict.fromkeys([156 + i for i in range(16)],
                                     self._create_156to171))
        catalog.update(dict.fromkeys([172 + i for i in range(16)],
                                     self._create_172to187))

        try:
            catalog[self.variant]()
        except KeyError:
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
