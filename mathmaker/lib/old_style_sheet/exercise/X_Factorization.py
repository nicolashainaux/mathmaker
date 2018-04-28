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
from string import ascii_uppercase as alphabet

from mathmaker.lib.core.calculus import Expression
from .X_Structure import X_Structure
from . import question

# Here the list of available values for the parameter x_kind='' and the
# matching self.x_subkind values
# Note: the bypass value allows to give the value of *x_subkind* directly to
# the matching question Constructor, bypassing the action of the present class
AVAILABLE_X_KIND_VALUES = \
    {'preformatted': ['level_01_easy',
                      'level_03_sum_squares',
                      'level_03_difference_squares',
                      'level_03_squares_differences',
                      'level_03_some_not_factorizable'],
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

             ('preformatted', 'level_01_easy'):
             {'exc': [None, 'all'],
              'ans': [['?', 6, 6, 6], 'all']
              },

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
        if self.x_kind == 'level_03_some_not_factorizable':
            # __
            self.text = {'exc': _("Factorise, if possible:"),
                         'ans': ""
                         }

        # PREFORMATTED EXERCISES
        if self.x_kind == 'preformatted':
            if self.x_subkind == 'level_01_easy':
                # n is the number of questions still left to do
                n = 10
                lil_box = []

                lil_box.append(default_question(
                               q_kind='level_01',
                               q_subkind='ax² + bx',
                               expression_number=10 - n))

                n -= 1

                if random.choice([True, False]):
                    lil_box.append(default_question(q_kind='level_01',
                                                    q_subkind='ax² + bx',
                                                    expression_number=10 - n))

                    n -= 1

                lil_box.append(default_question(
                               q_kind='level_01',
                               q_subkind='ax² + b',
                               expression_number=10 - n))

                n -= 1

                if random.choice([True, False]):
                    lil_box.append(default_question(
                                   q_kind='level_01',
                                   q_subkind='ax² + b',
                                   expression_number=10 - n))

                    n -= 1

                if random.choice([True, False]):
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

                random.shuffle(lil_box)
                for i in range(len(lil_box)):
                    q = lil_box.pop()
                    q.expression.name = alphabet[i]
                    for expression in q.steps:
                        expression.name = alphabet[i]
                    self.questions_list.append(q)

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
                    q.expression.name = alphabet[i]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = alphabet[i]
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
                    q.expression.name = alphabet[i]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = alphabet[i]
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
                    q.expression.name = alphabet[i]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = alphabet[i]
                    self.questions_list.append(q)

            elif self.x_subkind == 'level_03_some_not_factorizable':
                q1 = default_question(q_kind='level_03',
                                      q_subkind='any_true_mixed',
                                      expression_number=1)

                q2 = default_question(q_kind='level_03',
                                      q_subkind='any_fake_straight',
                                      expression_number=2)

                lil_box = [q1, q2]
                random.shuffle(lil_box)

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
                    q.expression.name = alphabet[i]
                    for expression in q.steps:
                        if isinstance(expression, Expression):
                            expression.name = alphabet[i]
                    self.questions_list.append(q)

        # OTHER EXERCISES (BY_PASS OPTION)
        else:
            for i in range(self.q_nb):
                self.questions_list.append(
                    default_question(expression_number=i + self.start_number,
                                     q_kind=self.x_subkind,
                                     **options))
