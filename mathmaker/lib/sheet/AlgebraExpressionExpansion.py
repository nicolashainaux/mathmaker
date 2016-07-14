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
                'ans': [[1, 7.5, 10.5], (1, 1)]
                }


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class AlgebraExpressionExpansion
# @brief One exercise with 3x(2-7x) & 5(3+x) objects, another with (2+x)(3-x)
class AlgebraExpressionExpansion(S_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param **options Any options
    #   @return One instance of sheet.ExpressionExpansion
    def __init__(self, **options):
        self.derived = True
        S_Structure.__init__(self, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = ""
        self.title = _("Training exercises sheet:")
        self.subtitle = _("Expand an algebraic expression")
        self.text = ""
        self.answers_title = _("Examples of answers")
        ex1 = exercise.X_AlgebraExpressionExpansion(x_kind='preformatted',
                                                    x_subkind='mixed_monom'
                                                              '_polyn1',
                                                    ratio_mmp=0.4,
                                                    number_of_questions=5,
                                                    randomly_reversed=0.25)
        ex2 = exercise.X_AlgebraExpressionExpansion(x_kind='bypass',
                                                    x_subkind='polyn1_polyn1',
                                                    number_of_questions=5)
        self.exercises_list.append(ex1)
        self.exercises_list.append(ex2)
