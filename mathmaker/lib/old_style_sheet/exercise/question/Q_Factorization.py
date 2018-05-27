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

from mathmaker.lib.tools.maths import coprimes_to
from mathmaker.lib import shared
from mathmaker.lib.core.root_calculus import Exponented
from mathmaker.lib.core.base_calculus import (Item, Product, Expandable, Sum,
                                              Monomial, Polynomial)
from mathmaker.lib.core.calculus import Equality, Expression
from .Q_Structure import Q_Structure
from mathmaker.lib.constants import RANDOMLY

AVAILABLE_Q_KIND_VALUES = \
    {'level_01':
     ['default',
      'ax + b',
      'ax² + b',
      'ax² + bx',
      'three_terms',
      'not_factorizable',
      'mixed',
      'mixed_factorizable'],
     # C: common factor
     # F1 & F2: the other factors
     # deg1 and deg2 represent polynoms
     # of 1st and 2d degree
     # F1 and F2 will be randomly exchanged at creation
     # of the expression, so a case like a×deg1 + a×deg2
     # contains also a×deg2 + a×deg1

     # C × F1  ±  C × F2

     'level_02':
     ['default',   # synonym to type_123
      'type_123',  # any of type_1, type_2, type_3 (a polynom as common factor)
      'type_1',    # any of type_1_*
      'type_1_ABC',  # any of type 1 A, B and C cases
      'type_1_DEF',  # any of type 1 D, E and F cases
      'type_1_GHI',  # any of type 1 G, H and I cases
      'type_1_A',  # any of A1 or A0
      'type_1_B',  # any of B1 or B0
      'type_1_C',  # synonym to C0
      'type_1_D',  # any of D1 or D0
      'type_1_E',  # .
      'type_1_F',  # .
      'type_1_G',  # .
      'type_1_H',  # .
      'type_1_I',  # .
      'type_1_0',  # any of type_1_ * 0 cases
      'type_1_1',  # any of type_1_*1 cases
      'type_1_A0',  # a×deg1 + a×deg1' (deg * : at least 2 terms & a!=1)
      'type_1_B0',  # a×deg2 + a×deg2' (deg * : at least 2 terms & a!=1)
      'type_1_C0',  # a×deg1 + a×deg2 (deg * : at least 2 terms & a!=1)
      'type_1_D0',  # ax×deg1 + ax×deg1' (deg * : at least 2 terms)
      'type_1_E0',  # ax×deg2 + ax×deg2' (deg * : at least 2 terms)
      'type_1_F0',  # ax×deg1 + ax×deg2 (deg * : at least 2 terms)
      'type_1_G0',  # ax²×deg1 + ax²×deg1' (deg * : at least 2 terms)
      'type_1_H0',  # ax²×deg2 + ax²×deg2' (deg * : at least 2 terms)
      'type_1_I0',  # ax²×deg1 + ax²×deg2 (deg * : at least 2 terms)
      'type_1_A1',  # a×deg1 + a×1
      'type_1_B1',  # a×deg2 + a×1
      # 'type_1_C1', # C1 has no sense
      'type_1_D1',  # ax×deg1 + ax×1
      'type_1_E1',  # ax×deg2 + ax×1
      # 'type_1_F1', # F1 has no sense
      'type_1_G1',  # ax²×deg1 + ax²×1
      'type_1_H1',  # ax²×deg2 + ax²×1
      # 'type_1_I1', # I1 has no sense

      'type_2',    # any of type_2_*
      'type_2_ABC',  # any of type 2 A, B and C cases
      'type_2_DEF',  # any of type 2 D, E and F cases
      'type_2_A',  # any of A1 or A0
      'type_2_B',  # any of B1 or B0
      'type_2_C',  # synonym to C0
      'type_2_D',  # any of D1 or D0
      'type_2_E',  # .
      'type_2_F',  # .
      'type_2_0',  # any of type_2_ * 0 cases
      'type_2_1',  # any of type_2_*1 cases
      'type_2_A0',  # (ax+b)×deg1 + (ax+b)×deg1'
      'type_2_B0',  # (ax+b)×deg2 + (ax+b)×deg2'
      'type_2_C0',  # (ax+b)×deg1 + (ax+b)×deg2
      'type_2_D0',  # (ax²+b)×deg1 + (ax²+b)×deg1'
      'type_2_E0',  # (ax²+b)×deg2 + (ax²+b)×deg2'
      'type_2_F0',  # (ax²+b)×deg1 + (ax²+b)×deg2
      'type_2_A1',  # (ax+b)×deg1 + (ax+b)×1
      'type_2_B1',  # (ax+b)×deg2 + (ax+b)×1
      # 'type_2_C1', # C1 has no sense
      'type_2_D1',  # (ax²+b)×deg1 + (ax²+b)×1
      'type_2_E1',  # (ax²+b)×deg2 + (ax²+b)×1
      # 'type_2_F1', # F1 has no sense

      'type_3',    # any of type_3_*
      'type_3_ABC',  # any of type 3 A, B and C cases
      'type_3_A',  # any of A1 or A0
      'type_3_B',  # any of B1 or B0
      'type_3_C',  # synonym to C0
      'type_3_0',   # any of type_3_ * 0 cases
      'type_3_1'   # any of type_3_*1 cases
      'type_3_A0',  # (ax²+bx+c)×deg1 + (ax²+bx+c)×deg1'
      'type_3_B0',  # (ax²+bx+c)×deg2 + (ax²+bx+c)×deg2'
      'type_3_C0',  # (ax²+bx+c)×deg1 + (ax²+bx+c)×deg2
      'type_3_A1',  # (ax²+bx+c)×deg1 + (ax²+bx+c)×1
      'type_3_B1',  # (ax²+bx+c)×deg2 + (ax²+bx+c)×1
      # 'type_3_C1'  # C1 has no sense
      'type_4_A0'  # (ax+b)²×deg1 + (ax+b)×deg1'
      ],

     # Here are the binomial identities
     'level_03':
     ['default',   # synonym to 'any'
      'any',
      'any_mixed',  # any but from the mixed types (changed order of the terms)
      'any_straight',           # any but not from a mixed type
      'any_true',               # any that can be factorized
      'any_fake',               # any that cannot be factorized
      'any_true_straight',      # any that can be factorized, not mixed
      'any_fake_straight',      # any that cannot be factorized, not mixed
      'any_true_mixed',         # any that can be factorized, mixed
      'any_fake_mixed',         # any that cannot be factorized, mixed
      'sum_square',               # (ax)² + 2abx + b²
      'sum_square_mixed',         # like above but terms' order is changed
      'difference_square',        # (ax)² - 2abx + b²
      'difference_square_mixed',  # like above but terms' order is changed
      'squares_difference',       # (ax)² - b²
      'squares_difference_mixed',  # like above but terms' order is changed
      'fake_01',       # 2×a×b doesn't match a² and b² (sum)
      'fake_01_mixed',  # 2×a×b doesn't match a² and b² (sum, mixed)
      'fake_02',       # 2×a×b doesn't match a² and b² (difference)
      'fake_02_mixed',  # 2×a×b doesn't match a² and b² (difference, mixed)
      'fake_03',       # (ax)² + b²
      'fake_03_mixed',  # b² + (ax)²
      'fake_04_any',   # any of fake_04 (signs don't match a binomial)
      'fake_04_any_straight',
      'fake_04_any_mixed',
      'fake_04_A',        # (ax)² + 2abx - b²
      'fake_04_A_mixed',
      'fake_04_B',        # -(ax)² + 2abx + b²
      'fake_04_B_mixed',
      'fake_04_C',        # (ax)² - 2abx - b²
      'fake_04_C_mixed',
      'fake_04_D',        # -(ax)² - 2abx + b²
      'fake_04_D_mixed']}


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Q_Factorization
# @brief Question related to the factorization of a literal expression
class Q_Factorization(Q_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Any options
    #   @return One instance of question.Q_Factorization
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
        q_subkind = self.q_subkind

        # That's the number of the question, not of the expressions it might
        # contain !
        self.number = ""

        steps_method = None

        if q_kind == 'level_01':
            steps_method = level_01

            if q_subkind == 'mixed':
                q_subkind = random.choice(['default',
                                           'three_terms',
                                           'not_factorizable'])
            elif q_subkind == 'mixed_factorizable':
                q_subkind = random.choice(['default',
                                           'three_terms'])

        elif q_kind == 'level_03':
            steps_method = level_03
            options['markup'] = shared.machine.markup

            if q_subkind == 'any' or q_subkind == 'default':
                q_subkind = random.choice(['any_straight',
                                           'any_mixed'])

            if q_subkind == 'any_straight':
                q_subkind = random.choice(['any_true_straight',
                                           'any_fake_straight'])

            if q_subkind == 'any_mixed':
                q_subkind = random.choice(['any_true_mixed',
                                           'any_fake_mixed'])

            if q_subkind == 'any_true':
                q_subkind = random.choice(['any_true_straight',
                                           'any_true_mixed'])

            if q_subkind == 'any_fake':
                q_subkind = random.choice(['any_fake_straight',
                                           'any_fake_mixed'])

            if q_subkind == 'any_true_straight':
                q_subkind = random.choice(['sum_square',
                                           'difference_square',
                                           'squares_difference'])

            if q_subkind == 'any_fake_straight':
                q_subkind = random.choice(['fake_01',
                                           'fake_02',
                                           'fake_03',
                                           'fake_04_any_straight'])

            if q_subkind == 'any_true_mixed':
                q_subkind = random.choice(['sum_square_mixed',
                                           'difference_square_mixed',
                                           'squares_difference_mixed'])

            if q_subkind == 'any_fake_mixed':
                q_subkind = random.choice(['fake_01_mixed',
                                           'fake_02_mixed',
                                           'fake_03_mixed',
                                           'fake_04_any_mixed'])

            if q_subkind == 'fake_04_any':
                q_subkind = random.choice(['fake_04_any_mixed',
                                           'fake_04_any_straight'])

            if q_subkind == 'fake_04_any_mixed':
                q_subkind = random.choice(['fake_04_A_mixed',
                                           'fake_04_B_mixed',
                                           'fake_04_C_mixed',
                                           'fake_04_D_mixed'])

            if q_subkind == 'fake_04_any_straight':
                q_subkind = random.choice(['fake_04_A',
                                           'fake_04_B',
                                           'fake_04_C',
                                           'fake_04_D'])

        steps = steps_method(q_subkind, **options)

        # Creation of the expression:
        number = 0
        if ('expression_number' in options
            and is_natural(options['expression_number'])):
            # __
            number = options['expression_number']
        self.expression = Expression(number, steps[0])

        # Putting the steps and the solution together:
        self.steps = []

        # for i in xrange(len(steps) - 1):
        #    self.steps.append(Expression(number,
        #                                          steps[i]
        #                                          )
        #                     )
        #
        # solution = steps[len(steps) - 1]
        #
        # if isinstance(solution, Exponented):
        #    self.steps.append(Expression(number,
        #                                          solution
        #                                          )
        #                     )
        # else:
        #    self.steps.append(solution)

        for i in range(len(steps)):
            if isinstance(steps[i], Exponented):
                self.steps.append(Expression(number, steps[i]))
            else:
                self.steps.append(steps[i])

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

        for i in range(len(self.steps)):
            if type(self.steps[i]) == str:
                result += M.write(self.steps[i])
            else:
                result += M.write_math_style2(M.type_string(self.steps[i]))
            result += M.write_new_line()

        return result


# --------------------------------------------------------------------------
##
#   @brief Creates & returns the solution and the answer's steps.
#   @return steps (list containing the steps)
def level_01(q_subkind, **options):
    if q_subkind == 'default' \
       or q_subkind == 'three_terms' \
       or q_subkind == 'ax + b' \
       or q_subkind == 'ax² + b' \
       or q_subkind == 'ax² + bx':
        # __
        # the idea is to build the final factorized result first and to
        # expand it to get the question (and the solution's steps
        # in the same time)

        if q_subkind == 'default':
            common_factor = Monomial((RANDOMLY, 6, 1))
            # In order to reduce the number of cases where x² appears,
            # let the common factor be of degree 0 most of the time.
            common_factor.set_degree(random.choices([0, 1],
                                                    weights=[0.85, 0.15])[0])
        elif q_subkind in ['three_terms', 'ax + b', 'ax² + b']:
            common_factor = Monomial((RANDOMLY, 6, 0))

        elif q_subkind == 'ax² + bx':
            common_factor = Monomial((RANDOMLY, 6, 1))
            common_factor.set_degree(1)

        # to avoid having a situation like 1×(2x + 3) which isn't
        # factorizable:
        if common_factor.get_degree() == 0:
            common_factor.set_coeff(random.randint(2, 6))

        # signs are randomly chosen ; the only case that is to be avoided
        # is all signs are negative (then it wouldn't factorize well...
        # I mean then the '-' should be factorized and not left in the final
        # result)
        signs_box = [['+', '+'], ['+', '-']]
        signs = random.choice(signs_box)

        # this next test is to avoid -2x + 6 being factorized -2(x - 3)
        # which is not wrong but not "natural" to pupils
        # this test should be changed when a third term is being used.
        if signs == ['+', '-']:
            common_factor.set_sign('+')

        coeff_1 = random.randint(2, 10)
        coeff_2 = random.choice(coprimes_to(coeff_1, [i + 1
                                                      for i in range(10)]))
        coeff_3 = None

        if q_subkind == 'three_terms':
            coeff_3 = random.choice(coprimes_to(coeff_1 * coeff_2,
                                                [i + 1 for i in range(9)]))
            third_sign = random.choice(['+', '-'])
            if third_sign == '-':
                common_factor.set_sign('+')

            signs.append(third_sign)

        lil_box = []
        lil_box.append(Monomial(('+', 1, 0)))

        if q_subkind == 'ax² + b':
            lil_box.append(Monomial(('+', 1, 2)))
        else:
            lil_box.append(Monomial(('+', 1, 1)))

        if ((common_factor.get_degree() == 0
             and random.randint(1, 20) > 17
             and q_subkind == 'default')
            or q_subkind == 'three_terms'):
            # __
            lil_box.append(Monomial(('+', 1, 2)))

        random.shuffle(lil_box)
        first_term = lil_box.pop()
        second_term = lil_box.pop()
        third_term = None

        random.shuffle(signs)
        first_term.set_coeff(coeff_1)
        first_term.set_sign(signs.pop())
        second_term.set_coeff(coeff_2)
        second_term.set_sign(signs.pop())

        if q_subkind == 'three_terms':
            third_term = lil_box.pop()
            third_term.set_coeff(coeff_3)
            third_term.set_sign(signs.pop())
            if first_term.is_positive() and second_term.is_positive()\
               and third_term.is_positive():
                # __
                common_factor.set_sign(random.choice(['+', '-']))

        if not (q_subkind == 'three_terms'):
            if common_factor.get_degree() == 0 \
               and first_term.get_degree() >= 1 \
               and second_term.get_degree() >= 1:
                # __
                if random.choice([True, False]):
                    first_term.set_degree(0)
                else:
                    second_term.set_degree(0)

        if q_subkind == 'three_terms':
            solution = Expandable((common_factor,
                                   Sum([first_term,
                                        second_term,
                                        third_term])))

        else:
            solution = Expandable((common_factor,
                                   Sum([first_term,
                                        second_term])))

        # now create the expanded step and the reduced step (which will
        # be given as a question)
        temp_steps = []
        current_step = solution.clone()

        while current_step is not None:
            temp_steps.append(current_step)
            current_step = current_step.expand_and_reduce_next_step()

        # now we put the steps in the right order
        steps = []
        for i in range(len(temp_steps)):
            steps.append(temp_steps[len(temp_steps) - 1 - i])

        return steps

    elif q_subkind == 'not_factorizable':
        signs_box = [['+', '+'], ['+', '-']]
        signs = random.choice(signs_box)

        coeff_1 = random.randint(2, 10)
        coeff_2 = random.choice(coprimes_to(coeff_1,
                                            [i + 1 for i in range(10)]))

        lil_box = []
        lil_box.append(Monomial(('+', 1, 0)))
        lil_box.append(Monomial(('+', 1, 1)))
        lil_box.append(Monomial(('+', 1, 2)))

        random.shuffle(lil_box)
        first_term = lil_box.pop()
        second_term = lil_box.pop()

        random.shuffle(signs)
        first_term.set_coeff(coeff_1)
        first_term.set_sign(signs.pop())

        second_term.set_coeff(coeff_2)
        second_term.set_sign(signs.pop())

        if first_term.get_degree() >= 1 \
           and second_term.get_degree() >= 1:
            # __
            if random.choice([True, False]):
                first_term.set_degree(0)
            else:
                second_term.set_degree(0)

        steps = []
        solution = _("So far, we don't know if this expression can be "
                     "factorized.")
        steps.append(Sum([first_term, second_term]))
        steps.append(solution)

        return steps


# --------------------------------------------------------------------------
##
#   @brief Creates & returns the solution and the answer's steps.
#   @return steps (list containing the steps)
def level_03(q_subkind, **options):

    a = random.randint(1, 10)
    b = random.randint(1, 10)

    steps = []

    if q_subkind in ['sum_square', 'sum_square_mixed', 'difference_square',
                     'difference_square_mixed']:
        # __
        first_term = Monomial(('+',
                               Item(('+', a, 2)).evaluate(),
                               2))

        second_term = Monomial(('+',
                                Item(('+', Product([2, a, b]).evaluate(), 1))
                                .evaluate(),
                                1))

        third_term = Monomial(('+', Item(('+', b, 2)).evaluate(), 0))

        if q_subkind in ['difference_square', 'difference_square_mixed']:
            second_term.set_sign('-')

        if q_subkind in ['sum_square_mixed', 'difference_square_mixed']:
            ordered_expression = Polynomial([first_term,
                                             second_term,
                                             third_term])
            terms = [first_term, second_term, third_term]
            random.shuffle(terms)
            first_term, second_term, third_term = terms

        steps.append(Polynomial([first_term, second_term, third_term]))

        if q_subkind in ['sum_square_mixed', 'difference_square_mixed']:
            steps.append(ordered_expression)

        sq_a_monom = Monomial(('+', a, 1))
        sq_b_monom = Monomial(('+', b, 0))

        let_a_eq = Equality([Item('a'),
                             sq_a_monom])

        let_b_eq = Equality([Item('b'),
                             sq_b_monom])

        steps.append(_("Let") + " "
                     + let_a_eq.into_str(force_expression_markers=True)
                     + " " + _("and") + " "
                     + let_b_eq.into_str(force_expression_markers=True))

        sq_a_monom.set_exponent(2)
        sq_b_monom.set_exponent(2)

        a_square_eq = Equality([Item(('+', 'a', 2)),
                                sq_a_monom,
                                sq_a_monom.reduce_()])

        b_square_eq = Equality([Item(('+', 'b', 2)),
                                sq_b_monom,
                                sq_b_monom.reduce_()])

        steps.append(_("then") + " "
                     + a_square_eq.into_str(force_expression_markers=True))

        steps.append(_("and") + " "
                     + b_square_eq.into_str(force_expression_markers=True))

        two_times_a_times_b_numeric = Product([Item(2),
                                               Monomial(('+', a, 1)),
                                               Item(b)])

        two_times_a_times_b_reduced = two_times_a_times_b_numeric.reduce_()

        two_times_a_times_b_eq = Equality([Product([Item(2),
                                                    Item('a'),
                                                    Item('b')]),
                                           two_times_a_times_b_numeric,
                                           two_times_a_times_b_reduced])

        steps.append(_("and") + " " + two_times_a_times_b_eq.into_str(
            force_expression_markers=True))

        steps.append(_("So it is possible to factorize:"))

        if q_subkind in ['difference_square', 'difference_square_mixed']:
            b = -b

        factorized_expression = Sum([Monomial(('+', a, 1)), Item(b)])
        factorized_expression.set_exponent(2)

        steps.append(factorized_expression)

    elif q_subkind in ['squares_difference', 'squares_difference_mixed']:
        # To have some (ax)² - b² but also sometimes b² - (ax)²:
        degrees = [2, 0, 1, 0]

        if random.randint(1, 10) >= 8:
            degrees = [0, 2, 0, 1]

        first_term = Monomial(('+',
                               Item(('+', a, 2)).evaluate(),
                               degrees[0]))

        second_term = Monomial(('-',
                                Item(('+', b, 2)).evaluate(),
                                degrees[1]))

        sq_first_term = Monomial(('+',
                                  Item(('+', a, 1)).evaluate(),
                                  degrees[2]))

        sq_second_term = Monomial(('-',
                                   Item(('+', b, 1)).evaluate(),
                                   degrees[3]))

        # The 'mixed' cases are: -b² + (ax)² and -(ax)² + b²
        if q_subkind == 'squares_difference_mixed':
            first_term, second_term = second_term, first_term
            sq_first_term, sq_second_term = sq_second_term, sq_first_term

        positive_sq_first = sq_first_term.clone()
        positive_sq_first.set_sign('+')
        positive_sq_second = sq_second_term.clone()
        positive_sq_second.set_sign('+')

        steps.append(Polynomial([first_term, second_term]))

        first_inter = None
        second_inter = None

        if sq_second_term.is_negative():
            first_inter = positive_sq_first.clone()
            first_inter.set_exponent(2)
            temp_second_inter = positive_sq_second.clone()
            temp_second_inter.set_exponent(2)
            second_inter = Product([-1, temp_second_inter])
        else:
            temp_first_inter = positive_sq_first.clone()
            temp_first_inter.set_exponent(2)
            first_inter = Product([-1, temp_first_inter])
            second_inter = positive_sq_second.clone()
            second_inter.set_exponent(2)

        steps.append(Sum([first_inter, second_inter]))

        if q_subkind == 'squares_difference_mixed':
            steps.append(Sum([second_inter, first_inter]))

        steps.append(_("So, this expression can be factorized:"))

        sum1 = None
        sum2 = None

        if sq_second_term.is_negative():
            sum1 = Sum([sq_first_term, sq_second_term])
            sq_second_term.set_sign('+')
            sum2 = Sum([sq_first_term, sq_second_term])

        else:
            sum1 = Sum([sq_second_term, sq_first_term])
            sq_first_term.set_sign('+')
            sum2 = Sum([sq_second_term, sq_first_term])

        lil_box = [sum1, sum2]
        random.shuffle(lil_box)
        steps.append(Product([lil_box.pop(), lil_box.pop()]))

    elif q_subkind in ['fake_01', 'fake_01_mixed', 'fake_02', 'fake_02_mixed',
                       'fake_03', 'fake_03_mixed', 'fake_04_A',
                       'fake_04_A_mixed', 'fake_04_B', 'fake_04_B_mixed',
                       'fake_04_C', 'fake_04_C_mixed', 'fake_04_D',
                       'fake_04_D_mixed']:
        # __
        straight_cases = ['fake_01', 'fake_02', 'fake_03',
                          'fake_04_A', 'fake_04_B', 'fake_04_C', 'fake_04_D']
        match_pb_cases = ['fake_01', 'fake_02',
                          'fake_01_mixed', 'fake_02_mixed']
        sign_pb_cases = ['fake_03', 'fake_03_mixed',
                         'fake_04_A', 'fake_04_B', 'fake_04_C', 'fake_04_D',
                         'fake_04_A_mixed', 'fake_04_B_mixed',
                         'fake_04_C_mixed', 'fake_04_D_mixed']

        ax = Monomial(('+', a, 1))
        b_ = Monomial(('+', b, 0))

        ax_2 = ax.clone()
        ax_2.set_exponent(2)
        a2x2 = Monomial(('+', a * a, 2))

        b_2 = Monomial(('+', b, 0))
        b_2.set_exponent(2)

        b2 = Monomial(('+', b * b, 0))

        two_ax_b = Product([Item(2),
                            Monomial(('+', a, 1)),
                            Item(b)])

        twoabx = Monomial(('+', 2 * a * b, 1))

        fake_twoabx = Monomial(('+', a * b, 1))

        if random.randint(1, 10) >= 8:
            fake_twoabx = Monomial(('+',
                                    2 * a * b
                                    + random.choice([-1, 1])
                                    * random.randint(1, 5),
                                    1))
        first_term = None
        second_term = None
        third_term = None

        ordered_expression = None
        mixed_expression = None

        if q_subkind == 'fake_03' or q_subkind == 'fake_03_mixed':
            first_term = a2x2.clone()
            second_term = b2.clone()
            ordered_expression = Polynomial([first_term, second_term])
            mixed_expression = Polynomial([second_term, first_term])

        else:
            first_term = a2x2.clone()
            third_term = b2.clone()

            if q_subkind in ['fake_01', 'fake_01_mixed', 'fake_02',
                             'fake_02_mixed']:
                # __
                second_term = fake_twoabx.clone()

            else:
                second_term = twoabx.clone()

            if q_subkind == 'fake_02' or q_subkind == 'fake_02_mixed':
                second_term.set_sign('-')

            elif q_subkind == 'fake_04_A' or q_subkind == 'fake_04_A_mixed':
                third_term.set_sign('-')

            elif q_subkind == 'fake_04_B' or q_subkind == 'fake_04_B_mixed':
                first_term.set_sign('-')

            elif q_subkind == 'fake_04_C' or q_subkind == 'fake_04_C_mixed':
                second_term.set_sign('-')
                third_term.set_sign('-')

            elif q_subkind == 'fake_04_D' or q_subkind == 'fake_04_D_mixed':
                first_term.set_sign('-')
                second_term.set_sign('-')

            terms = [first_term, second_term, third_term]
            ordered_expression = Polynomial(terms)
            random.shuffle(terms)
            mixed_expression = Polynomial(terms)
        if q_subkind in straight_cases:
            steps.append(ordered_expression)

        elif q_subkind == 'fake_03_mixed':
            steps.append(mixed_expression)

        else:
            steps.append(mixed_expression)
            steps.append(ordered_expression)

        if q_subkind in match_pb_cases:
            let_a_eq = Equality([Item('a'),
                                 ax])

            let_b_eq = Equality([Item('b'),
                                 b_])

            steps.append(_("Let") + " "
                         + let_a_eq.into_str(force_expression_markers=True)
                         + " " + _("and") + " "
                         + let_b_eq.into_str(force_expression_markers=True))

            a_square_eq = Equality([Item(('+', 'a', 2)),
                                    ax_2,
                                    a2x2])

            b_square_eq = Equality([Item(('+', 'b', 2)),
                                    b_2,
                                    b2])

            steps.append(_("then") + " "
                         + a_square_eq.into_str(force_expression_markers=True))

            steps.append(_("and") + " "
                         + b_square_eq.into_str(force_expression_markers=True))

            two_times_a_times_b_eq = Equality([Product([Item(2),
                                                        Item('a'),
                                                        Item('b')]),
                                               two_ax_b,
                                               twoabx,
                                               fake_twoabx],
                                              equal_signs=['=', '=', 'neq'])

            steps.append(_("but") + " "
                         + two_times_a_times_b_eq.into_str(
                force_expression_markers=True))

            steps.append(_("So it does not match a binomial identity."))
            steps.append(_("This expression cannot be factorized."))

        elif q_subkind in sign_pb_cases:
            steps.append(_("Because of the signs,"))
            steps.append(_("it does not match a binomial identity."))
            steps.append(_("This expression cannot be factorized."))

    return steps
