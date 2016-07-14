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

from mathmaker.lib import randomly, is_
from mathmaker.lib.maths_lib import gcd
from mathmaker.lib import shared
from .Q_Structure import Q_Structure
from mathmaker.lib.core.base_calculus import (Item, Fraction, Product,
                                              Quotient, Sum)
from mathmaker.lib.core.calculus import Expression

AVAILABLE_Q_KIND_VALUES = \
    {'fraction_simplification': ['default'],
     'fractions_sum': ['default'],
     'fractions_product': ['default'],
     'fractions_quotient': ['default']
     }

FRACTION_PRODUCT_AND_QUOTIENT_TABLE = [0.07,  # 2
                                       0.08,  # 3
                                       0.08,  # 4
                                       0.08,  # 5
                                       0.08,  # 6
                                       0.07,  # 7
                                       0.08,  # 8
                                       0.08,  # 9
                                       0.09,  # 10
                                       0.02,  # 11
                                       0.05,  # 12
                                       0.02,  # 13
                                       0.05,  # 14
                                       0.03,  # 15
                                       0.04,  # 16
                                       0.01,  # 17
                                       0.03,  # 18
                                       0.01,  # 19
                                       0.03   # 20
                                       ]

FRACTIONS_SUMS_TABLE = [([1, 2], 15),
                        ([1, 3], 15),
                        ([1, 4], 15),
                        ([1, 5], 15),
                        ([1, 6], 15),
                        ([1, 7], 15),
                        ([2, 3], 17),
                        ([2, 5], 10),
                        ([2, 7], 7),
                        ([3, 4], 9),
                        ([3, 5], 7),
                        ([3, 7], 5),
                        ([4, 5], 5),
                        ([4, 7], 3),
                        ([5, 6], 4),
                        ([5, 7], 4),
                        ([6, 7], 3)]

FRACTIONS_SUMS_SCALE_TABLE = [0.02,  # (1, 2)
                              0.02,
                              0.02,
                              0.01,
                              0.005,
                              0.005,  # (1, 7)
                              0.21,  # (2, 3)
                              0.14,  # (2, 5)
                              0.02,  # (2, 7)
                              0.21,  # (3, 4)
                              0.14,  # (3, 5)
                              0.01,  # (3, 7)
                              0.16,  # (4, 5)
                              0.01,  # (4, 7)
                              0.01,  # (5, 6)
                              0.005,  # (5, 7)
                              0.005]  # (6, 7)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Q_Calculation
