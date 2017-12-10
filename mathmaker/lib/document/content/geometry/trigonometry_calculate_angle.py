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
        # nb1 and nb2 are sides' lengths,
        # they may require to be ordered, later on...
        super().setup("numbers", nb=build_data,
                      shuffle_nbs=False, sort_nbs=True, **options)

        if self.variant in ['default', 'random']:
            variant = shared.trigo_functions_source.next()[0]
        else:
            variant = self.variant

        if variant not in ['cos', 'sin', 'tan']:
            raise ValueError('XMLFileFormatError: invalid variant: {v}, '
                             .format(v=variant) + 'It should be in: '
                             '[\'cos\', \'sin\', \'tan\']')

        # nb2 being the greatest length (the numbers have been ordered at
        # setup), it must be used as hypotenuse's length in cosine and sine
        # cases
        up_val = self.nb1
        down_val = self.nb2
        if variant == 'tan' and random.choice([True, False]):
            up_val, down_val = down_val, up_val

        self.right_triangle.setup_for_trigonometry(
            angle_nb=random.choice([0, 2]),
            trigo_fct=variant,
            down_length_val=down_val,
            up_length_val=up_val,
            length_unit=self.length_unit)

        self.wording = ''
        setup_wording_format_of(self)

        trigo_eq = self.right_triangle.trigonometric_equality(autosetup=True)
        self.resolution = trigo_eq.auto_resolution(
            dont_display_equations_name=True,
            skip_fraction_simplification=True,
            decimal_result=self.decimal_result,
            unit='\\textdegree')
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
