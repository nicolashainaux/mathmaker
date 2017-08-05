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

# from . import exercise
from .S_Structure import S_Structure

FONT_SIZE_OFFSET = 0
SHEET_LAYOUT_TYPE = 'std|short_test|mini_test|equations|mental'
SHEET_LAYOUT_UNIT = "cm"
# EXAMPLE OF A SHEET NOT USING ANY LAYOUT
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = {'exc': [None, 'all'],
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
# @class S_Model
# @brief Use it as a copy/paste model to create new sheets.
class S_Model(S_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param **options Any options
    #   @return One instance of sheet.Model
    def __init__(self, **options):
        self.derived = True
        S_Structure.__init__(self, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = ""
        self.title = _("Training exercises sheet:")
        self.subtitle = ""
        self.text = ""
        self.answers_title = _("Examples of answers")

        # For instance:
        # ex1 = exercise.ProductReduction( many=30)
        # self.exercises_list.append(ex1)

        # END -----------------------------------------------------------------
        # Instructions for use (creating a new sheet):
        # - Put its name in the header's comment
        #   & in the one of the documentation (@class)
        # - Write the @brief comment
        # - Replace Model by the chosen name
        # - Choose the values for the globals
        # - In the constructor's comment, replace Model by the chosen name at
        #   the @return line
        # - Skip to the zone to rewrite and for each exercise, follow the
        #   example (i.e. write on two lines:
        #   - ex_number_n = exercise.ThmPythagore( options...)
        #   - self.exercises_list.append(ex_number_n)
        #   and so on with ex<n+1>, ex<n+2> as many as desired)
