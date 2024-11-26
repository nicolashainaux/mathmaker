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

import math
import random

from . import converse_of_pythagorean_theorem


class sub_object(converse_of_pythagorean_theorem.sub_object):

    def __init__(self, build_data, picture=False, **options):
        build_data = list(build_data)

        exactness = build_data[-1]

        if exactness == 'approx':
            # then either leg0 or hyp is supposed to equal 0
            if str(build_data[0]) == '0':
                leg1, hyp = build_data[1], build_data[2]
                build_data[0] = round(math.sqrt(hyp * hyp - leg1 * leg1))
            elif str(build_data[2]) == '0':
                leg0, leg1 = build_data[0], build_data[1]
                build_data[2] = round(math.sqrt(leg0 * leg0 + leg1 * leg1))

        else:  # exactness == 'exact', so we'll change exactly one value
            # to ensure the triplet is NOT pythagorean
            # 0 is leg0; 2 is hyp
            choice = random.choice([0, 2])
            max_delta = int(0.1 * build_data[choice])
            min_delta = 1
            if min_delta > max_delta:
                max_delta = min_delta
            chosen_delta = random.choice(
                [i + min_delta for i in range(max_delta - min_delta + 1)])

            factor = -1 if choice == 0 else 1
            build_data[choice] = build_data[choice] + factor * chosen_delta

        super().__init__(tuple(build_data), picture=picture, **options)
