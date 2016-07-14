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
SHEET_LAYOUT_TYPE = 'mini_test'
SHEET_LAYOUT_UNIT = "cm"
# EXAMPLE OF A SHEET NOT USING ANY LAYOUT
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = {'exc': [[1, 9, 9], (1, 1)],
                'ans': [None, 'all']
                }
# ANOTHER EXAMPLE
# ------------------------  lines_nb    col_widths   exercises
# SHEET_LAYOUT = {'exc': [[1, 6, 15], (1, 1),
#                            None, 1
#                         ],
#                'ans': [[1, 6.5, 12], (1, 1),
#                            'jump',   'next_page',
#                            None, 1
#                         ]
#                }
# NOTE THAT FOR SHORT_TEST SHEETS, THE LAYOUT HAS TO BE GIVEN ONLY ONCE
# AND IT WILL BE DUPLICATED FOR THE SECOND SET OF EXERCISES

# EXPLANATION ABOUT THE EXAMPLE OF SHEET_LAYOUT:
# [1, 6, 15] means a table of 1 line with columns widths 6 and 15.
# (1, 1) means one exercise in each of these two cells.
# This tuple should contains as many numbers as nb of lines × nb of cols.
# To leave one cell empty, just write 0.
# None means no tabular and the following 1 means for the 1 next exercise.
# 'all' and 'all_left' are synonym
# 'jump' and 'next_page' will include a jump to next page before the next ones


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class AlgebraMiniTest1
# @brief One expansion (randomly but sum of 2 expandables) + 2 factorizations
class AlgebraMiniTest1(S_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param **options Any options
    #   @return One instance of sheet.AlgebraMiniTest1
    def __init__(self, **options):
        self.derived = True
        S_Structure.__init__(self, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = _("Name: ....................... Class: ...........")
        self.title = _("Mini Test: Algebra")
        self.subtitle = ""
        self.text = ""
        self.answers_title = _("Examples of answers")

        for i in range(2):
            ex1 = exercise.X_AlgebraExpressionExpansion(x_kind='mini_test',
                                                        x_subkind='two_'
                                                                  'expansions_'
                                                                  'hard')
            self.exercises_list.append(ex1)

            ex2 = exercise.X_Factorization(x_kind='mini_test',
                                           x_subkind='two_factorizations',
                                           start_number=2)
            self.exercises_list.append(ex2)
