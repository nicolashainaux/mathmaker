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
SHEET_LAYOUT_TYPE = 'short_test'
SHEET_LAYOUT_UNIT = "cm"
# EXAMPLE OF A SHEET NOT USING ANY LAYOUT
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = {'exc': [None, 'all'],
                'ans': [None, 'all']
                }


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class PythagoreanTheoremShortTest
# @brief The short test about the pythagorean theorem
class PythagoreanTheoremShortTest(S_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param **options Any options
    #   @return One instance of sheet.PythagoreanTheoremShortTest
    def __init__(self, **options):
        self.derived = True
        S_Structure.__init__(self, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE, write_texts_twice=True)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = _("Name: .......................................")
        self.title = _("Short Test: pythagorean theorem")
        self.subtitle = ""
        self.text = ""
        self.answers_title = _("Examples of answers")

        for i in range(2):
            ex1 = exercise.X_RightTriangle(x_kind='short_test',
                                           x_subkind='pythagorean_theorem_'
                                                     'one_of_each')

            self.exercises_list.append(ex1)