# @brief All kinds of numeric calculation questions (Fractions Sums,
# Products, numeric Sums & Products with priorities etc.)
class Q_Calculation(Q_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Any options
    #   @return One instance of question.Q_Calculation
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

        # That's the number of the question, not of the expressions it might
        # contain !
        self.number = ""
        if 'number_of_questions' in options:
            self.number = options['number_of_questions']

        self.objct = None

        # 1st OPTION
        if q_kind == 'fraction_simplification':
            root = randomly.integer(2,
                                    19,
                                    weighted_table=[0.225, 0.225, 0, 0.2,
                                                    0, 0.2, 0, 0, 0, 0.07,
                                                    0, 0.0375, 0, 0, 0,
                                                    0.0375, 0, 0.005])

            factors_list = [j + 1 for j in range(10)]

            ten_power_factor1 = 1
            ten_power_factor2 = 1

            if 'with_ten_powers' in options \
               and is_.a_number(options['with_ten_powers']) \
               and options['with_ten_powers'] <= 1 \
               and options['with_ten_powers'] >= 0:
                # __
                if randomly.decimal_0_1() < options['with_ten_powers']:
                    ten_powers_list = [10, 10, 100, 100]
                    ten_power_factor1 = randomly.pop(ten_powers_list)
                    ten_power_factor2 = randomly.pop(ten_powers_list)

            self.objct = Fraction(('+',
                                   root * randomly.pop(factors_list)
                                   * ten_power_factor1,
                                   root * randomly.pop(factors_list)
                                   * ten_power_factor2))

        # 2d & 3d OPTIONS
        # Fractions Products | Quotients
        elif q_kind in ['fractions_product', 'fractions_quotient']:
            # In some cases, the fractions will be generated
            # totally randomly
            if randomly.decimal_0_1() < 0:
                lil_box = [n + 2 for n in range(18)]
                a = randomly.pop(
                    lil_box,
                    weighted_table=FRACTION_PRODUCT_AND_QUOTIENT_TABLE)
                b = randomly.pop(
                    lil_box,
                    weighted_table=FRACTION_PRODUCT_AND_QUOTIENT_TABLE)

                lil_box = [n + 2 for n in range(18)]
                c = randomly.pop(
                    lil_box,
                    weighted_table=FRACTION_PRODUCT_AND_QUOTIENT_TABLE)
                d = randomly.pop(
                    lil_box,
                    weighted_table=FRACTION_PRODUCT_AND_QUOTIENT_TABLE)

                f1 = Fraction((randomly.sign(plus_signs_ratio=0.75),
                               Item((randomly.sign(plus_signs_ratio=0.80),
                                     a)),
                               Item((randomly.sign(plus_signs_ratio=0.80),
                                     b))))

                f2 = Fraction((randomly.sign(plus_signs_ratio=0.75),
                               Item((randomly.sign(plus_signs_ratio=0.80),
                                     c)),
                               Item((randomly.sign(plus_signs_ratio=0.80),
                                     d))))

                # f1 = f1.simplified()
                # f2 = f2.simplified()

            # In all other cases (80%), we'll define a "seed" a plus two
            # randomly numbers i and j to form the Product | Quotient:
            # a×i / b  ×   c / a × j
            # Where b is a randomly number coprime to a×i
            # and c is a randomly number coprime to a×j
            else:
                a = randomly.integer(2, 8)
                lil_box = [i + 2 for i in range(7)]
                i = randomly.pop(lil_box)
                j = randomly.pop(lil_box)

                b = randomly.coprime_to(a * i, [n + 2 for n in range(15)])
                c = randomly.not_coprime_to(b,
                                            [n + 2 for n in range(30)],
                                            excepted=a * j)

                f1 = Fraction((randomly.sign(plus_signs_ratio=0.75),
                               Item((randomly.sign(plus_signs_ratio=0.80),
                                     a * i)),
                               Item((randomly.sign(plus_signs_ratio=0.80),
                                     b))))

                f2 = Fraction((randomly.sign(plus_signs_ratio=0.75),
                               Item((randomly.sign(plus_signs_ratio=0.80),
                                     c)),
                               Item((randomly.sign(plus_signs_ratio=0.80),
                                     a * j))))

                if randomly.heads_or_tails():
                    f3 = f1.clone()
                    f1 = f2.clone()
                    f2 = f3.clone()

                if q_kind == 'fractions_quotient':
                    f2 = f2.invert()

            if q_kind == 'fractions_product':
                self.objct = Product([f1, f2])

            elif q_kind == 'fractions_quotient':
                self.objct = Quotient(('+', f1, f2, 1,
                                       'use_divide_symbol'))

        # 4th OPTION
        # Fractions Sums
        elif q_kind == 'fractions_sum':
            randomly_position = randomly\
                .integer(0, 16, weighted_table=FRACTIONS_SUMS_SCALE_TABLE)

            chosen_seed_and_generator = FRACTIONS_SUMS_TABLE[randomly_position]

            seed = randomly.integer(2, chosen_seed_and_generator[1])

            # The following test is only intended to avoid having "high"
            # results too often. We just check if the common denominator
            # will be higher than 75 (arbitrary) and if yes, we redetermine
            # it once. We don't do it twice since we don't want to totally
            # forbid high denominators.
            if seed * chosen_seed_and_generator[0][0] \
                    * chosen_seed_and_generator[0][1] >= 75:
                # __
                seed = randomly.integer(2, chosen_seed_and_generator[1])

            lil_box = [0, 1]
            gen1 = chosen_seed_and_generator[0][lil_box.pop()]
            gen2 = chosen_seed_and_generator[0][lil_box.pop()]

            den1 = Item(gen1 * seed)
            den2 = Item(gen2 * seed)

            temp1 = randomly.integer(1, 20)
            temp2 = randomly.integer(1, 20)

            num1 = Item(temp1 // gcd(temp1, gen1 * seed))
            num2 = Item(temp2 // gcd(temp2, gen2 * seed))

            f1 = Fraction((randomly.sign(plus_signs_ratio=0.7),
                          num1,
                          den1))
            f2 = Fraction((randomly.sign(plus_signs_ratio=0.7),
                          num2,
                          den2))

            self.objct = Sum([f1.simplified(),
                              f2.simplified()])

        # 5th
        # still to imagine:o)

        # Creation of the expression:
        number = 0
        if 'expression_number' in options                                     \
           and is_.a_natural_int(options['expression_number']):
            # __
            number = options['expression_number']
        self.expression = Expression(number, self.objct)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the text of the question as a str
    def text_to_str(self):
        M = shared.machine

        return M.write_math_style1(M.type_string(self.expression))

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        M = shared.machine

        result = ""

        while self.objct is not None:
            result += M.write_math_style1(M.type_string(self.expression))

            self.objct = self.objct.calculate_next_step()
            if self.objct is not None:
                self.expression = Expression(self.expression.name,
                                             self.objct)
        return result
