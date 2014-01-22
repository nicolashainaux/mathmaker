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

import machine
import exercise

from S_Structure import S_Structure

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
# @brief This is a sheet for the teacher to make oral mental calculation tests
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
        self.title = _("Mental calculation :")
        self.subtitle = ""
        self.text = ""
        self.answers_title = ""

        for i in xrange(8):
            ex = exercise.X_MentalCalculation(self.machine,
                                            x_kind='bypass',
                                            x_subkind='5m_3rm_2d_2-9',
                                            number_of_questions=1)
            self.exercises_list.append(ex)

        #for i in xrange(3):
        #    ex = exercise.X_MentalCalculation(self.machine,
        #                                    preformatted='yes',
        #                                    x_kind='5m_3rm_2d_2-9')
        #    self.exercises_list.append(ex)
