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


from . import exercise
from .S_Structure import S_Structure

FONT_SIZE_OFFSET = -1
SHEET_LAYOUT_TYPE = 'std'
SHEET_LAYOUT_UNIT = "cm"
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = {'exc': [None, 'all'],
                'ans': [[1, 9, 9], (1, 1),
                        'jump', 'next_page',
                        None, 'all_left']
                }


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class AlgebraExpressionReduction
# @brief Reduce a Product, a Sum, a Sum of Products
class AlgebraExpressionReduction(S_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param **options Any options
    #   @return One instance of exercise.ExpressionReduction
    def __init__(self, **options):
        self.derived = True
        S_Structure.__init__(self, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING REWRITTEN ZONE ---------------------------------------------
        self.header = ""
        self.title = _("Training exercises sheet:")
        self.subtitle = _("Reduce an algebraic expression")
        self.text = ""
        self.answers_title = _("Examples of answers")

        ex1 = exercise.X_AlgebraExpressionReduction(x_kind='preformatted',
                                                    x_subkind='product')

        ex2 = exercise.X_AlgebraExpressionReduction(x_kind='bypass',
                                                    x_subkind='sum',
                                                    number_of_questions=10)

        ex3 = exercise.X_AlgebraExpressionReduction(x_kind='bypass',
                                                    x_subkind='sum_of_'
                                                              'products',
                                                    number_of_questions=10)

        self.exercises_list.append(ex1)
        self.exercises_list.append(ex2)
        self.exercises_list.append(ex3)
