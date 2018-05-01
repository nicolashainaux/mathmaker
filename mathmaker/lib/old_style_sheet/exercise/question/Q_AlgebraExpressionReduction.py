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

from mathmakerlib.calculus import is_integer, is_natural

from mathmaker.lib import shared
from .Q_Structure import Q_Structure
from mathmaker.lib.core.base_calculus import (Product, Monomial, Item, Sum,
                                              Polynomial)
from mathmaker.lib.core.calculus import Expression
from mathmaker.lib.constants import RANDOMLY, NUMERIC

# Shared constants
AVAILABLE_Q_KIND_VALUES = {'product': ['default'],
                           'sum_of_products': ['default'],
                           'sum': ['default'],
                           'long_sum': ['default'],
                           'long_sum_including_a_coeff_1': ['default'],
                           'sum_not_reducible': ['default'],
                           'sum_with_minus-brackets': ['default']}

MAX_COEFF_TABLE = {'product': 10,
                   'sum_of_products': 10,
                   'sum': 10,
                   'long_sum': 15,
                   'long_sum_including_a_coeff_1': 15,
                   'sum_not_reducible': 20,
                   'sum_with_minus-brackets': 15}

MAX_EXPONENT_TABLE = {'product': 1,
                      'sum_of_products': 1,
                      'sum': 2,
                      'long_sum': 2,
                      'long_sum_including_a_coeff_1': 2,
                      'sum_not_reducible': 2,
                      'sum_with_minus-brackets': 2}

DEFAULT_MINIMUM_LENGTH_TABLE = {'product': 1,
                                'sum_of_products': 2,
                                'sum': 2,
                                'long_sum': 7,
                                'long_sum_including_a_coeff_1': 7,
                                'sum_not_reducible': 2,
                                'sum_with_minus-brackets': 4}

DEFAULT_MAXIMUM_LENGTH_TABLE = {'product': 1,
                                'sum_of_products': 4,
                                'sum': 6,
                                'long_sum': 10,
                                'long_sum_including_a_coeff_1': 10,
                                'sum_not_reducible': 3,
                                'sum_with_minus-brackets': 6}

