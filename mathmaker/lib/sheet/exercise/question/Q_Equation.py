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

from mathmaker.lib.common.cst import RANDOMLY
from mathmaker.lib import shared
from mathmaker.lib.core.calculus import Equation
from .Q_Structure import Q_Structure

AVAILABLE_Q_KIND_VALUES = {'any_basic': ['default'],
                           'basic_addition': ['default'],
                           'basic_addition_r': ['default'],
                           'any_basic_addition': ['default'],
                           'basic_multiplication': ['default'],
                           'basic_multiplication_r': ['default'],
                           'any_basic_multiplication': ['default'],
                           'any_classic': ['default'],
                           'classic': ['default'],
                           'classic_r': ['default'],
                           'classic_with_fractions': ['default'],
                           'classic_x_twice': ['default'],
                           'any_simple_expandable': ['default'],
                           'any_double_expandable': ['default']}


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Q_Equation
# @brief All questions about Equations (first degree, one unknown variable)
class Q_Equation(Q_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Any options
    #   @return One instance of question.Q_Equation
    def __init__(self, q_kind='default_nothing', **options):
        self.derived = True

        # The call to the mother class __init__() method will set the
        # fields matching optional arguments which are so far:
        # self.q_kind, self.q_subkind
        # plus self.options (modified)
        Q_Structure.__init__(self,
                             q_kind, AVAILABLE_Q_KIND_VALUES,
                             **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        # That's the number of the question, not of the expressions it might
        # contain !
        self.number = ""
        # if 'number_of_questions' in options:
        #    self.number = options['number_of_questions']

        self.equation = Equation((RANDOMLY, q_kind))

        if 'expression_number' in options:
            self.equation.set_number(options['expression_number'])

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the text of the question as a str
    def text_to_str(self):
        M = shared.machine

        result = M.write_math_style2(M.type_string(self.equation,
                                                   display_name='OK'))
        result += M.write_new_line()

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        M = shared.machine

        return M.write(self.equation.auto_resolution())
