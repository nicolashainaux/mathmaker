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

import sys, random

from lib import *
from lib.common.cst import *
from .Q_Structure import Q_Structure
from . import mc_modules
from core.base_calculus import *

# 'table_2_9'
# 'table_11' --> 11×n where 10 < n < 100, no carry over
# 'table_15' --> 15×n where 2 <= n <= 6
# 'table_25' --> 25×n where 2 <= n <= 6
# 'int_irreducible_frac' --> (n, p/n) where 2 <= n <= 20 and p/n is irreducible
USER_Q_SUBKIND_VALUES = {'table_2_9', 'table_2', 'table_3', 'table_4',
                         'table_2_11_50', 'table_3_11_50', 'table_4_11_50',
                         'table_2_9_for_sums_diffs',
                         'table_11',
                         'table_15',
                         'table_25',
                         'int_irreducible_frac',
                         'rank_word',
                         'integers_10_100',
                         'integers_10_100_for_sums_diffs',
                         'decimals_0_20_1',
                         'decimal_and_10_100_1000',
                         'decimal_and_0.1_0.01_0.001',
                         'bypass'}

AVAILABLE_Q_SUBKIND_VALUES = {'table_2_9', 'table_2', 'table_3', 'table_4',
                              'table_2_11_50', 'table_3_11_50', 'table_4_11_50',
                              'table_2_9_for_sums_diffs',
                              'table_11',
                              'table_15',
                              'table_25',
                              'int_irreducible_frac',
                              'rank_word',
                              'integers_10_100',
                              'integers_10_100_for_sums_diffs',
                              'decimals_0_20_1',
                              'decimal_and_10_100_1000_for_divi',
                              'decimal_and_10_100_1000_for_multi',
                              'decimal_and_0.1_0.01_0.001_for_divi',
                              'decimal_and_0.1_0.01_0.001_for_multi',
                              'bypass'}

PART_OF_ANOTHER_SOURCE = { 'table_2' : 'table_2_9',
                           'table_3' : 'table_2_9',
                           'table_4' : 'table_2_9',
                           'integers_10_100_for_sums_diffs' : 'integers_10_100'
                         }

SUBKINDS_TO_UNPACK = {'simple_parts_of_a_number' : {'half', 'third', 'quarter'},
                      'simple_multiples_of_a_number' : {'double', 'triple',
                                                        'quadruple'},
                      'simple_parts_or_multiples_of_a_number' : {'half',
                                                                 'third',
                                                                 'quarter',
                                                                 'double',
                                                                 'triple',
                                                                 'quadruple'},
                      'operation' : {'multi', 'divi', 'addi', 'subtr'}
                     }

UNPACKABLE_SUBKINDS = {'half', 'third', 'quarter',
                       'double', 'triple', 'quadruple',
                       'multi', 'divi', 'addi', 'subtr'
                      }

SOURCES_TO_UNPACK = {'auto_table' : {'half' : {'table_2'},
                                     'third' : {'table_3'},
                                     'quarter' : {'table_4'},
                                     'double' : {'table_2'},
                                     'triple' : {'table_3'},
                                     'quadruple' : {'table_4'},
                                     'multi' : {'table_2_9'},
                                     'divi' : {'table_2_9'},
                                     'addi' : {'table_2_9_for_sums_diffs'},
                                     'subtr' : {'table_2_9_for_sums_diffs'}},
                     'auto_11_50' : {'half' : {'table_2_11_50'},
                                     'third' : {'table_3_11_50'},
                                     'quarter' : {'table_4_11_50'},
                                     'double' : {'table_2_11_50'},
                                     'triple' : {'table_3_11_50'},
                                     'quadruple' : {'table_4_11_50'}},
                     'auto_vocabulary' :  \
                               {'half' : {'table_2', 'table_2_11_50'},
                                'third' : {'table_3', 'table_3_11_50'},
                                'quarter' : {'table_4', 'table_4_11_50'},
                                'double' : {'table_2', 'table_2_11_50'},
                                'triple' : {'table_3', 'table_3_11_50'},
                                'quadruple' : {'table_4', 'table_4_11_50'},
                                'multi' : {'table_2_9'},
                                'divi' : {'table_2_9'},
                                'addi' : {'integers_10_100_for_sums_diffs',
                                          'decimals_0_20_1'},
                                'subtr' : {'integers_10_100_for_sums_diffs',
                                           'decimals_0_20_1'}},
                     'decimal_and_10_100_1000' : \
                {'multi_direct' : {'decimal_and_10_100_1000_for_multi'},
                 'divi_direct' : {'decimal_and_10_100_1000_for_divi'},
                 'area_rectangle' : {'decimal_and_10_100_1000_for_multi'},
                 'multi_hole' : {'decimal_and_10_100_1000_for_multi'},
                 'vocabulary_multi' : {'decimal_and_10_100_1000_for_multi'},
                 'vocabulary_divi' : {'decimal_and_10_100_1000_for_divi'}
                 },
                     'decimal_and_0.1_0.01_0.001': \
                 {'multi_direct' : {'decimal_and_0.1_0.01_0.001_for_multi'},
                  'divi_direct' : {'decimal_and_0.1_0.01_0.001_for_divi'},
                  'area_rectangle' : {'decimal_and_0.1_0.01_0.001_for_multi'},
                  'multi_hole' : {'decimal_and_0.1_0.01_0.001_for_multi'},
                  'vocabulary_multi' : {'decimal_and_0.1_0.01_0.001_for_multi'},
                  'vocabulary_divi' : {'decimal_and_0.1_0.01_0.001_for_divi'}
                  }
                     }

