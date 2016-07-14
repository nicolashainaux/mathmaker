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

# This module will ask the figure of a given rank in a given decimal number.

import copy
import random

from decimal import Decimal
from mathmaker.lib.core.base_calculus import Item
from mathmaker.lib import randomly
from mathmaker.lib.common.cst import RANKS, RANKS_CONFUSING, RANKS_WORDS

DEFAULT_WIDTH = "random"
DEFAULT_RANKS_SCALE = RANKS


class sub_object(object):

    def __init__(self, rank_to_use, **options):
        rank_to_use = rank_to_use[0]
        generation_type = options.get('generation_type',
                                      randomly.pop(["default", "alternative"]))
        figures = [str(i + 1) for i in range(9)]
        ranks_scale = options.get('ranks_scale',
                                  copy.copy(DEFAULT_RANKS_SCALE))
        width = DEFAULT_WIDTH
        if 'width' in options:
            try:
                width = int(options['width'])
                if not (1 <= width <= len(ranks_scale)):
                    width = DEFAULT_WIDTH
            except ValueError:
                width = DEFAULT_WIDTH

        if width == "random":
            if generation_type == "default":
                width = randomly.pop([3, 4, 5, 6, 7])
            else:
                width = randomly.pop([2, 3, 4, 5],
                                     weighted_table=[0.1, 0.3, 0.35, 0.25])
            if 'numberof' in options:
                width = randomly.pop([2, 3, 4, 5],
                                     weighted_table=[0.15, 0.4, 0.3, 0.15])
        if 'numberof' in options:
            generation_type = "default"

        rank_matches_invisible_zero = False
        if "direct" not in options:
            if ('rank_matches_invisible_zero' in options
                and options['rank_matches_invisible_zero']
                not in ["", "False"]):
                # __
                rank_matches_invisible_zero = True

        self.chosen_deci = Decimal("0")

        # Two different ways to generate a number. Here is the "default" one:
        if generation_type == "default":
            ranks = []

            if not rank_matches_invisible_zero:
                if 'numberof' not in options:
                    lr = ranks_scale.index(rank_to_use) - width + 1
                    lowest_start_rank = lr if lr >= 0 else 0

                    hr = ranks_scale.index(rank_to_use)
                    highest_start_rank = hr if hr + width < len(ranks_scale) \
                        else len(ranks_scale) - 1 - width
                    highest_start_rank = highest_start_rank \
                        if highest_start_rank >= lowest_start_rank \
                        else lowest_start_rank

                    possible_start_ranks = [lowest_start_rank + r
                                            for r in range(
                                                highest_start_rank
                                                - lowest_start_rank
                                                + 1)]

                    start_rank = randomly.pop(possible_start_ranks)

                    ranks = [start_rank + r for r in range(width)]

                else:
                    ranks += [ranks_scale.index(rank_to_use)]
                    # Probability to fill a higher rank rather than a lower one
                    phr = 0.5
                    hr = lr = ranks_scale.index(rank_to_use)
                    for i in range(width - 1):
                        if lr == 0:
                            phr = 1
                        elif hr == len(ranks_scale) - 1:
                            phr = 0

                        if random.random() < phr:
                            hr += 1
                            ranks += [hr]
                            phr *= 0.4
                        else:
                            lr -= 1
                            ranks += [lr]
                            phr *= 2.5

            else:
                if rank_to_use <= Decimal("0.1"):
                    ranks = [ranks_scale.index(r) for r in ranks_scale
                             if r > rank_to_use]
                    width = min(width, len(ranks))
                    ranks = ranks[-width:]
                elif rank_to_use >= Decimal("10"):
                    ranks = [ranks_scale.index(r) for r in ranks_scale
                             if r < rank_to_use]
                    width = min(width, len(ranks))
                    ranks = ranks[:width]

            # Let's start the generation of the number:
            for r in ranks:
                figure = randomly.pop(figures)
                self.chosen_deci += Decimal(figure) * ranks_scale[r]

        # "Alternative" way of generating a number randomly:
        else:
            figure = "0" if rank_matches_invisible_zero \
                else randomly.pop(figures)

            self.chosen_deci += Decimal(figure) * rank_to_use
            ranks_scale.remove(rank_to_use)

            if rank_matches_invisible_zero:
                if rank_to_use <= Decimal("0.1"):
                    next_rank = rank_to_use * Decimal("10")
                    figure = randomly.pop(figures)
                    self.chosen_deci += Decimal(figure) * next_rank
                    ranks_scale = [r for r in ranks_scale if r > next_rank]
                elif rank_to_use >= Decimal("10"):
                    next_rank = rank_to_use * Decimal("0.1")
                    figure = randomly.pop(figures)
                    self.chosen_deci += Decimal(figure) * next_rank
                    ranks_scale = [r for r in ranks_scale if r < next_rank]

            width = min(width, len(ranks_scale))

            if rank_to_use != Decimal("1") and not rank_matches_invisible_zero:
                figure = randomly.pop(figures)
                r = RANKS_CONFUSING[-(RANKS_CONFUSING.index(rank_to_use) + 1)]
                self.chosen_deci += Decimal(figure) * r
                ranks_scale.remove(r)
                width -= 1

            for i in range(width):
                figure = randomly.pop(figures)
                r = randomly.pop(ranks_scale)
                self.chosen_deci += Decimal(figure) * r

        self.chosen_figure = (self.chosen_deci
                              % (rank_to_use * Decimal('10'))) // rank_to_use

        self.chosen_deci_str = Item((self.chosen_deci)).printed

        self.chosen_rank = rank_to_use

    def q(self, **options):
        return _("Which figure matches the {rank} in the number \
{decimal_number}?").format(decimal_number=self.chosen_deci_str,
                           rank=_(str(RANKS_WORDS[self.chosen_rank])))

    def a(self, **options):
        return self.chosen_figure
