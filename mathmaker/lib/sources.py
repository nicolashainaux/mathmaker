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
from mathmaker.lib.mathtools import coprime_generator, generate_decimal
from mathmaker.lib.core.base_calculus import Fraction


##
#   @brief  Will tell if the tag belongs to int pairs, decimal numbers etc.
def classify_tag(tag):
    if (tag.startswith('intpairs_') or tag.startswith('table_')
        or tag.startswith('multiplesof')):
        # __
        return 'int_pairs'
    elif tag.startswith('singleint_'):
        return 'single_int'
    elif tag.startswith('singledeci1_'):
        return 'single_deci1'
    elif tag in ['int_deci_clever_pairs', 'rank_words',
                 'int_irreducible_frac', 'nothing',
                 'decimal_and_10_100_1000_for_multi',
                 'decimal_and_10_100_1000_for_divi',
                 'decimal_and_one_digit_for_multi',
                 'decimal_and_one_digit_for_divi']:
        # __
        return tag
    raise ValueError(tag + " is not recognized as a valid 'tag' that can be "
                     "used in a mathmaker xml file.")


##
#   @brief  Will turn the tag into the matching conditions for the db query.
#           Note that any value matching a 'nbN' key (like 'nb1': '11') will
#           be automatically removed from any "NOT IN(...)" condition in a
#           query. The "raw" keyword allows to give more complex queries but
#           as the 'nbN' keys are then "buried" inside the query string, it's
#           possible to add a "prevail": 'value' in the returned dictionary
#           to allow this very same behaviour (as directly adding a
#           'nbN': 'value' may change the query).
#   @return A dictionary
def translate_int_pairs_tag(tag):
    d = {}
    # 'table_11' is a shortcut for a special range
    if tag == 'table_11':
        d = {'nb2_in': ['11', '12', '13', '14', '15', '16', '17', '18', '21',
                        '22', '23', '24', '25', '26', '27', '31', '32', '33',
                        '34', '35', '36', '41', '42', '43', '44', '45', '51',
                        '52', '53', '54', '61', '62', '63', '71', '72', '81'],
             'nb1': '11'}
    # 'table_N' is a shortcut for 'multiplesofN_2to9' if N <= 10
    # and for 'multiplesofN_2to6' if N >= 12 (11 is managed separately)
    elif tag.startswith('table_'):
        n = int(tag[6:])
        r = "_2to9" if n <= 10 else "_2to6"
        tag = 'multiplesof' + str(n) + r

    if tag.startswith('intpairs_'):
        if '×' not in tag:
            n1, n2 = tag[9:].split(sep='to')
            d = {'nb1_min': n1, 'nb1_max': n2,
                 'nb2_min': n1, 'nb2_max': n2}
        else:
            nb1_part, nb2_part = tag.replace('intpairs_', '').split(sep='×')
            min1, max1 = nb1_part.split(sep='to')
            min2, max2 = nb2_part.split(sep='to')
            d = {'nb1_min': min1, 'nb1_max': max1,
                 'nb2_min': min2, 'nb2_max': max2}
    elif tag.startswith('multiplesof'):
        N, r = tag[11:].split(sep='_')
        mini, maxi = r.split(sep='to')
        d = {'raw': '(nb1 = ' + N + ' and (nb2 >= ' + mini
                    + ' and nb2 <= ' + maxi + ')) or (nb2 = ' + N
                    + ' and (nb1 >= ' + mini + ' and nb1 <= ' + maxi + '))',
             'prevails': [N]}

    return d


def translate_single_nb_tag(tag):
    """From single..._mintomax, get and return min and max in a dictionary."""
    n1, n2 = tag.split(sep='_')[1].split(sep='to')
    return {'nb1_min': n1, 'nb1_max': n2}


##
#   @brief  Generates a list of values to be used
#   @todo   Several cases should be factorized or maybe later moved to the db
def generate_values(source_id):
    if source_id == 'int_irreducible_frac':
        return [(k, Fraction((n, k))) for k in [i + 2 for i in range(18)]
                for n in coprime_generator(k)]

    elif source_id == 'rank_words':
        return [(elt,) for elt in RANKS]

    elif source_id == 'trigo_functions':
        return ['cos', 'cos', 'sin', 'sin', 'tan', 'tan']

    elif source_id == 'trigo_vocabulary':
        return ['adjacent', 'adjacent', 'opposite', 'opposite']

    elif source_id == 'decimal_and_10_100_1000_for_multi':
        box_10_100_1000 = [10, 100, 1000]
        result = set()
        for n in range(20):
            if not box_10_100_1000:
                box_10_100_1000 = [10, 100, 1000]
            chosen_10_100_1000 = box_10_100_1000.pop()
            ranks_scale = list(RANKS[2:])
            width = random.choices([1, 2, 3], weights=[0.14, 0.63, 0.33])[0]
            start_rank = random.choice([n for n in range(len(ranks_scale))])
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
            width = random.choices([1, 2, 3], weights=[0.14, 0.63, 0.33])[0]
            wt = {10: [0.2, 0.2, 0.2, 0.2, 0.2],
                  100: [0.25, 0.25, 0.25, 0.25, 0],
                  1000: [0.34, 0.33, 0.33, 0, 0]}
            start_rank = random.choices([n for n in range(len(ranks_scale))],
                                        weights=wt[chosen_10_100_1000])[0]
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
            width = random.choices([1, 2, 3, 4],
                                   weights=[0.14, 0.43, 0.33, 0.2])[0]
            start_rank = random.choice([n for n in range(len(ranks_scale))])
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
            width = random.choices([1, 2, 3, 4],
                                   weights=[0.14, 0.43, 0.33, 0.2])[0]
            start_rank = random.choice([n for n in range(len(ranks_scale))])
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
        elif tag_classification.startswith('single'):
            kwargs.update(translate_single_nb_tag(source_id))
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
