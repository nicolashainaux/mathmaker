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

from mathmaker.lib import randomly
from mathmaker.lib.core.calculus import Expression
from mathmaker.lib.common import alphabet
from .X_Structure import X_Structure
from . import question

# Here the list of available values for the parameter x_kind='' and the
# matching self.x_subkind values
# Note: the bypass value allows to give the value of *x_subkind* directly to
# the matching question Constructor, bypassing the action of the present class
AVAILABLE_X_KIND_VALUES = \
    {'short_test': ['medium_level', 'hard_level'],
     'mini_test': ['two_factorizations'],
     'preformatted': ['level_01_easy', 'level_02_easy',
                      'level_02_intermediate', 'level_03_sum_squares',
                      'level_03_difference_squares',
                      'level_03_squares_differences',
                      'level_03_some_not_factorizable',
                      'level_03_all_kinds'],
     'bypass': ['level_01']
     }

X_LAYOUT_UNIT = "cm"
ALT_DEFAULT_LAYOUT = {'exc': [None, 'all'],
                      'ans': [[2, 9, 9], (1, 1,
                                          1, 1),
                              None, 1]
                      }
# ----------------------  lines_nb    col_widths   questions
# In each list, the first number is the number of lines (or the value '?'),
# then follow the columns widths. The tuple contains the questions per cell.
# For instance, [2, 6, 6, 6], (1, 1, 1, 1, 1, 1) means 2 lines, 3 cols (widths
# 6 cm each), then 1 question per cell.
X_LAYOUTS = {'default':
             {'exc': [None, 'all'],
              'ans': [[1, 6, 6, 6], (1, 1, 1)]
              },

             ('short_test', 'hard_level'):
             {'exc': [None, 'all'],
              'ans': [[4, 9, 9], (1, 1,
                                  1, 1,
                                  1, 1,
                                  1, 1)]
              },

             ('mini_test', 'two_factorizations'):
             {'exc': [None, 'all'],
              'ans': [None, 'all']
              },

             ('preformatted', 'level_01_easy'):
             {'exc': [None, 'all'],
              'ans': [['?', 6, 6, 6], 'all']
              },

             ('preformatted', 'level_02_easy'): ALT_DEFAULT_LAYOUT,

             ('preformatted', 'level_02_intermediate'): ALT_DEFAULT_LAYOUT,

             ('preformatted', 'level_03_some_not_factorizable'):
             {'exc': [None, 'all'],
              'ans': [['?', 6, 6, 6], 'all']
              },

             ('bypass', 'level_01'):
             {'exc': [None, 'all'],
              'ans': [['?', 9, 9], 'all']
              }
             }


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_Factorization
# @brief Factorization exercises.
class X_Factorization(X_Structure):

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
    #   @todo Complete the description of the possible options !
    #   @return One instance of exercise.Factorization
    def __init__(self, x_kind='default_nothing', **options):
        self.derived = True
        X_Structure.__init__(self,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        # BEGINING OF THE ZONE TO REWRITE -------------------------------------

        default_question = question.Q_Factorization

        # TEXTS OF THE EXERCISE
        self.text = {'exc': _("Factorise: "),
                     'ans': ""
                     }

        # alternate texts section
        if self.x_kind == 'level_02_easy' \
           or self.x_kind == 'level_02_intermediate':
            self.text = {'exc': _("Factorise:"),
                         'ans': ""
                         }

        elif (self.x_kind == 'level_03_some_not_factorizable'
              or (self.x_kind, self.x_subkind)
              == ('mini_test', 'two_factorizations')):
            # __
            self.text = {'exc': _("Factorise, if possible:"),
                         'ans': ""
                         }

        # SHORT TEST & OTHER PREFORMATTED EXERCISES
        if self.x_kind == 'short_test':
            if self.x_subkind == 'easy_level':
                # NOTE: the algebra (easy) short test uses directly one
                # question and passes its arguments (x_kind...) directly
                # to question.Factorization() (see below, at the end)
                pass

            elif self.x_subkind == 'medium_level':
                lil_box = []

                lil_box.append(default_question(q_kind='level_01',
                                                q_subkind='ax² + bx',
                                                expression_number=0))

                if randomly.heads_or_tails():
                    lil_box.append(default_question(q_kind='level_01',
                                                    q_subkind='ax² + b',
                                                    expression_number=0))
                else:
                    lil_box.append(default_question(q_kind='level_01',
                                                    q_subkind='ax + b',
                                                    expression_number=0))

                lil_box.append(default_question(q_kind='level_01',
                                                q_subkind='not_factorizable',
                                                expression_number=0))

                for i in range(len(lil_box)):
                        q = randomly.pop(lil_box)
                        q.expression.name = alphabet.UPPERCASE[i]
                        for expression in q.steps:
                            expression.name = alphabet.UPPERCASE[i]
                        self.questions_list.append(q)

            elif self.x_subkind == 'hard_level':
                lil_box = []

                l03_kinds = ['sum_square_mixed',
                             'difference_square_mixed',
                             randomly.pop(['squares_difference',
                                           'squares_difference_mixed']),
                             randomly.pop(['fake_01',
                                           'fake_01_mixed',
                                           'fake_02',
                                           'fake_02_mixed',
                                           'fake_03',
                                           'fake_03_mixed']),
                             'fake_04_any_mixed']

                for n in range(len(l03_kinds)):
                    lil_box.append(default_question(
                                   q_kind='level_03',
                                   q_subkind=l03_kinds[n],
                                   expression_number=n + 1))

                l02_kinds = [('type_2_A1', False),
                             ('type_2_A0', True),
                             ('type_4_A0', False)]

                for n in range(len(l02_kinds)):
                    lil_box.append(default_question(
                                   q_kind='level_02',
                                   q_subkind=l02_kinds[n][0],
                                   max_coeff=10,
                                   minus_sign=l02_kinds[n][1],
                                   expression_number=n + len(l03_kinds) + 1))

                for i in range(len(lil_box)):
                    q = randomly.pop(lil_box)
                    q.expression.name = alphabet.UPPERCASE[i]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = alphabet.UPPERCASE[i]
                    self.questions_list.append(q)

        elif self.x_kind == 'mini_test':
            if self.x_subkind == 'two_factorizations':
                lil_box = []

                lil_box.append(default_question(
                    q_kind='level_03',
                    q_subkind=randomly.pop(['any_fake',
                                            'any_true'],
                                           weighted_table=[0.2, 0.8]),
                    expression_number=1))

                l02_kinds = [('type_2_A1', False),
                             ('type_2_A0', True),
                             ('type_4_A0', False)]

                n = randomly.pop([0, 1, 2])

                lil_box.append(default_question(q_kind='level_02',
                                                q_subkind=l02_kinds[n][0],
                                                max_coeff=10,
                                                minus_sign=l02_kinds[n][1],
                                                expression_number=2))

                for i in range(len(lil_box)):
                    q = randomly.pop(lil_box)
                    q.expression.name = \
                        alphabet.UPPERCASE[i + self.start_number]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = \
                                alphabet.UPPERCASE[i + self.start_number]
                    self.questions_list.append(q)

        elif self.x_kind == 'preformatted':
            if self.x_subkind == 'level_01_easy':
                # n is the number of questions still left to do
                n = 10
                lil_box = []

                lil_box.append(default_question(
                               q_kind='level_01',
                               q_subkind='ax² + bx',
                               expression_number=10 - n))

                n -= 1

                if randomly.heads_or_tails():
                    lil_box.append(default_question(q_kind='level_01',
                                                    q_subkind='ax² + bx',
                                                    expression_number=10 - n))

                    n -= 1

                lil_box.append(default_question(
                               q_kind='level_01',
                               q_subkind='ax² + b',
                               expression_number=10 - n))

                n -= 1

                if randomly.heads_or_tails():
                    lil_box.append(default_question(
                                   q_kind='level_01',
                                   q_subkind='ax² + b',
                                   expression_number=10 - n))

                    n -= 1

                if randomly.heads_or_tails():
                    lil_box.append(default_question(
                                   q_kind='level_01',
                                   q_subkind='ax² + b',
                                   expression_number=10 - n))

                    n -= 1

                for i in range(n):
                    lil_box.append(default_question(
                                   q_kind='level_01',
                                   q_subkind='ax + b',
                                   expression_number=n - i))

                for i in range(len(lil_box)):
                    q = randomly.pop(lil_box)
                    q.expression.name = alphabet.UPPERCASE[i]
                    for expression in q.steps:
                        expression.name = alphabet.UPPERCASE[i]
                    self.questions_list.append(q)

            elif self.x_subkind == 'level_02_easy':
                subkinds = ['type_1_A0',
                            'type_1_D0',
                            'type_1_G0']

                n1 = len(subkinds)

                for i in range(n1):
                    self.questions_list.append(
                        default_question(q_kind='level_02',
                                         q_subkind=randomly.pop(subkinds),
                                         minus_sign=False,
                                         expression_number=i))

                subkinds = ['type_2_A0',
                            'type_2_D0']

                n2 = len(subkinds)

                for i in range(n2):
                    self.questions_list.append(
                        default_question(q_kind='level_02',
                                         q_subkind=randomly.pop(subkinds),
                                         minus_sign=False,
                                         expression_number=i + n1))

            elif self.x_subkind == 'level_02_intermediate':
                subkinds = ['type_1_D',
                            'type_1_G0',
                            'type_1_1']

                n1 = len(subkinds)

                for i in range(n1):
                    self.questions_list.append(
                        default_question(q_kind='level_02',
                                         q_subkind=randomly.pop(subkinds),
                                         minus_sign=False,
                                         expression_number=i))

                subkinds = randomly.pop([['type_2_A0', 'type_2_D1'],
                                         ['type_2_A1', 'type_2_D0']])

                n2 = len(subkinds)

                for i in range(n2):
                    self.questions_list.append(
                        default_question(q_kind='level_02',
                                         q_subkind=randomly.pop(subkinds),
                                         minus_sign=False,
                                         expression_number=i + n1))

            elif self.x_subkind == 'level_03_sum_squares':
                lil_box = []

                for n in range(2):
                    lil_box.append(default_question(
                                   q_kind='level_03',
                                   q_subkind='sum_square',
                                   expression_number=n + 1))

                lil_box.append(default_question(q_kind='level_03',
                                                q_subkind='sum_square_mixed',
                                                expression_number=n + 1))

                for i in range(len(lil_box)):
                    q = lil_box[i]
                    q.expression.name = alphabet.UPPERCASE[i]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = alphabet.UPPERCASE[i]
                    self.questions_list.append(q)

            elif self.x_subkind == 'level_03_difference_squares':
                lil_box = []

                for n in range(2):
                    lil_box.append(default_question(
                                   q_kind='level_03',
                                   q_subkind='difference_square',
                                   expression_number=n + 1))

                lil_box.append(default_question(q_kind='level_03',
                                                subkind='difference_square'
                                                        '_mixed',
                                                expression_number=n + 1))

                for i in range(len(lil_box)):
                    q = lil_box[i]
                    q.expression.name = alphabet.UPPERCASE[i]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = alphabet.UPPERCASE[i]
                    self.questions_list.append(q)

            elif self.x_subkind == 'level_03_squares_differences':
                lil_box = []

                for n in range(2):
                    lil_box.append(default_question(
                                   q_kind='level_03',
                                   q_subkind='squares_difference',
                                   expression_number=n + 1))

                lil_box.append(default_question(
                               q_kind='level_03',
                               q_subkind='squares_difference_mixed',
                               expression_number=n + 1))

                for i in range(len(lil_box)):
                    q = lil_box[i]
                    q.expression.name = alphabet.UPPERCASE[i]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = alphabet.UPPERCASE[i]
                    self.questions_list.append(q)

            elif self.x_subkind == 'level_03_some_not_factorizable':
                lil_box = []

                q1 = default_question(q_kind='level_03',
                                      q_subkind='any_true_mixed',
                                      expression_number=1)

                q2 = default_question(q_kind='level_03',
                                      q_subkind='any_fake_straight',
                                      expression_number=2)

                q1q2 = [q1, q2]

                lil_box.append(randomly.pop(q1q2))
                lil_box.append(randomly.pop(q1q2))

                for n in range(3):
                    lil_box.append(default_question(q_kind='level_03',
                                                    q_subkind='any_true',
                                                    expression_number=n + 3))

                for n in range(2):
                    lil_box.append(default_question(q_kind='level_03',
                                                    q_subkind='any_fake',
                                                    expression_number=n + 5))

                for n in range(2):
                    lil_box.append(default_question(q_kind='level_03',
                                                    q_subkind='any',
                                                    expression_number=n + 7))

                for i in range(len(lil_box)):
                    q = lil_box[i]
                    q.expression.name = alphabet.UPPERCASE[i]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = alphabet.UPPERCASE[i]
                    self.questions_list.append(q)

            elif self.x_subkind == 'level_03_all_kinds':
                all_kinds = ['sum_square',
                             'sum_square_mixed',
                             'difference_square',
                             'difference_square_mixed',
                             'squares_difference',
                             'squares_difference_mixed',
                             'fake_01',
                             'fake_01_mixed',
                             'fake_02',
                             'fake_02_mixed',
                             'fake_03',
                             'fake_03_mixed',
                             'fake_04_A',
                             'fake_04_A_mixed',
                             'fake_04_B',
                             'fake_04_B_mixed',
                             'fake_04_C',
                             'fake_04_C_mixed',
                             'fake_04_D',
                             'fake_04_D_mixed']

                lil_box = []

                for n in range(len(all_kinds)):
                    lil_box.append(default_question(
                                   q_kind='level_03',
                                   q_subkind=all_kinds[n],
                                   expression_number=n + 1))

                for i in range(len(lil_box)):
                    q = lil_box[i]
                    q.expression.name = alphabet.UPPERCASE[i]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = alphabet.UPPERCASE[i]
                    self.questions_list.append(q)

        # OTHER EXERCISES (BY_PASS OPTION)
        else:
            for i in range(self.q_nb):
                self.questions_list.append(
                    default_question(expression_number=i + self.start_number,
                                     q_kind=self.x_subkind,
                                     **options))
