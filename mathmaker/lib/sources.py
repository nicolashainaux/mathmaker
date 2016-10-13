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

import random
from decimal import Decimal

from mathmaker.lib import shared
from mathmaker.lib.common.cst import RANKS
from mathmaker.lib import randomly
from mathmaker.lib.maths_lib import coprime_generator, generate_decimal
from mathmaker.lib.tools.tag import (classify_tag, translate_int_pairs_tag,
                                     translate_single_int_tag)
from mathmaker.lib.core.base_calculus import Fraction


##
#   @brief  Generates a list of values to be used
#   @todo   Several cases should be factorized or maybe later moved to the db
def generate_values(source_id):
    if source_id == 'int_irreducible_frac':
        return [(k, Fraction((n, k))) for k in [i + 2 for i in range(18)]
                for n in coprime_generator(k)]

    elif source_id == 'rank_words':
        return [(elt,) for elt in RANKS]

    elif source_id == 'decimal_and_10_100_1000_for_multi':
        box_10_100_1000 = [10, 100, 1000]
        result = set()
        for n in range(20):
            if not box_10_100_1000:
                box_10_100_1000 = [10, 100, 1000]
            chosen_10_100_1000 = box_10_100_1000.pop()
            ranks_scale = list(RANKS[2:])
            width = randomly.pop([1, 2, 3], weighted_table=[0.14, 0.63, 0.33])
            start_rank = randomly.pop([n for n in range(len(ranks_scale))])
            result |= {(chosen_10_100_1000,
                        generate_decimal(width, ranks_scale, start_rank))}
        return list(result)

    elif source_id == 'decimal_and_10_100_1000_for_divi':
        box_10_100_1000 = [10, 100, 1000]
        result = set()
        for n in range(20):
            if not box_10_100_1000:
                box_10_100_1000 = [10, 100, 1000]
            chosen_10_100_1000 = box_10_100_1000.pop()
            ranks_scale = list(RANKS[2:])
            width = randomly.pop([1, 2, 3], weighted_table=[0.14, 0.63, 0.33])
            wt = {10: [0.2, 0.2, 0.2, 0.2, 0.2],
                  100: [0.25, 0.25, 0.25, 0.25, 0],
                  1000: [0.34, 0.33, 0.33, 0, 0]}
            start_rank = randomly.pop([n for n in range(len(ranks_scale))],
                                      weighted_table=wt[chosen_10_100_1000])
            result |= {(chosen_10_100_1000,
                        generate_decimal(width, ranks_scale, start_rank))}
        return list(result)

    elif source_id == 'decimal_and_one_digit_for_multi':
        box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]
        result = set()
        for n in range(20):
            if not box:
                box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]
            chosen = box.pop()
            ranks_scale = list()
            if chosen == Decimal('0.1'):
                ranks_scale = list(RANKS[:-1])
            elif chosen == Decimal('0.01'):
                ranks_scale = list(RANKS[:-2])
            elif chosen == Decimal('0.001'):
                ranks_scale = list(RANKS[:-3])
            width = randomly.pop([1, 2, 3, 4],
                                 weighted_table=[0.14, 0.43, 0.33, 0.2])
            start_rank = randomly.pop([n for n in range(len(ranks_scale))])
            result |= {(chosen,
                        generate_decimal(width, ranks_scale, start_rank))}
        return list(result)

    elif source_id == 'decimal_and_one_digit_for_divi':
        box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]
        result = set()
        for n in range(20):
            if not box:
                box = [Decimal('0.1'), Decimal('0.01'), Decimal('0.001')]
            chosen = box.pop()
            ranks_scale = list()
            if chosen == Decimal('0.1') or chosen == Decimal('0.01'):
                ranks_scale = list(RANKS)
            elif chosen == Decimal('0.001'):
                ranks_scale = list(RANKS[1:])
            width = randomly.pop([1, 2, 3, 4],
                                 weighted_table=[0.14, 0.43, 0.33, 0.2])
            start_rank = randomly.pop([n for n in range(len(ranks_scale))])
            result |= {(chosen,
                        generate_decimal(width, ranks_scale, start_rank))}
        return list(result)

    elif source_id in ['nothing', 'bypass']:
        return []


class sub_source(object):
    ##
    #   @brief  Initializer
    def __init__(self, source_id):
        self.values = generate_values(source_id)
        random.shuffle(self.values)
        self.current = 0
        self.max = len(self.values)

    ##
    #   @brief  Resets the source
    def _reset(self):
        random.shuffle(self.values)
        self.current = 0

    ##
    #   @brief  Synonym of self.next(), but makes the source an Iterator.
    def __next__(self):
        return self.next()

    ##
    #   @brief  Handles the choice of the next value to return
    def next(self, **kwargs):
        if self.current == self.max:
            self._reset()
        self.current += 1
        return self.values[self.current - 1]


class mc_source(object):
    ##
    #   @brief  Handles the choice of the next value to return
    def next(self, source_id, **kwargs):
        tag_classification = classify_tag(source_id)
        if tag_classification == 'int_pairs':
            kwargs.update(translate_int_pairs_tag(source_id))
            return shared.int_pairs_source.next(**kwargs)
        elif tag_classification == 'single_int':
            kwargs.update(translate_single_int_tag(source_id))
            return shared.single_ints_source.next(**kwargs)
        elif tag_classification == 'int_deci_clever_pairs':
            return shared.int_deci_clever_pairs_source.next(**kwargs)
        elif tag_classification == 'rank_words':
            return shared.rank_words_source.next(**kwargs)
        elif tag_classification == 'int_irreducible_frac':
            return shared.int_fracs_source.next(**kwargs)
        elif tag_classification == 'decimal_and_10_100_1000_for_multi':
            return shared.deci_10_100_1000_multi_source.next(**kwargs)
        elif tag_classification == 'decimal_and_10_100_1000_for_divi':
            return shared.deci_10_100_1000_divi_source.next(**kwargs)
        elif tag_classification == 'decimal_and_one_digit_for_multi':
            return shared.deci_one_digit_multi_source.next(**kwargs)
        elif tag_classification == 'decimal_and_one_digit_for_divi':
            return shared.deci_one_digit_divi_source.next(**kwargs)
        elif tag_classification == 'nothing':
            return ()
