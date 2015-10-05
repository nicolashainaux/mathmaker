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
from lib.common import default

import machine
from . import exercise

from .S_Structure import S_Structure
from .S_Structure import get_sheet_config

# ------------------------  lines_nb    col_widths   exercises
#SHEET_LAYOUT = { 'exc' : [ None,                    'all'
#                         ],
#                 'ans' : [ None,                    'all'
#                         ]
#               }

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
        mc_mm_file = options['filename'] if 'filename' in options \
                                         else default.MC_MM_FILE
        (header,
         title,
         subtitle,
         text,
         answers_title,
         sheet_layout_type,
         font_size_offset,
         sheet_layout_unit,
         sheet_layout) = get_sheet_config(mc_mm_file)

        S_Structure.__init__(self, embedded_machine, font_size_offset,
                             sheet_layout_unit, sheet_layout,
                             sheet_layout_type, **options)

        self.header = _(header) if header != "" else ""
        self.title = _(title) if title != "" else ""
        self.subtitle = _(subtitle) if subtitle != "" else ""
        self.text = _(text) if text != "" else ""
        self.answers_title = _(answers_title) if answers_title != "" else ""

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        ex = exercise.X_MentalCalculation(self.machine, **options)
        self.exercises_list.append(ex)
