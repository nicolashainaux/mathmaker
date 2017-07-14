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
        elif self.variant in [108, 112, 109, 113, 110, 114, 111, 115]:
            # a×(b ± c)×d   a×(b ± c)÷d  a÷(b ± c)×d  a÷(b ± c)÷d
            # (a ± b)×c ± d;    (a ± b)÷c ± d
            # and their symmetrics d ± (a ± b)×c;    d ± (a ± b)÷c
            N, P = kwargs['N'], kwargs['P']
            return max(depth,
                       mad - digits_nb(N) - digits_nb(P),
                       random.choice([i for i in range(mad + 1)]))

    def adjust_numbers(self):
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
