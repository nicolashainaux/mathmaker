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
from mathmaker.lib.core.base_calculus import Item
from mathmaker.lib.document.content import component

ALL_LENGTHS_TO_CALCULATE = ['oneside', 'twosides']


class sub_object(component.structure):

    def __init__(self, build_data, picture='true', **options):
        super().setup("minimal", **options)
        if build_data[0] < 11:
            raise ValueError('build_data[0] == {} whereas it should be '
                             '>= 11'.format(str(build_data[0])))
        build_data = (build_data[0] / 10, ) + build_data[1:]
        super().setup("numbers", nb=build_data,
                      shuffle_nbs=False, **options)
        super().setup("length_units", **options)
        super().setup("intercept_theorem_figure", butterfly=True, **options)

        if self.variant == 'default':
            variant = ['random', 'random']
        else:
            if self.variant.count('_') != 1:
                raise ValueError('XMLFileFormatError: the variant for '
                                 'intercept_theorem_butterfly '
                                 'shoud contain one _')
            variant = self.variant.split(sep='_')

        valid_variant = [['random', 'oneside', 'twosides'],
                         ['random', 'all', 'twocouples']]

        for v, valid, n in zip(variant, valid_variant,
                               ['first', 'second', 'third']):
            if v not in valid:
                raise ValueError('XMLFileFormatError: Invalid {} part of the '
                                 'variant. It should be in: {}'
                                 .format(n, str(valid)))

        if variant[0] == 'random':
            if variant[1] == 'twocouples':
                variant[0] = 'oneside'
            else:
                variant[0] = random.choice(['oneside', 'twosides'])
        if variant[1] == 'random':
            if variant[0] == 'twosides':
                variant[1] = 'twocouples'
            else:
                variant[1] == random.choice(['all', 'twocouples'])

        if variant == ['twosides', 'twocouples']:
            raise ValueError('XMLFileFormatError: The twosides_twocouples '
                             'variant is impossible.')

        # The order is:
        # small[0] small[1] small[2] side[0] side[1] side[2]
        labels_configurations = {
            'oneside_all': [
                ['?', True, True, True, True, True],
                [True, '?', True, True, True, True],
                [True, True, '?', True, True, True],
                [True, True, True, '?', True, True],
                [True, True, True, True, '?', True],
                [True, True, True, True, True, '?']
            ],
            'oneside_twocouples': [
                ['?', True, False, True, True, False],
                [False, True, '?', False, True, True],
                [True, True, False, True, '?', False],
                [False, True, True, False, '?', True],
                ['?', False, True, True, False, True],
                [True, False, '?', True, False, True],
                [True, '?', False, True, True, False],
                [False, '?', True, False, True, True],
                [False, True, True, False, True, '?'],
                [True, True, False, '?', True, False],
                [True, False, True, True, False, '?'],
                [True, False, True, '?', False, True],
            ],
            'twosides_all': [
                ['?', '?', True, True, True, True],
                ['?', True, '?', True, True, True],
                [True, '?', '?', True, True, True],
                ['?', True, True, True, '?', True],
                ['?', True, True, True, True, '?'],
                [True, '?', True, '?', True, True],
                [True, '?', True, True, True, '?'],
                [True, True, '?', True, '?', True],
                [True, True, '?', '?', True, True],
                [True, True, True, '?', '?', True],
                [True, True, True, '?', True, '?'],
                [True, True, True, True, '?', '?'],
            ]
        }

        variant_key = '_'.join(variant)
        labels_conf = random.choice(labels_configurations[variant_key])

        self.figure.setup_labels(labels_conf,
                                 segments_list=self.figure.small
                                 + self.figure.side)

        lengths_to_calculate = [s.length_name
                                for s in self.figure.small + self.figure.side
                                if s.label == Value('?')]

        self.line1 = self.figure.small[1].length_name
        self.line2 = self.figure.side[1].length_name
        self.length1_name = lengths_to_calculate[0]
        if len(lengths_to_calculate) == 2:
            self.length2_name = lengths_to_calculate[1]

        if len(lengths_to_calculate) == 1:
            self.wording = _('The drawn figure is out of shape. {newline} '
                             'The lengths are given in {length_unit}. '
                             '{newline} '
                             'The {line1} is parallel to {line2}. {newline} '
                             '{newline} '
                             'Determine the length of {length1_name}.')
        else:
            self.wording = _('The drawn figure is out of shape. {newline} '
                             'The lengths are given in {length_unit}. '
                             '{newline} '
                             'The {line1} is parallel to {line2}. {newline} '
                             '{newline} '
                             'Determine the lengths of {length1_name} '
                             'and {length2_name}.')
        setup_wording_format_of(self)

        self.ratios = shared.machine.write_math_style1(
            self.figure.ratios_equalities().into_str())
        self.ratios_substituted = shared.machine.write_math_style1(
            self.figure.ratios_equalities_substituted().into_str())

        self.resolution0 = self.figure.ratios_equalities_substituted()\
            .into_crossproduct_equation(Item(lengths_to_calculate[0]))\
            .auto_resolution(dont_display_equations_name=True,
                             skip_first_step=True,
                             skip_fraction_simplification=True,
                             decimal_result=2,
                             unit=self.length_unit,
                             underline_result=True)
        lengths_resolutions_part = _('hence: {resolution0} ')
        if len(lengths_to_calculate) == 2:
            self.resolution1 = self.figure.ratios_equalities_substituted()\
                .into_crossproduct_equation(Item(lengths_to_calculate[1]))\
                .auto_resolution(dont_display_equations_name=True,
                                 skip_first_step=True,
                                 skip_fraction_simplification=True,
                                 decimal_result=2,
                                 unit=self.length_unit,
                                 underline_result=True)
            lengths_resolutions_part = shared.machine.write(
                lengths_resolutions_part + _('and: {resolution1} '),
                multicolumns=2)

        ans_variant = options.get('ans_variant', 'default')
        ans_texts = {
            'default': _('As: {line1} {parallel_to} {line2}, '
                         '{main_vertex_name} {belongs_to} {chunk0_length_name}'
                         ' and '
                         '{main_vertex_name} {belongs_to} {chunk1_length_name}'
                         ', then by the intercept theorem: {newline} '
                         '{ratios} '
                         'thus: {ratios_substituted} '),
            'alternative1': _('As {line1} is parallel to {line2}, '
                              'and as the line {chunk0_length_name} cuts '
                              'the line {chunk1_length_name} at point '
                              '{main_vertex_name}, '
                              'then by the intercept theorem: {newline} '
                              '{ratios} '
                              'thus: {ratios_substituted} '),
            'alternative2': _('As: {line1} is parallel to {line2}, '
                              'and as {point0_name}, {main_vertex_name} and '
                              '{vertex1_name} on one hand, '
                              '{point1_name}, {main_vertex_name} and '
                              '{vertex2_name} on the other hand,'
                              'are aligned in the same order, '
                              'then by the intercept theorem: {newline} '
                              '{ratios} '
                              'thus: {ratios_substituted} ')
        }

        self.answer_wording = ans_texts[ans_variant] + lengths_resolutions_part

        setup_wording_format_of(self, w_prefix='answer_')

    def q(self, **options):
        return shared.machine.write_layout(
            (1, 2),
            [10, 10],
            [self.wording.format(**self.wording_format),
             shared.machine.insert_picture(self.figure,
                                           scale=0.7,
                                           top_aligned_in_a_tabular=True)])

    def a(self, **options):
        return self.answer_wording.format(**self.answer_wording_format)

    # TODO: create the "js" answer (for interactive pdf)
    # def js_a(self, **kwargs):
    #     return [self......jsprinted]
