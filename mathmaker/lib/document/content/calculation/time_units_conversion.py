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
from mathmakerlib.calculus import ClockTime

from mathmaker.lib import shared
from mathmaker.lib.constants.latex import COLORED_QUESTION_MARK
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import post_process
from mathmaker.lib.tools.wording import setup_wording_format_of

OPTIONS_VALUES = {(1, 1, 'right'), (1, 1, 'left'),
                  (2, 2, 'right'), (2, 3, 'left'),
                  (3, 2, 'right'), (3, 3, 'left')}

TIME_CONTEXT = {'sep': 'as_si_units', 'si_show_0h': False,
                'si_show_0min': False, 'si_show_0s': False}


def check_options_consistency(category, level, direction):
    possible_triplets = []
    for option in OPTIONS_VALUES:
        if ((category is None or category == option[0])
            and (level is None or level == option[1])
            and (direction is None or direction == option[2])):
            possible_triplets.append(option)
    if not possible_triplets:
        raise ValueError('Invalid set of options for this question: '
                         'category={}, level={}, direction={}'
                         .format(category, level, direction))
    return random.choice(possible_triplets)


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup('minimal', **options)
        n1, n2 = Number(build_data[0]), Number(build_data[1])
        # super().setup('numbers', shuffle_nbs=False, nb=build_data)
        # get options and check their consistency
        level = options.get('level', None)
        category = options.get('category', None)
        direction = options.get('direction', None)
        if category is not None:
            category = int(category)
        if level is not None:
            level = int(level)
        category, level, direction = check_options_consistency(category, level,
                                                               direction)
        self.transduration = 30

        # u1, u2 are basically hours, minutes OR minutes, seconds
        self.time_unit1, self.time_unit2 = \
            shared.time_units_couples_source.next()
        hint_unit = ''
        # self.nb4 is the amount of the lowest unit (minutes or seconds)
        # for instance 375 minutes
        self.nb4 = n1 * n2
        # self.nb1 is the integer of the highest unit
        # for instance 6 hours is self.nb1 for 375 minutes
        self.nb1 = Number(self.nb4 // 60)
        # self.nb2 is the rest in the lowest unit
        # for instance 15 minutes is self.nb2 for 375 minutes
        self.nb2 = Number(self.nb4 % 60)
        # self.nb3 is the amount in the highest unit (hours or minutes)
        # possibly decimal
        # for instance, 6,25 hours matches 375 minutes
        self.nb3 = self.nb1 + self.nb2 / Number(60)
        # Finally, we have:
        # self.nb1 (u1) self.nb2 (u2) = self.nb3 (u1) = self.nb4 (u2)
        u1_u2_js_ans = [self.nb1, self.nb2]

        self.time_unit = ('', self.time_unit1, '', self.time_unit2)
        if self.time_unit1 == 'h':
            clocktime = ClockTime(self.nb1, self.nb2, 0, context=TIME_CONTEXT)
        else:  # u1 == 'min'
            clocktime = ClockTime(0, self.nb1, self.nb2, context=TIME_CONTEXT)
        self.clocktime = clocktime.printed

        if category == 1:
            if direction == 'right':
                wording_part = '{clocktime} = QUESTION_MARK~{time_unit1}'
                self.solution = Number(self.nb3, unit=self.time_unit1)
                self.js_answer = self.nb3.uiprinted
                hint_unit = 'time_unit1'
            else:  # direction == 'left'
                wording_part = '{nb3} {time_unit1} = '\
                    'QUESTION_MARK~{time_unit1} QUESTION_MARK~{time_unit2}'
                self.solution = clocktime
                self.js_answer = u1_u2_js_ans
                hint_unit = 'time_unit'
        elif category == 2:
            if direction == 'right':
                wording_part = '{nb3} {time_unit1} = '\
                    'QUESTION_MARK~{time_unit2}'
                self.solution = Number(self.nb4, unit=self.time_unit2)
                self.js_answer = self.nb4.uiprinted
                hint_unit = 'time_unit2'
            else:  # direction == 'left'
                wording_part = '{nb4} {time_unit2} = '\
                    'QUESTION_MARK~{time_unit1}'
                self.solution = Number(self.nb3, unit=self.time_unit1)
                self.js_answer = self.nb3.uiprinted
                hint_unit = 'time_unit1'
        elif category == 3:
            if direction == 'right':
                wording_part = '{nb1} {time_unit1} {nb2} {time_unit2} = '\
                    'QUESTION_MARK~{time_unit2}'
                self.solution = Number(self.nb4, unit=self.time_unit2)
                self.js_answer = self.nb4.uiprinted
                hint_unit = 'time_unit2'
            else:  # direction == 'left'
                wording_part = '{nb4} {time_unit2} = '\
                    'QUESTION_MARK~{time_unit1} QUESTION_MARK~{time_unit2}'
                self.solution = clocktime
                self.js_answer = u1_u2_js_ans
                hint_unit = 'time_unit'

        self.wording = _('Convert: {} |hint:{}|').format(wording_part,
                                                         hint_unit)
        setup_wording_format_of(self)

    def q(self, **options):
        return post_process(self.wording.format(**self.wording_format))\
            .replace('QUESTION_MARK', COLORED_QUESTION_MARK)

    def a(self, **options):
        return self.solution.printed

    def js_a(self, **kwargs):
        return [self.js_answer]
