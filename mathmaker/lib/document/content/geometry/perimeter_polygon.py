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

from mathmakerlib.calculus import Number

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import setup_wording_format_of


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup('minimal', **options)
        level = int(build_data[5])
        # super().setup('numbers', nb=, **options)
        # super().setup('nb_variants', **options)
        super().setup('length_units', **options)

        # We know the wording will be in two lines:
        super().setup('polygon', polygon_data=build_data, wlines_nb=2)

        perimeter = self.polygon.lbl_perimeter

        qvariant = options.get('qvariant', 'default')

        if qvariant == 'missing_length':
            unmasked = [i for i, s in enumerate(self.polygon.sides)
                        if s.label_mask is None]
            to_find = random.choice(unmasked)
            self.polygon.sides[to_find].label_mask = '?'
            self.answer = self.polygon.sides[to_find].label_value

            if self.slideshow:
                self.wording = _(r'Perimeter: {}~{{length_unit}}.\newline '
                                 r'Length of the missing side? '
                                 r'|hint:length_unit|').format(perimeter)
            else:
                self.wording = {
                    3: _(r'The perimeter of this triangle is '
                         r'{}~{{length_unit}}.\newline What is the length of '
                         r'the missing side? |hint:length_unit|')
                    .format(perimeter),
                    4: _(r'The perimeter of this quadrilateral is {}~'
                         r'{{length_unit}}.\newline What is the length of the '
                         r'missing side? |hint:length_unit|')
                    .format(perimeter),
                    5: _(r'The perimeter of this pentagon is '
                         r'{}~{{length_unit}}.\newline What is the length of '
                         r'the missing side? |hint:length_unit|')
                    .format(perimeter),
                    6: _(r'The perimeter of this hexagon is '
                         r'{}~{{length_unit}}.\newline What is the length '
                         r'of the missing side? |hint:length_unit|')
                    .format(perimeter)
                }[len(self.polygon.sides)]

        else:  # default
            self.answer = self.polygon.lbl_perimeter
            self.wording = {
                3: _(r'Perimeter of this triangle?\newline '
                     r'(length unit: {length_unit}) |hint:length_unit|'),
                4: _(r'Perimeter of this quadrilateral?\newline '
                     r'(length unit: {length_unit}) |hint:length_unit|'),
                5: _(r'Perimeter of this pentagon?\newline '
                     r'(length unit: {length_unit}) |hint:length_unit|'),
                6: _(r'Perimeter of this hexagon?\newline '
                     r'(length unit: {length_unit}) |hint:length_unit|')
            }[len(self.polygon.sides)]

        self.transduration = 15 + 3 * (level - 1)

        setup_wording_format_of(self)
        self.wording = self.wording.format(**self.wording_format)

    def q(self, **options):
        if self.slideshow:
            return '{}{}{}'.format(self.wording,
                                   shared.machine.addvspace(height='10pt'),
                                   self.polygon.drawn)
        else:
            return shared.machine.write_layout(
                (1, 2), [4, 9], [self.polygon.drawn, self.wording])

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return Number(self.answer, unit=self.length_unit).printed

    def js_a(self, **kwargs):
        return [Number(self.answer, unit=None).uiprinted]
