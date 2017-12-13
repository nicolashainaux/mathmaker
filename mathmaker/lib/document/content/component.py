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

from mathmakerlib.calculus import Number, is_integer
from mathmakerlib.calculus.unit import COMMON_LENGTH_UNITS

from mathmaker.lib.core.root_calculus import Unit, Value
from mathmaker.lib.core.base_calculus import Product, Quotient, Item
from mathmaker.lib import shared
from mathmaker.lib.constants import BOOLEAN
from mathmaker.lib.tools import rotate, fix_math_style2_fontsize
from mathmaker.lib.tools.wording import setup_wording_format_of
from mathmaker.lib.tools.shapes import ShapeGenerator


class structure(object):

    @property
    def q_wordings_collection(self):
        return {'turn_to_decimal_repr': _('What is {} as a decimal?'),
                'turn_to_decimal_fraction':
                    _('What is {} as a decimal fraction?')}

    def h(self, **kwargs):
        if hasattr(self, 'hint'):
            return "\hfill" + Value("", unit=self.hint)\
                .into_str(display_SI_unit=True)
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
            self.tikz_linesegments_thickness = 'thick'
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

    def _setup_numbers(self, **kwargs):
        nb_list = list(kwargs['nb'])
        if kwargs.get('shuffle_nbs', True):
            random.shuffle(nb_list)
        elif kwargs.get('sort_nbs', False):
            nb_list = sorted(nb_list)
        for i in range(len(nb_list)):
            if isinstance(nb_list[i], Quotient):
                setattr(self, 'nb' + str(i + 1), nb_list[i])
            else:
                setattr(self, 'nb' + str(i + 1), Number(str(nb_list[i])))
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

    def _setup_division(self, **kwargs):
        nb_list = list(kwargs['nb'])
        self.divisor = self.result = self.dividend = 0
        self.result_str = self.quotient_str = ""

        if '10_100_1000' in kwargs and kwargs['10_100_1000']:
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

    def _setup_rectangle(self, **kwargs):
        from mathmaker.lib.core.base_geometry import Point
        from mathmaker.lib.core.geometry import Rectangle
        if hasattr(self, 'nb1') and hasattr(self, 'nb2'):
            nb1, nb2 = self.nb1, self.nb2
        elif 'nb' in kwargs:
            nb1, nb2 = kwargs['nb'][0], kwargs['nb'][1]
        else:
            raise RuntimeError('Impossible to Setup a rectangle if no width '
                               'nor length have been provided yet.')
        if (not hasattr(self, 'unit_length')
            or not hasattr(self, 'unit_area')):
            self.setup(self, "units", **kwargs)

        # nb1 = Decimal(str(nb1))
        # nb2 = Decimal(str(nb2))

        W = Value(min([nb1, nb2]), unit=self.unit_length)
        L = Value(max([nb1, nb2]), unit=self.unit_length)

        rectangle_name = "DCBA"
        if self.picture:
            rectangle_name = next(shared.four_letters_words_source)[0]
        self.rectangle = Rectangle([Point(rectangle_name[3], 0, 0),
                                    3,
                                    1.5,
                                    rectangle_name[2],
                                    rectangle_name[1],
                                    rectangle_name[0]],
                                   read_name_clockwise=True)
        self.rectangle.set_lengths([L, W])
        self.rectangle.setup_labels([False, False, True, True])

    def _setup_square(self, **kwargs):
        from mathmaker.lib.core.base_geometry import Point
        from mathmaker.lib.core.geometry import Square
        if hasattr(self, 'nb1'):
            nb1 = self.nb1
        elif 'nb' in kwargs:
            nb1 = kwargs['nb'][0]
        else:
            raise RuntimeError('Impossible to Setup a square if no side\'s '
                               'length have been provided yet.')
        if (not hasattr(self, 'unit_length')
            or not hasattr(self, 'unit_area')):
            # __
            self.setup(self, "units", **kwargs)

        square_name = "DCBA"
        if self.picture:
            square_name = next(shared.four_letters_words_source)[0]
        self.square = Square([Point(square_name[3], 0, 0),
                             2,
                             square_name[2],
                             square_name[1],
                             square_name[0]],
                             read_name_clockwise=True)
        self.square.set_lengths([Value(nb1, unit=self.unit_length)])
        self.square.setup_labels([False, False, True, False])
        self.square.set_marks(random.choice(["simple", "double",
                                             "triple"]))

    def _setup_right_triangle(self, **kwargs):
        from mathmaker.lib.core.geometry import RightTriangle
        # Too many different possibilities for a Right Triangle,
        # so the angles|lengths' labels must be set outside of this setup()
        if (not hasattr(self, 'unit_length')
            or not hasattr(self, 'unit_area')):
            self.setup(self, "units", **kwargs)

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
        wording_kwargs = {'q_id': kwargs['q_id'],
                          'nb1_to_check': self.nb1,
                          'nb2_to_check': self.nb2}
        if 'back_to_unit' in kwargs:
            val = 1 if BOOLEAN[kwargs['back_to_unit']]() else 0
            wording_kwargs.update({'back_to_unit': val})
        self.wording = _(shared.mini_problems_wordings_source
                         .next(**wording_kwargs)[0])
        setup_wording_format_of(self)

    def _setup_complement_wording(self, **kwargs):
        upper_bound = self.nb1
        if self.context == 'complement_wording':
            self.context += str(random.choice([1, 2]))
        if self.context == 'complement_wording1':
            self.wording = _('What number must be added to'
                             ' {number1} to make {number2}?')\
                .format(number1=Value(self.nb2), number2=Value(self.nb1))
        elif self.context == 'complement_wording2':
            if upper_bound == 10:
                self.wording = _('What is the tens complement '
                                 'of {number}?').format(number=Value(self.nb2))
            elif upper_bound == 100:
                self.wording = _('What is the hundreds complement '
                                 'of {number}?').format(number=Value(self.nb2))
            else:
                self.wording = _('What is the complement to {number1} '
                                 'of {number2}?')\
                    .format(number1=Value(self.nb1), number2=Value(self.nb2))
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
        self.polygon.scale = self.tikz_picture_scale
        for s in self.polygon.sides:
            s.label_scale = Number('0.85') * self.tikz_picture_scale

    def _setup_polygon(self, polygon_data=None):
        # polygon_data is of the form:
        # (sides_nb, codename, specificname, sides_particularity, level,
        #  variant, table2, table3, table4, table5, table6, ...)
        # where ... are the available numbers to use for sides labeling.
        polygon_data = list(polygon_data)
        self.polygon_sides_nb = polygon_data[0]
        self.polygon_codename = polygon_data[3]
        variant = polygon_data[6]
        self.polygon_name = None
        self.label_polygon_vertices = False
        # We'll browse the multiples in reversed order
        multiples = [int(_)
                     for _ in self.polygon_codename.split('_')[1:]][::-1]
        labels = []
        for m in multiples:
            if m == 1:
                labels.append((1, polygon_data.pop()))
            elif m >= 2:
                other = polygon_data.pop()
                if m == other:
                    other = polygon_data.pop()
                else:
                    polygon_data.pop()
                labels.append((m, other))
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
