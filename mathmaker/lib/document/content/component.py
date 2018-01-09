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
import copy
from decimal import Decimal
from string import ascii_lowercase as alphabet

from mathmakerlib.calculus import Number, Unit, Fraction, is_integer
from mathmakerlib.calculus.unit import COMMON_LENGTH_UNITS

from mathmaker.lib.core.base_calculus import Division
from mathmaker.lib import shared
from mathmaker.lib.constants import BOOLEAN
from mathmaker.lib.tools import rotate, lined_up, fix_math_style2_fontsize
from mathmaker.lib.tools.wording import setup_wording_format_of
from mathmaker.lib.tools.shapes import ShapeGenerator
from mathmaker.lib.tools.database import preprocess_qkw


class structure(object):

    @property
    def q_wordings_collection(self):
        return {'turn_to_decimal_repr': _('What is {} as a decimal?'),
                'turn_to_decimal_fraction':
                    _('What is {} as a decimal fraction?')}

    def h(self, **kwargs):
        if hasattr(self, 'hint'):
            return '\hfill ${}$'.format(self.hint)
        else:
            return ""

    def js_a(self, **kwargs):
        """
        Return the object as a list of user quickly writable strings.

        The elements of this list will be used in embedded javascript of pdf
        files to compare to user's answer. Most of the time, only one answer
        is possible (like answer of '7×8 = ?' is equal to '56') but sometimes
        it is useful to have several different answers to accept, like for
        fractions of a figure: '6/12' should lead to also accept, at least,
        '3/6', '2/4' and '1/2'.

        Must be reimplemented in each question.
        """
        return _('undefined')

    @property
    def nb_list(self):
        return [getattr(self, 'nb' + str(i + 1)) for i in range(self.nb_nb)]

    def _setup_logging(self, **kwargs):
        from mathmaker import settings
        self.log = settings.output_watcher_logger.debug

    def _setup_minimal(self, **kwargs):
        self.newline = '\\newline'
        self.parallel_to = '$\parallel$'
        self.belongs_to = '$\in$'
        self.percent_symbol = '\%'
        self.nb_source = kwargs.get('nb_source')
        self.preset = kwargs.get('preset', 'default')
        if 'nb_variant' in kwargs and kwargs['nb_variant'] == 'decimal':
            kwargs['nb_variant'] = random.choice(['decimal1', 'decimal2'])
        self.x_layout_variant = kwargs.get('x_layout_variant', 'default')
        self.slideshow = (self.x_layout_variant == 'slideshow')
        self.tikz_picture_scale = 1
        self.tikz_linesegments_thickness = 'thin'
        if self.slideshow:
            self.tikz_picture_scale = 3
            self.tikz_linesegments_thickness = 'very thick'
        self.variant = kwargs.get('variant', 'default')
        self.subvariant = kwargs.get('subvariant', 'default')
        self.nb_variant = kwargs.get('nb_variant', 'default')
        self.context = kwargs.get('context', 'default')
        self.picture = BOOLEAN[kwargs.get('picture', 'false')]()
        self.decimal_result = int(kwargs.get('decimal_result', 2))
        self.allow_extra_digits = int(kwargs.get('allow_extra_digits', 0))
        self.allow_division_by_decimal = BOOLEAN[
            kwargs.get('allow_division_by_decimal', 'false')]()

    def _setup_length_units(self, **kwargs):
        if 'unit' in kwargs:
            self.unit_length = Unit(kwargs['unit'])
            self.unit_area = Unit(self.unit_length.content, exponent=2)
            self.length_unit = self.unit_length.content
        else:
            if hasattr(self, 'length_unit'):
                self.unit_length = Unit(self.length_unit)
                self.unit_area = Unit(self.unit_length.content, exponent=2)
            elif hasattr(self, 'unit_length'):
                self.length_unit = self.unit_length.content
                self.unit_area = Unit(self.unit_length.content, exponent=2)
            else:
                length_units_names = copy.deepcopy(COMMON_LENGTH_UNITS)
                self.unit_length = Unit(random.choice(length_units_names))
                self.unit_area = Unit(self.unit_length.content, exponent=2)
                self.length_unit = self.unit_length.content

    def _setup_numbers(self, **kwargs):
        nb_list = list(kwargs['nb'])
        if kwargs.get('shuffle_nbs', True):
            random.shuffle(nb_list)
        elif kwargs.get('sort_nbs', False):
            nb_list = sorted(nb_list)
        for i in range(len(nb_list)):
            if isinstance(nb_list[i], Fraction):
                setattr(self, 'nb' + str(i + 1), nb_list[i])
            else:
                setattr(self, 'nb' + str(i + 1), Number(str(nb_list[i])))
        if kwargs.get('standardize_decimal_numbers', False):
            for i in range(len(nb_list)):
                nb = getattr(self, 'nb{}'.format(i + 1))
                if isinstance(nb, Number):
                    setattr(self, 'nb' + str(i + 1), nb.standardized())
        self.nb_nb = len(nb_list)

    def _setup_nb_variants(self, **kwargs):
        if self.nb_variant.startswith('decimal'):
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
        elif (self.nb_variant in ['±half', '±quarter', '±halforquarter']
              and self.nb_nb >= 2):
            # Depending on the case we randomly add or substract 0.5 or 0.25
            # (or randomly a mix of them) to a random sample of numbers
            # (self.nb*)
            if self.nb_variant == '±half':
                g_xnb = (Number('0.5') for _ in range(self.nb_nb))
            if self.nb_variant == '±quarter':
                g_xnb = (Number('0.25') for _ in range(self.nb_nb))
            if self.nb_variant == '±halforquarter':
                def g_xnb():
                    first_couple = [Number('0.5'), Number('0.25')]
                    random.shuffle(first_couple)
                    yield first_couple.pop()
                    yield first_couple.pop()
                    while True:
                        yield random.choice([Number('0.5'), Number('0.25')])
                g_xnb = g_xnb()
            all_nb_ids = [i + 1 for i in range(self.nb_nb)]
            random.shuffle(all_nb_ids)
            how_many = random.choice([i + 1 for i in range(self.nb_nb)])
            chosen_ones = random.sample(all_nb_ids, how_many)
            signs = [1, -1]
            random.shuffle(signs)
            signs = signs * len(chosen_ones)
            for i in range(len(chosen_ones)):
                setattr(self, 'nb' + str(chosen_ones[i]),
                        getattr(self, 'nb' + str(chosen_ones[i]))
                        + next(g_xnb) * signs[i])

    def _setup_euclidean_division(self, **kwargs):
        nb_list = list(kwargs['nb'])
        # For couples like (3, 15) or (4, 25) we want to ensure the divisor
        # will be 15 (or 25), in order to ask a not too hard question.
        # Using 11 or more as divisor makes it already quite a more
        # difficult question.
        if not (15 in nb_list or 25 in nb_list):
            random.shuffle(nb_list)
        self.divisor = Number(nb_list.pop())
        self.quotient = Number(nb_list.pop())
        allow_null_remainder = kwargs.get('allow_null_remainder', False)
        force_null_remainder = kwargs.get('force_null_remainder', False)
        if force_null_remainder:
            self.remainder = Number(0)
        else:
            mini = 0 if allow_null_remainder else 1
            self.remainder = \
                Number(random.choice(range(mini, int(self.divisor))))
        self.dividend = self.quotient * self.divisor + self.remainder

    def _setup_division(self, **kwargs):
        nb_list = list(kwargs['nb'])
        self.divisor = self.result = self.dividend = 0
        self.result_str = self.quotient_str = ""

        if '10_100_1000' in kwargs and kwargs['10_100_1000']:
            self.divisor, self.dividend = nb_list[0], nb_list[1]
            self.result = self.dividend / self.divisor
        else:
            order = kwargs.get('order', 'random')
            if order == 'divisor,quotient':
                self.divisor, self.result = nb_list[0], nb_list[1]
            elif order == 'quotient,divisor':
                self.divisor, self.result = nb_list[1], nb_list[0]
            else:
                self.divisor = Number(nb_list.pop(random.choice([0, 1])))
                self.result = Number(nb_list.pop())
            if self.variant[:-1] == 'decimal':
                self.result /= 10
            self.dividend = self.divisor * self.result

        if self.context == "from_area":
            self.subcontext = "w" if self.result < self.divisor else "l"

        self.dividend_str = Number(self.dividend).printed
        self.divisor_str = Number(self.divisor).printed
        self.result_str = Number(self.result).printed
        q = Division(('+', self.dividend, self.divisor))
        self.quotient_str = q.printed

    def _setup_rectangle(self, **kwargs):
        if hasattr(self, 'nb1') and hasattr(self, 'nb2'):
            nb1, nb2 = self.nb1, self.nb2
        elif 'nb' in kwargs:
            nb1, nb2 = kwargs['nb'][0], kwargs['nb'][1]
        else:
            raise RuntimeError('Impossible to Setup a rectangle if no width '
                               'nor length have been provided yet.')
        if (not hasattr(self, 'unit_length')
            or not hasattr(self, 'unit_area')):
            self.setup('length_units', **kwargs)

        W = Number(min([nb1, nb2]), unit=self.unit_length)
        L = Number(max([nb1, nb2]), unit=self.unit_length)
        self.label_polygon_vertices = False
        self.polygon_name = None
        if self.picture:
            self.polygon_name = next(shared.four_letters_words_source)[0]

        self._generate_polygon('quadrilateral_2_2', 2, [(2, W), (2, L)])
        self.rectangle = self.polygon

    def _setup_right_triangle(self, **kwargs):
        from mathmaker.lib.core.geometry import RightTriangle
        # Too many different possibilities for a Right Triangle,
        # so the angles|lengths' labels must be set outside of this setup()
        if (not hasattr(self, 'unit_length')
            or not hasattr(self, 'unit_area')):
            self.setup('length_units', **kwargs)

        rt_name = next(shared.three_letters_words_source)[0]
        alpha, beta = next(shared.angle_ranges_source)
        rotation_angle = alpha + random.choice(range(beta - alpha))
        self.right_triangle = RightTriangle(
            ((rt_name[0], rt_name[1], rt_name[2]),
             {'leg0': Decimal(str(random.choice(range(20, 40)) / 10)),
              'leg1': Decimal(str(random.choice(range(20, 40)) / 10))}),
            rotate_around_isobarycenter=rotation_angle)

    def _setup_intercept_theorem_figure(self, **kwargs):
        from mathmaker.lib.core.geometry import InterceptTheoremConfiguration
        butterfly = kwargs.get('butterfly', False)
        set_lengths = kwargs.get('set_lengths', True)
        if set_lengths:
            if not all([hasattr(self, 'nb1'), hasattr(self, 'nb2'),
                        hasattr(self, 'nb3'), hasattr(self, 'nb4')]):
                # __
                raise RuntimeError('Impossible to Setup an intercept theorem '
                                   'figure without a coefficient and 3 other '
                                   'lengths provided.')
        points_names = next(shared.five_letters_words_source)[0]
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
            from mathmaker.lib.core.root_calculus import Value
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

    def _setup_mini_problem_wording(self, **kwargs):
        wording_kwargs = {'nb1_to_check': self.nb1, 'nb2_to_check': self.nb2}
        if kwargs.get('proportionality', False):
            source = shared.mini_problems_prop_wordings_source
            wording_kwargs.update({'coeff_to_check': self.coeff,
                                   'nb3_to_check': self.nb3,
                                   'solution_to_check': self.nb4,
                                   'lock_equal_contexts': True})
            if not is_integer(self.nb1):
                wording_kwargs.update({'nb1_may_be_deci': 1})
            if not is_integer(self.nb2):
                wording_kwargs.update({'nb2_may_be_deci': 1})
            if not is_integer(self.nb3):
                wording_kwargs.update({'nb3_may_be_deci': 1})
            if not is_integer(self.nb4):
                wording_kwargs.update({'solution_may_be_deci': 1})
            wording_kwargs.update(preprocess_qkw('mini_pb_prop_wordings',
                                                 qkw=kwargs))
        else:
            source = shared.mini_problems_wordings_source
            wording_kwargs.update({'q_id': kwargs['q_id']})
            if 'back_to_unit' in kwargs:
                val = 1 if BOOLEAN[kwargs['back_to_unit']]() else 0
                wording_kwargs.update({'back_to_unit': val})
        drawn_wording = source.next(**wording_kwargs)
        self.wording = _(drawn_wording[1])
        self.wording_context = drawn_wording[0]
        if kwargs.get('proportionality', False):
            self.solution = self.nb4
            nb1_xcoeff = Number(str(drawn_wording[2]))
            nb2_xcoeff = Number(str(drawn_wording[3]))
            nb3_xcoeff = Number(str(drawn_wording[4]))
            if nb1_xcoeff != 1:
                self.nb1 *= nb1_xcoeff
                self.solution /= nb1_xcoeff
            if nb2_xcoeff != 1:
                self.nb2 *= nb2_xcoeff
                self.solution *= nb2_xcoeff
            if nb3_xcoeff != 1:
                self.nb3 *= nb3_xcoeff
                self.solution *= nb3_xcoeff
            if self.wording_context in ['price', 'groceries']:
                self.solution = self.solution.rounded(Number('0.01'))
                if self.solution.fracdigits_nb() > 0:
                    self.solution = self.solution.quantize(Number('0.01'))
            else:
                if self.solution.fracdigits_nb() == 0:
                    self.solution = self.solution.quantize(Number('1'))
                if self.nb3.fracdigits_nb() == 0:
                    self.nb3 = self.nb3.quantize(Number('1'))

        setup_wording_format_of(self)

    def _setup_complement_wording(self, **kwargs):
        upper_bound = self.nb1
        if self.context == 'complement_wording':
            self.context += str(random.choice([1, 2]))
        if self.context == 'complement_wording1':
            self.wording = _('What number must be added to'
                             ' {number1} to make {number2}?')\
                .format(number1=self.nb2.printed, number2=self.nb1.printed)
        elif self.context == 'complement_wording2':
            if upper_bound == 10:
                self.wording = _('What is the tens complement '
                                 'of {number}?')\
                    .format(number=self.nb2.printed)
            elif upper_bound == 100:
                self.wording = _('What is the hundreds complement '
                                 'of {number}?')\
                    .format(number=self.nb2.printed)
            else:
                self.wording = _('What is the complement to {number1} '
                                 'of {number2}?')\
                    .format(number1=self.nb1.printed, number2=self.nb2.printed)
        else:
            raise ValueError('Cannot recognize context: {}\n'
                             .format(self.context))
        setup_wording_format_of(self)

    def _setup_ask_question(self, **kwargs):
        values = kwargs.get('values')
        self.wording = self.q_wordings_collection[kwargs['q_key']]\
            .format(*values)
        if kwargs.get('fix_math_style2_fontsize', False):
            self.wording = fix_math_style2_fontsize(self.wording)
        setup_wording_format_of(self)

    def _setup_rectangle_grid(self, **kwargs):
        from mathmaker.lib.core.base_geometry import Point
        from mathmaker.lib.core.geometry import RectangleGrid
        rows = str(min(self.nb3, self.nb4))
        cols = str(max(self.nb3, self.nb4))
        frows = str(min(self.nb1, self.nb2))
        fcols = str(max(self.nb1, self.nb2))
        self.rectangle_grid = \
            RectangleGrid([Point('A', Decimal('0'), Decimal('0')),
                           Decimal(cols), Decimal(rows), 'B', 'C', 'D'],
                          layout='×'.join([rows, cols]),
                          fill='×'.join([frows, fcols]))

    def _generate_polygon(self, codename, variant, labels):
        # codename: see database, table polygons
        # labels: come as [(1, nb), (2, nb), (2, nb)]
        # (see _setup_polygon below)
        self.polygon = ShapeGenerator()\
            .generate(codename, variant=variant, labels=labels,
                      name=self.polygon_name,
                      label_vertices=self.label_polygon_vertices,
                      thickness=self.tikz_linesegments_thickness,
                      length_unit=self.length_unit)
        # Without patching polygons to NOT cycle when drawn, the scaling of
        # tikzpicture will produce a displaying bug (not nice)
        self.polygon.do_cycle = False
        self.polygon.scale = self.tikz_picture_scale
        for s in self.polygon.sides:
            s.label_scale = Number('0.85')

    def _setup_polygon(self, polygon_data=None):
        # polygon_data is of the form:
        # (check the tables' columns in shapes.db-dist)
        # (sides_nb, type, special, codename, sides_particularity, level,
        #  variant, table2, table3, table4, table5, table6, ...)
        # where ... are the available numbers to use for sides labeling.
        polygon_data = list(polygon_data)
        self.polygon_sides_nb = polygon_data[0]
        self.polygon_codename = polygon_data[3]
        variant = polygon_data[6]
        self.polygon_name = None
        self.label_polygon_vertices = False
        # We'll browse the multiples in reversed order
        nb_to_use = polygon_data[-self.polygon_sides_nb:]
        labels = lined_up(nb_to_use)
        # Now, we have lengths stored in labels as, for example:
        # [(1, nb), (2, nb), (2, nb)]
        self._generate_polygon(self.polygon_codename, variant, labels)

    def setup(self, arg, **kwargs):
        if type(arg) is not str:
            raise TypeError('arg must be a str')
        try:
            getattr(self, '_setup_' + arg)(**kwargs)
        except AttributeError as excinfo:
            if str(excinfo).endswith('has no attribute \'_setup_{}\''
                                     .format(arg)):
                raise ValueError('There is no private method _setup_{}() '
                                 'to handle setup of \'{}\'.'
                                 .format(arg, arg))

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
                    if any(Number(n).fracdigits_nb() > max_dn
                           for n in numbers):
                        tests = [Number(n).fracdigits_nb() > max_dn
                                 for n in numbers]
                        msg += 'At least a number among ' \
                            + ', '.join(letters[0:len(numbers) - 1]) + ' and '\
                            + letters[len(numbers) - 1] \
                            + (' has more digits than expected: {m} ; '
                               + 'tests = {t}; numbers = {n}') \
                            .format(m=max_dn, t=tests, n=numbers)
                    if (self.nb_variant.startswith('decimal')
                        and all(Number(n).fracdigits_nb() == 0
                                for n in numbers)):
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
