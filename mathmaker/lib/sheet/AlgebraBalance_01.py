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

FONT_SIZE_OFFSET = 0
SHEET_LAYOUT_TYPE = 'std'
SHEET_LAYOUT_UNIT = "cm"
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = {'exc': [None, 'all'],
                'ans': [None, 'all']
                }


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class AlgebraBalance_01
# @brief A complete expansion&reduction training sheet. 01 without binomials
class AlgebraBalance_01(S_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param **options Any options
    #   @return One instance of sheet.AlgebraBalance_01
    def __init__(self, **options):
        self.derived = True
        S_Structure.__init__(self, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = ""
        self.title = _("Training exercises sheet:")
        self.subtitle = _("Expanding and reducing algebraic expressions")
        self.text = ""
        self.answers_title = _("Examples of answers")

        # Exercises list:
        ex1 = exercise.X_AlgebraExpressionReduction(x_kind='short_test',
                                                    x_subkind='easy')

        ex2 = exercise.X_AlgebraExpressionExpansion(x_kind='bypass',
                                                    x_subkind='sign_expansion',
                                                    number_of_questions=4,
                                                    start_number=3)

        ex3 = exercise.X_AlgebraExpressionExpansion(x_kind='bypass',
                                                    x_subkind='any_basic_expd',
                                                    number_of_questions=5,
                                                    start_number=7)

        ex4 = exercise.X_AlgebraExpressionExpansion(x_kind='bypass',
                                                    x_subkind='sum_of_any_'
                                                              'basic_expd',
                                                    number_of_questions=3,
                                                    start_number=12)

        self.exercises_list.append(ex1)
        self.exercises_list.append(ex2)
        self.exercises_list.append(ex3)
        self.exercises_list.append(ex4)
