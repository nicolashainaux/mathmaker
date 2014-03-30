# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

from lib import *
from .Q_Structure import Q_Structure

from core.base_calculus import *

# The matching number indicates how many different questions can be asked
# in the theme
GAUGES = {'table_2-9' : 36,
          'table_11' : 28, # 11×n where 10 < n < 100, no carry over
          'table_15' : 6, # 15×n where 2 <= n <= 6
          'table_25' : 6 # 25×n where 2 <= n <= 6
         }

AVAILABLE_Q_KIND_VALUES = \
    {{'multiplication', 'direct'} : ['table_2-9',
                                     'table_11',
                                     'table_15',
                                     'table_25'],
     {'multiplication', 'reversed'} : ['table_2-9'],
     {'multiplication', 'decimal'} : ['table_2-9'],
     {'multiplication', 'decimal_1'} : ['table_2-9'],
     {'multiplication', 'decimal_2'} : ['table_2-9'],
     {'division', 'direct'} : ['table_2-9'],
     {'division', 'decimal_1'} : ['table_2-9'],
     {'area', 'rectangle', 'with_drawing'} : ['table_2-9',
                                              'table_11',
                                              'table_15',
                                              'table_25'],
     {'area', 'rectangle', 'without_drawing'} : ['table_2-9',
                                                 'table_11',
                                                 'table_15',
                                                 'table_25'],
     {'area', 'right_rectangle'} : ['table_2-9',
                                    'table_11',
                                    'table_15',
                                    'table_25']
    }





# --------------------------------------------------------------------------
##
#   @brief Returns a list of numbers of the given kind
def generate_numbers(kind, subkind):
    if not kind in AVAILABLE_Q_KIND_VALUES:
        raise error.OutOfRangeArgument(kind,
                                       str(AVAILABLE_Q_KIND_VALUES.keys()))

    if not subkind in AVAILABLE_Q_KIND_VALUES[kind]:
        raise error.OutOfRangeArgument(subkind,
                                       str(AVAILABLE_Q_KIND_VALUES[kind]))

    if subkind == 'table_2-9':
        return [(2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9),
                (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
                (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                (6, 6), (6, 7), (6, 8), (6, 9),
                (7, 7), (7, 8), (7, 9),
                (8, 8), (8, 9),
                (9, 9)]

    elif subkind == 'table_11':
        return [(11, 11), (11, 12), (11, 13), (11, 14), (11, 15), (11, 16),
                (11, 17), (11, 18),
                (11, 21), (11, 22), (11, 23), (11, 24), (11, 25), (11, 26),
                (11, 27),
                (11, 31), (11, 32), (11, 33), (11, 34), (11, 35), (11, 36),
                (11, 41), (11, 42), (11, 43), (11, 44), (11, 45),
                (11, 51), (11, 52), (11, 53), (11, 54),
                (11, 61), (11, 62), (11, 63),
                (11, 71), (11, 72),
                (11, 81)
               ]

    elif subkind == 'table_15':
        return[(15, 2), (15,3), (15, 4), (15,5), (15, 6)]

    elif subkind == 'table_25':
        return[(25, 2), (25,3), (25, 4), (25,5), (25, 6)]






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
    def __init__(self, embedded_machine, q_kind='default_nothing', **options):
        self.derived = True

        # The call to the mother class __init__() method will set the
        # fields matching optional arguments which are so far :
        # self.q_kind, self.q_subkind
        # plus self.machine, self.options (modified)
        Q_Structure.__init__(self, embedded_machine,
                             q_kind, AVAILABLE_Q_KIND_VALUES,
                             **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        self.calculus_list = []
        self.results_list = []

        if q_kind == '10m_2-9':
            # The following intension list creates all (i , j) couples, i and
            # j taking their values in 2-9 and j >= i to avoid having duplicates
            # like (3, 2) which would be the same as (2, 3)
            # pairs = [(i, j) for i in xrange(2, 10) for j in xrange(i, 10)]
            # We put off 2×2 and 2×3
            pairs =

            (self.calculus_list, self.results_list) = ten_products(pairs)

        elif q_kind == '10m_4-9':
            # The following intension list creates all (i , j) couples, i and
            # j taking their values in 4-9 and j >= i to avoid having duplicates
            # like (5, 6) which would be the same as (6, 5)
            # pairs = [(i, j) for i in xrange(4, 10) for j in xrange(i, 10)]
            pairs = [(4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                     (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (6, 6),
                     (6, 7), (6, 8), (6, 9), (7, 7), (7, 8), (7, 9),
                     (8, 8), (8, 9), (9, 9)]


            (self.calculus_list, self.results_list) = ten_products(pairs)


        elif q_kind == '5m_3rm_2d_2-9':
            # The following intension list creates all (i , j) couples, i and
            # j take their values in 2 - 9 and j >= i to avoid having duplicates
            # like (3, 2) which would be the same as (2, 3)
            # pairs = [(i, j) for i in xrange(2, 10) for j in xrange(i, 10)]
            # We put off 2×2 and 2×3
            pairs = [(2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9),
                     (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
                     (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                     (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                     (6, 6), (6, 7), (6, 8), (6, 9),
                     (7, 7), (7, 8), (7, 9),
                     (8, 8), (8, 9),
                     (9, 9)]

            for i in range(5):
                current_pair = randomly.pop(pairs)
                if randomly.heads_or_tails():
                    self.calculus_list.append(Product([current_pair[0],
                                                       current_pair[1]]))
                else:
                    self.calculus_list.append(Product([current_pair[1],
                                                       current_pair[0]]))

                self.results_list.append(Product([current_pair[0],
                                                  current_pair[1]]).evaluate()
                                                  )

            for i in range(3):
                current_pair = randomly.pop(pairs)
                self.calculus_list.append(Product([current_pair[0],
                                                  current_pair[1]]).evaluate()
                                                  )

                self.results_list.append(Product([current_pair[0],
                                                  current_pair[1]]))

            # We put (2, 2) and (2, 3) back in the possible pairs
            pairs.append((2, 2))
            pairs.append((2, 3))

            for i in range(2):
                current_pair = randomly.pop(pairs)

                if randomly.heads_or_tails():
                    quotient = Quotient(('+',
                                         Product([current_pair[0],
                                                  current_pair[1]]).evaluate(),
                                         current_pair[0]),
                                         use_divide_symbol='yes')

                    self.calculus_list.append(quotient)

                    self.results_list.append(current_pair[1])

                else:
                    quotient = Quotient(('+',
                                         Product([current_pair[0],
                                                  current_pair[1]]).evaluate(),
                                         current_pair[1]),
                                         use_divide_symbol='yes')

                    self.calculus_list.append(quotient)

                    self.results_list.append(current_pair[0])









    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the text of the question as a str
    def text_to_str(self):
        M = self.machine

        result = M.write(_("Date") + " : ............." \
                         + _("Class") + " : .............")

        result += M.write_new_line()

        size = (3, 10)
        col_widths = [1.4 for i in range(10)]
        content = [i+1 for i in range(10)] \
                  + [M.write_math_style2(\
                    M.type_string(self.calculus_list[i])) for i in range(10)] \
                  + [M.write_math_style2(\
                    M.type_string(self.results_list[i])) for i in range(10)]

        result += M.write_layout(size, col_widths, content,
                                borders='all', center='ok')

        result += M.write_new_line_twice()

        return result








    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        pass











