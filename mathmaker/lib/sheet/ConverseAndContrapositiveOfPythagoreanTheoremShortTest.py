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
from mathmaker.lib import randomly

from .S_Structure import S_Structure

FONT_SIZE_OFFSET = 0
SHEET_LAYOUT_TYPE = 'short_test'
SHEET_LAYOUT_UNIT = "cm"
# EXAMPLE OF A SHEET NOT USING ANY LAYOUT
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = {'exc': [None, 'all'],
                'ans': [None, 'all']
                }


# ------------------------------------------------------------------------------
# CLASS: sheet.ConverseAndContrapositiveOfPythagoreanTheoremShortTest ---------
# ------------------------------------------------------------------------------
##
# @class ConverseAndContrapositiveOfPythagoreanTheoremShortTest
# @brief The short test about the converse and contrapositive of the
# @brief pythagorean theorem
class ConverseAndContrapositiveOfPythagoreanTheoremShortTest(S_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param **options Any options
    #   @return One instance of
    #   @return sheet.ConverseAndContrapositiveOfPythagoreanTheoremShortTest
    def __init__(self, **options):
        self.derived = True
        S_Structure.__init__(self, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = _("Name: .......................................")
        self.title = \
            _("Short Test: converse and contrapositive of pythagorean theorem")
        self.subtitle = ""
        self.text = ""
        self.answers_title = _("Examples of answers")

        boolean_list = [True, False]

        ex1 = exercise.X_RightTriangle(x_kind='short_test',
                                       x_subkind='contrapositive_of_'
                                                 'pythagorean_theorem',
                                       use_decimals=randomly.pop(boolean_list))

        ex2 = exercise.X_RightTriangle(x_kind='short_test',
                                       x_subkind='converse_of_pythagorean'
                                                 '_theorem',
                                       use_decimals=randomly.pop(boolean_list))

        boolean_list = [True, False]

        ex3 = exercise.X_RightTriangle(x_kind='short_test',
                                       x_subkind='converse_of_'
                                                 'pythagorean_theorem',
                                       use_decimals=randomly.pop(boolean_list))

        ex4 = exercise.X_RightTriangle(x_kind='short_test',
                                       x_subkind='contrapositive_of_'
                                                 'pythagorean_theorem',
                                       use_decimals=randomly.pop(boolean_list))

        if randomly.heads_or_tails():
            x_list = [ex1, ex2, ex3, ex4]
        else:
            x_list = [ex3, ex4, ex1, ex2]

        self.exercises_list = x_list
