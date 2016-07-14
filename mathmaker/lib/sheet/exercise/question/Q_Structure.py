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
from mathmaker.lib import error


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Q_Structure
# @brief Contains the method to be reimplemented by any question.*
class Q_Structure(object):

    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined. Constructor.
    #   @warning Exception NotInstanciableObject.
    #   @param **options Any options
    def __init__(self, q_kind, AVAILABLE_Q_KIND_VALUES,
                 **options):
        try:
            self.derived
        except AttributeError:
            raise error.NotInstanciableObject(self)

        # OPTIONS -------------------------------------------------------------
        # It is necessary to define an options field to pass the
        # possibly modified value to the child class
        self.options = options

        # That's the number of the question, not of the expressions it might
        # contain !
        self.number = ""
        if 'number_of_the_question' in options:
            self.number = options['number_of_the_question']

        q_kind_id = q_kind
        q_context = ""
        if 'context' in options:
            q_context = options['context']

        if AVAILABLE_Q_KIND_VALUES is not None:
            try:
                AVAILABLE_Q_KIND_VALUES[q_kind]
            except KeyError:
                if q_context == "":
                    raise KeyError('The given question kind (' + q_kind
                                   + ') does not belong to the available '
                                   'questions kinds: '
                                   + str(AVAILABLE_Q_KIND_VALUES))
                else:
                    try:
                        AVAILABLE_Q_KIND_VALUES[q_kind + "_" + q_context]
                        q_kind_id = q_kind + "_" + q_context
                    except KeyError:
                        raise KeyError('The give question_context kind ('
                                       + q_kind + "_" + q_context
                                       + ') does not belong to the available '
                                       'questions kinds: '
                                       + str(AVAILABLE_Q_KIND_VALUES))

        self.displayable_number = ""

        if self.number != "":
            self.displayable_number = \
                shared.machine.write(str(self.number) + ". ", emphasize='bold')

        q_subkind = 'default'
        if 'q_subkind' in options:
            q_subkind = options['q_subkind']
            # let's remove this option from the options
            # since we re-use it recursively
            temp_options = dict()
            for key in options:
                if key != 'q_subkind':
                    temp_options[key] = options[key]
            self.options = temp_options

        if AVAILABLE_Q_KIND_VALUES is not None:
            if q_subkind not in AVAILABLE_Q_KIND_VALUES[q_kind_id]:
                raise KeyError('The question subkinds (' + q_subkind
                               + ') does not belong to available question '
                               'subkinds: '
                               + str(AVAILABLE_Q_KIND_VALUES[q_kind_id]))

        # these two fields for the case of needing to know the them in the
        # answer_to_str() especially
        self.q_kind = q_kind
        self.q_subkind = q_subkind

    # --------------------------------------------------------------------------
    ##
    #   Redirects to text_to_str() or answer_to_str()
    def to_str(self, ex_or_answers):
        if ex_or_answers == 'exc':
            return self.text_to_str()

        elif ex_or_answers == 'ans':
            return self.answer_to_str()

        elif ex_or_answers == 'hint':
            return self.hint_to_str()

        else:
            raise error.OutOfRangeArgument(ex_or_answers, 'exc|ans')

    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined.
    #   Returns a str
    #   @warning Exception NotInstanciableObject.
    def text_to_str(self, **options):
        raise error.MethodShouldBeRedefined(self, 'text_to_str')

    # --------------------------------------------------------------------------
    ##
    #   @brief /!\ Must be redefined.
    #   Writes the answers of the questions to the output.
    #   @warning Exception NotInstanciableObject.
    def answer_to_str(self, **options):
        raise error.MethodShouldBeRedefined(self, 'answer_to_str')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns " " if not redefined otherwise.
    def hint_to_str(self, **options):
        return " "