AVAILABLE_Q_KIND_VALUES = \
    { 'multi_direct' : ['table_2_9',
                        'table_2', 'table_3', 'table_4',
                        'table_11',
                        'table_15',
                        'table_25',
                        'decimal_and_10_100_1000',
                        'decimal_and_0.1_0.01_0.001',
                        'bypass'],
      'area_rectangle' : ['table_2_9',
                          'table_2', 'table_3', 'table_4',
                          'table_11',
                          'table_15',
                          'table_25',
                          'decimal_and_10_100_1000',
                          'decimal_and_0.1_0.01_0.001',
                          'bypass'],
      'multi_reversed' : ['table_2_9',
                          'table_2', 'table_3', 'table_4',
                          'bypass'],
      'multi_hole' : ['table_2_9',
                      'table_2', 'table_3', 'table_4',
                      'table_11',
                      'table_15',
                      'table_25',
                      'decimal_and_10_100_1000',
                      'decimal_and_0.1_0.01_0.001',
                      'bypass'],
      'divi_direct' : ['table_2_9',
                       'table_2', 'table_3', 'table_4',
                       'table_11',
                       'table_15',
                       'table_25',
                       'decimal_and_10_100_1000',
                       'decimal_and_0.1_0.01_0.001',
                       'bypass'],
      'rank_direct' : ['rank_word',
                       'bypass'],
      'rank_reversed' : ['rank_word',
                         'bypass'],
      'rank_numberof' : ['rank_word',
                           'bypass'],
      'vocabulary_half' : {'table_2', 'table_2_11_50', 'bypass'},
      'vocabulary_third' : {'table_3', 'table_3_11_50', 'bypass'},
      'vocabulary_quarter' : {'table_4', 'table_4_11_50', 'bypass'},
      'vocabulary_double' : {'table_2', 'table_2_11_50', 'bypass'},
      'vocabulary_triple' : {'table_3', 'table_3_11_50', 'bypass'},
      'vocabulary_quadruple' : {'table_4', 'table_4_11_50', 'bypass'},
      'vocabulary_multi' : {'table_2_9',
                            'table_2', 'table_3', 'table_4',
                            'table_11',
                            'table_15',
                            'table_25',
                            'decimal_and_10_100_1000',
                            'decimal_and_0.1_0.01_0.001',
                            'table_2_11_50', 'table_3_11_50', 'table_4_11_50',
                            'bypass'},
      'vocabulary_divi' : {'table_2_9',
                           'table_2', 'table_3', 'table_4',
                           'table_11',
                           'table_15',
                           'table_25',
                           'decimal_and_10_100_1000',
                           'decimal_and_0.1_0.01_0.001',
                           'table_2_11_50', 'table_3_11_50', 'table_4_11_50',
                           'bypass'},
      'vocabulary_addi' : {'table_2_9', 'table_2_9_for_sums_diffs',
                           'integers_10_100', 'integers_10_100_for_sums_diffs',
                           'decimals_0_20_1', 'bypass'},
      'vocabulary_subtr' : {'table_2_9', 'table_2_9_for_sums_diffs',
                            'integers_10_100', 'integers_10_100_for_sums_diffs',
                            'decimals_0_20_1', 'bypass'}

#     frozenset(('area', 'rectangle', 'with_drawing')) : ['table_2_9',
#                                              'table_11',
#                                              'table_15',
#                                              'table_25'],
#     frozenset(('area', 'rectangle', 'without_drawing')) : ['table_2_9',
#                                                 'table_11',
#                                                 'table_15',
#                                                 'table_25'],
#     frozenset(('area', 'right_triangle')) : ['table_2_9',
#                                   'table_11',
#                                   'table_15',
#                                   'table_25']
    }

