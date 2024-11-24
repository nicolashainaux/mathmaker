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
from mathmakerlib.calculus.equations import PythagoreanEquation
# from mathmakerlib import required

from mathmaker.lib import shared
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, picture=False, **options):
        # required.package['ulem'] = True
        super().setup("minimal", **options)
        super().setup("length_units", **options)

        angles = random.choice([[0, 180], [90, 270]])
        random_signs = [random.choice([-1, 1]), random.choice([-1, 1])]
        rot_angle = random.choice(angles) \
            + random_signs[0] * random.randint(0, 20)
        super().setup("right_triangle", rotation_angle=rot_angle,
                      mark_right_angle=False, **options)

        use_decimals = options.get('use_decimals', 'false')

        self.figure_in_the_text = options.get('figure_in_the_text', False)

        leg0 = Number(build_data[0], unit=self.length_unit)
        leg1 = Number(build_data[1], unit=self.length_unit)
        hyp = Number(build_data[2], unit=self.length_unit)

        if use_decimals == 'true':
            leg0 = leg0 / 10
            leg1 = leg1 / 10
            hyp = hyp / 10

        self.rt.setup_labels([leg0, leg1, hyp])

        # setup_wording_format_of(self, w_prefix='answer_')
        self.q_nb_included_in_wording = False

        self.q_nb = options.get('number_of_the_question', None)
        if self.q_nb:
            self.q_nb = shared.machine.write(self.q_nb + '. ',
                                             emphasize='bold')

    def q(self, **options):
        if self.figure_in_the_text:
            result = self.rt.drawn
        else:
            sides = [self.rt.leg0, self.rt.leg1, self.rt.hyp]
            random.shuffle(sides)
            result = _("{triangle_name} is a triangle such as "
                       "{side_length0} = {nb0}, {side_length1} = {nb1} "
                       "and {side_length2} = {nb2}.")\
                .format(triangle_name=self.rt.name,
                        side_length0=sides[0].length_name,
                        nb0=sides[0].label,
                        side_length1=sides[1].length_name,
                        nb1=sides[1].label,
                        side_length2=sides[2].length_name,
                        nb2=sides[2].label)

        result += r" \newline " + _("Is it a right triangle ? Prove your "
                                    "answer and if the triangle is right, "
                                    "give the name of the right angle.")

        return result + shared.machine.write_new_line()

    def a(self, **options):
        M = shared.machine

        result = M.write(PythagoreanEquation(self.rt).autotest())

        if self.figure_in_the_text:
            return result
        else:
            content = [_("Sketch") + ":" + M.write_new_line()
                       + self.rt.drawn, result]
            return M.write_layout((1, 2), [9, 9], content,
                                  tabular_options='[t]')
