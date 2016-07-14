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

FONT_SIZE_OFFSET = -2
SHEET_LAYOUT_TYPE = 'short_test'
SHEET_LAYOUT_UNIT = "cm"
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = {'exc': [None, 'all'],
                'ans': [None, 2,
                        'jump', 'next_page',
                        None, 1]
                }


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class EquationsTest
# @brief A short test on first degree equations
class EquationsTest(S_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param **options Any options
    #   @return One instance of sheet.EquationsTest
    def __init__(self, **options):
        self.derived = True
        S_Structure.__init__(self, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = _("Name: .......................................")
        self.title = _("Short Test: Equations")
        self.subtitle = ""
        self.text = _("Solve the following equations.")
        self.answers_title = _("Examples of answers")

        # Exercises:
        for i in range(2):
            ex1 = exercise.X_Equation(x_kind='short_test',
                                      x_subkind='basic')

            ex2 = exercise.X_Equation(x_kind='short_test',
                                      x_subkind='classic_harder')

            ex3 = exercise.X_Equation(x_kind='short_test',
                                      x_subkind='harder_harder')

            self.exercises_list.append(ex1)
            self.exercises_list.append(ex2)
            self.exercises_list.append(ex3)
