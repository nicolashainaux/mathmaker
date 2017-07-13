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
from string import ascii_lowercase as alphabet

from mathmaker import settings
from mathmaker.lib import shared
from mathmaker.lib.tools.auxiliary_functions \
    import (is_integer, move_digits_to, split_nb, digits_nb,
            remove_digits_from)
from mathmaker.lib.core.base_calculus import (Item, Sum, Product, Division,
                                              Expandable)
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
        decimals distribution: will check if there are only integers when one
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
            elif r == 'decimals distribution':
                if not self.nb_variant.startswith('decimal'):
                    max_dn = 0
                else:
                    max_dn = int(self.nb_variant[-1])
                if any(digits_nb(n) > max_dn for n in letters):
                    msg += 'At least a number among ' \
                        + ', '.join(alphabet[0:len(letters) - 1]) + ' and ' \
                        + alphabet[len(letters) - 1] \
                        + ' has more digits than expected ({})'.format(max_dn)
                if (self.nb_variant.startswith('decimal')
                    and all(digits_nb(n) == 0 for n in letters)):
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
        elif self.variant in [108, 112, 109, 113, 110, 114, 111, 115,
                              148, 149, 150, 151, 152, 153, 154, 155]:
            # a×(b ± c)×d   a×(b ± c)÷d  a÷(b ± c)×d  a÷(b ± c)÷d
            # (a ± b)×c ± d;    (a ± b)÷c ± d
            # and their symmetrics d ± (a ± b)×c;    d ± (a ± b)÷c
            N, P = kwargs['N'], kwargs['P']
            return max(depth,
                       mad - digits_nb(N) - digits_nb(P),
                       random.choice([i for i in range(mad + 1)]))
        elif 132 <= self.variant <= 139:
            # (a±b)×(c±d) and (a±b)÷(c±d)
            last = kwargs.get('last', False)
            if (self.nb_variant.startswith('decimal')
                and is_integer(n)):
                if (n == 1 or
                    (last
                     and is_integer(kwargs['N']) and is_integer(kwargs['P']))):
                    return max(depth, int(self.nb_variant[-1]))
                else:
                    return depth + random.choice([i for i in range(mad + 1)])
            else:
                return depth + random.choice([i for i in range(mad + 1)])
        elif 140 <= self.variant <= 147:
            # a ± b×(c ± d) and a ± b÷(c ± d)
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
        if (116 <= self.variant <= 131
            and self.nb_variant.startswith('decimal')
            and self.deci_restriction == '+-'):
            super().setup('nb_variants', bypass=True)
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
            if self.variant in [117, 119, 121, 123, 125, 129]:
                # sys.stderr.write('\nnb1; nb2; nb3; nb4 = {}; {}; {}; {}'
                #                  .format(self.nb1, self.nb2,
                #                          self.nb3, self.nb4))
                if not is_integer(self.nb4):
                    try:
                        self.nb4, self.nb3, self.nb1 = \
                            remove_digits_from(self.nb4, to=[self.nb3,
                                                             self.nb1])
                    except ValueError:
                        # Impossible case. We give up, there won't be a
                        # decimal :-/
                        self.nb2, self.nb4 = \
                            move_digits_to(self.nb2, from_nb=[self.nb4, ])
            if self.variant == 122:
                if not is_integer(self.nb2):
                    try:
                        if random.choice([True, False]):
                            self.nb2, self.nb3, self.nb4 = \
                                remove_digits_from(self.nb2,
                                                   to=[self.nb3, self.nb4])
                        else:
                            self.nb2, self.nb4, self.nb3 = \
                                remove_digits_from(self.nb2,
                                                   to=[self.nb4, self.nb3])
                    except ValueError:
                        # Impossible case. We give up, there won't be a
                        # decimal :-/
                        if random.choice([True, False]):
                            self.nb4, self.nb2 = \
                                move_digits_to(self.nb4, from_nb=[self.nb2, ])
                        else:
                            self.nb3, self.nb2 = \
                                move_digits_to(self.nb4, from_nb=[self.nb3, ])

            # Processing for variant 118 is specific to 118, so it's not
            # factorized here with others.
            # 119 should be moved to 119, too
            if self.variant == 119:
                if not is_integer(self.nb2) and is_integer(self.nb3):
                    if self.nb3 % 10 == 0 or random.choice([True, False]):
                        self.nb1, self.nb2 = move_digits_to(self.nb1,
                                                            from_nb=[self.nb2])
                    else:
                        self.nb3, self.nb2 = move_digits_to(self.nb3,
                                                            from_nb=[self.nb2])
                if is_integer(self.nb2) and not is_integer(self.nb3):
                    self.nb2 += int(self.nb2 + self.nb3 + 1) \
                        - (self.nb2 + self.nb3)
            if self.variant in [126, 130]:
                if not is_integer(self.nb4):
                    choice = random.choice([1, 2, 3])
                    try:
                        if choice is 1:
                            self.nb4, self.nb1, self.nb2, self.nb3 = \
                                remove_digits_from(self.nb4,
                                                   to=[self.nb1, self.nb2,
                                                       self.nb3])
                        elif choice is 2:
                            self.nb4, self.nb2, self.nb3, self.nb1 = \
                                remove_digits_from(self.nb4,
                                                   to=[self.nb2, self.nb3,
                                                       self.nb1])
                        elif choice is 3:
                            self.nb4, self.nb3, self.nb1, self.nb2 = \
                                remove_digits_from(self.nb4,
                                                   to=[self.nb3, self.nb1,
                                                       self.nb2])
                    except ValueError:
                        rnd = random.choice([i
                                             for i in range(-4, 5)
                                             if i != 0])
                        if choice is 1:
                            self.nb1 += rnd
                            self.nb4, self.nb1 = \
                                remove_digits_from(self.nb4, to=[self.nb1])
                        elif choice is 2:
                            self.nb2 += rnd
                            self.nb4, self.nb2 = \
                                remove_digits_from(self.nb4, to=[self.nb2])
                        elif choice is 3:
                            self.nb3 += rnd
                            self.nb4, self.nb3 = \
                                remove_digits_from(self.nb4, to=[self.nb3])
            if self.variant in [127, 131]:
                rnd = random.choice([i for i in range(-4, 5) if i != 0])
                if not is_integer(self.nb2):
                    try:
                        self.nb2, self.nb1, self.nb3 = remove_digits_from(
                            self.nb2, to=[self.nb1, self.nb3])
                    except ValueError:
                        self.nb1 += rnd
                        self.nb2, self.nb1 = remove_digits_from(
                            self.nb2, to=[self.nb1])
                if not is_integer(self.nb4):
                    try:
                        self.nb4, self.nb3, self.nb1 = remove_digits_from(
                            self.nb4, to=[self.nb3, self.nb1])
                    except ValueError:
                        self.nb3 += rnd
                        self.nb4, self.nb3 = remove_digits_from(
                            self.nb4, to=[self.nb3])
            if self.variant in [133, 135, 137, 139, 150, 151, 154, 155]:
                if not is_integer(self.nb2):
                    if is_integer(self.nb1):
                        self.nb1, self.nb2 = self.nb2, self.nb1
                    else:
                        self.nb2, self.nb1 = remove_digits_from(
                            self.nb2, to=[self.nb1])
            if self.variant in [141, 143, 145, 147]:
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
        self.watch('no negative; a isnt 1; d isnt deci; decimals distribution',
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

    def _create_116_120_124(self):
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
        self.watch('no negative; decimals distribution', a, b, c, d)

    def _create_117_121_125_129(self):
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
        self.watch('no negative; decimals distribution; d isnt 1', a, b, c, d)
        if self.variant in [117, 121]:
            self.watch('a isnt 1; d isnt deci', a, b, c, d)
        elif self.variant in [125, 129]:
            self.watch('b isnt 1; b isnt deci', a, b, c, d)

    def _create_118(self):
        # a÷(b + c×d)
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and not is_integer(a)
            and all(is_integer(x) for x in [b, c, d])
            and is_integer(a * (b + c * d))):
            try:
                a, b, c, d = remove_digits_from(a, to=[b, c, d])
            except ValueError:
                rnd = random.choice([i for i in range(-4, 5) if i != 0])
                choice = random.choice([1, 2, 3])
                if choice is 1:
                    b += rnd
                elif choice is 2:
                    c += rnd
                else:
                    d += rnd
                a, b, c, d = remove_digits_from(a, to=[b, c, d])
        if (not self.allow_division_by_decimal
            and self.nb_variant.startswith('decimal')
            and not is_integer(b + c * d)):
            if not is_integer(b):
                # For instance, b + c×d is 0.8 + 10×6
                try:
                    b, c, d = remove_digits_from(b, to=[c, d])
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
                    b, c, d = remove_digits_from(b, to=[c, d])
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
        self.watch('no negative; decimals distribution; c isnt 1; d isnt 1; '
                   'e isnt deci', a, b, c, d, e)

    def _create_119(self):
        # a÷(b + c÷d)
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and not is_integer(a)
            and all(is_integer(x) for x in [b, c, d])
            and is_integer(a * (b + c))):
            try:
                a, b, c = remove_digits_from(a, to=[b, c])
            except ValueError:
                rnd = random.choice([i for i in range(-4, 5) if i != 0])
                if random.choice([True, False]):
                    b += rnd
                else:
                    c += rnd
                a, b, c = remove_digits_from(a, to=[b, c])
        if (not self.allow_division_by_decimal
            and self.nb_variant.startswith('decimal')
            and not is_integer(b + c)):
            if not is_integer(b):
                try:
                    b, c = remove_digits_from(b, to=[c])
                except ValueError:
                    c += random.choice([i for i in range(-4, 5)])
                    b, c = remove_digits_from(b, to=[c])
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
        self.watch('no negative; decimals distribution; d isnt 1; '
                   'd isnt deci; e isnt deci', a, b, c, d, e)

    def _create_122(self):
        # a÷(b - c×d)
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and not is_integer(a)
            and all(is_integer(x) for x in [b, c, d])
            and is_integer(a * b)):
            try:
                a, c, d = remove_digits_from(a, to=[c, d])
                # sys.stderr.write('\n(I) a turned into = {}'.format(a))
            except ValueError:
                rnd = random.choice([i for i in range(-4, 5)])
                if random.choice([True, False]):
                    c += rnd
                else:
                    d += rnd
                a, c, d = remove_digits_from(a, to=[c, d])
                # sys.stderr.write('\n(II) a turned into = {}'.format(a))
        if (not self.allow_division_by_decimal
            and self.nb_variant.startswith('decimal')
            and not is_integer(b - c * d)):
            if not is_integer(b):
                try:
                    b, c, d = remove_digits_from(b, to=[c, d])
                    # sys.stderr.write('\n(1) b turned to = {}'.format(b))
                except ValueError:
                    rnd = random.choice([i for i in range(-4, 5)])
                    if random.choice([True, False]):
                        c += rnd
                    else:
                        d += rnd
                    b, c, d = remove_digits_from(b, to=[c, d])
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
        self.watch('no negative; decimals distribution; c isnt 1; d isnt 1; '
                   'e isnt deci', a, b, c, d, e)

    def _create_123(self):
        # a÷(b - c÷d)
        a, b, c, d = self.nb1, self.nb2, self.nb3, self.nb4
        if (self.nb_variant.startswith('decimal')
            and not is_integer(a)
            and all(is_integer(x) for x in [b, c, d])
            and is_integer(a * b)):
            try:
                a, c = remove_digits_from(a, to=[c])
            except ValueError:
                c += random.choice([i for i in range(-4, 5) if i != 0])
                a, c = remove_digits_from(a, to=[c])
        if (not self.allow_division_by_decimal
            and self.nb_variant.startswith('decimal')
            and not is_integer(b - c)):
            if not is_integer(b):
                try:
                    b, c = remove_digits_from(b, to=[c])
                except ValueError:
                    c += random.choice([i for i in range(-4, 5) if i != 0])
                    b, c = remove_digits_from(b, to=[c])
        a = a * b
        b = b + c
        c = c * d
        self.obj = Division(('+', a, Sum([b, Division(('-', c, d))])))
        # a÷(b - c÷d)
        e = b - c / d
        self.watch('no negative; decimals distribution; d isnt 1; '
                   'd isnt deci; e isnt deci', a, b, c, d, e)

    def _create_126(self):
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
                    c, a, b = remove_digits_from(c, to=[a, b])
                except ValueError:
                    rnd = random.choice([i for i in range(-4, 5) if i != 0])
                    if random.choice([True, False]):
                        a += rnd
                    else:
                        b += rnd
                    c, a, b = remove_digits_from(c, to=[a, b])
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
                        a, c = remove_digits_from(a, to=[c])
                    except ValueError:
                        c += random.choice([i + 1 for i in range(9)])
                        a, c = remove_digits_from(a, to=[c])
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
        self.watch('no negative; decimals distribution; d isnt 1; '
                   'd isnt deci; a isnt 1; b isnt 1', a, b, c, d)

    def _create_127_131(self):
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
                    c, a = remove_digits_from(c, to=[a])
                except ValueError:
                    a += random.choice([i for i in range(-4, 5) if i != 0])
                    c, a = remove_digits_from(c, to=[a])
            else:
                d += random.choice([-1, 1])
                if d == 1:
                    d = 3
        elif (self.nb_variant == 'decimal1'
              and is_integer(a * b)
              and not is_integer(a)):
            if not is_integer(c * d / 10):
                try:
                    a, c = remove_digits_from(a, to=[c])
                except ValueError:
                    c += random.choice([i for i in range(-4, 5) if i != 0])
                    a, c = remove_digits_from(a, to=[c])
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
        self.watch('no negative; decimals distribution; d isnt 1; '
                   'd isnt deci; b isnt 1; b isnt deci', a, b, c, d)

    def _create_128_130(self):
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
        watch_rules = 'no negative; decimals distribution'
        if self.variant == 130:
            watch_rules += '; d isnt deci'
        self.watch(watch_rules, a, b, c, d)

    def _create_132to139(self):
        ab_signs = dict.fromkeys([132, 133, 134, 135], '+')
        ab_signs.update(dict.fromkeys([136, 137, 138, 139], '-'))
        cd_signs = dict.fromkeys([132, 133, 136, 137], '+')
        cd_signs.update(dict.fromkeys([134, 135, 138, 139], '-'))
        opn_signs = {'+': 1, '-': -1}
        if self.variant in [132, 134, 136, 138]:
            a, b = split_nb(self.nb1, operation=ab_signs[self.variant],
                            dig=self.adjust_depth(self.allow_extra_digits,
                                                  n=self.nb1))
        else:
            a, b = split_nb(self.nb1 * self.nb2,
                            operation=ab_signs[self.variant],
                            dig=self.adjust_depth(self.allow_extra_digits,
                                                  n=self.nb1 * self.nb2))
        c, d = split_nb(self.nb2, operation=cd_signs[self.variant],
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb2, last=True,
                                              N=a, P=b))
        nabs = opn_signs[ab_signs[self.variant]]
        ncds = opn_signs[cd_signs[self.variant]]
        if self.variant in [132, 134, 136, 138]:
            self.obj = Product([Sum([a, nabs * b]),
                                Sum([c, ncds * d])],
                               compact_display=False)
        else:
            self.obj = Division(('+',
                                 Sum([a, nabs * b]),
                                 Sum([c, ncds * d])))
        e = self.nb2
        watch_rules = 'no negative; decimals distribution'
        if self.variant in [133, 135, 137, 139]:
            watch_rules += '; e isnt deci'
        self.watch(watch_rules, a, b, c, d, e)

    def _create_140to147(self):
        b_signs = dict.fromkeys([140, 141, 142, 143], '+')
        b_signs.update(dict.fromkeys([144, 145, 146, 147], '-'))
        cd_signs = dict.fromkeys([140, 141, 144, 145], '+')
        cd_signs.update(dict.fromkeys([142, 143, 146, 147], '-'))
        opn_signs = {'+': 1, '-': -1}
        nbs = opn_signs[b_signs[self.variant]]
        ncds = opn_signs[cd_signs[self.variant]]
        a = self.nb1
        if self.variant in [141, 143, 145, 147]:
            b = self.nb2 * self.nb3
        else:
            b = self.nb2
        if self.subvariant == 'only_positive':
            if self.variant in [144, 146]:
                if a - b * self.nb3 < 0:
                    a += b * self.nb3
            elif self.variant in [145, 147]:
                if a - b < 0:
                    a += b
        c, d = split_nb(self.nb3, operation=cd_signs[self.variant],
                        dig=self.adjust_depth(self.allow_extra_digits,
                                              n=self.nb3, N=a, P=b))
        if self.variant in [140, 142, 144, 146]:
            self.obj = Sum([a,
                            Product([nbs * b,
                                     Sum([c, ncds * d])],
                                    compact_display=False)])
        elif self.variant in [141, 143, 145, 147]:
            self.obj = Sum([a,
                            Division((b_signs[self.variant],
                                      b,
                                      Sum([c, ncds * d])))])
        e = self.nb3
        watch_rules = 'no negative; decimals distribution'
        if self.variant in [141, 143, 145, 147]:
            watch_rules += '; e isnt deci'
        elif self.variant in [140, 142, 144, 146]:
            watch_rules += '; b isnt 1'
        self.watch(watch_rules, a, b, c, d, e)

    def _create_148to155(self):
        # (a ± b)×c ± d;    (a ± b)÷c ± d
        # and their symmetrics d ± (a ± b)×c;    d ± (a ± b)÷c
        b_signs = dict.fromkeys([148, 149, 150, 151], '+')
        b_signs.update(dict.fromkeys([152, 153, 154, 155], '-'))
        d_signs = dict.fromkeys([148, 150, 152, 154], '+')
        d_signs.update(dict.fromkeys([149, 151, 153, 155], '-'))
        opn_signs = {'+': 1, '-': -1}
        nbs = opn_signs[b_signs[self.variant]]
        nds = opn_signs[d_signs[self.variant]]
        symm = False
        if (self.nb_variant.startswith('decimal')
            and self.variant in [150, 151, 154, 155]
            and not is_integer(self.nb1)
            and is_integer(self.nb1 * self.nb2)):
            try:
                remove_digits_from(self.nb1, to=[self.nb3])
            except ValueError:
                self.nb3 += random.choice([i for i in range(-4, 5) if i != 0])
                remove_digits_from(self.nb1, to=[self.nb3])
        c, d = self.nb2, self.nb3
        if self.variant in [148, 149, 152, 153]:
            a, b = split_nb(self.nb1, operation=b_signs[self.variant],
                            dig=self.adjust_depth(self.allow_extra_digits,
                                                  n=self.nb1, N=c, P=d))
        else:
            a, b = split_nb(self.nb1 * self.nb2,
                            operation=b_signs[self.variant],
                            dig=self.adjust_depth(self.allow_extra_digits,
                                                  n=self.nb1 * self.nb2,
                                                  N=c, P=d))
        if self.subvariant == 'only_positive' and self.variant in [149, 153]:
            if self.nb1 * self.nb2 < self.nb3:
                symm = True
        elif self.subvariant == 'only_positive' and self.variant in [151, 155]:
            if self.nb1 < self.nb3:
                symm = True
        else:
            symm = random.choice([True, False])
        if self.variant in [148, 149, 152, 153]:
            if symm:
                self.obj = Sum([d,
                                Product([Expandable((Item(nds),
                                                     Sum([a, nbs * b]))),
                                         c], compact_display=False)])
            else:
                self.obj = Sum([Product([Sum([a, nbs * b]), c],
                                        compact_display=False),
                                nds * d])
        elif self.variant in [150, 151, 154, 155]:
            if symm:
                self.obj = Sum([d,
                                Division((d_signs[self.variant],
                                          Sum([a, nbs * b]),
                                          c))])
            else:
                self.obj = Sum([Division(('+',
                                          Sum([a, nbs * b]),
                                          c)),
                                nds * d])
        watch_rules = 'no negative; decimals distribution; c isnt 1'
        if self.variant in [150, 151, 154, 155]:
            watch_rules += '; c isnt deci'
        self.watch(watch_rules, a, b, c, d)

    def __init__(self, numbers_to_use, **options):
        super().setup("minimal", **options)
        super().setup("numbers", nb=numbers_to_use, shuffle_nbs=False,
                      **options)
        super().setup("nb_variants", **options)

        self.log = settings.output_watcher_logger.debug

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
        catalog.update(dict.fromkeys([116, 120, 124],
                                     self._create_116_120_124))
        catalog.update(dict.fromkeys([117, 121, 125, 129],
                                     self._create_117_121_125_129))
        catalog.update(dict.fromkeys([118], self._create_118))
        catalog.update(dict.fromkeys([119], self._create_119))
        catalog.update(dict.fromkeys([122], self._create_122))
        catalog.update(dict.fromkeys([123], self._create_123))
        catalog.update(dict.fromkeys([126], self._create_126))
        catalog.update(dict.fromkeys([127, 131], self._create_127_131))
        catalog.update(dict.fromkeys([128, 130], self._create_128_130))
        catalog.update(dict.fromkeys([132, 133, 134, 135, 136, 137, 138, 139],
                                     self._create_132to139))
        catalog.update(dict.fromkeys([140, 141, 142, 143, 144, 145, 146, 147],
                                     self._create_140to147))
        catalog.update(dict.fromkeys([148, 149, 150, 151, 152, 153, 154, 155],
                                     self._create_148to155))

        try:
            catalog[self.variant]()
        except KeyError:
            raise ValueError('Unknown variant identifier for priorities_in'
                             '_calculation_without_parentheses: {}'
                             .format(str(self.variant)))

        # 132: (a + b)×(c + d)
        # 133: (a + b)÷(c + d)
        # 134: (a + b)×(c - d)
        # 135: (a + b)÷(c - d)
        # 136: (a - b)×(c + d)
        # 137: (a - b)÷(c + d)
        # 138: (a - b)×(c - d)
        # 139: (a - b)÷(c - d)

        # 140: a + b×(c + d)        # 148: (a + b)×c + d
        # 141: a + b÷(c + d)        # 149: (a + b)×c - d
        # 142: a + b×(c - d)        # 150: (a + b)÷c + d
        # 143: a + b÷(c - d)        # 151: (a + b)÷c - d
        # 144: a - b×(c + d)        # 152: (a - b)×c + d
        # 145: a - b÷(c + d)        # 153: (a - b)×c - d
        # 146: a - b×(c - d)        # 154: (a - b)÷c + d
        # 147: a - b÷(c - d)        # 155: (a - b)÷c - d

        self.expression = Expression(shared.number_of_the_question,
                                     self.obj)
        self.expression_str = self.expression.printed
        shared.number_of_the_question += 1

    def q(self, **options):
        return shared.machine.write_math_style2(self.expression_str)

    def a(self, **options):
        return shared.machine.write(
            self.expression.auto_expansion_and_reduction(**options))
