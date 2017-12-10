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
from mathmaker.lib.core.root_calculus import Value
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, picture='true', **options):
        super().setup("minimal", **options)
        super().setup("length_units", **options)
        super().setup("right_triangle", **options)
        # There's no need to setup numbers for this question.

        if self.variant in ['default', 'random']:
            variant = shared.trigo_functions_source.next()[0]
        else:
            variant = self.variant

        if variant not in ['cos', 'sin', 'tan']:
            raise ValueError('XMLFileFormatError: invalid variant: {v}, '
                             .format(v=variant) + 'It should be in: '
                             '[\'cos\', \'sin\', \'tan\']')

        angle_nb = random.choice([0, 2])

        self.right_triangle.setup_for_trigonometry(
            angle_nb=angle_nb,
            trigo_fct=variant,
            down_length_val=Value(''),
            up_length_val=Value(''),
            length_unit=self.length_unit,
            only_mark_unknown_angle=True)

        self.trigo_fct = variant
        self.the_formula_of_trigo_fct = {
            'cos': _('the formula of cosine'),
            'sin': _('the formula of sine'),
            'tan': _('the formula of tangent')}[variant]
        self.acute_angle = shared.machine.write_math_style2(
            self.right_triangle.angle[angle_nb].printed)

        self.wording = options.get('text', options.get('wording', ''))
        if self.wording:
            self.wording = _(self.wording)
        setup_wording_format_of(self)

        self.formula = shared.machine.write_math_style1(
            self.right_triangle.trigonometric_equality(
                angle=self.right_triangle.angle[angle_nb],
                trigo_fct=variant).printed)

        self.answer_wording = \
            _('The formula is: {formula}')
        setup_wording_format_of(self, w_prefix='answer_')
        self.q_nb_included_in_wording = False

    def q(self, **options):
        q_nb = options.get('number_of_the_question', '')
        if q_nb:
            q_nb = shared.machine.write(q_nb + '. ', emphasize='bold')
        if self.wording:
            self.q_nb_included_in_wording = True
            return shared.machine.write_layout(
                (1, 2),
                [12, 8],
                [q_nb + self.wording.format(**self.wording_format),
                 shared.machine.insert_picture(
                    self.right_triangle,
                    scale=0.8,
                    vertical_alignment_in_a_tabular=True)])
        else:
            return shared.machine.insert_picture(
                self.right_triangle,
                scale=0.8,
                vertical_alignment_in_a_tabular=True)

    def a(self, **options):
        return self.answer_wording.format(**self.answer_wording_format)