MODULES =  \
    { 'multi_direct' : mc_modules.multi_direct,
      'multi_reversed' : mc_modules.multi_reversed,
      'multi_hole' : mc_modules.multi_hole,
      'divi_direct' : mc_modules.divi_direct,
      'rank_direct' : mc_modules.rank_direct,
      'rank_reversed' : mc_modules.rank_reversed,
      'rank_numberof' : mc_modules.rank_numberof,
      'vocabulary_half' : mc_modules.vocabulary_simple_part_of_a_number,
      'vocabulary_third' : mc_modules.vocabulary_simple_part_of_a_number,
      'vocabulary_quarter' : mc_modules.vocabulary_simple_part_of_a_number,
      'vocabulary_double' : mc_modules.vocabulary_simple_multiple_of_a_number,
      'vocabulary_triple' : mc_modules.vocabulary_simple_multiple_of_a_number,
      'vocabulary_quadruple': mc_modules.vocabulary_simple_multiple_of_a_number,
      'vocabulary_multi' : mc_modules.vocabulary_multi,
      'vocabulary_divi' : mc_modules.vocabulary_divi,
      'vocabulary_addi': mc_modules.vocabulary_addi,
      'vocabulary_subtr' : mc_modules.vocabulary_subtr,
      'area_rectangle' : mc_modules.area_rectangle

#     ('division', 'direct') : mc_modules.divi_dir,
#     ('division', 'decimal_1') : mc_modules.divi_deci1,
#     ('area', 'rectangle', 'with_drawing') : mc_modules.area_rect_dr,
#     ('area', 'rectangle', 'without_drawing') : mc_modules.area_rect_no_dr,
#     ('area', 'right_triangle') : mc_modules.area_right_tri
    }



# --------------------------------------------------------------------------
##
#   @brief Access to sources of numbers
def nb_sources():
    return AVAILABLE_Q_SUBKIND_VALUES




# --------------------------------------------------------------------------
##
#   @brief Generator of coprime numbers
def coprime_generator(n):
    for i in range(20):
        if maths_lib.gcd(i, n) == 1:
            yield i




# --------------------------------------------------------------------------
##
#   @brief Returns a list of numbers of the given kind
def generate_decimal(width, ranks_scale, start_rank):
    # Probability to fill a higher rank rather than a lower one
    phr = 0.5
    hr = lr = start_rank
    ranks = [start_rank]

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

    figures = [str(i+1) for i in range(9)]

    deci = Decimal('0')

    for r in ranks:
        figure = randomly.pop(figures)
        deci +=  Decimal(figure) * ranks_scale[r]

    return deci





