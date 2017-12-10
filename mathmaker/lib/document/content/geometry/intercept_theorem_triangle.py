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
from mathmaker.lib.core.base_calculus import Item, Sum
from mathmaker.lib.core.calculus import Equality, Equation
from mathmaker.lib.document.content import component

ALL_LENGTHS_TO_CALCULATE = ['oneside', 'onechunk', 'twosides', 'twochunks',
                            'onesideonechunk']


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
        super().setup("intercept_theorem_figure", **options)

        if self.variant == 'default':
            variant = ['oneside', 'random', 'false']
        else:
            if self.variant.count('_') != 2:
                raise ValueError('XMLFileFormatError: the variant for '
                                 'intercept_theorem_triangle '
                                 'shoud contain two _')
            variant = self.variant.split(sep='_')

        valid_variant = [['onerandom', 'tworandom', 'random', 'oneside',
                          'onechunk', 'twosides', 'twochunks',
                          'onesideonechunk'],
                         ['random', 'all', 'twocouples'],
                         ['random', 'true', 'false']]

        for v, valid, n in zip(variant, valid_variant,
                               ['first', 'second', 'third']):
            if v not in valid:
                raise ValueError('XMLFileFormatError: invalid {} part of the '
                                 'variant. It should be in: {}'
                                 .format(n, str(valid)))

        if variant[0] == 'onerandom':
            variant[0] = random.choice(['oneside', 'onechunk'])
        elif variant[0] == 'tworandom':
            if variant[1] == 'twocouples':
                raise ValueError('XMLFileFormatError: the '
                                 'tworandom_twocouples_* '
                                 'variants are impossible.')
            if variant[2] == 'random':
                variant[2] = random.choice(['true', 'false'])

            if variant[2] == 'false':
                variant[0] = random.choice(['twosides', 'twochunks',
                                            'onesideonechunk'])
            elif variant[2] == 'true':
                variant[0] = random.choice(['twosides', 'onesideonechunk'])
            else:
                raise ValueError('XMLFileFormatError: the third part of the '
                                 'variant should be "true" or "false".')

        # The order is:
        # small[0] small[1] small[2] side[0] side[1] side[2] chunk[0] chunk[1]
        # 'hid' means 'hidden', e.g. the length won't be displayed but can be
        # easily calculated before using the intercept theorem.
        labels_configurations = {
            'oneside_all_false': [
                ['?', True, True, True, True, True, False, False],
                [True, '?', True, True, True, True, False, False],
                [True, True, '?', True, True, True, False, False],
                [True, True, True, '?', True, True, False, False],
                [True, True, True, True, '?', True, False, False],
                [True, True, True, True, True, '?', False, False]
            ],
            'oneside_all_true': [
                ['?', True, True, True, True, 'hid', False, True],
                [True, '?', True, 'hid', True, 'hid', True, True],
                [True, '?', True, 'hid', True, True, True, False],
                [True, '?', True, True, True, 'hid', False, True],
                [True, True, '?', 'hid', True, True, True, False],
                [True, True, True, '?', True, 'hid', False, True],
                [True, True, True, True, '?', 'hid', False, True],
                [True, True, True, 'hid', '?', 'hid', True, True],
                [True, True, True, 'hid', '?', True, True, False],
                [True, True, True, 'hid', True, '?', True, False],
            ],
            'onechunk_all_false': [
                [True, True, True, False, True, True, '?', False],
                [True, True, True, True, True, False, False, '?']
            ],
            'onechunk_all_true': [
                [True, True, True, False, True, 'hid', '?', True],
                [True, True, True, 'hid', True, False, True, '?']
            ],
            'twosides_all_false': [
                ['?', '?', True, True, True, True, False, False],
                ['?', True, '?', True, True, True, False, False],
                [True, '?', '?', True, True, True, False, False],
                ['?', True, True, True, '?', True, False, False],
                ['?', True, True, True, True, '?', False, False],
                [True, '?', True, '?', True, True, False, False],
                [True, '?', True, True, True, '?', False, False],
                [True, True, '?', True, '?', True, False, False],
                [True, True, '?', '?', True, True, False, False],
                [True, True, True, '?', '?', True, False, False],
                [True, True, True, '?', True, '?', False, False],
                [True, True, True, True, '?', '?', False, False],
            ],
            'twosides_all_true': [
                ['?', '?', True, True, True, 'hid', False, True],
                [True, '?', '?', 'hid', True, True, True, False],
                ['?', True, True, True, '?', 'hid', False, True],
                [True, '?', True, '?', True, 'hid', False, True],
                [True, '?', True, False, True, '?', True, False],
                [True, True, '?', False, '?', True, True, False],
                [True, True, True, '?', '?', 'hid', False, True],
                [True, True, True, 'hid', '?', '?', True, False],
            ],
            'twochunks_all_false': [
                [False, True, False, True, True, True, '?', '?'],
                [True, True, False, False, True, True, '?', '?'],
                [False, True, True, True, True, False, '?', '?'],
                [True, True, True, False, True, False, '?', '?'],
            ],
            'onesideonechunk_all_false': [
                [False, '?', True, True, True, True, '?', False],
                [True, '?', False, True, True, True, False, '?'],
                [True, '?', True, False, True, True, '?', False],
                [True, '?', True, True, True, False, False, '?'],
                [False, True, '?', True, True, True, '?', False],
                ['?', True, False, True, True, True, False, '?'],
                [True, True, '?', False, True, True, '?', False],
                ['?', True, True, True, True, False, False, '?'],
                [True, True, True, False, True, '?', '?', False],
                [True, True, True, '?', True, False, False, '?'],
                [False, True, True, True, True, '?', '?', False],
                [True, True, False, '?', True, True, False, '?'],
                [False, True, True, True, '?', True, '?', False],
                [True, True, False, True, '?', True, False, '?'],
                [True, True, True, False, '?', True, '?', False],
                [True, True, True, True, '?', False, False, '?'],
            ],
            'onesideonechunk_all_true': [
                [True, '?', True, False, True, 'hid', '?', True],
                [True, '?', True, 'hid', True, False, True, '?'],
                [False, '?', True, True, True, 'hid', '?', True],
                [True, '?', False, 'hid', True, True, True, '?'],
                [True, True, True, False, '?', 'hid', '?', True],
                [True, True, True, 'hid', '?', False, True, '?'],
                [False, True, True, True, '?', 'hid', '?', True],
                [True, True, False, 'hid', '?', True, True, '?'],
            ],
            'oneside_twocouples_false': [
                ['?', True, False, True, True, False, False, False],
                [False, True, '?', False, True, True, False, False],
                [True, True, False, True, '?', False, False, False],
                [False, True, True, False, '?', True, False, False],
                ['?', False, True, True, False, True, False, False],
                [True, False, '?', True, False, True, False, False],
                [True, '?', False, True, True, False, False, False],
                [False, '?', True, False, True, True, False, False],
                [False, True, True, False, True, '?', False, False],
                [True, True, False, '?', True, False, False, False],
                [True, False, True, True, False, '?', False, False],
                [True, False, True, '?', False, True, False, False],
            ],
            'oneside_twocouples_true': [
                ['?', False, True, True, False, 'hid', False, True],
                [True, False, '?', 'hid', False, True, True, False],
                [True, '?', False, 'hid', True, False, True, False],
                [False, '?', True, False, True, 'hid', False, True],
                [True, True, False, 'hid', '?', False, True, False],
                [False, True, True, False, '?', 'hid', False, True],
                [True, False, True, '?', False, 'hid', False, True],
                [True, False, True, 'hid', False, '?', True, False],
            ],
            'onechunk_twocouples_false': [
                [True, True, False, False, True, False, '?', False],
                [False, True, True, False, True, False, False, '?'],
                [True, False, True, False, False, True, '?', False],
                [True, False, True, True, False, False, False, '?'],
            ],
            'onechunk_twocouples_true': [
                [True, False, True, False, False, 'hid', '?', True],
                [True, False, True, 'hid', False, False, True, '?'],
            ]
        }

        random_nb = variant.count('random')
        if random_nb == 3:
            variant = random.choice(
                list(labels_configurations.keys())).split(sep='_')
        elif random_nb == 2:
            if variant[0] == 'random' and variant[1] == 'random':
                if variant[2] == 'false':
                    variant[0] = random.choice(ALL_LENGTHS_TO_CALCULATE)
                    if variant[0] in ['twosides', 'twochunks',
                                      'onesideonechunk']:
                        variant[1] = 'all'
                    else:
                        variant[1] = random.choice(['all', 'twocouples'])
                elif variant[2] == 'true':
                    variant[0] = random.choice(['oneside', 'onechunk',
                                                'twosides', 'onesideonechunk'])
                    if variant[0] in ['oneside', 'onechunk']:
                        variant[1] = random.choice(['all', 'twocouples'])
                    else:
                        variant[1] = 'all'
            elif variant[0] == 'random' and variant[2] == 'random':
                if variant[1] == 'all':
                    variant[0] = random.choice(ALL_LENGTHS_TO_CALCULATE)
                    if variant[0] == 'twochunks':
                        variant[2] = 'false'
                    else:
                        variant[2] = random.choice(['true', 'false'])
                elif variant[1] == 'twocouples':
                    variant[0] = random.choice(['oneside', 'onechunk'])
                    variant[2] = random.choice(['true', 'false'])
            elif variant[1] == 'random' and variant[2] == 'random':
                if variant[0] in ['oneside', 'onechunk']:
                    variant[1] = random.choice(['all', 'twocouples'])
                    variant[2] = random.choice(['true', 'false'])
                elif variant[0] in ['twosides', 'onesideonechunk']:
                    variant[1] = 'all'
                    variant[2] = random.choice(['true', 'false'])
                elif variant[0] == 'twochunks':
                    variant[1] = 'all'
                    variant[2] = 'false'
        elif random_nb == 1:
            if variant[0] == 'random':
                if variant[1] == 'twocouples':
                    variant[0] = random.choice(['oneside', 'onechunk'])
                elif variant[1] == 'all':
                    if variant[2] == 'true':
                        variant[0] = random.choice(['oneside', 'onechunk',
                                                    'twosides',
                                                    'onesideonechunk'])
                    elif variant[2] == 'false':
                        variant[0] = random.choice(ALL_LENGTHS_TO_CALCULATE)
            elif variant[1] == 'random':
                if variant[0] in ['oneside', 'onechunk']:
                    variant[1] = random.choice(['all', 'twocouples'])
                elif variant[0] in ['twosides', 'onesideonechunk']:
                    variant[1] = 'all'
                elif variant[0] == 'twochunks':
                    if variant[2] == 'false':
                        variant[1] = 'all'
                    else:
                        raise ValueError('XMLFileFormatError: invalid'
                                         'variants: "twochunks_*_true".')
            elif variant[2] == 'random':
                if variant[0] in ['oneside', 'onechunk']:
                    variant[2] = random.choice(['true', 'false'])
                elif variant[1] == 'twocouples':
                    raise ValueError('XMLFileFormatError: invalid variants: '
                                     '"two..._twocouples_*".')
                else:
                    if variant[0] == 'twochunks':
                        variant[2] = 'false'
                    else:
                        variant[2] = random.choice(['true', 'false'])

        variant_key = '_'.join(variant)
        labels_conf = random.choice(labels_configurations[variant_key])

        self.figure.setup_labels(labels_conf,
                                 segments_list=self.figure.small
                                 + [self.figure.u,
                                    self.figure.side[1],
                                    self.figure.v]
                                 + self.figure.chunk)

        self.figure.setup_labels([labels_conf[3], labels_conf[5]],
                                 segments_list=[self.figure.side[0],
                                                self.figure.side[2]])

        lengths_to_calculate = [s.length_name
                                for s in self.figure.small + self.figure.side
                                if s.label == Value('?')]

        chunks_to_calculate = []
        chunks_infos = []

        if 'chunk' in variant_key:
            if len(lengths_to_calculate) == 1:
                chunks_to_calculate = [None]
                chunks_infos = [None]
            if labels_conf[6] == '?':
                # This matches chunk0
                chunks_to_calculate += [self.figure.chunk[0].length_name]
                chunks_infos += [(self.figure.side[0].length_name,
                                  self.figure.small[0].length_name,
                                  self.figure.side[0].length,
                                  self.figure.small[0].length)]
                if not labels_conf[0]:
                    lengths_to_calculate += [self.figure.small[0].length_name]
                else:
                    lengths_to_calculate += [self.figure.side[0].length_name]
            if labels_conf[7] == '?':
                # This matches chunk1
                chunks_to_calculate += [self.figure.chunk[1].length_name]
                chunks_infos += [(self.figure.side[2].length_name,
                                  self.figure.small[2].length_name,
                                  self.figure.side[2].length,
                                  self.figure.small[2].length)]
                if not labels_conf[2]:
                    lengths_to_calculate += [self.figure.small[2].length_name]
                else:
                    lengths_to_calculate += [self.figure.side[2].length_name]

        self.line1 = self.figure.small[1].length_name
        self.line2 = self.figure.side[1].length_name
        lengths_asked_for = [s.length_name
                             for s in self.figure.small + self.figure.side
                             + self.figure.chunk
                             if s.label == Value('?')]
        self.length1_name = lengths_asked_for[0]
        if len(lengths_asked_for) == 2:
            self.length2_name = lengths_asked_for[1]

        if len(lengths_asked_for) == 1:
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

        preamble = ''
        if variant_key.endswith('true'):
            self.pre_reso0 = self.pre_reso1 = ''
            if labels_conf[6] is True:
                pre_equality0 = Equality(
                    [Item(self.side0_length_name),
                     Sum([Item(self.small0_length_name),
                          Item(self.chunk0_length_name)
                          ])],
                    subst_dict={Value(self.small0_length_name):
                                Value(self.figure.small[0].length),
                                Value(self.chunk0_length_name):
                                Value(self.figure.chunk[0].length)}
                )
                pre_equality0_str = pre_equality0.into_str()
                pre_equation0 = Equation(pre_equality0.substitute())
                self.pre_reso0 = shared.machine.write_math_style1(
                    pre_equality0_str) \
                    + pre_equation0.auto_resolution(
                        dont_display_equations_name=True,
                        decimal_result=2,
                        unit=self.length_unit,
                        underline_result=True)
            if labels_conf[7] is True:
                pre_equality1 = Equality(
                    [Item(self.side1_length_name),
                     Sum([Item(self.small1_length_name),
                          Item(self.chunk1_length_name)
                          ])],
                    subst_dict={Value(self.small1_length_name):
                                Value(self.figure.small[2].length),
                                Value(self.chunk1_length_name):
                                Value(self.figure.chunk[1].length)}
                )
                pre_equality1_str = pre_equality1.into_str()
                pre_equation1 = Equation(pre_equality1.substitute())
                self.pre_reso1 = shared.machine.write_math_style1(
                    pre_equality1_str) \
                    + pre_equation1.auto_resolution(
                        dont_display_equations_name=True,
                        decimal_result=2,
                        unit=self.length_unit,
                        underline_result=True)
            if labels_conf[6] is True and labels_conf[7] is True:
                preamble = _('Note: {pre_reso0} {newline} and: {pre_reso1} '
                             '{newline} ')
            elif labels_conf[6] is True:
                preamble = _('Note: {pre_reso0} {newline} ')
            elif labels_conf[7] is True:
                preamble = _('Note: {pre_reso1} {newline} ')

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

        chunks_part = ''
        if len(chunks_to_calculate):
            if chunks_to_calculate[0] is not None:
                chunk_equality0 = Equality(
                    [Item(chunks_to_calculate[0]),
                     Sum([Item(chunks_infos[0][0]),
                          Item(('-', chunks_infos[0][1]))
                          ])],
                    subst_dict={Value(chunks_infos[0][0]):
                                Value(chunks_infos[0][2]),
                                Value(chunks_infos[0][1]):
                                Value(chunks_infos[0][3])})
                chunk_equality0_str = chunk_equality0.into_str()
                chunk_equation0 = Equation(chunk_equality0.substitute())
                self.chunk_reso0 = shared.machine.write_math_style1(
                    chunk_equality0_str) \
                    + chunk_equation0.auto_resolution(
                        dont_display_equations_name=True,
                        decimal_result=2,
                        unit=self.length_unit,
                        underline_result=True)
                chunks_part += _('so: {chunk_reso0} ')
            else:
                chunks_part += '~\n\n\\newline\\newline\\newline\\newline\n\n'

            if len(chunks_to_calculate) == 2:
                chunk_equality1 = Equality(
                    [Item(chunks_to_calculate[1]),
                     Sum([Item(chunks_infos[1][0]),
                          Item(('-', chunks_infos[1][1]))
                          ])],
                    {Value(chunks_infos[1][0]): Value(chunks_infos[1][2]),
                     Value(chunks_infos[1][1]): Value(chunks_infos[1][3])})
                chunk_equality1_str = chunk_equality1.into_str()
                chunk_equation1 = Equation(chunk_equality1.substitute())
                self.chunk_reso1 = shared.machine.write_math_style1(
                    chunk_equality1_str) \
                    + chunk_equation1.auto_resolution(
                        dont_display_equations_name=True,
                        decimal_result=2,
                        unit=self.length_unit,
                        underline_result=True)
                chunks_part = shared.machine.write(
                    chunks_part + _('so: {chunk_reso1} '),
                    multicolumns=2)

        ans_variant = options.get('ans_variant', 'default')
        ans_texts = {
            'default': _('As: {line1} {parallel_to} {line2}, '
                         '{point0_name} {belongs_to} {side0_length_name} and '
                         '{point1_name} {belongs_to} {side1_length_name}, '
                         'then by the intercept theorem: {newline} '
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
                              'and as {vertex1_name}, {point0_name} and '
                              '{main_vertex_name} on one hand, '
                              '{vertex2_name}, {point1_name} and '
                              '{main_vertex_name} on the other hand,'
                              'are aligned in the same order, '
                              'then by the intercept theorem: {newline} '
                              '{ratios} '
                              'thus: {ratios_substituted} ')
        }

        self.answer_wording = preamble \
            + ans_texts[ans_variant] \
            + lengths_resolutions_part \
            + chunks_part

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