# Product Reduction constants (PR_*)
PR_MAX_LITERAL_ITEMS_NB = 2
PR_SAME_LETTER_MAX_OCCURENCES_NB = 2
PR_NUMERIC_ITEMS_MAX_NB = 2


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Q_AlgebraExpressionReduction
# @brief All algebraic expression reduction questions
class Q_AlgebraExpressionReduction(Q_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param q_kind= the kind of question desired
    #          Available values are: 'product'
    #                                 'sum'
    #                                 'sum_of_products'
    #   @param **options Options detailed below:
    #          - short_test=bool
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #          - q_subkind=<string>
    #                    'minus_brackets_nb' (values: 1, 2, 3)
    #                    'plus_brackets_nb' (values: 1, 2, 3)
    #   @todo describe the different available options in this comment
    #   @return One instance of question.Q_AlgebraExpressionReduction
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

        MAX_COEFF = MAX_COEFF_TABLE[q_kind]
        MAX_EXPONENT = MAX_EXPONENT_TABLE[q_kind]
        MIN_LENGTH = DEFAULT_MINIMUM_LENGTH_TABLE[q_kind]
        MAX_LENGTH = DEFAULT_MAXIMUM_LENGTH_TABLE[q_kind]
        LENGTH_SPAN = MAX_LENGTH - MIN_LENGTH + 1

        # This field is to be used in the answer_to_strs() method
        # to determine a possibly different algorithm for particular cases
        self.kind_of_answer = ""

        # Max coefficient & degree values...
        max_coeff = options.get('max_coeff', MAX_COEFF)
        max_expon = options.get('max_expon', MAX_EXPONENT)
        length = options.get('length',
                             random.choice([n + MIN_LENGTH
                                            for n in range(LENGTH_SPAN)]))

        # 1st CASE:
        # PRODUCT REDUCTION
        if q_kind == 'product':
            # First let's determine a pack of letters where to draw
            # The default one will be [a, b, c, x, y, z]
            # but the reduced or entire alphabets can be used as well
            letters_package = ['a', 'b', 'c', 'x', 'y', 'z']

            self.kind_of_answer = 'product_detailed'
            if 'use_reduced_alphabet' in options:
                letters_package = ['a', 'b', 'c', 'd', 'g', 'h', 'k', 'p',
                                   'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                                   'y', 'z']

            elif ('use_these_letters' in options
                  and type(options['use_these_letters']) is list
                  and all([type(elt) is str
                           for elt in options['use_these_letters']])):
                # __
                letters_package = options['use_these_letters']

            # Maximum Items number. (We make sure at the same time that
            # we won't
            # risk to draw a greater number of letters than the available
            # letters
            # in letters_package)
            max_literal_items_nb = min(PR_MAX_LITERAL_ITEMS_NB,
                                       len(letters_package))

            # Maximum number of occurences of the same letter in
            # the initial expression
            same_letter_max_occurences = PR_SAME_LETTER_MAX_OCCURENCES_NB

            if ('nb_occurences_of_the_same_letter' in options
                and options['nb_occurences_of_the_same_letter'] >= 1):
                # __
                same_letter_max_occurences = options['nb_occurences_of'
                                                     '_the_same_letter']

            # CREATION OF THE EXPRESSION
            # We draw randomly the letters that will appear
            # in the expression
            current_letters_package = list(letters_package)

            nb_of_letters_to_draw = random.randint(1, max_literal_items_nb)

            drawn_letters = list()

            for j in range(nb_of_letters_to_draw):
                drawn_letters.append(
                    random.choice(current_letters_package))

            # Let's determine how many times will appear each letter
            # and then create a list containing each of these letters
            # the number of times they will appear
            pre_items_list = list()
            items_list = list()

            for j in range(len(drawn_letters)):
                if j == 0:
                    # We make sure that at least one letter occurs twice
                    # so that the exercise remains interesting !
                    # But the number of cases this letter occurs 3 three
                    # times  should be limited to keep sufficient
                    # simple cases for the pupils to begin with.
                    # It is really easy to make it much more complicated
                    # simply giving:
                    # nb_occurences_of_the_same_letter=<enough_high_nb>
                    # as an argument.
                    if random.random() < 0.5:
                        occurences_nb = 2
                    else:
                        occurences_nb = \
                            random.randint(
                                min(2, same_letter_max_occurences),
                                same_letter_max_occurences)
                else:
                    occurences_nb = \
                        random.randint(1, same_letter_max_occurences)

                if occurences_nb >= 1:
                    for k in range(occurences_nb):
                        pre_items_list.append(drawn_letters[j])

            # draw the number of numeric Items
            nb_item_num = random.randint(1, PR_NUMERIC_ITEMS_MAX_NB)

            # put them in the pre items' list
            for j in range(nb_item_num):
                pre_items_list.append(NUMERIC)

            # prepare the items' list that will be given to the Product's
            # constructor
            loop_nb = len(pre_items_list)

            for j in range(loop_nb):
                next_item_kind = random.choice(pre_items_list)

                # It's not really useful nor really possible to limit the
                # number
                # of occurences of the same letter being drawn twice in
                # a row because it belongs to the exercise and there
                # are many cases when
                # the same letter is in the list in 3 over 4 elements.
                # if j >= 1 and next_item_kind == items_list[j - 1]
                # .raw_value:
                #    pre_items_list.append(next_item_kind)
                #    next_item_kind = random.choice(pre_items_list)

                if next_item_kind == NUMERIC:
                    temp_item = Item((random.choices(['+', '-'],
                                                     cum_weights=[0.75,
                                                                  1])[0],
                                      random.randint(1, max_coeff),
                                      1))
                    items_list.append(temp_item)

                else:
                    item_value = next_item_kind
                    temp_item = Item((random.choices(['+', '-'],
                                                     cum_weights=[0.9,
                                                                  1])[0],
                                      item_value,
                                      random.randint(1, max_expon)))
                    items_list.append(temp_item)

            # so now that the items_list is complete,
            # let's build the Product !
            self.objct = Product(items_list)
            self.objct.set_compact_display(False)

            # Let's take some × symbols off the Product to match a more
            # usual situation
            for i in range(len(self.objct) - 1):
                if ((self.objct.factor[i].is_numeric()
                     and self.objct.factor[i + 1].is_literal())
                    or (self.objct.factor[i].is_literal()
                        and self.objct.factor[i + 1].is_literal()
                        and self.objct.factor[i].raw_value
                        != self.objct.factor[i + 1].raw_value
                    and random.random() > 0.5)):
                    # __
                    self.objct.info[i] = False

        # 2d CASE:
        # SUM OF PRODUCTS REDUCTION
        if q_kind == 'sum_of_products':
            if (not ('length' in options and is_integer(options['length'])
                and options['length'] >= 2)):
                # __
                length = random.choices(
                    [n + MIN_LENGTH for n in range(LENGTH_SPAN)],
                    weights=[n for n in range(LENGTH_SPAN)])[0]

            # Creation of the list to give later to the Sum constructor
            products_list = list()

            for i in range(length):
                monomial1 = Monomial((RANDOMLY,
                                      max_coeff,
                                      max_expon))
                monomial2 = Monomial((RANDOMLY,
                                      max_coeff,
                                      max_expon))
                products_list.append(Product([monomial1, monomial2]))

            # Creation of the Sum
            self.objct = Sum(products_list)

        # 3d CASE:
        # SUM REDUCTION
        if q_kind == 'sum':
            self.kind_of_answer = 'sum'
            length = options.get('length',
                                 random.choice([n + MIN_LENGTH
                                                for n in range(LENGTH_SPAN)]))
            self.objct = Polynomial((RANDOMLY,
                                     max_coeff,
                                     max_expon,
                                     length))

        # Creation of the expression:
        number = 0
        if ('expression_number' in options
            and is_natural(options['expression_number'])):
            # __
            number = options['expression_number']

        self.expression = Expression(number, self.objct)

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

        result = ""

        if self.kind_of_answer == 'product_detailed':
            result += M.write_math_style2(M.type_string(self.expression))
            result += M.write_new_line()

            if not all(self.objct.factor[i]
                       .alphabetical_order_cmp(self.objct.factor[i + 1]) > 0
                       for i in range(len(self.objct.factor) - 1)):
                ordered_product = self.objct.order()
                ordered_product.set_compact_display(False)
                ordered_expression = Expression(self.expression.name,
                                                ordered_product)
                result += M.write_math_style2(
                    M.type_string(ordered_expression))
                result += M.write_new_line()

            final_product = self.objct.reduce_()
            final_expression = Expression(self.expression.name,
                                          final_product)

            result += M.write_math_style2(M.type_string(final_expression))
            result += M.write_new_line()

        elif ((self.kind_of_answer in ['sum', 'sum_not_reducible'])
              and self.expression.
              right_hand_side.expand_and_reduce_next_step() is None):
            # __
            result += M.write_math_style2(M.type_string(self.expression))
            result += M.write_new_line()
            result += M.write(_("This expression is not reducible."))
            result += M.write_new_line()

        else:
            result += M.write(self.expression.auto_expansion_and_reduction())

        return result
