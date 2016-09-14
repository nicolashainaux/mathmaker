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

from mathmaker.lib import shared
from .Q_Structure import Q_Structure
from . import algebra_modules, mc_modules


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Q_Generic
# @brief Creates one 'generic' question
class Q_Generic(Q_Structure):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Any options
    #   @return One instance of question.Q_Generic
    def __init__(self, q_kind, q_options, **options):

        self.derived = True

        options.update(q_options)

        # The call to the mother class __init__() method will set the
        # fields matching optional arguments which are so far:
        # self.q_kind, self.q_subkind
        # plus self.options (modified)
        Q_Structure.__init__(self, q_kind, None,
                             q_subkind='bypass', **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options

        numbers_to_use = options['numbers_to_use']
        del options['numbers_to_use']

        # modules
        try:
            module = getattr(mc_modules, self.q_kind)
        except AttributeError:
            module = getattr(algebra_modules, self.q_kind)
        m = module.sub_object(numbers_to_use, **options)

        self.q_text = m.q(**options)
        self.q_answer = m.a(**options)
        if hasattr(m, 'h'):
            self.q_hint = m.h(**options)
        else:
            self.q_hint = ""

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the text of the question as a str
    def text_to_str(self):
        return self.q_text + shared.machine.write_new_line()

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        return self.q_answer

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def hint_to_str(self):
        return self.q_hint
