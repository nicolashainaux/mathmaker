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
import sys
from decimal import Decimal
from string import ascii_lowercase as alphabet

from mathmaker import settings
from mathmaker.lib import shared
from mathmaker.lib.tools.auxiliary_functions \
    import (is_integer, move_decimal, split_nb, digits_nb, force_shift_decimal)
from mathmaker.lib.core.base_calculus import Item, Sum, Product, Division
from mathmaker.lib.core.calculus import Expression
from .. import submodule

# Possible variants are identified with a number:
# A partial symmetric of a variant is identified with a *
# a symmetric of a variant is identified with a **
# see 128 for instance.

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
# 127*: (c + a÷b)÷d
# 128: (a×b - c)×d          # 136: (a - b)×(c + d)
# 128*: (c - a×b)×d
# 128**: d×(a×b - c)
# 128*** is 120
# 129: (a÷b - c)×d          # 137: (a - b)÷(c + d)
# 129*: (c - a÷b)×d
# 129**: d×(a÷b - c)
# 129*** is 121
# 130: (a×b - c)÷d          # 138: (a - b)×(c - d)
# 130*: (c - a×b)÷d
# 131: (a÷b - c)÷d          # 139: (a - b)÷(c - d)
# 131*: (c - a÷b)÷d

# 140: a + b×(c + d)        # 148: (a + b)×c + d
# 141: a + b÷(c + d)        # 149: (a + b)×c - d
# 142: a + b×(c - d)        # 150: (a + b)÷c + d
# 143: a + b÷(c - d)        # 151: (a + b)÷c - d
# 144: a - b×(c + d)        # 152: (a - b)×c + d
# 145: a - b÷(c + d)        # 153: (a - b)×c - d
# 146: a - b×(c - d)        # 154: (a - b)÷c + d
# 147: a - b÷(c - d)        # 155: (a - b)÷c - d


