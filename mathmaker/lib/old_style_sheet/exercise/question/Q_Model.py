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

# from mathmaker.lib import shared
# from mathmaker.lib import ...
# from mathmaker.lib.core.base_calculus import ...
from .Q_Structure import Q_Structure

# AVAILABLE_Q_KIND_VALUES lists so: {'q_kind1': ['q_subkind1',
#                                                  'q_subkind2',
#                                                   etc.],
#                                     'q_kind2': ...}

AVAILABLE_Q_KIND_VALUES = {'A': ['default', '1', '2'],
                           'B': ['default', '1', '2'],
                           'C': ['default', '1', '2']}


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Q_Model
# @brief Use it as a copy/paste model to create new questions.
class Q_Model(Q_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Any options
    #   @return One instance of question.Q_Model
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

        # Here you can begin to write code for the different
        # q_kinds & q_subkinds
        # if self.q_kind == '...':
        #    if self.q_subkind == '...':
        # etc.

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the text of the question as a str
    def text_to_str(self):
        # M = shared.machine
        result = ""

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        # M = shared.machine
        result = ""

        return result
