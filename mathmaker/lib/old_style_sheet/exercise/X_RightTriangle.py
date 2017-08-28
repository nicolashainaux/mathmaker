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

import random

from .X_Structure import X_Structure
from . import question
from mathmaker.lib.constants.numeration import TENTH, HUNDREDTH

# Here the list of available values for the parameter x_kind='' and the
# matching x_subkind values
# Note: the bypass value allows to give the value of *x_subkind* directly to
# the matching question Constructor, bypassing the action of the present class
AVAILABLE_X_KIND_VALUES = \
    {'short_test': ['pythagorean_theorem_one_of_each',
                    'converse_of_pythagorean_theorem',
                    'contrapositive_of_pythagorean_theorem']
     }

X_LAYOUT_UNIT = "cm"  # [1, 9, 9], (1, 1)
# ----------------------  lines_nb    col_widths   questions
# In each list, the first number is the number of lines (or the value '?'),
# then follow the columns widths. The tuple contains the questions per cell.
# For instance, [2, 6, 6, 6], (1, 1, 1, 1, 1, 1) means 2 lines, 3 cols (widths
# 6 cm each), then 1 question per cell.
X_LAYOUTS = {'default':
             {'exc': [None, 'all'],
              'ans': [None, 'all']}
             }


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class X_RightTriangle
# @brief All exercices about the Right Triangle.
class X_RightTriangle(X_Structure):

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
    #   @return One instance of exercise.X_RightTriangle
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
        default_question = question.Q_RightTriangle

        # TEXTS OF THE EXERCISE
        self.text = {'exc': "",
                     'ans': ""
                     }

        # alternate texts section
        # if self.x_kind == 'short_test' \
        #    and self.x_subkind == 'pythagorean_theorem_one_of_each':
        #    # __
        #    self.text = {'exc': "",
        #                'ans': _("The drawings below are only sketches.")
        #                }
        #
        # elif self.x_kind == '...':
        # self.text = {'exc': "",
        #             'ans': ""
        #            }

        # SHORT TEST & OTHER PREFORMATTED EXERCISES
        units = ['m', 'dm', 'cm', 'mm']
        angles = random.choice([[0, 180], [90, 270]])
        random_signs = [random.choice([-1, 1]),
                        random.choice([-1, 1])]

        if self.x_kind == 'short_test':
            if self.x_subkind == 'pythagorean_theorem_one_of_each':
                q_subkinds = ['calculate_hypotenuse', 'calculate_one_leg']
                if random.choice([True, False]):
                    self.questions_list.append(
                        default_question(
                            q_kind='pythagorean_theorem',
                            q_subkind=random.choice(q_subkinds),
                            use_pythagorean_triples=True,
                            use_decimals=True,
                            final_unit=random.choice(units),
                            number_of_the_question='a',
                            figure_in_the_text=False,
                            rotate_around_barycenter=random.choice(angles)
                            + random_signs[0] * random.randint(0, 20)))
                    self.questions_list.append(
                        default_question(
                            q_kind='pythagorean_theorem',
                            q_subkind=random.choice(q_subkinds),
                            use_pythagorean_triples=False,
                            round_to=random.choice([TENTH,
                                                    HUNDREDTH]),
                            final_unit=random.choice(units),
                            number_of_the_question='b',
                            figure_in_the_text=False,
                            rotate_around_barycenter=random.choice(angles)
                            + random_signs[1] * random.randint(0, 20)))
                else:
                    self.questions_list.append(
                        default_question(
                            q_kind='pythagorean_theorem',
                            q_subkind=random.choice(q_subkinds),
                            use_pythagorean_triples=False,
                            round_to=random.choice([TENTH,
                                                    HUNDREDTH]),
                            final_unit=random.choice(units),
                            number_of_the_question='a',
                            figure_in_the_text=False,
                            rotate_around_barycenter=random.choice(angles)
                            + random_signs[0] * random.randint(0, 20)))

                    self.questions_list.append(
                        default_question(
                            q_kind='pythagorean_theorem',
                            q_subkind=random.choice(q_subkinds),
                            use_pythagorean_triples=True,
                            use_decimals=True,
                            final_unit=random.choice(units),
                            number_of_the_question='b',
                            figure_in_the_text=False,
                            rotate_around_barycenter=random.choice(angles)
                            + random_signs[1] * random.randint(0, 20)))

            elif self.x_subkind == 'converse_of_pythagorean_theorem':

                self.questions_list.append(
                    default_question(
                        q_kind='converse_of_pythagorean_theorem',
                        q_subkind='default',
                        use_pythagorean_triples=True,
                        final_unit=random.choice(units),
                        figure_in_the_text=False,
                        rotate_around_barycenter=random.choice(angles)
                        + random_signs[0] * random.randint(0, 20),
                        **options))

            elif self.x_subkind == 'contrapositive_of_pythagorean_theorem':
                self.questions_list.append(
                    default_question(
                        q_kind='contrapositive_of_pythagorean_theorem',
                        q_subkind='default',
                        final_unit=random.choice(units),
                        figure_in_the_text=False,
                        rotate_around_barycenter=random.choice(angles)
                        + random_signs[0] * random.randint(0, 20),
                        **options))
