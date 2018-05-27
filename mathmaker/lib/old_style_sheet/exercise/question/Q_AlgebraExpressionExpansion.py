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

import random

from mathmakerlib.calculus import is_natural

from mathmaker.lib import shared
from mathmaker.lib.constants import RANDOMLY
from .Q_Structure import Q_Structure
from mathmaker.lib.core.base_calculus import (Expandable, BinomialIdentity,
                                              Sum, Monomial, Polynomial)
from mathmaker.lib.core.calculus import Expression

# DON'T FORGET FOR THIS QUESTION TO ALSO DEFINE
# THE INIT CALLER (JUST AFTER AVAILABLE_Q_KIND_VALUES)
AVAILABLE_Q_KIND_VALUES = \
    {'monom01_polyn1': ['default'],  # any of the 2 next
     'monom0_polyn1': ['default'],  # a×(bx + c)
     'monom1_polyn1': ['default'],  # ax×(bx + c)
     'polyn1_polyn1': ['default'],  # (ax + b)×(cx + d)
     'sum_of_any_basic_expd': ['default', 'easy', 'harder', 'with_a_binomial'],
     'sign_expansion': ['default'],
     'sign_expansion_short_test': ['default'],
     'sum_square': ['default'],  # passed to an __init__()
     'difference_square': ['default'],  # idem
     'squares_difference': ['default'],  # idem
     'any_binomial': ['default']   # idem (not really good ?)
     }

INIT_CALLER = \
    {'monom01_polyn1': Expandable,
     'monom0_polyn1': Expandable,
     'monom1_polyn1': Expandable,
     'polyn1_polyn1': Expandable,
     'sum_of_any_basic_expd': Expandable,
     'sign_expansion': Expandable,
     'sign_expansion_short_test': Expandable,
     'sum_square': BinomialIdentity,
     'difference_square': BinomialIdentity,
     'squares_difference': BinomialIdentity,
     'any_binomial': BinomialIdentity}


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Q_AlgebraExpressionExpansion
# @brief An object to expand (like 2(x-3), 4x(2-9x), (3+x)(x-1) or (x+1)² etc.)
class Q_AlgebraExpressionExpansion(Q_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param **options Any options
    #   @return One instance of question.Q_AlgebraExpressionExpansion
    def __init__(self, q_kind='default_nothing', **options):
        self.derived = True

        # The call to the mother class __init__() method will set the
        # fields matching optional arguments which are so far:
        # self.q_kind, self.q_subkind
        # plus self.options (modified)
        Q_Structure.__init__(self,
                             q_kind, AVAILABLE_Q_KIND_VALUES,
                             **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        init_caller = INIT_CALLER[q_kind]

        self.expandable_objct = None

        self.numeric_aux = None

        if q_kind in ['monom0_polyn1', 'monom1_polyn1']:
            self.expandable_objct = Expandable((RANDOMLY,
                                                q_kind),
                                               randomly_reversed=0.5)
        elif q_kind == 'monom01_polyn1':
            self.expandable_objct = Expandable((RANDOMLY,
                                                random.choice(['monom0_polyn1',
                                                               'monom1_polyn1'
                                                               ])),
                                               randomly_reversed=0.5)

        elif q_kind == 'polyn1_polyn1':
            self.expandable_objct = Expandable((RANDOMLY,
                                                'polyn1_polyn1'))

        elif q_kind == 'sum_of_any_basic_expd':
            if self.q_subkind == 'easy':
                aux_expd_list = list()
                aux_expd_list.append(
                    Expandable((RANDOMLY,
                                random.choice(['monom0_polyn1',
                                               'monom1_polyn1']))))
                last_term = Expandable((RANDOMLY, 'sign_exp')) \
                    if random.choice([True, False]) \
                    else Monomial((RANDOMLY, 15, random.randint(0, 2)))
                aux_expd_list.append(last_term)
                random.shuffle(aux_expd_list)
                self.expandable_objct = Sum(aux_expd_list)

        elif q_kind in ['sign_expansion', 'sign_expansion_short_test']:
            # Creation of the terms
            long_aux_expd = Expandable((Monomial(('-', 1, 0)),
                                        Polynomial((RANDOMLY, 15, 2, 3))))
            aux_monomial = Monomial((RANDOMLY, 15, 2))
            aux_terms_list = [long_aux_expd, aux_monomial]
            random.shuffle(aux_terms_list)
            self.expandable_objct = Sum(aux_terms_list)

        else:
            if q_kind == 'any_binomial':
                q_kind = 'any'

            self.expandable_objct = init_caller((RANDOMLY, q_kind),
                                                **options)

        # Creation of the expression:
        number = 0
        if 'expression_number' in options                                     \
           and is_natural(options['expression_number']):
            # __
            number = options['expression_number']
        self.expression = Expression(number, self.expandable_objct)
        if self.numeric_aux is not None:
            self.numeric_aux = Expression(number, self.numeric_aux)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the text of the question as a str
    def text_to_str(self):
        M = shared.machine

        result = M.write_math_style2(M.type_string(self.expression))
        result += M.write_new_line()

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        M = shared.machine

        result = M.write(self.expression.auto_expansion_and_reduction())

        return result
