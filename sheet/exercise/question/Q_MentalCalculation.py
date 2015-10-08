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

from lib import *
from .Q_Structure import Q_Structure

from core.base_calculus import *


AVAILABLE_Q_KIND_VALUES = {'10m_2-9': ['default'],
                           '10m_4-9': ['default'],
                           '5m_3rm_2d_2-9': ['default']
                          }

# --------------------------------------------------------------------------
##
#   @brief Produces a randomly list of ten products and results
#   @param embedded_machine The machine to be used
#   @param **options Any options
#   @return A couple ([products], [results])
def ten_products(pairs):

    if not len(pairs) >= 10:
        raise error.WrongArgument("a list of at least 10 items",
                                  "a list containing less than 10 items")

    calculus_list = []
    results_list = []

    for i in range(10):
        current_pair = randomly.pop(pairs)
        if randomly.heads_or_tails():
            calculus_list.append(Product([current_pair[0],
                                          current_pair[1]]))
        else:
            calculus_list.append(Product([current_pair[1],
                                          current_pair[0]]))

        results_list.append(Product([current_pair[0],
                                     current_pair[1]]).evaluate()
                            )

    return (calculus_list, results_list)






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
            pairs = [(2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9),
                     (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
                     (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
                     (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                     (6, 6), (6, 7), (6, 8), (6, 9),
                     (7, 7), (7, 8), (7, 9),
                     (8, 8), (8, 9),
                     (9, 9)]

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





