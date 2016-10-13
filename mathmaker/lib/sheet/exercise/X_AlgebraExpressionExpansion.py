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

from mathmaker.lib import randomly, is_, error
from mathmaker.lib.core.base_calculus import Monomial
from .X_Structure import X_Structure
from . import question


AVAILABLE_X_KIND_VALUES = \
    {'short_test': ['sign_expansion', 'medium_level',
                    'three_binomials', 'three_numeric_binomials',
                    'default'],
     'mini_test': ['two_expansions_hard', 'two_randomly'],
     'preformatted': ['mixed_monom_polyn1'],
     'bypass': ['sign_expansion', 'any_basic_expd', 'sum_of_any_basic_expd',
                'sum_square', 'difference_square', 'squares_difference',
                'any_binomial', 'polyn1_polyn1', 'two_expansions_hard']}

DEFAULT_RATIO_MIXED_MONOM_POLYN1 = 0.5

X_LAYOUT_UNIT = "cm"
# ----------------------  lines_nb    col_widths   questions
# In each list, the first number is the number of lines (or the value '?'),
# then follow the columns widths. The tuple contains the questions per cell.
# For instance, [2, 6, 6, 6], (1, 1, 1, 1, 1, 1) means 2 lines, 3 cols (widths
# 6 cm each), then 1 question per cell.
X_LAYOUTS = {'default':
             {'exc': [None, 'all'],
              'ans': [None, 'all']},

             ('short_test', 'three_numeric_binomials'):
             {'exc': [None, 'all'],
              'ans': [[1, 5.5, 5.5], (2, 1)], }}


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_AlgebraExpressionExpansion
# @brief Expressions to expand (like 2(x-3) or 4x(2-9x) or (3+x)(x-1))
class X_AlgebraExpressionExpansion(X_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Options detailed below:
    #          - start_number=<integer>
    #                         (should be >= 1)
    #          - number_of_questions=<integer>
    #            /!\ only useful if you use x_kind and not preformatted
    #                         (should be >= 1)
    #          - x_kind=<string>
    #                         ...
    #                         ...
    #          - preformatted=<string>
    #            /!\ preformatted is useless with short_test
    #            /!\ number_of_questions is useless with preformatted
    #            /!\ if you use it with the x_kind option, ensure there's a
    #                preformatted possibility with this option
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #          - short_test=bool
    #            /!\ the x_kind option above can't be used along this option
    #            use subtype if you need to make different short_test exercises
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #          - subtype=<string>
    #                         ...
    #                         ...
    #   @return One instance of exercise.AlgebraExpressionExpansion
    def __init__(self, x_kind='default_nothing', **options):
        self.derived = True
        X_Structure.__init__(self,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        default_question = question.Q_AlgebraExpressionExpansion

        # TEXTS OF THE EXERCISE
        self.text = {'exc': _("Expand and reduce") + ": ",
                     'ans': ""}

        # alternate texts section
        if self.x_subkind == 'three_numeric_binomials':
            self.text = {'exc': _("Calculate thanks to a binomial "
                                  "identity:"),
                         'ans': ""}

        # PREFORMATTED EXERCISES
        if self.x_kind == 'short_test':
            if self.x_subkind == 'sign_expansion':
                q = default_question(q_kind='sign_expansion_short_test',
                                     expression_number=self.start_number,
                                     **options)

                self.questions_list.append(q)

            elif self.x_subkind == 'medium_level':

                q = default_question(q_kind='monom01_polyn1',
                                     expression_number=self.start_number,
                                     **options)

                self.questions_list.append(q)

                q = default_question(q_kind='polyn1_polyn1',
                                     expression_number=self.start_number,
                                     **options)

                self.questions_list.append(q)

                q = default_question(q_kind='sum_of_any_basic_expd',
                                     expression_number=self.start_number,
                                     **options)

                self.questions_list.append(q)

            elif self.x_subkind == 'three_binomials':
                kinds_list = ['sum_square',
                              'difference_square',
                              'squares_difference']

                for i in range(3):
                    q = default_question(q_kind=randomly.pop(kinds_list),
                                         expression_number=i,
                                         **options)
                    self.questions_list.append(q)

            elif self.x_subkind == 'three_numeric_binomials':
                a_list1 = [20, 30, 40, 50, 60, 70, 80, 90, 100]
                a_list2 = [200, 300, 400, 500, 600, 700, 800, 1000]
                b_list = [1, 2, 3]
                a1_choice = randomly.pop(a_list2)
                b1_choice = randomly.pop(b_list)
                a2_choice = randomly.pop(a_list1)
                b2_choice = randomly.pop(b_list)
                a3_choice = randomly.pop(a_list1)
                b3_choice = randomly.pop(b_list)

                a1 = Monomial(('+', a1_choice, 0))
                b1 = Monomial(('+', b1_choice, 0))
                a2 = Monomial(('+', a2_choice, 0))
                b2 = Monomial(('+', b2_choice, 0))
                a3 = Monomial(('+', a3_choice, 0))
                b3 = Monomial(('+', b3_choice, 0))

                kinds_list = ['numeric_sum_square',
                              'numeric_difference_square',
                              'numeric_squares_difference']

                monomials_to_use = [(a1, b1), (a2, b2), (a3, b3)]

                ordered_kinds_list = []
                squares_differences_option = [0, 0, 0]

                for i in range(3):
                    ordered_kinds_list.append(randomly.pop(kinds_list))
                    if ordered_kinds_list[i] == 'numeric_difference_square':
                        monomials_to_use[i][1].set_sign('-')
                    elif ordered_kinds_list[i] == 'numeric_squares_difference':
                        squares_differences_option[i] = 1

                for i in range(3):
                    if squares_differences_option[i] == 1:
                        q = default_question(q_kind=ordered_kinds_list[i],
                                             couple=monomials_to_use[i],
                                             squares_difference=True,
                                             expression_number=i,
                                             **options)
                    else:
                        q = default_question(q_kind=ordered_kinds_list[i],
                                             couple=monomials_to_use[i],
                                             expression_number=i,
                                             **options)
                    self.questions_list.append(q)

            else:  # default short_test option
                if randomly.heads_or_tails():
                    q1 = default_question(
                        q_kind='monom0_polyn1',
                        expression_number=0 + self.start_number)

                    q2 = default_question(
                        q_kind='monom1_polyn1',
                        expression_number=1 + self.start_number,
                        reversed='OK')

                else:
                    q1 = default_question(
                        q_kind='monom0_polyn1',
                        reversed='OK',
                        expression_number=0 + self.start_number)

                    q2 = default_question(
                        q_kind='monom1_polyn1',
                        expression_number=1 + self.start_number)

                q3 = default_question(q_kind='polyn1_polyn1',
                                      expression_number=2 + self.start_number)

                self.questions_list.append(q1)
                self.questions_list.append(q2)
                self.questions_list.append(q3)

        elif self.x_kind == 'mini_test':
            if self.x_subkind == 'two_expansions_hard':
                if randomly.heads_or_tails():
                    q1 = default_question(
                        q_kind='sum_of_any_basic_expd',
                        q_subkind='harder',
                        expression_number=0 + self.start_number)
                    q2 = default_question(
                        q_kind='sum_of_any_basic_expd',
                        q_subkind='with_a_binomial',
                        expression_number=1 + self.start_number)
                else:
                    q1 = default_question(
                        q_kind='sum_of_any_basic_expd',
                        q_subkind='with_a_binomial',
                        expression_number=0 + self.start_number)
                    q2 = default_question(
                        q_kind='sum_of_any_basic_expd',
                        q_subkind='harder',
                        expression_number=1 + self.start_number)

                self.questions_list.append(q1)
                self.questions_list.append(q2)

            elif self.x_subkind == 'two_randomly':
                if randomly.heads_or_tails():
                    q = default_question(q_kind='sign_expansion_short_test',
                                         expression_number=self.start_number,
                                         **options)

                    self.questions_list.append(q)

                    q = default_question(
                        q_kind='polyn1_polyn1',
                        expression_number=self.start_number + 1,
                        **options)

                    self.questions_list.append(q)

                else:
                    q = default_question(q_kind='monom01_polyn1',
                                         expression_number=self.start_number,
                                         **options)

                    self.questions_list.append(q)

                    q = default_question(
                        q_kind='sum_of_any_basic_expd',
                        q_subkind='easy',
                        expression_number=self.start_number + 1,
                        **options)

                    self.questions_list.append(q)

        elif self.x_kind == 'preformatted':
            # Mixed expandable expressions from the following types:
            # 0-degree Monomial × (1st-degree Polynomial)
            # 1-degree Monomial × (1st-degree Polynomial)
            # The Monomial & the polynomial may be swapped: it depends
            # if the option 'reversed' has been given in
            # argument in this method
            if self.x_subkind == 'mixed_monom_polyn1':
                choices_list = list()
                ratio = DEFAULT_RATIO_MIXED_MONOM_POLYN1

                if 'ratio_mmp' in options \
                   and is_.a_number(options['ratio_mmp']) \
                   and options['ratio_mmp'] > 0 \
                   and options['ratio_mmp'] < 1:
                    # __
                    ratio = options['ratio_mmp']
                else:
                    raise error.ArgumentNeeded("the ratio_mmp option "
                                               "because the "
                                               "mixed_monom_polyn1 option "
                                               "has been specified.")

                for i in range(int(self.q_nb * ratio) + 1):
                    choices_list.append('monom0_polyn1')
                for i in range(int(self.q_nb - self.q_nb * ratio)):
                    choices_list.append('monom1_polyn1')

                temp_nb = len(choices_list)

                for i in range(temp_nb):
                    choice = randomly.pop(choices_list)
                    if choice == 'monom0_polyn1':
                        q = default_question(
                            q_kind='monom0_polyn1',
                            expression_number=i + self.start_number,
                            **options)
                        self.questions_list.append(q)
                    else:
                        q = default_question(
                            q_kind='monom1_polyn1',
                            expression_number=i + self.start_number,
                            **options)
                        self.questions_list.append(q)

        # OTHER EXERCISES
        else:
            for i in range(self.q_nb):
                q = default_question(
                    q_kind=self.x_subkind,
                    expression_number=i + self.start_number,
                    **options)
                self.questions_list.append(q)