class sub_object(submodule.structure):

    def dbg_info(self, msg, *letters):
        """
        Create log message to record including self.nb* and a, b, c... values.

        :param msg: the msg to join to the values' list
        :type msg: str
        :param letters: the values of the numbers a, b, c etc.
        :type letters: numbers
        :rtype: str
        """
        figures = '123456789'
        nb = 'nb' + '; nb'.join(figures[:len(self.nb_list)]) + " = " \
            + '; '.join('{}' for _ in range(len(self.nb_list))) \
            .format(*self.nb_list)
        abcd = '; '.join(alphabet[0:len(letters)]) + " = " \
            + '; '.join('{}' for _ in range(len(letters))) \
            .format(*letters)
        return ('(variant {}): \\n{} {}\\n'
                + ''.join([' ' for _ in range(len(msg) + 1)]) + '{}') \
            .format(self.variant, msg, nb, abcd)

    def watch(self, rules, *letters):
        """
        Check the quality of numbers created, according to the rules.

        If something is wrong, it will be logged.

        Possible rules:
        no negative: will check if there's any negative when only positive
                     numbers were expected
        not all integers: will check if there are only integers when one
                          decimal number at least was expected.
        <letter> isnt deci: check this letter does not contain a decimal
                            when division by a decimal is not allowed
        <letter> isnt 1: check this letter is different from 1
                         under any circumstances

        :param rules: a string containing rules separated by '; '. See above
                      for possible rules
        :type rules: str
        :param letters: the values of the numbers a, b, c etc.
        :type letters: numbers
        """
        for r in rules.split(sep='; '):
            msg = ''
            if r == 'no negative' and self.subvariant == 'only_positive':
                if any([n < 0 for n in letters]):
                    msg += 'Negative number detected!'
            elif (r == 'not all integers'
                  and self.nb_variant.startswith('decimal')):
                if all(is_integer(n) for n in letters):
                    msg += ', '.join(alphabet[0:len(letters) - 1]) + ' and ' \
                        + alphabet[len(letters) - 1] + ' are all integers!'
            elif r.endswith('isnt 1'):
                if letters[alphabet.index(r[0])] == 1:
                    msg += r[0] + ' == 1!'
            elif (r.endswith('isnt deci')
                  and not self.allow_division_by_decimal):
                if not is_integer(letters[alphabet.index(r[0])]):
                    msg += r[0] + ' is decimal! => Division by decimal!'
            if msg != '':
                self.log(self.dbg_info(msg, *letters))

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
        if (self.nb_variant.startswith('decimal')
            and self.deci_restriction == '+-'):
            return max(depth, digits_nb(n) + 1)
        if self.variant in [100, 102, 104, 106]:
            # (a + b)×c  a×(b + c)  (a - b)×c  a×(b - c)
            if self.nb_variant == 'decimal1' and is_integer(n):
                return depth + random.choice([0, 1])
        elif self.variant in [101, 105]:  # (a + b)÷c
            if (not self.allow_division_by_decimal
                and self.nb_variant == 'decimal1'
                and is_integer(n)):
                return max(depth, digits_nb(n) + 1)
        elif self.variant in [103, 107]:  # a÷(b + c) a÷(b + c)
            N = kwargs['N']
            if (self.nb_variant.startswith('decimal')
                and is_integer(N)):
                return max(depth, digits_nb(n) + 1)
            elif self.nb_variant == 'decimal1' and is_integer(n):
                return depth + random.choice([0, 1])
        elif self.variant in [108, 112, 109, 113, 110, 114, 111, 115]:
            # a×(b ± c)×d   a×(b ± c)÷d  a÷(b ± c)×d  a÷(b ± c)÷d
            N, P = kwargs['N'], kwargs['P']
            if (self.nb_variant.startswith('decimal')
                and all(is_integer(x) for x in [n, N, P])):
                return max(depth, digits_nb(n) + 1)
            elif self.nb_variant == 'decimal1' and is_integer(n):
                return depth + random.choice([0, 1])
        return depth

    def adjust_numbers(self):
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
                    move_decimal(self.nb1, numbers=[self.nb2, self.nb3])
            if self.variant in [117, 119, 121, 123, 125, 129]:
                # sys.stderr.write('\nnb1; nb2; nb3; nb4 = {}; {}; {}; {}'
                #                  .format(self.nb1, self.nb2,
                #                          self.nb3, self.nb4))
                if not is_integer(self.nb4):
                    try:
                        self.nb4, self.nb3, self.nb1 = \
                            force_shift_decimal(self.nb4, wishlist=[self.nb3,
                                                                    self.nb1])
                    except ValueError:
                        # Impossible case. We give up, there won't be a
                        # decimal :-/
                        self.nb2, self.nb4 = \
                            move_decimal(self.nb2, numbers=[self.nb4, ])
            if self.variant == 122:
                if not is_integer(self.nb2):
                    try:
                        if random.choice([True, False]):
                            self.nb2, self.nb3, self.nb4 = \
                                force_shift_decimal(self.nb2,
                                                    wishlist=[self.nb3,
                                                              self.nb4])
                        else:
                            self.nb2, self.nb4, self.nb3 = \
                                force_shift_decimal(self.nb2,
                                                    wishlist=[self.nb4,
                                                              self.nb3])
                    except ValueError:
                        # Impossible case. We give up, there won't be a
                        # decimal :-/
                        if random.choice([True, False]):
                            self.nb4, self.nb2 = \
                                move_decimal(self.nb4, numbers=[self.nb2, ])
                        else:
                            self.nb3, self.nb2 = \
                                move_decimal(self.nb4, numbers=[self.nb3, ])

            # Processing for variant 118 is specific to 118, so it's not
            # factorized here with others.
            # 119 should be moved to 119, too
            if self.variant == 119:
                if not is_integer(self.nb2) and is_integer(self.nb3):
                    if self.nb3 % 10 == 0 or random.choice([True, False]):
                        self.nb1, self.nb2 = move_decimal(self.nb1,
                                                          numbers=[self.nb2, ])
                    else:
                        self.nb3, self.nb2 = move_decimal(self.nb3,
                                                          numbers=[self.nb2, ])
                if is_integer(self.nb2) and not is_integer(self.nb3):
                    self.nb2 += int(self.nb2 + self.nb3 + 1) \
                        - (self.nb2 + self.nb3)
            if self.variant in [126, 130]:
                if not is_integer(self.nb4):
                    choice = random.choice([1, 2, 3])
                    try:
                        if choice is 1:
                            self.nb4, self.nb1, self.nb2, self.nb3 = \
                                force_shift_decimal(self.nb4,
                                                    wishlist=[self.nb1,
                                                              self.nb2,
                                                              self.nb3])
                        elif choice is 2:
                            self.nb4, self.nb2, self.nb3, self.nb1 = \
                                force_shift_decimal(self.nb4,
                                                    wishlist=[self.nb2,
                                                              self.nb3,
                                                              self.nb1])
                        elif choice is 3:
                            self.nb4, self.nb3, self.nb1, self.nb2 = \
                                force_shift_decimal(self.nb4,
                                                    wishlist=[self.nb3,
                                                              self.nb1,
                                                              self.nb2])
                    except ValueError:
                        rnd = random.choice([i
                                             for i in range(-5, 6)
                                             if i != 0])
                        if choice is 1:
                            self.nb1 += rnd
                            self.nb4, self.nb1 = \
                                force_shift_decimal(self.nb4,
                                                    wishlist=[self.nb1])
                        elif choice is 2:
                            self.nb2 += rnd
                            self.nb4, self.nb2 = \
                                force_shift_decimal(self.nb4,
                                                    wishlist=[self.nb2])
                        elif choice is 3:
                            self.nb3 += rnd
                            self.nb4, self.nb3 = \
                                force_shift_decimal(self.nb4,
                                                    wishlist=[self.nb3])
            if self.variant in [127, 131]:
                rnd = random.choice([i for i in range(-5, 6) if i != 0])
                if not is_integer(self.nb2):
                    try:
                        self.nb2, self.nb1, self.nb3 = force_shift_decimal(
                            self.nb2, wishlist=[self.nb1, self.nb3])
                    except ValueError:
                        self.nb1 += rnd
                        self.nb2, self.nb1 = force_shift_decimal(
                            self.nb2, wishlist=[self.nb1])
                if not is_integer(self.nb4):
                    try:
                        self.nb4, self.nb3, self.nb1 = force_shift_decimal(
                            self.nb4, wishlist=[self.nb3, self.nb1])
                    except ValueError:
                        self.nb3 += rnd
                        self.nb4, self.nb3 = force_shift_decimal(
                            self.nb4, wishlist=[self.nb3])


    def create_100_104(self):
        # (a + b)×c    (a - b)×c
        ops = '+' if self.variant == 100 else '-'
        opn = 1 if self.variant == 100 else -1
        c = self.nb2
        a, b = split_nb(self.nb1, operation=ops,
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb1))
        self.obj = Product([Sum([Item(a), Item(opn * b)]),
                            Item(c)])
        a = b = c = 3
        self.watch('no negative; c isnt 1; not all integers', a, b, c)

    def create_101_105(self):
        # (a + b)÷c     (a - b)÷c
        ops = '+' if self.variant == 101 else '-'
        opn = 1 if self.variant == 101 else -1
        c = self.nb2
        self.nb1 = self.nb1 * self.nb2
        a, b = split_nb(self.nb1, operation=ops,
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb1))
        self.obj = Division(('+', Sum([a, opn * b]), c))
        self.watch('no negative; c isnt 1; c isnt deci; not all integers',
                   a, b, c)

    def create_102_106(self):
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
        self.watch('no negative; a isnt 1; not all integers', a, b, c)

    def create_103_107(self):
        # a÷(b + c)     a÷(b - c)
        ops = '+' if self.variant == 101 else '-'
        opn = 1 if self.variant == 101 else -1
        a = self.nb1 * self.nb2
        b, c = split_nb(self.nb2, operation=ops,
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb2, N=a))
        self.obj = Division(('+', a, Sum([b, opn * c])))
        d = b + opn * c
        self.watch('no negative; a isnt 1; d isnt deci; not all integers',
                   a, b, c, d)

    def create_108_112(self):
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
        self.watch('no negative; a isnt 1; d isnt 1; not all integers',
                   a, b, c, d)

    def create_109_113(self):
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
                   'not all integers', a, b, c, d)

    def create_110_114(self):
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
        self.watch('no negative; a isnt 1; d isnt 1; d isnt deci; '
                   'e isnt deci; not all integers', a, b, c, d, e)

    def create_111_115(self):
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
        self.watch('no negative; a isnt 1; d isnt 1; d isnt deci; '
                   'e isnt deci; not all integers', a, b, c, d, e)

    def create_116_120_124(self):
        # a×(b ± c×d)   (a×b + c)×d
        opn = 1 if self.variant in [116, 124] else -1
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if self.variant in [116, 124]:
            if ((not self.subvariant == 'only_positive')
                or (self.subvariant == 'only_positive' and b - c * d > 0)):
                b = b - c * d
        else:
            b = b + c * d
        if self.variant in [116, 120]:
            self.obj = Product([a,
                                Sum([b, Product([opn * c, d])])],
                               compact_display=False)
        elif self.variant == 124:
            a, b, c, d = c, d, b, a
            self.obj = Product([Sum([Product([a, b],
                                     compact_display=False),
                                     c]),
                                d], compact_display=False)
        self.watch('no negative; not all integers', a, b, c, d)

    def create_117_121_125_129(self):
        # 117, 121: a×(b ± c÷d)
        # 125, 129, 129*: (a÷b ± c)×d   *(c ± a÷b)×d
        # We won't deal with only integers problems because they cannot show up
        # For instance if c÷d is 4÷5, then b being initially an integer, will
        # become decimal after addition or subtraction of c÷d
        ops = '+' if self.variant in [117, 125] else '-'
        opn = 1 if self.variant in [117, 125] else -1
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        psymm_129 = False
        if self.variant in [117, 125]:
            if ((not self.subvariant == 'only_positive')
                or (self.subvariant == 'only_positive' and b - c > 0)):
                b = b - c
        elif self.variant == 129:
            if ((not self.subvariant == 'only_positive')
                or (self.subvariant == 'only_positive' and c - b > 0)):
                b = c - b
            elif self.subvariant == 'only_positive':
                # Here we have c - b <= 0
                psymm_129 = True
                b = b + c
            if not self.subvariant == 'only_positive':
                psymm_129 = random.choice([True, False])
        else:
            b = b + c
        c = c * d
        if self.variant in [117, 121]:
            self.obj = Product([a,
                                Sum([b, Division((ops, c, d))])],
                               compact_display=False)
        elif self.variant in [125, 129]:
            a, b, c, d = c, d, b, a
            if psymm_129:
                self.obj = Product([Sum([c,
                                         Division(('-', a, b))]),
                                    d], compact_display=False)
            else:
                self.obj = Product([Sum([Division(('+', a, b)),
                                         opn * c]),
                                    d], compact_display=False)
        # a×(b ± c÷d)     (a÷b + c)×d
        self.watch('no negative; not all integers; d isnt 1', a, b, c, d)
        if self.variant in [117, 121]:
            self.watch('a isnt 1; d isnt deci', a, b, c, d)
        elif self.variant in [125, 129]:
            self.watch('b isnt 1; b isnt deci', a, b, c, d)

    def create_118(self):
        # a÷(b + c×d)
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and not is_integer(a)
            and all(is_integer(x) for x in [b, c, d])
            and is_integer(a * (b + c * d))):
            try:
                a, b, c, d = force_shift_decimal(a, wishlist=[b, c, d])
            except ValueError:
                rnd = random.choice([i for i in range(-5, 6) if i != 0])
                choice = random.choice([1, 2, 3])
                if choice is 1:
                    b += rnd
                elif choice is 2:
                    c += rnd
                else:
                    d += rnd
                a, b, c, d = force_shift_decimal(a, wishlist=[b, c, d])
        if (not self.allow_division_by_decimal
            and self.nb_variant.startswith('decimal')
            and not is_integer(b + c * d)):
            if not is_integer(b):
                # For instance, b + c×d is 0.8 + 10×6
                try:
                    b, c, d = force_shift_decimal(b, wishlist=[c, d])
                    # Now it is 8 + 10×0.6
                except ValueError:
                    # Bad luck, it was something like 0.8 + 50×10
                    # (and a = 20). We have to change c or d in order to
                    # ensure one of them at least can be turned into a
                    # decimal
                    rnd = random.choice([i
                                         for i in range(-5, 6)
                                         if i != 0])
                    if random.choice([True, False]):
                        c += rnd
                    else:
                        d += rnd
                    b, c, d = force_shift_decimal(b, wishlist=[c, d])
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
        self.obj = Division(('+', a, Sum([b, Product([c, d])])))
        # a÷(b + c×d)
        e = b + c * d
        self.watch('no negative; not all integers; c isnt 1; d isnt 1; '
                   'e isnt deci', a, b, c, d, e)

    def create_119(self):
        # a÷(b + c÷d)
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and not is_integer(a)
            and all(is_integer(x) for x in [b, c, d])
            and is_integer(a * (b + c))):
            try:
                a, b, c = force_shift_decimal(a, wishlist=[b, c])
            except ValueError:
                rnd = random.choice([i for i in range(-5, 6) if i != 0])
                if random.choice([True, False]):
                    b += rnd
                else:
                    c += rnd
                a, b, c = force_shift_decimal(a, wishlist=[b, c])
        if (not self.allow_division_by_decimal
            and self.nb_variant.startswith('decimal')
            and not is_integer(b + c)):
            if not is_integer(b):
                try:
                    b, c = force_shift_decimal(b, wishlist=[c])
                except ValueError:
                    c += random.choice([i for i in range(-5, 6)])
                    b, c = force_shift_decimal(b, wishlist=[c])
            # Now it's sure b is an integer
            # this doesn't mean that b + c is
            if not is_integer(b + c):
                if ((not self.subvariant == 'only_positive')
                    or (self.subvariant == 'only_positive'
                        and b - c > 0)):
                    b = b - c
                else:
                    x = c
                    y = random.choice([n for n in range(int(b) + 1)])
                    b = Decimal(y) + 1 - (x - int(x))

        a *= (b + c)
        c *= d
        self.obj = Division(('+', a, Sum([b, Division(('+', c, d))])))
        # a÷(b + c÷d)
        e = b + c / d
        self.watch('no negative; not all integers; d isnt 1; d isnt deci; '
                   'e isnt deci', a, b, c, d, e)

    def create_122(self):
        # a÷(b - c×d)
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and not is_integer(a)
            and all(is_integer(x) for x in [b, c, d])
            and is_integer(a * b)):
            try:
                a, c, d = force_shift_decimal(a, wishlist=[c, d])
                # sys.stderr.write('\n(I) a turned into = {}'.format(a))
            except ValueError:
                rnd = random.choice([i for i in range(-5, 6)])
                if random.choice([True, False]):
                    c += rnd
                else:
                    d += rnd
                a, c, d = force_shift_decimal(a, wishlist=[c, d])
                # sys.stderr.write('\n(II) a turned into = {}'.format(a))
        if (not self.allow_division_by_decimal
            and self.nb_variant.startswith('decimal')
            and not is_integer(b - c * d)):
            if not is_integer(b):
                try:
                    b, c, d = force_shift_decimal(b, wishlist=[c, d])
                    # sys.stderr.write('\n(1) b turned to = {}'.format(b))
                except ValueError:
                    rnd = random.choice([i for i in range(-5, 6)])
                    if random.choice([True, False]):
                        c += rnd
                    else:
                        d += rnd
                    b, c, d = force_shift_decimal(b, wishlist=[c, d])
                    # sys.stderr.write('\n(2) b turned to = {}'.format(b))
        # Now it's sure b is an integer
        # this doesn't mean that b - c*d is
        b = b + c * d
        # sys.stderr.write('\n(3) b turned to = {}'.format(b))

        a = self.nb1 * (b - c * d)
        self.obj = Division(('+', a, Sum([b, Product([-c, d])])))
        # sys.stderr.write('\nFINAL a; b; c; d = {}; {}; {}; {}'
        #                  .format(a, b, c, d))
        # a÷(b - c×d)
        e = b - c * d
        self.watch('no negative; not all integers; c isnt 1; d isnt 1; '
                   'e isnt deci', a, b, c, d, e)

    def create_123(self):
        # a÷(b - c÷d)
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and not is_integer(a)
            and all(is_integer(x) for x in [b, c, d])
            and is_integer(a * b)):
            try:
                a, c = force_shift_decimal(a, wishlist=[c])
            except ValueError:
                c += random.choice([i for i in range(-5, 6) if i != 0])
                a, c = force_shift_decimal(a, wishlist=[c])
        if (not self.allow_division_by_decimal
            and self.nb_variant.startswith('decimal')
            and not is_integer(b - c)):
            if not is_integer(b):
                try:
                    b, c = force_shift_decimal(b, wishlist=[c])
                except ValueError:
                    c += random.choice([i for i in range(-5, 6) if i != 0])
                    b, c = force_shift_decimal(b, wishlist=[c])
        a = a * b
        b = b + c
        c = c * d
        self.obj = Division(('+', a, Sum([b, Division(('-', c, d))])))
        # a÷(b - c÷d)
        e = b - c / d
        self.watch('no negative; not all integers; d isnt 1; d isnt deci; '
                   'e isnt deci', a, b, c, d, e)

    def create_126(self):
        # (a×b + c)÷d
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
                    c, a, b = force_shift_decimal(c, wishlist=[a, b])
                except ValueError:
                    rnd = random.choice([i for i in range(-5, 6) if i != 0])
                    if random.choice([True, False]):
                        a += rnd
                    else:
                        b += rnd
                    c, a, b = force_shift_decimal(c, wishlist=[a, b])
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
                        a, c = force_shift_decimal(a, wishlist=[c])
                    except ValueError:
                        c += random.choice([i + 1 for i in range(9)])
                        a, c = force_shift_decimal(a, wishlist=[c])
                    a, b, c, d = c, d, a, b
        if not is_integer(d):
            c, d = d, c
        if a * b == c * d:
            c = c * d
        else:
            c = c * d - a * b
        self.obj = Division(('+',
                             Sum([Product([a, b], compact_display=False), c]),
                             d))
        # (a×b + c)÷d
        self.watch('no negative; not all integers; d isnt 1; d isnt deci; '
                   'a isnt 1; b isnt 1', a, b, c, d)

    def create_127_131(self):
        # (a÷b + c)÷d
        # (a÷b - c)÷d    *(c - a÷b)÷d
        ops = '+' if self.variant == 127 else '-'
        opn = 1 if self.variant == 127 else -1
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant == 'decimal1'
            and is_integer(c * d)
            and not is_integer(c)):
            if not is_integer(a * b / 10):
                try:
                    c, a = force_shift_decimal(c, wishlist=[a])
                except ValueError:
                    a += random.choice([i for i in range(-5, 6) if i != 0])
                    c, a = force_shift_decimal(c, wishlist=[a])
            else:
                d += random.choice([-1, 1])
                if d == 1:
                    d = 3
        elif (self.nb_variant == 'decimal1'
            and is_integer(a * b)
            and not is_integer(a)):
            if not is_integer(c * d / 10):
                try:
                    a, c = force_shift_decimal(a, wishlist=[c])
                except ValueError:
                    c += random.choice([i for i in range(-5, 6) if i != 0])
                    a, c = force_shift_decimal(a, wishlist=[c])
            else:
                b += random.choice([-1, 1])
                if b == 1:
                    b = 3
        psymm = False
        if self.variant == 127:
            if a > c * d and self.subvariant == 'only_positive':
                a, b, c, d = c, d, a, b
            if c * d != a:
                c = c * d - a
            else:
                # Do not forget the case c * d == a:
                c = c * d
            psymm = random.choice([True, False])
        elif self.variant == 131:
            if a <= c * d and self.subvariant == 'only_positive':
                psymm = True
                c = c * d + a
            else:
                if self.subvariant != 'only_positive':
                    psymm = random.choice([True, False])
                if psymm:
                    c = c * d + a
                else:
                    c = a - c * d
        a = a * b
        if psymm:
            self.obj = Division(('+',
                                 Sum([c, Division((ops, a, b))]),
                                 d))
        else:
            self.obj = Division(('+',
                                 Sum([Division(('+', a, b)), opn * c]),
                                 d))
        # (a÷b + c)÷d
        self.watch('no negative; not all integers; d isnt 1; d isnt deci; '
                   'b isnt 1; b isnt deci', a, b, c, d)

    def create_128_130(self):
        # 128, 128*: (a×b - c)×d   *(c - a×b)×d
        # 130, 130*: (a×b - c)÷d   *(c - a×b)÷d
        psymm = False
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if self.variant == 130:
            if (self.nb_variant == 'decimal1'
                and is_integer(c * d)
                and not is_integer(c)):
                # It is enough to swap a,b and c,d in all cases.
                # If this would lead to a negative number, then it is possible
                # to create the symmetric expression
                a, b, c, d = c, d, a, b
            c = c * d
        if self.subvariant == 'only_positive' and a * b < c:
            psymm = True
        elif self.subvariant != 'only_positive':
            psymm = random.choice([True, False])
        if psymm:
            if a * b != c:
                c = a * b + c
            first_factor = Sum([c, Product([-a, b], compact_display=False)])
            if self.variant == 128:
                self.obj = Product([first_factor, d], compact_display=False)
            elif self.variant == 130:
                self.obj = Division(('+', first_factor, d))
        else:
            if a * b != c:
                c = a * b - c
            first_factor = Sum([Product([a, b], compact_display=False), -c])
            if self.variant == 128:
                self.obj = Product([first_factor, d], compact_display=False)
            elif self.variant == 130:
                self.obj = Division(('+', first_factor, d))
        watch_rules = 'no negative; not all integers'
        if self.variant == 130:
            watch_rules += '; d isnt deci'
        self.watch(watch_rules, a, b, c, d)

    def __init__(self, numbers_to_use, **options):
        super().setup("minimal", **options)
        super().setup("numbers", nb=numbers_to_use, shuffle_nbs=False,
                      **options)
        super().setup("nb_variants", nb=numbers_to_use, **options)

        self.log = settings.output_watcher_logger.debug

        self.adjust_numbers()
        self.expression = None
        self.obj = None

        if self.variant in [100, 104]:
            self.create_100_104()
        elif self.variant in [101, 105]:
            self.create_101_105()
        elif self.variant in [102, 106]:
            self.create_102_106()
        elif self.variant in [103, 107]:
            self.create_103_107()
        elif self.variant in [108, 112]:
            self.create_108_112()
        elif self.variant in [109, 113]:
            self.create_109_113()
        elif self.variant in [110, 114]:
            self.create_110_114()
        elif self.variant in [111, 115]:
            self.create_111_115()
        elif self.variant in [116, 120, 124]:
            self.create_116_120_124()
        elif self.variant in [117, 121, 125, 129]:
            self.create_117_121_125_129()
        elif self.variant == 118:
            self.create_118()
        elif self.variant == 119:
            self.create_119()
        elif self.variant == 122:
            self.create_122()
        elif self.variant == 123:
            self.create_123()
        elif self.variant == 126:
            self.create_126()
        elif self.variant in [127, 131]:
            self.create_127_131()
        elif self.variant in [128, 130]:
            self.create_128_130()

                                    # 132: (a + b)×(c + d)
                                    # 133: (a + b)÷(c + d)
                                    # 134: (a + b)×(c - d)
                                    # 135: (a + b)÷(c - d)
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
