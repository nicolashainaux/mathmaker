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

# This module will ask the figure of a given rank in a given decimal number.

import copy
import random

from mathmaker.lib import shared
from mathmaker.lib.tools import fix_math_style2_fontsize
from mathmaker.lib.tools.database import generate_random_decimal_nb
from mathmaker.lib.core.base_calculus import Item, Fraction


class sub_object(object):

    def __init__(self, **options):
        self.preset = options.get('preset', 'default')
        rank_to_use = options.get('numbers_to_use')[0]

        self.decimal_representation = \
            generate_random_decimal_nb(rank_to_use,
                                       width=random.choice([1, 2, 3]),
                                       generation_type='default',
                                       unique_figures=options.get(
                                           'unique_figures', False),
                                       grow_left=True,
                                       **options)
        self.fraction = Fraction(self.decimal_representation)
        self.fraction10 = copy.deepcopy(self.fraction)
        self.fraction10.set_numerator(
            Item(self.fraction.numerator.evaluate() * 10))
        self.fraction10.set_denominator(
            Item(self.fraction.denominator.evaluate() * 10))
        directions = {'left': 'to_decimal', 'right': 'to_fraction'}
        self.direction = options.get('direction',
                                     directions[
                                         next(shared.alternate_source)[0]])
        self.transduration = 8

    def q(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        if self.direction == 'to_decimal':
            result = _('Decimal representation of {}?') \
                .format(fix_math_style2_fontsize(
                    shared.machine.write_math_style2(
                        self.fraction.printed)))
        else:
            result = _('Decimal fraction equal to {}?') \
                .format(shared.machine.write_math_style2(
                    Item(self.decimal_representation).printed))
        return result

    def a(self, **options):
        if self.direction == 'to_decimal':
            return shared.machine.write_math_style2(
                Item(self.decimal_representation).printed)
        else:
            return fix_math_style2_fontsize(_('{} (or {} etc.)').format(
                shared.machine.write_math_style2(self.fraction.printed),
                shared.machine.write_math_style2(self.fraction10.printed)),
                mathsize='\large')
