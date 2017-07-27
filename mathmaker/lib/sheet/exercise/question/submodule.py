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
from string import ascii_lowercase as alphabet

from mathmaker.lib.core.root_calculus import Unit, Value
from mathmaker.lib.core.base_calculus import Product, Quotient, Item
from mathmaker.lib.core.base_geometry import Point
from mathmaker.lib.core.geometry import (Rectangle, Square, RightTriangle,
                                         InterceptTheoremConfiguration)
from mathmaker.lib import error
from mathmaker.lib import shared
from mathmaker.lib.common.cst import COMMON_LENGTH_UNITS, XML_BOOLEANS
from mathmaker.lib.tools.wording import setup_wording_format_of
from mathmaker.lib.tools.auxiliary_functions \
    import (rotate, is_integer, digits_nb, )


class structure(object):

    def h(self, **options):
        if hasattr(self, 'hint'):
            return "\hfill" + Value("", unit=self.hint)\
                .into_str(display_SI_unit=True)
        else:
            return ""

    @property
    def nb_list(self):
        return [getattr(self, 'nb' + str(i + 1)) for i in range(self.nb_nb)]

    def setup(self, arg, shuffle_nbs=True, sort_nbs=False, **options):
        if arg == 'logging':
            from mathmaker import settings
            self.log = settings.output_watcher_logger.debug
        elif arg == "minimal":
            self.newline = '\\newline'
            self.parallel_to = '$\parallel$'
            self.belongs_to = '$\in$'
            if 'nb_variant' in options and options['nb_variant'] == 'decimal':
                options['nb_variant'] = random.choice(['decimal1', 'decimal2'])

            self.variant = options.get('variant', "default")
            self.subvariant = options.get('subvariant', "default")
            self.nb_variant = options.get('nb_variant', "default")
            self.deci_restriction = ''
            nbv_chunks = self.nb_variant.split(sep='_')
            if len(nbv_chunks) == 2:
                if nbv_chunks[1] in ['+-', '×÷']:
                    self.deci_restriction += nbv_chunks[1]
                else:
                    warnings.warn('Ignored unrecognized option in nb_variant:'
                                  ' {}'.format(nbv_chunks[1]))
                self.nb_variant = nbv_chunks[0]
            self.context = options.get('context', "default")
            self.picture = XML_BOOLEANS[options.get('picture', "false")]()
            self.decimal_result = int(options.get('decimal_result', 2))
            self.allow_extra_digits = int(options.get('allow_extra_digits', 0))
            self.allow_division_by_decimal = XML_BOOLEANS[
                options.get('allow_division_by_decimal', "false")]()

        elif arg == "length_units":
            if 'unit' in options:
                self.unit_length = Unit(options['unit'])
                self.unit_area = Unit(self.unit_length.name, exponent=2)
                self.length_unit = self.unit_length.name
            else:
                if hasattr(self, 'length_unit'):
                    self.unit_length = Unit(self.length_unit)
                    self.unit_area = Unit(self.unit_length.name, exponent=2)
                elif hasattr(self, 'unit_length'):
                    self.length_unit = self.unit_length.name
                    self.unit_area = Unit(self.unit_length.name, exponent=2)
                else:
                    length_units_names = copy.deepcopy(COMMON_LENGTH_UNITS)
                    self.unit_length = Unit(random.choice(length_units_names))
                    self.unit_area = Unit(self.unit_length.name, exponent=2)
                    self.length_unit = self.unit_length.name

        elif arg == "numbers":
            nb_list = list(options['nb'])
            if shuffle_nbs:
                random.shuffle(nb_list)
            elif sort_nbs:
                nb_list = sorted(nb_list)
            for i in range(len(nb_list)):
                setattr(self, 'nb' + str(i + 1), Decimal(str(nb_list[i])))
            self.nb_nb = len(nb_list)

        elif arg == "nb_variants":
            if ((self.nb_variant.startswith('decimal')
                 and self.deci_restriction != '+-')
                or options.get('bypass', False)):
                deci_nb = int(self.nb_variant[-1])  # so, from decimal1 up to 9
                # In order to ensure we'll have at least one decimal number,
                # we should try to remove all multiples of 10 from our possible
                # choices:
                all_nb_ids = [i + 1
                              for i in range(self.nb_nb)
                              if not getattr(self,
                                             'nb' + str(i + 1)) % 10 == 0]
                # But if this would lead to remove too many numbers, then
                # we have to change the extraneous multiples of 10
                if len(all_nb_ids) < deci_nb:
                    remaining = list(
                        set(i + 1 for i in range(self.nb_nb))
                        - set(all_nb_ids))
                    while len(all_nb_ids) < min(deci_nb, self.nb_nb):
                        random.shuffle(remaining)
                        i = remaining.pop()
                        setattr(self, 'nb' + str(i),
                                getattr(self,
                                        'nb' + str(i))
                                + random.choice([i for i in range(-4, 5)
                                                 if i != 0]))
                        all_nb_ids += [i]
                chosen_ones = random.sample(all_nb_ids, deci_nb)
                for i in chosen_ones:
                    setattr(self, 'nb' + str(i),
                            getattr(self, 'nb' + str(i)) / 10)

        elif arg == "division":
            nb_list = list(options['nb'])
            self.divisor = self.result = self.dividend = 0
            self.result_str = self.quotient_str = ""

            if '10_100_1000' in options and options['10_100_1000']:
                self.divisor, self.dividend = nb_list[0], nb_list[1]
                self.result = Quotient(('+', self.dividend, self.divisor))\
                    .evaluate()
            else:
                self.divisor = nb_list.pop(random.choice([0, 1]))
                self.result = nb_list.pop()
                if self.variant[:-1] == 'decimal':
                    self.result /= 10
                self.dividend = Product([self.divisor, self.result]).evaluate()

            if self.context == "from_area":
                self.subcontext = "w" if self.result < self.divisor else "l"

            self.dividend_str = Item(self.dividend).printed
            self.divisor_str = Item(self.divisor).printed
            self.result_str = Item(self.result).printed
            q = Quotient(('+', self.dividend, self.divisor),
                         use_divide_symbol=True)
            self.quotient_str = q.printed

        elif arg == "rectangle":
            if hasattr(self, 'nb1') and hasattr(self, 'nb2'):
                nb1, nb2 = self.nb1, self.nb2
            elif 'nb' in options:
                nb1, nb2 = options['nb'][0], options['nb'][1]
            else:
                raise error.ImpossibleAction("Setup a rectangle if no width "
                                             "nor length have been provided"
                                             " yet.")
            if (not hasattr(self, 'unit_length')
                or not hasattr(self, 'unit_area')):
                self.setup(self, "units", **options)

            # nb1 = Decimal(str(nb1))
            # nb2 = Decimal(str(nb2))

            w = Value(min([nb1, nb2]), unit=self.unit_length)
            l = Value(max([nb1, nb2]), unit=self.unit_length)

            rectangle_name = "DCBA"
            if self.picture:
                rectangle_name = next(shared.four_letters_words_source)
            self.rectangle = Rectangle([Point([rectangle_name[3], (0, 0)]),
                                        3,
                                        1.5,
                                        rectangle_name[2],
                                        rectangle_name[1],
                                        rectangle_name[0]],
                                       read_name_clockwise=True)
            self.rectangle.set_lengths([l, w])
            self.rectangle.setup_labels([False, False, True, True])

        elif arg == "square":
            if hasattr(self, 'nb1'):
                nb1 = self.nb1
            elif 'nb' in options:
                nb1 = options['nb'][0]
            else:
                raise error.ImpossibleAction("Setup a square if no side's "
                                             "length have been provided "
                                             "yet.")
            if (not hasattr(self, 'unit_length')
                or not hasattr(self, 'unit_area')):
                # __
                self.setup(self, "units", **options)

            square_name = "DCBA"
            if self.picture:
                square_name = next(shared.four_letters_words_source)
            self.square = Square([Point([square_name[3], (0, 0)]),
                                 2,
                                 square_name[2],
                                 square_name[1],
                                 square_name[0]],
                                 read_name_clockwise=True)
            self.square.set_lengths([Value(nb1, unit=self.unit_length)])
            self.square.setup_labels([False, False, True, False])
            self.square.set_marks(random.choice(["simple", "double",
                                                 "triple"]))

        elif arg == 'right_triangle':
            # Too many different possibilities for a Right Triangle,
            # so the angles|lengths' labels must be set outside of this setup()
            if (not hasattr(self, 'unit_length')
                or not hasattr(self, 'unit_area')):
                self.setup(self, "units", **options)

            rt_name = next(shared.three_letters_words_source)
            alpha, beta = next(shared.angle_ranges_source)
            rotation_angle = alpha + random.choice(range(beta - alpha))
            self.right_triangle = RightTriangle(
                ((rt_name[0], rt_name[1], rt_name[2]),
                 {'leg0': Decimal(str(random.choice(range(20, 40)) / 10)),
                  'leg1': Decimal(str(random.choice(range(20, 40)) / 10))}),
                rotate_around_isobarycenter=rotation_angle)

        elif arg == 'intercept_theorem_figure':
            butterfly = options.get('butterfly', False)
            set_lengths = options.get('set_lengths', True)
            if set_lengths:
                if not all([hasattr(self, 'nb1'), hasattr(self, 'nb2'),
                            hasattr(self, 'nb3'), hasattr(self, 'nb4')]):
                    # __
                    raise error.ImpossibleAction("Setup an intercept theorem "
                                                 "figure without a "
                                                 "coefficient and 3 other "
                                                 "lengths provided.")
            points_names = next(shared.five_letters_words_source)
            if butterfly:
                points_names = list(rotate(points_names, -1))
                (points_names[0], points_names[1]) = (points_names[1],
                                                      points_names[0])
                points_names = ''.join(points_names)
            else:
                points_names = rotate(points_names, random.choice(range(5)))
            alpha, beta = next(shared.angle_ranges_source)
            rotation_angle = alpha + random.choice(range(beta - alpha))
            self.figure = InterceptTheoremConfiguration(
                points_names=points_names,
                build_ratio=random.choice(range(25, 75)) / 100,
                sketch=False,
                butterfly=butterfly,
                build_dimensions={
                    False: {'side0': Decimal('5'),
                            'angle1':
                            Decimal(str(random.choice(range(45, 120)))),
                            'side1':
                            Decimal(str(random.choice(range(20, 60)) / 10))},
                    True: {'side0': Decimal('4'),
                           'angle1':
                           Decimal(str(random.choice(range(55, 110)))),
                           'side1':
                           Decimal(str(random.choice(range(15, 50)) / 10))}
                }[butterfly],
                rotate_around_isobarycenter=rotation_angle)

            if set_lengths:
                self.figure.set_lengths([self.nb2, self.nb3, self.nb4],
                                        Value(self.nb1))
            self.figure.side[2].invert_length_name()
            self.figure.small[2].invert_length_name()
            self.point0_name = self.figure.point[0].name
            self.point1_name = self.figure.point[1].name
            self.main_vertex_name = self.figure.vertex[0].name
            self.vertex1_name = self.figure.vertex[1].name
            self.vertex2_name = self.figure.vertex[2].name
            self.side0_length_name = self.figure.side[0].length_name
            self.small0_length_name = self.figure.small[0].length_name
            self.chunk0_length_name = self.figure.chunk[0].length_name
            self.side0_length = str(self.figure.side[0].length)
            self.small0_length = str(self.figure.small[0].length)
            self.chunk0_length = str(self.figure.chunk[0].length)
            self.side1_length_name = self.figure.side[2].length_name
            self.small1_length_name = self.figure.small[2].length_name
            self.chunk1_length_name = self.figure.chunk[1].length_name
            self.side1_length = str(self.figure.side[2].length)
            self.small1_length = str(self.figure.small[2].length)
            self.chunk1_length = str(self.figure.chunk[1].length)

        elif arg == 'mini_problem_wording':
            self.wording = _(shared.mini_problems_wordings_source
                             .next(q_id=options['q_id'],
                                   nb1_to_check=self.nb1,
                                   nb2_to_check=self.nb2))
            setup_wording_format_of(self)

    def dbg_info(self, msg, *numbers, letters=alphabet):
        """
        Create log message to record including self.nb* and a, b, c... values.

        :param msg: the msg to join to the values' list
        :type msg: str
        :param numbers: the values of the numbers a, b, c etc.
        :type numbers: numbers
        :rtype: str
        """
        figures = '123456789'
        nb = 'nb' + '; nb'.join(figures[:len(self.nb_list)]) + " = " \
            + '; '.join('{}' for _ in range(len(self.nb_list))) \
            .format(*self.nb_list)
        abcd = '; '.join(letters[0:len(numbers)]) + " = " \
            + '; '.join('{}' for _ in range(len(numbers))) \
            .format(*numbers)
        return ('(variant {}): \\n{} {}\\n'
                + ''.join([' ' for _ in range(len(msg) + 1)]) + '{}') \
            .format(self.variant, msg, nb, abcd)

    def watch(self, rules, *numbers, letters=alphabet):
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
        :param numbers: the values of the numbers a, b, c etc.
        :type numbers: numbers
        :param letters: the names of the variables, in order of appearance.
                        Default is the normal alphabet, low case.
        :type letters: str
        """
        if hasattr(self, 'log'):
            for r in rules.split(sep='; '):
                msg = ''
                if r == 'no negative' and self.subvariant == 'only_positive':
                    if any([n < 0 for n in numbers]):
                        msg += 'Negative number detected!'
                elif r == 'decimals distribution':
                    if not self.nb_variant.startswith('decimal'):
                        max_dn = 0
                    else:
                        max_dn = int(self.nb_variant[-1])
                    if any(digits_nb(n) > max_dn for n in numbers):
                        tests = [digits_nb(n) > max_dn for n in numbers]
                        msg += 'At least a number among ' \
                            + ', '.join(letters[0:len(numbers) - 1]) + ' and '\
                            + letters[len(numbers) - 1] \
                            + (' has more digits than expected: {m} ; '
                               + 'tests = {t}; numbers = {n}') \
                            .format(m=max_dn, t=tests, n=numbers)
                    if (self.nb_variant.startswith('decimal')
                        and all(digits_nb(n) == 0 for n in numbers)):
                        msg += ', '.join(letters[0:len(numbers) - 1]) \
                            + ' and ' \
                            + letters[len(numbers) - 1] + ' are all integers!'
                elif (r.endswith('isnt deci')
                      and not self.allow_division_by_decimal):
                    if not is_integer(numbers[letters.index(r[0])]):
                        msg += r[0] + ' is decimal! => Division by decimal!'
                elif len(r.split(' isnt ')) == 2:
                    l, n = r.split(' isnt ')
                    if numbers[letters.index(l)] == int(n):
                        msg += l + ' == {}!'.format(n)
                if msg != '':
                    self.log(self.dbg_info(msg, *numbers, letters=letters))
