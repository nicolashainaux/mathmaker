# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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

# This module will ask to tell the rank of a figure in a given number.

from mathmaker.lib.common.cst import RANKS_WORDS
from . import rank_reversed


class sub_object(object):

    def __init__(self, rank_to_use, **options):
        rank_reversed.sub_object.__init__(self, rank_to_use, direct=True,
                                          **options)

    def q(self, **options):
        return _("What is the rank of the figure {figure} in the number \
{decimal_number}?").format(decimal_number=self.chosen_deci_str,
                           figure=self.chosen_figure)

    def a(self, **options):
        return _(str(RANKS_WORDS[self.chosen_rank]))
