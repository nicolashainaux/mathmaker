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
from mathmakerlib.geometry import Point, Angle, AngleDecoration
from mathmakerlib.LaTeX import XCOLOR_DVIPSNAMES

from mathmaker.lib import shared
from mathmaker.lib.document.content import component

COLORS = list(XCOLOR_DVIPSNAMES)
COLORS.pop(COLORS.index('White'))


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        super().setup("numbers", nb=build_data, **options)
        # super().setup("nb_variants", nb=build_data, **options)

        self.q_nb_included_in_wording = True

        read_direction = options.get('read', 'alternate')
        if read_direction == 'alternate':
            read_direction = \
                shared.alternate_clockwise_anticlockwise_source.next()[0]

        direction = -1 if read_direction == 'clockwise' else 1
        A = Point(5.5 * direction, 0, 'A')
        Ω = Point(0, 0, 'O')
        self.answer = Number(self.nb1, unit=r'\degree').printed
        self.vrule = r'\vrule width 0pt height 0.5cm'
        self.color = random.choice(COLORS)
        self.q_nb = options.get('number_of_the_question', '')
        self.q_text = f'n°{self.q_nb} :' + r' \dots\dots\dots ' + self.vrule
        self.a_text = f'n°{self.q_nb} : {self.answer} ' + self.vrule

        ω = Angle(A, Ω, direction * self.nb1, thickness='thick',
                  arrow_tips='round cap-round cap',
                  callout_text=self.q_text,
                  callout_fmt={'fillcolor': f'{self.color}!20'})
        ω.decoration = AngleDecoration(fillcolor=f'{self.color}!30',
                                       color=self.color, radius='auto',
                                       thickness='thick')
        ω.rotate(random.choice(range(-15, 15)))
        self.q_angle = ω.drawn

        ω.callout_text = self.a_text
        ω.setup_callout()
        self.a_angle = ω.drawn

    def q(self, **options):
        return self.q_angle

    def a(self, **options):
        return self.a_angle

    def js_a(self, **kwargs):
        pass
