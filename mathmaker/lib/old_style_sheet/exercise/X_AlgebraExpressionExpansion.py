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

from .X_Structure import X_Structure
from . import question


AVAILABLE_X_KIND_VALUES = \
    {'short_test': ['sign_expansion', 'medium_level',
                    'three_binomials', 'three_numeric_binomials',
                    'default'],
     'mini_test': ['two_randomly'],
     'bypass': ['sign_expansion', 'sum_of_any_basic_expd',
                'sum_square', 'difference_square', 'squares_difference',
                'any_binomial', 'polyn1_polyn1']}

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
        if self.x_kind == 'mini_test':
            if self.x_subkind == 'two_randomly':
                if random.choice([True, False]):
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

        # OTHER EXERCISES
        else:
            for i in range(self.q_nb):
                q = default_question(
                    q_kind=self.x_subkind,
                    expression_number=i + self.start_number,
                    **options)
                self.questions_list.append(q)
