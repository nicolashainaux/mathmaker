# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

from lib.common import shared
from lib.common.cst import RANKS
from lib import randomly
from lib.maths_lib import coprime_generator, generate_decimal
from lib.tools.tag import classify_tag, translate_int_pairs_tag
from core.base_calculus import Fraction

##
#   @todo   Turn the old source ids' tags into the new ones:
#           table_2_9       ->      intpairs_2to9
#           table_4_9       ->      intpairs_4to9
#           table_N_11_50   ->      multiplesofN_11to50
#           integers_10_100 ->      intpairs_10to100
#           integers_5_20   ->      intpairs_5to20
#           The ones that remain the same:
#           table_N (for N in [2, 3, ..., 9, 11, 15, 25])
#           The ones that will disappear:
#           *_for_sums_diffs:   a kwarg should be added to inform the source
#                               there's a special condition on the numbers to
#                               return
#           *_for_rectangles:   same as above
#           *_for_multi_reversed:   same as above
#           square*
#           Yet to think about: integers_10_100_diff7atleast
INT_PAIRS_IDS = ['tables_2_9', 'tables_4_9', 'table_2', 'table_3', 'table_4',
                 'table_11', 'table_15', 'table_25',
                 'table_2_11_50', 'table_3_11_50', 'table_4_11_50',
                 'integers_10_100', 'integers_5_20',
                 'integers_10_100_diff7atleast',
                 'table_2_9_for_sums_diffs',
                 'integers_10_100_for_sums_diffs',
                 'squares_2_9', 'squares_4_9', 'square_11',
                 'squares_10_100', 'squares_5_20',
                 'table_2_9_for_rectangles', 'table_4_9_for_rectangles',
                 'table_11_for_rectangles', 'integers_10_100_for_rectangles',
                 'integers_5_20_for_rectangles',
                 'table_2_9_for_multi_reversed', 'table_4_9_for_multi_reversed']

##
#   @brief  Generates a list of values to be used
def generate_values(source_id):
    if source_id == 'int_irreducible_frac':
        return [(k, Fraction((n, k))) for k in [i+2 for i in range(18)]
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

    elif source_id == 'bypass':
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

