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

from mathmaker.lib import shared
from mathmaker.lib import randomly, is_
from mathmaker.lib.common.cst import RANDOMLY
from .Q_Structure import Q_Structure
from mathmaker.lib.core.base_calculus import (Expandable, BinomialIdentity,
                                              Sum, Product, Monomial,
                                              Polynomial)
from mathmaker.lib.core.calculus import Expression

# DON'T FORGET FOR THIS QUESTION TO ALSO DEFINE
# THE INIT CALLER (JUST AFTER AVAILABLE_Q_KIND_VALUES)
AVAILABLE_Q_KIND_VALUES = \
    {'monom01_polyn1': ['default'],  # any of the 2 next
     'monom0_polyn1': ['default'],  # a×(bx + c)
     'monom1_polyn1': ['default'],  # ax×(bx + c)
     'polyn1_polyn1': ['default'],  # (ax + b)×(cx + d)
     'any_basic_expd': ['default'],  # any of the 3 prev.
     'sum_of_any_basic_expd': ['default', 'easy', 'harder', 'with_a_binomial'],
     'sign_expansion': ['default'],
     'sign_expansion_short_test': ['default'],
     'numeric_sum_square': ['default'],
     'numeric_difference_square': ['default'],
     'numeric_squares_difference': ['default'],
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
     'any_basic_expd': Expandable,
     'sum_of_any_basic_expd': Expandable,
     'sign_expansion': Expandable,
     'sign_expansion_short_test': Expandable,
     'numeric_sum_square': BinomialIdentity,
     'numeric_difference_square': BinomialIdentity,
     'numeric_squares_difference': BinomialIdentity,
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

        if q_kind == 'any_basic_expd':
            randomly_drawn = randomly.decimal_0_1()
            if randomly_drawn <= 0.25:
                self.expandable_objct = Expandable((RANDOMLY,
                                                    'monom0_polyn1'),
                                                   randomly_reversed=0.5)
            elif randomly_drawn <= 0.50:
                self.expandable_objct = Expandable((RANDOMLY,
                                                    'monom1_polyn1'),
                                                   randomly_reversed=0.5)
            else:
                self.expandable_objct = Expandable((RANDOMLY,
                                                    'polyn1_polyn1'))

        elif q_kind in ['monom0_polyn1', 'monom1_polyn1']:
            self.expandable_objct = Expandable((RANDOMLY,
                                                q_kind),
                                               randomly_reversed=0.5)
        elif q_kind == 'monom01_polyn1':
            self.expandable_objct = Expandable((RANDOMLY,
                                                randomly
                                                .pop(['monom0_polyn1',
                                                      'monom1_polyn1'])),
                                               randomly_reversed=0.5)

        elif q_kind == 'polyn1_polyn1':
            self.expandable_objct = Expandable((RANDOMLY,
                                                'polyn1_polyn1'))

        elif q_kind == 'sum_of_any_basic_expd':
            if self.q_subkind in ['harder', 'with_a_binomial']:
                # __
                choices = ['monom0_polyn1', 'monom1_polyn1']

                drawn_types = list()
                drawn_types.append(randomly.pop(choices))

                if self.q_subkind == 'with_a_binomial':
                    drawn_types.append('any_binomial')
                else:
                    drawn_types.append('minus_polyn1_polyn1')

                aux_expd_list = list()

                for t in drawn_types:
                    if t == 'any_binomial':
                        aux_expd_list.append(BinomialIdentity((RANDOMLY,
                                                               'any'),
                                                              **options))
                    else:
                        aux_expd_list.append(Expandable((RANDOMLY, t)))

                final_list = list()
                for i in range(len(aux_expd_list)):
                    final_list.append(randomly.pop(aux_expd_list))

                self.expandable_objct = Sum(final_list)

            elif self.q_subkind == 'easy':
                choices = ['monom0_polyn1', 'monom1_polyn1']

                aux_expd_list = list()
                aux_expd_list.append(Expandable((RANDOMLY,
                                                 randomly.pop(choices))))

                if randomly.heads_or_tails():
                    aux_expd_list.append(Expandable((RANDOMLY, 'sign_exp')))
                else:
                    aux_expd_list.append(Monomial((RANDOMLY, 15,
                                                   randomly.integer(0, 2))))

                final_list = list()
                for i in range(len(aux_expd_list)):
                    final_list.append(randomly.pop(aux_expd_list))

                self.expandable_objct = Sum(final_list)

            else:
                choices = ['monom0_polyn1', 'monom0_polyn1',
                           'monom1_polyn1', 'monom1_polyn1',
                           'polyn1_polyn1',
                           'minus_polyn1_polyn1']

                drawn_types = list()
                drawn_types.append(randomly.pop(choices))
                drawn_types.append(randomly.pop(choices))

                aux_expd_list = list()

                for element in drawn_types:
                    aux_expd_list.append(Expandable((RANDOMLY, element)))

                aux_expd_list.append(Monomial((RANDOMLY, 15, 2)))

                final_list = list()
                for i in range(len(aux_expd_list)):
                    final_list.append(randomly.pop(aux_expd_list))

                self.expandable_objct = Sum(final_list)

        elif q_kind in ['sign_expansion', 'sign_expansion_short_test']:
            sign_exp_kind = options.get('sign_exp_kind', 0)

            if q_kind == 'sign_expansion_short_test':
                sign_exp_kind = 1

            if sign_exp_kind == 0:
                sign_exp_kind = randomly.integer(1, 5)

            # Creation of the terms
            aux_terms_list = list()

            aux_expd_1 = Expandable((Monomial((randomly.sign(), 1, 0)),
                                     Polynomial((RANDOMLY, 15, 2, 2))))

            aux_expd_2 = Expandable((Monomial((randomly.sign(), 1, 0)),
                                     Polynomial((RANDOMLY, 15, 2, 2))))

            aux_expd_3 = Expandable((Monomial((randomly.sign(), 1, 0)),
                                     Polynomial((RANDOMLY, 15, 2, 2))))

            long_aux_expd = Expandable((Monomial((randomly.sign(), 1, 0)),
                                        Polynomial((RANDOMLY, 15, 2, 3))))

            if q_kind == 'sign_expansion_short_test':
                long_aux_expd = Expandable((Monomial(('-', 1, 0)),
                                            Polynomial((RANDOMLY, 15, 2, 3))))

            aux_monomial = Monomial((RANDOMLY, 15, 2))

            # 1st kind: a Monomial and ± (long Polynomial)
            # (like in a short test)
            if sign_exp_kind == 1:
                aux_terms_list.append(long_aux_expd)
                aux_terms_list.append(aux_monomial)

            # 2d kind: ± (x+3) ± (4x - 7)
            elif sign_exp_kind == 2:
                aux_terms_list.append(aux_expd_1)
                aux_terms_list.append(aux_expd_2)

            # 3d kind: ± (x+3) ± (4x - 7) ± (x² - 5x)
            elif sign_exp_kind == 3:
                aux_terms_list.append(aux_expd_1)
                aux_terms_list.append(aux_expd_2)
                aux_terms_list.append(aux_expd_3)

            # 4th kind: ± (x+3) ± (4x - 7) ± Monomial
            elif sign_exp_kind == 4:
                aux_terms_list.append(aux_expd_1)
                aux_terms_list.append(aux_expd_2)
                aux_terms_list.append(aux_monomial)

            # 5th kind: ± (x+3) ± Monomial ± (long Polynomial)
            elif sign_exp_kind == 5:
                aux_terms_list.append(aux_expd_2)
                aux_terms_list.append(aux_monomial)
                aux_terms_list.append(long_aux_expd)

            # add as many possibilities as wanted,
            # don't forget to increase the last number here:
            # sign_exp_kind = randomly.integer(1, 5) (what's a bit above)

            # Now let's distribute the terms randomly
            final_terms_list = list()
            for i in range(len(aux_terms_list)):
                final_terms_list.append(randomly.pop(aux_terms_list))

            self.expandable_objct = Sum(final_terms_list)

        elif q_kind in ['numeric_sum_square', 'numeric_difference_square',
                        'numeric_squares_difference']:
            # __
            self.expandable_objct = init_caller((options['couple'][0],
                                                 options['couple'][1]),
                                                **options)
            if q_kind in ['numeric_sum_square', 'numeric_difference_square']:
                self.numeric_aux = Sum([options['couple'][0],
                                        options['couple'][1]]).reduce_()
                self.numeric_aux.set_exponent(2)

            else:  # squares_difference's case
                aux1 = Sum([options['couple'][0],
                            options['couple'][1]]).reduce_()
                temp = options['couple'][1].clone()
                temp.set_sign('-')
                aux2 = Sum([options['couple'][0],
                            temp]).reduce_()
                self.numeric_aux = Product([aux1, aux2])

        else:
            if q_kind == 'any_binomial':
                q_kind = 'any'

            self.expandable_objct = init_caller((RANDOMLY, q_kind),
                                                **options)

        # Creation of the expression:
        number = 0
        if 'expression_number' in options                                     \
           and is_.a_natural_int(options['expression_number']):
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

        result = ""

        if self.q_kind in ['numeric_sum_square', 'numeric_difference_square',
                           'numeric_squares_difference']:
            # __
            result += M.write_math_style2(M.type_string(self.numeric_aux))

        else:
            result += M.write_math_style2(M.type_string(self.expression))

        result += M.write_new_line()

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        M = shared.machine

        result = ""

        if self.q_kind in ['numeric_sum_square', 'numeric_difference_square',
                           'numeric_squares_difference']:
            # __
            result += M.write_math_style2(M.type_string(self.numeric_aux))
            result += M.write_new_line()

        result += M.write(self.expression.auto_expansion_and_reduction())

        return result
