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

FONT_SIZE_OFFSET = -1
SHEET_LAYOUT_TYPE = 'short_test'
SHEET_LAYOUT_UNIT = "cm"
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = { 'exc' : [ None,                    'all'
                         ],
                 'ans' : [ [1,         9, 9],        (1, 1),
                           None,                    1
                         ]
               }

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class EquationsShortTest
# @brief A short test on first degree equations
class EquationsShortTest(S_Structure):





    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param embedded_machine The machine to be used
    #   @param **options Any options
    #   @return One instance of sheet.Model
    def __init__(self, embedded_machine, **options):
        self.derived = True
        S_Structure.__init__(self, embedded_machine, FONT_SIZE_OFFSET,
                             SHEET_LAYOUT_UNIT, SHEET_LAYOUT,
                             SHEET_LAYOUT_TYPE)

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------
        self.header = _("Name : .......................................")
        self.title = _("Short Test : Equations")
        self.subtitle = ""
        self.text = _("Solve the following equations.")
        self.answers_title = _("Examples of answers")

        # Exercises :
        for i in xrange(2):
            ex1 = exercise.X_Equation(self.machine,
                                      x_kind='short_test',
                                      x_subkind='basic')

            ex2 = exercise.X_Equation(self.machine,
                                      x_kind='short_test',
                                      x_subkind='classic')

            ex3 = exercise.X_Equation(self.machine,
                                      x_kind='short_test',
                                      x_subkind='harder')

            self.exercises_list.append(ex1)
            self.exercises_list.append(ex2)
            self.exercises_list.append(ex3)




    # --------------------------------------------------------------------------
    ##
    #   @brief Writes to the output all exercises' answers
    #def write_answers(self, first_and_last):
    #    first = first_and_last[0]
    #    last = first_and_last[1]

    #    self.machine.reset_exercises_counter()
    #    self.machine.write_set_font_size_to('large')

    #    self.machine.write_exercise_number()
    #    self.exercises_list[first].write_answer()
    #    self.machine.write_new_line()

    #    self.machine.write_tabular_begins("p{9 cm} p{9 cm}")

    #    self.machine.write_exercise_number()
    #    self.exercises_list[first+1].write_answer()

    #    self.machine.write_separator_tabular_columns()

    #    self.machine.write_exercise_number()
    #    self.exercises_list[first+2].write_answer()

    #    self.machine.write_tabular_ends()





    # END ---------------------------------------------------------------------
