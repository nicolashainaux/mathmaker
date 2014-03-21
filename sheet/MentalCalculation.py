# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

from lib.common.cst import YES

import machine
from . import exercise

from .S_Structure import S_Structure

FONT_SIZE_OFFSET = 0
SHEET_LAYOUT_TYPE = 'mental'
SHEET_LAYOUT_UNIT = "cm"
# ------------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = { 'exc' : [ None,                    'all'
                         ],
                 'ans' : [ None,                    'all'
                         ]
               }

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class MentalCalculation
# @brief This sheet is either a slideshow of Mental Calculation questions or
#        a sheet of one single exercise being a tabular of n questions.
class MentalCalculation(S_Structure):





    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param embedded_machine The machine to be used
    #   @param **options Any options
    #   @return One instance of sheet.MentalCalculation
    def __init__(self, embedded_machine, **options):
        self.derived = True
        S_Structure.__init__(self, embedded_machine, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = ""
        self.title = _("Mental calculation:")
        self.subtitle = ""
        self.text = ""
        self.answers_title = ""

        self.slideshow = False

        if 'slideshow' in options and options['slideshow'] in YES:
            self.slideshow = True



        ex = exercise.X_MentalCalculation(self.machine,
                                          x_kind='slideshow' if self.slideshow \
                                                             else 'tabular',
                                          number_of_questions=1)
        self.exercises_list.append(ex)