# --------------------------------------------------------------------------
##
#   @brief Returns a list of numbers of the given kind
def generate_numbers(subkind):
    if subkind == 'table_2_9' or subkind == 'table_2_9_for_sums_diffs':
        return {(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9),
                (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
                (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                (6, 6), (6, 7), (6, 8), (6, 9),
                (7, 7), (7, 8), (7, 9),
                (8, 8), (8, 9),
                (9, 9)}

    elif subkind == 'table_2':
        return {(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9)}

    elif subkind == 'table_3':
        return {(3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9)}

    elif subkind == 'table_4':
        return {(4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9)}

    elif subkind == 'table_2_11_50':
        return {(2, n+11) for n in range(40)}

    elif subkind == 'table_3_11_50':
        return {(3, n+11) for n in range(40)}

    elif subkind == 'table_4_11_50':
        return {(4, n+11) for n in range(40)}

    elif subkind == 'table_11':
        return {(11, 11), (11, 12), (11, 13), (11, 14), (11, 15), (11, 16),
                (11, 17), (11, 18),
                (11, 21), (11, 22), (11, 23), (11, 24), (11, 25), (11, 26),
                (11, 27),
                (11, 31), (11, 32), (11, 33), (11, 34), (11, 35), (11, 36),
                (11, 41), (11, 42), (11, 43), (11, 44), (11, 45),
                (11, 51), (11, 52), (11, 53), (11, 54),
                (11, 61), (11, 62), (11, 63),
                (11, 71), (11, 72),
                (11, 81)}

    elif subkind == 'table_15':
        return {(15, 2), (15,3), (15, 4), (15,5), (15, 6)}

    elif subkind == 'table_25':
        return {(25, 2), (25,3), (25, 4), (25,5), (25, 6)}

    elif subkind == 'integers_10_100':
        return { (i+10, j+10) for i in range(90) for j in range(90) if i <= j }

    elif subkind == 'integers_10_100_for_sums_diffs':
        return set(random.sample({ (i+10, j+10) for i in range(90) \
                                                for j in range(90) \
                                                if i < j }, 100))

    elif subkind == 'decimals_0_20_1':
        return { (Decimal(str(i/10)), Decimal(str(j/10))) for (i, j) in \
                    random.sample({ (i, j) for i in range(200) \
                                           for j in range (200) if i < j },
                                  100)}

    elif subkind == 'decimal_and_10_100_1000_for_multi':
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

        return result

    elif subkind == 'decimal_and_10_100_1000_for_divi':
        box_10_100_1000 = [10, 100, 1000]

        result = set()

        for n in range(20):
            if not box_10_100_1000:
                box_10_100_1000 = [10, 100, 1000]

            chosen_10_100_1000 = box_10_100_1000.pop()

            ranks_scale = list(RANKS[2:])
            width = randomly.pop([1, 2, 3], weighted_table=[0.14, 0.63, 0.33])

            wt = {10 : [0.2, 0.2, 0.2, 0.2, 0.2],
                  100 : [0.25, 0.25, 0.25, 0.25, 0],
                  1000 : [0.34, 0.33, 0.33, 0, 0]}

            start_rank = randomly.pop([n for n in range(len(ranks_scale))],
                                      weighted_table=wt[chosen_10_100_1000])

            result |= {(chosen_10_100_1000,
                        generate_decimal(width, ranks_scale, start_rank))}

        return result

    elif subkind == 'decimal_and_0.1_0.01_0.001_for_multi':
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

        return result

    elif subkind == 'decimal_and_0.1_0.01_0.001_for_divi':
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

        return result

    elif subkind == 'int_irreducible_frac':
        result = set()
        for k in [i+2 for i in range(18)]:
            result |= {(k, Fraction((n, k))) for n in coprime_generator(k)}
        return result

    elif subkind == 'rank_word':
        return {(elt,) for elt in RANKS}

    elif subkind == 'bypass':
        return set()

    else:
        raise error.OutOfRangeArgument(subkind,
                                       "'" \
                                       + " ,".join(AVAILABLE_Q_SUBKIND_VALUES) \
                                       + "'")




# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Q_MentalCalculation
# @brief Creates one whole tabular full of questions + answers
class Q_MentalCalculation(Q_Structure):


    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param embedded_machine The machine to be used
    #   @param **options Any options
    #   @return One instance of question.Q_MentalCalculation
    def __init__(self, embedded_machine, q_kind,
                 q_options, **options):

        self.derived = True

        # The call to the mother class __init__() method will set the
        # fields matching optional arguments which are so far :
        # self.q_kind, self.q_subkind
        # plus self.machine, self.options (modified)
        Q_Structure.__init__(self, embedded_machine,
                             q_kind, AVAILABLE_Q_KIND_VALUES,
                             q_subkind='bypass', **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        options.update(q_options)

        numbers_to_use = options['numbers_to_use']
        del options['numbers_to_use']

        # module
        m = MODULES[self.q_kind].sub_object(numbers_to_use,
                                            **options)

        self.q_text = m.q(embedded_machine, **options)
        self.q_answer = m.a(embedded_machine, **options)










    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the text of the question as a str
    def text_to_str(self):
        return self.q_text








    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        return self.q_answer
