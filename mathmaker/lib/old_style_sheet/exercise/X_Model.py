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

# from mathmaker.lib import ...
from .X_Structure import X_Structure

# Here the list of available values for the parameter x_kind='' and the
# matching x_subkind values
# Note: the bypass value allows to give the value of *x_subkind* directly to
# the matching question Constructor, bypassing the action of the present class
AVAILABLE_X_KIND_VALUES = \
    {'short_test': ['x_subkind1', 'x_subkind2'],
     'preformatted': [''],
     'bypass': ['']
     }

X_LAYOUT_UNIT = "cm"
# ----------------------  lines_nb    col_widths   questions
# In each list, the first number is the number of lines (or the value '?'),
# then follow the columns widths. The tuple contains the questions per cell.
# For instance, [2, 6, 6, 6], (1, 1, 1, 1, 1, 1) means 2 lines, 3 cols (widths
# 6 cm each), then 1 question per cell.
X_LAYOUTS = {'default':
             {'exc': [None, 'all'],
              'ans': [None, 'all']
              },

             ('short_test', 'x_subkind1'):
             {'exc': [[1, 6, 15], (1, 1),
                      None, 1],
              'ans': [[1, 6.5, 12], (1, 1),
                      None, 1]
              },

             ('short_test', 'x_subkind2'):
             {'exc': [['?', 6, 15], 'all'],
              'ans': [[1, 6.5, 12], (1, 1),
                      None, 1]
              }
             }


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_Model
# @brief Use it as a copy/paste model to create new exercises.
class X_Model(X_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #          - x_kind=<string>
    #                         see AVAILABLE_X_KIND_VALUES to check the
    #                         possible values to use and their matching
    #                         x_subkind options
    #   @param **options Options detailed below:
    #          - x_subkind=<string>
    #                         ...
    #                         ...
    #          - start_number=<integer>
    #                         (should be >= 1)
    #          - number_of_questions=<integer>
    #            /!\ probably only useful if you use bypass
    #                         (should be >= 1)
    #   @return One instance of exercise.Model
    def __init__(self, x_kind='default_nothing', **options):
        self.derived = True
        X_Structure.__init__(self,
                             x_kind, AVAILABLE_X_KIND_VALUES, X_LAYOUTS,
                             X_LAYOUT_UNIT, **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        # BEGINING OF THE ZONE TO REWRITE (see explanations below) ------------

        # should be default_question = question.Something
        # default_question = None

        # TEXTS OF THE EXERCISE
        self.text = {'exc': "",
                     'ans': ""
                     }

        # alternate texts section
        # if self.x_kind == '...':
        # self.text = {'exc': "",
        #             'ans': ""
        #            }
        #
        # elif self.x_kind == '...':
        # self.text = {'exc': "",
        #             'ans': ""
        #            }

        # SHORT TEST & OTHER PREFORMATTED EXERCISES
        # if self.x_kind == 'short_test':
        #   if self.x_subkind == 'sub1':
        #       self.questions_list.append(default_question(
        #                                       q_kind='product',
        #                                       expression_number=0)
        #                           )
        # etc.
        # elif self.x_kind == 'preformatted':
        #    if self.x_subkind == '...':
        # self.questions_list.append(default_question(
        #
        # etc.

        # OTHER EXERCISES (BYPASS OPTION !)
        # else:
        #   for i in xrange(self.q_nb):
        #       self.questions_list.append(
        #                    default_question(
        #                              q_kind=self.x_subkind,
        #                               expression_number=i+self.start_number,
        #                               **options)
        #                                 )

        # END OF THE ZONE TO REWRITE ------------------------------------------

    # INSTRUCTIONS TO CREATE A NEW EXERCISE -----------------------------------
    # - Indicate its name in the header comment
    #   the one of documentation (@class)
    # - Write the @brief description
    # - Replace the Model class name by the chosen one
    # - In the constructor comment, replace Model with the chosen name
    #   at the @return line
    # - Write the class name of the default_question. You must mention it
    #   because it will be used in the OTHER EXERCISES section.
    # - The different sections to rewrite are:
    #   * TEXTS OF THE EXERCISE:
    #       default text for all exercises of this class
    #   * alternate texts section:
    #       if you want to specify a different text for any particular kind
    #       of exercise
    #   * PREFORMATTED EXERCISES
    #       that's where preformatted exercises are described (the ones that
    #       won't repeat n times the same kind of randomly question)
    #   * OTHER EXERCISES section is meant to all exercises that repeat
    #       the same (maybe randomly chosen among many) kind of question.
    #       shouldn't be rewritten
    # - Finally, if the write_* methods from the exercise.Structure don't
    #   match your needs, copy & modify or rewrite them
