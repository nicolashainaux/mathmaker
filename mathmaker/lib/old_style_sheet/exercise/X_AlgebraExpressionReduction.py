# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

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

from .X_Structure import X_Structure
from . import question

AVAILABLE_X_KIND_VALUES = {'preformatted': ['product'],
                           'bypass': ['sum', 'sum_of_products']}

X_LAYOUT_UNIT = "cm"
# ----------------------  lines_nb    col_widths   questions
# In each list, the first number is the number of lines (or the value '?'),
# then follow the columns widths. The tuple contains the questions per cell.
# For instance, [2, 6, 6, 6], (1, 1, 1, 1, 1, 1) means 2 lines, 3 cols (widths
# 6 cm each), then 1 question per cell.
X_LAYOUTS = {'default':
             {'exc': [None, 'all'],
              'ans': [None, 'all']}}


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_AlgebraExpressionReduction
# @brief This new exercise object should include all possible
# reduction exercises
class X_AlgebraExpressionReduction(X_Structure):

    def __init__(self, x_kind='default_nothing', **options):
        self.derived = True
        X_Structure.__init__(self,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        default_question = question.Q_AlgebraExpressionReduction

        # TEXTS OF THE EXERCISES
        self.text = {'exc': _("Reduce the following expressions:"),
                     'ans': ""}

        # alternate texts section
        if self.x_subkind == 'product':
            self.text = {'exc': _("Reduce, if possible, the following "
                                  "products:"),
                         'ans': _("Pay attention that the intermediate "
                                  "line is optional.")}

        # elif self.x_subkind == 'sum_of_products':
        #    self.text = _("Reduce the following expressions:")

        elif self.x_subkind == 'sum':
            self.text = {'exc': _("Reduce, if possible, the following sums:"),
                         'ans': _("Pay attention that the intermediate line "
                                  "is optional.")}

        # PREFORMATTED EXERCISES
        if self.x_kind == 'preformatted':
            if self.x_subkind == 'product':
                self.questions_list.append(default_question(
                                           q_kind='product',
                                           expression_number=0,
                                           use_these_letters=['a', 'b'],
                                           nb_occurences_of_the_same_letter=1,
                                           **options))

                self.questions_list.append(default_question(
                                           q_kind='product',
                                           expression_number=1,
                                           use_these_letters=['x', 'y'],
                                           nb_occurences_of_the_same_letter=1,
                                           **options))

                self.questions_list.append(default_question(
                                           q_kind='product',
                                           expression_number=2,
                                           use_these_letters=['t', 'u'],
                                           nb_occurences_of_the_same_letter=1,
                                           **options))

                self.questions_list.append(default_question(
                                           q_kind='product',
                                           expression_number=3,
                                           use_these_letters=['x', 'y', 'z'],
                                           nb_occurences_of_the_same_letter=1,
                                           **options))

                self.questions_list.append(default_question(
                                           q_kind='product',
                                           expression_number=4,
                                           use_these_letters=['p', 'q', 'r'],
                                           **options))

                self.questions_list.append(default_question(
                                           q_kind='product',
                                           expression_number=5,
                                           use_these_letters=['a', 'b', 'x'],
                                           nb_occurences_of_the_same_letter=1,
                                           **options))

                self.questions_list.append(default_question(
                                           q_kind='product',
                                           expression_number=6,
                                           use_reduced_alphabet='OK',
                                           nb_occurences_of_the_same_letter=1,
                                           **options))

                self.questions_list.append(default_question(
                                           q_kind='product',
                                           expression_number=7,
                                           use_these_letters=['a', 'b', 'x'],
                                           nb_occurences_of_the_same_letter=1,
                                           **options))

                self.questions_list.append(default_question(
                                           q_kind='product',
                                           expression_number=8,
                                           use_these_letters=['x', 'y'],
                                           nb_occurences_of_the_same_letter=1,
                                           **options))

        # OTHER EXERCISES (BYPASS OPTION)
        else:
            for i in range(self.q_nb):
                self.questions_list.append(
                    default_question(q_kind=self.x_subkind,
                                     expression_number=i + self.start_number,
                                     **options))
