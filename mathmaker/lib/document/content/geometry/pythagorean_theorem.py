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

from mathmakerlib.calculus import Number
from mathmakerlib.calculus.equations import PythagoreanEquation
from mathmakerlib import required

from mathmaker.lib import shared
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, picture=False, **options):
        required.package['ulem'] = True
        super().setup("minimal", **options)
        super().setup("length_units", **options)

        self.exactness = build_data[-1]

        super().setup("right_triangle", **options)

        variants = ['calculate_hyp', 'calculate_leg0', 'calculate_leg1']
        if self.variant == 'calculate_leg':
            self.variant = 'calculate_leg' + random.choice(['0', '1'])
        if self.variant not in variants:
            raise ValueError(
                f'Got incorrect value "{self.variant}" for pythagorean '
                f'theorem variant; correct values are in {variants}.')

        use_decimals = options.get('use_decimals', 'false')
        self.round_to = options.get('round_to', None)
        if self.round_to is None and self.exactness == 'approx':
            self.round_to = random.choice(['1.0', '1.00'])
        if self.round_to is None:  # case self.exactness == 'exact'
            if use_decimals == 'true':
                self.round_to = '1.00'
            else:
                self.round_to = '1.0'

        self.figure_in_the_text = options.get('figure_in_the_text', False)

        leg0 = Number(build_data[0], unit=self.length_unit)
        leg1 = Number(build_data[1], unit=self.length_unit)
        hyp = Number(build_data[2], unit=self.length_unit)

        zero_length = Number(0, unit=self.length_unit)
        if self.variant == 'calculate_leg1' and leg0 == zero_length:
            leg0, leg1 = leg1, leg0

        if use_decimals == 'true':
            leg0 = leg0 / 10
            leg1 = leg1 / 10
            hyp = hyp / 10

        labels = [leg0, leg1, hyp]
        if self.variant == 'calculate_hyp':
            labels[2] = '?'
        elif self.variant == 'calculate_leg0':
            labels[0] = '?'
        elif self.variant == 'calculate_leg1':
            labels[1] = '?'
        self.right_triangle.setup_labels(labels)

        if self.variant.endswith('hyp'):
            self.calculate = 'hyp'
            self.unknown_side = self.right_triangle.hyp
            self.known_sides = [self.right_triangle.leg0,
                                self.right_triangle.leg1]

        elif self.variant.endswith('leg0'):
            self.calculate = 'leg0'
            self.unknown_side = self.right_triangle.leg0
            self.known_sides = [self.right_triangle.leg1,
                                self.right_triangle.hyp]

        elif self.variant.endswith('leg1'):
            self.calculate = 'leg1'
            self.unknown_side = self.right_triangle.leg1
            self.known_sides = [self.right_triangle.leg0,
                                self.right_triangle.hyp]

        else:
            raise ValueError(f'Got {self.variant = }')

        # setup_wording_format_of(self, w_prefix='answer_')
        self.q_nb_included_in_wording = False

        self.q_nb = options.get('number_of_the_question', None)
        if self.q_nb:
            self.q_nb = shared.machine.write(self.q_nb + '. ',
                                             emphasize='bold')

    def q(self, **options):
        PRECISION_IDIOMS = {'1': _("to the unit"),
                            '1.0': _("to the tenth"),
                            '1.00': _("to the hundreth"),
                            '1.000': _("to the thousandth"),
                            '1.0000': _("to the ten thousandth")}
        M = shared.machine

        if self.figure_in_the_text:
            result = self.right_triangle.drawn
        else:
            result = _("The triangle {triangle_name} has a right \
angle in {right_vertex}.")\
                .format(triangle_name=str(self.right_triangle.name),
                        right_vertex=str(self.right_triangle.vertices[1].name))
            known0 = str(self.known_sides[0].length_name)
            len0 = str(self.known_sides[0].label)
            known1 = str(self.known_sides[1].length_name)
            len1 = str(self.known_sides[1].label)
            result += f" {known0} = {len0}. {known1} = {len1}."

        result += " " + _("Calculate the length of {this_side}.")\
            .format(this_side=self.unknown_side.length_name)

        if self.length_unit:
            result += " " + _("Give the result in {this_unit}.")\
                .format(this_unit=self.length_unit)

        if self.exactness == 'approx':
            result += " " + _("Round the result {at_this_precision}.")\
                .format(at_this_precision=PRECISION_IDIOMS[self.round_to])

        return result + M.write_new_line()

    def a(self, **options):
        M = shared.machine
        result = _("The triangle {triangle_name} has a right angle in "
                   "{right_vertex}.")\
            .format(triangle_name=str(self.right_triangle.name),
                    right_vertex=str(self.right_triangle.vertices[1].name))

        result += M.write_new_line()

        result += _("Then by Pythagoras theorem") + ":"

        rounding = Decimal(self.round_to) \
            if self.exactness == 'approx' else None

        eq = PythagoreanEquation(self.right_triangle)\
            .autosolve(self.calculate, required_rounding=rounding)

        result += M.write(eq)

        if self.figure_in_the_text:
            return result
        else:
            content = [_("Sketch") + ":" + M.write_new_line()
                       + self.right_triangle.drawn, result]
            return M.write_layout((1, 2), [9, 9], content,
                                  tabular_options='[t]')
