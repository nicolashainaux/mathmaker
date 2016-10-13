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

from .X_Structure import X_Structure
from . import question

# Here the list of available values for the parameter x_kind='' and the
# matching x_subkind values
# Note: the bypass value allows to give the value of *x_subkind* directly to
# the matching question Constructor, bypassing the action of the present class
AVAILABLE_X_KIND_VALUES = \
    {'short_test': ['basic', 'classic', 'classic_harder', 'harder',
                    'harder_harder'],
     'preformatted': ['basic_additions', 'any_basic', 'basic_multiplications',
                      'classics', 'classic_xtwice_and_any'],
     'bypass': ['any_simple_expandable']}

X_LAYOUT_UNIT = "cm"

STD_LAYOUT_for_9_equations = {'exc': [None, 'all'],
                              'ans': [[1, 6, 6, 6], (3, 3, 3)]}

# ----------------------  lines_nb    col_widths   questions
# In each list, the first number is the number of lines (or the value '?'),
# then follow the columns widths. The tuple contains the questions per cell.
# For instance, [2, 6, 6, 6], (1, 1, 1, 1, 1, 1) means 2 lines, 3 cols (widths
# 6 cm each), then 1 question per cell.
X_LAYOUTS = {'default':
             {'exc': [None, 'all'],
              'ans': [[2, 6, 6, 6], (1, 1, 1,
                                     1, 1, 1)]},

             ('short_test', 'basic'):
             {'exc': [None, 'all'],
              'ans': [[2, 4.5, 4.5], (1, 1,
                                      1, 1)]},

             ('short_test', 'classic'):
             {'exc': [None, 'all'],
              'ans': [[1, 4.5, 4.5], (1, 1)]},

             ('short_test', 'harder'):
             {'exc': [None, 'all'],
              'ans': [[1, 6, 6], (1, 1)]},

             ('short_test', 'harder_harder'):
             {'exc': [None, 'all'],
              'ans': [[1, 7, 11], (1, 1)]},

             ('short_test', 'classic_harder'):
             {'exc': [None, 'all'],
              'ans': [[1, 5, 5, 7], (2, 1, 1)]},

             ('preformatted', 'basic_additions'): STD_LAYOUT_for_9_equations,

             ('preformatted', 'any_basic'): STD_LAYOUT_for_9_equations,

             ('preformatted', 'basic_multiplications'):
             STD_LAYOUT_for_9_equations,

             # ('preformatted', 'classic_xtwice_and_any'): EMPTY_LAYOUT,

             ('bypass', 'any_simple_expandable'):
             {'exc': [None, 'all'],
              'ans': [[1, 9, 9], (1, 1),
                      [1, 9, 9], (1, 1),
                      [1, 9, 9], (1, 1)]}}


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_Equation
# @brief All exercises related with equations resolution.
class X_Equation(X_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Options detailed below:
    #          - start_number=<integer>
    #                         (should be >= 1)
    #          - number_of_questions=<integer>
    #            /!\ only useful if you use x_kind and not preformatted
    #                         (should be >= 1)
    #          - x_kind=<string>
    #                         ...
    #                         ...
    #          - preformatted=<string>
    #            /!\ preformatted is useless with short_test
    #            /!\ number_of_questions is useless with preformatted
    #            /!\ if you use it with the x_kind option, ensure there's a
    #                preformatted possibility with this option
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #          - short_test=bool
    #            /!\ the x_kind option above can't be used along this option
    #                         'yes'
    #                         'OK'
    #                         any other value will be understood as 'no'
    #   @return One instance of exercise.Model
    def __init__(self, x_kind='default_nothing', **options):
        self.derived = True
        X_Structure.__init__(self,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        default_question = question.Q_Equation

        # FINALLY DEPRECATED:)
        # this field, which is specific to equation exercises, is used
        # in the write_answer() method from the StructureEquation class.
        # it can be changed depending on the x_kind of exercise desired.
        # should be useful as long as write_answer() is better implemented
        # to manage itself the displaying choices... maybe with the help
        # of a self.x_kind field ?
        # self.number_of_equations_per_column = 2

        # TEXTS OF THE EXERCISE
        self.text = {'exc': "",
                     'ans': ""}

        # alternate texts section
        # if self.x_kind == '...':
        # self.text = ...

        # PREFORMATTED EXERCISES
        if self.x_kind == 'short_test':
            if self.x_subkind == 'basic':
                self.questions_list.append(default_question(
                                           q_kind='basic_addition',
                                           expression_number=0))
                self.questions_list.append(default_question(
                                           q_kind='basic_addition_r',
                                           expression_number=1))
                self.questions_list.append(default_question(
                                           q_kind='basic_multiplication',
                                           expression_number=2))
                self.questions_list.append(default_question(
                                           q_kind='basic_multiplication_r',
                                           expression_number=3))
            elif self.x_subkind == 'classic':
                self.questions_list.append(default_question(
                                           q_kind='classic',
                                           expression_number=4))
                self.questions_list.append(default_question(
                                           q_kind='classic_r',
                                           expression_number=5))

            elif self.x_subkind == 'classic_harder':
                # __
                self.questions_list.append(default_question(
                                           q_kind='classic',
                                           expression_number=4))
                self.questions_list.append(default_question(
                                           q_kind='classic_r',
                                           expression_number=5))
                self.questions_list.append(default_question(
                                           q_kind='classic_x_twice',
                                           expression_number=6))
                self.questions_list.append(default_question(
                                           q_kind='classic_with_fractions',
                                           expression_number=7))

            elif self.x_subkind == 'harder':
                self.questions_list.append(default_question(
                                           q_kind='classic_x_twice',
                                           expression_number=6))
                self.questions_list.append(default_question(
                                           q_kind='any_simple_expandable',
                                           expression_number=7))

            elif self.x_subkind == 'harder_harder':
                # self.number_of_equations_per_column = 1
                self.questions_list.append(default_question(
                                           q_kind='any_simple_expandable',
                                           expression_number=8))
                self.questions_list.append(default_question(
                                           q_kind='any_double_expandable',
                                           expression_number=9))

        elif self.x_kind == 'preformatted':
            if self.x_subkind == 'basic_additions':
                # self.number_of_equations_per_column = 3
                for i in range(3):
                    self.questions_list.append(default_question(
                                               q_kind='basic_addition',
                                               expression_number=i))
                for i in range(2):
                    self.questions_list.append(default_question(
                                               q_kind='basic_addition_r',
                                               expression_number=i + 3))
                for i in range(4):
                    self.questions_list.append(default_question(
                                               q_kind='any_basic_addition',
                                               expression_number=i + 5))
            elif self.x_subkind == 'any_basic':
                # self.number_of_equations_per_column = 3
                for i in range(9):
                    self.questions_list.append(default_question(
                                               q_kind='any_basic',
                                               expression_number=i))

            elif self.x_subkind == 'basic_multiplications':
                # self.number_of_equations_per_column = 3
                for i in range(4):
                    self.questions_list.append(default_question(
                                               q_kind='basic_multiplication',
                                               expression_number=i))
                for i in range(2):
                    self.questions_list.append(default_question(
                                               q_kind='basic_multiplication_r',
                                               expression_number=i + 3))
                for i in range(3):
                    self.questions_list.append(default_question(
                        q_kind='any_basic_multiplication',
                        expression_number=i + 5))

            elif self.x_subkind == 'classics':
                for i in range(3):
                    self.questions_list.append(default_question(
                                               q_kind='classic',
                                               expression_number=i))
                for i in range(3):
                    self.questions_list.append(default_question(
                                               q_kind='classic_r',
                                               expression_number=i + 3))

            elif self.x_subkind == 'classic_xtwice_and_any':
                for i in range(3):
                    self.questions_list.append(default_question(
                                               q_kind='classic_x_twice',
                                               expression_number=i))
                for i in range(3):
                    self.questions_list.append(default_question(
                                               q_kind='any_classic',
                                               expression_number=i + 3))

        # OTHER EXERCISES
        # Take care: the displaying of the answers if
        # number_of_questions is different from 6 is not implemented yet !
        else:
            for i in range(self.q_nb):
                self.questions_list.append(
                    default_question(q_kind=self.x_subkind,
                                     expression_number=i + self.start_number,
                                     **options))
