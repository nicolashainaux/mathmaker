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

from mathmaker.lib import shared
from mathmaker.lib.tools.wording import setup_wording_format_of
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, picture='true', **options):
        super().setup("minimal", **options)
        super().setup("length_units", **options)
        super().setup("right_triangle", **options)
        # nb1 will be the length to use; nb2 the acute angle
        super().setup("numbers", nb=build_data,
                      shuffle_nbs=False, **options)

        valid_variants = ['cos_up', 'cos_down', 'sin_up', 'sin_down',
                          'tan_up', 'tan_down']

        if self.variant == 'default':
            variant = ['random', 'random']
        else:
            if self.variant.count('_') != 1:
                raise ValueError('XMLFileFormatError: the variant for '
                                 'trigonometry_calculate_length '
                                 'shoud contain one _')
            if self.variant in ['cos_opp', 'sin_adj', 'tan_hyp']:
                raise ValueError('XMLFileFormatError: invalid variant: {v}, '
                                 .format(v=variant) + 'It should be in: '
                                 + str(valid_variants))
            variant = self.variant.split(sep='_')

        if variant[0] == 'random':
            if variant[1] == 'random':
                variant[0] = shared.trigo_functions_source.next()[0]
                variant[1] = random.choice(['up', 'down'])
            elif variant[1] == 'adj':
                variant[0] = random.choice(['cos', 'tan'])
            elif variant[1] == 'opp':
                variant[0] = random.choice(['sin', 'tan'])
            elif variant[1] == 'hyp':
                variant[0] = random.choice(['sin', 'cos'])
            elif variant[1] in ['up', 'down']:
                variant[0] = shared.trigo_functions_source.next()[0]
        elif variant[0] in ['sin', 'cos', 'tan'] and variant[1] == 'random':
            variant[1] = random.choice(['up', 'down'])

        if variant[1] in ['adj', 'hyp', 'opp']:
            if variant[0] == 'cos':
                variant[1] = 'up' if variant[1] == 'adj' else 'down'
            elif variant[0] in ['sin', 'tan']:
                variant[1] = 'up' if variant[1] == 'opp' else 'down'

        if '_'.join(variant) not in valid_variants:
            raise ValueError('The provided variant, {v}, is not valid.'
                             .format(v='_'.join(variant)))

        # Now it's possible to setup the right triangle
        if variant[1] == 'up':
            self.right_triangle.setup_for_trigonometry(
                angle_nb=random.choice([0, 2]),
                trigo_fct=variant[0],
                angle_val=self.nb2,
                up_length_val=self.nb1,
                length_unit=self.length_unit)
        else:
            self.right_triangle.setup_for_trigonometry(
                angle_nb=random.choice([0, 2]),
                trigo_fct=variant[0],
                angle_val=self.nb2,
                down_length_val=self.nb1,
                length_unit=self.length_unit)

        self.wording = ''
        setup_wording_format_of(self)

        trigo_eq = self.right_triangle.trigonometric_equality(autosetup=True)
        self.resolution = trigo_eq.auto_resolution(
            dont_display_equations_name=True,
            skip_fraction_simplification=True,
            decimal_result=self.decimal_result,
            unit=self.length_unit)
        self.answer_wording = \
            _('The triangle {triangle_name} has a right angle in'
              ' {right_vertex_name}. {newline} Hence: {resolution}')
        self.triangle_name = self.right_triangle.name
        self.right_vertex_name = self.right_triangle.vertex[1].name
        setup_wording_format_of(self, w_prefix='answer_')

    def q(self, **options):
        if self.wording:
            return shared.machine.write_layout(
                (1, 2),
                [10, 10],
                [self.wording.format(**self.wording_format),
                 shared.machine.insert_picture(self.right_triangle,
                                               scale=0.8,
                                               top_aligned_in_a_tabular=True)])
        else:
            return shared.machine.insert_picture(
                self.right_triangle,
                scale=0.8,
                vertical_alignment_in_a_tabular=True)

    def a(self, **options):
        return self.answer_wording.format(**self.answer_wording_format)
