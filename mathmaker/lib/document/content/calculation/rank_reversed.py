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


from decimal import Decimal

from mathmaker.lib.tools.database import generate_random_decimal_nb
from mathmaker.lib.core.base_calculus import Item
from mathmaker.lib.constants.numeration import RANKS_WORDS


class sub_object(object):

    def __init__(self, **options):
        self.preset = options.get('preset', 'default')
        rank_to_use = options.get('numbers_to_use')[0]

        self.chosen_deci = \
            generate_random_decimal_nb(rank_to_use, **options)
        self.chosen_figure = (self.chosen_deci
                              % (rank_to_use * Decimal('10'))) // rank_to_use
        self.chosen_deci_str = Item((self.chosen_deci)).printed
        self.chosen_rank = rank_to_use
        self.transduration = 8

    def q(self, **options):
        if self.preset == 'mental calculation':
            result = _('Digit of {position} in {decimal_number}?')
        else:
            result = _('Which figure matches the {position} in the number \
    {decimal_number}?')

        return result.format(decimal_number=self.chosen_deci_str,
                             position=_(str(RANKS_WORDS[self.chosen_rank])))

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.chosen_figure
