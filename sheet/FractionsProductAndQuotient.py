# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

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
from . import exercise

from .S_Structure import S_Structure

FONT_SIZE_OFFSET = 0
SHEET_LAYOUT_TYPE = 'std'
SHEET_LAYOUT_UNIT = "cm"
# -----------------------  lines_nb    col_widths   exercises
SHEET_LAYOUT = { 'exc': [ None,                    'all'
                         ],
                 'ans': [ None,                    1,
                           'jump',                  'next_page',
                           None,                    1
                         ]
               }

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class FractionsProductAndQuotient
# @brief Products & Quotients of Fractions
class FractionsProductAndQuotient(S_Structure):





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
        self.header = ""
        self.title = _("Training exercises sheet:")
        self.subtitle = _("Products and quotients of fractions")
        self.text = ""
        self.answers_title = _("Examples of answers")

        ex1 = exercise.X_Calculation(self.machine,
                                   x_kind='preformatted',
                                   x_subkind='fractions_product',
                                   number_of_questions=6)
        self.exercises_list.append(ex1)


        ex2 = exercise.X_Calculation(self.machine,
                                   x_kind='preformatted',
                                   x_subkind='fractions_quotient',
                                   number_of_questions=6)
        self.exercises_list.append(ex2)





    # --------------------------------------------------------------------------
    ##
    #   @brief Writes to the output all exercises' texts
    #def write_texts(self):
    #    self.machine.reset_exercises_counter()
    #    self.machine.write_set_font_size_to('large')
    #    for e in self.exercises_list:
    #        self.machine.write_exercise_number()
    #        e.write_text()
    #        #self.machine.write_new_line()



    # --------------------------------------------------------------------------
    ##
    #   @brief Writes to the output all exercises' answers
    #def write_answers(self):
    #    self.machine.reset_exercises_counter()
    #    self.machine.write_set_font_size_to('large')
    #    for i in xrange(len(self.exercises_list)):
    #        self.machine.write_exercise_number()
    #        self.exercises_list[i].write_answer()
    #        if i != len(self.exercises_list) - 1:
    #            self.machine.write_jump_to_next_page()
    #        #self.machine.write_new_line()






    # END -----------------------------------------------------------------
