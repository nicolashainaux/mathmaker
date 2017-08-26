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
from mathmaker.lib.document.content import algebra, calculation, geometry

ALL_MODULES = (algebra, calculation, geometry)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @brief Creates one 'generic' question
class Question(object):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param **options Any options
    def __init__(self, q_kind, **options):
        # That's the number of the question, not of the expressions it might
        # contain!
        self.number = options.get('number_of_the_question', '')
        self.displayable_number = ''
        if self.number != '':
            self.displayable_number = \
                shared.machine.write(str(self.number) + ". ", emphasize='bold')

        self.q_kind = q_kind
        self.q_subkind = options.get('q_subkind', 'default')

        # modules
        mod_name = self.q_kind
        if mod_name in ['vocabulary_half', 'vocabulary_third',
                        'vocabulary_quarter', 'vocabulary_double',
                        'vocabulary_triple', 'vocabulary_quadruple']:
            # __
            mod_name = 'vocabulary_simple_multiple_of_a_number'

        for m in ALL_MODULES:
            if hasattr(m, mod_name):
                module = getattr(m, mod_name)
                break
        else:
            raise AttributeError(mod_name + ' not found in ALL_MODULES: '
                                 + ', '.join([m.__name__
                                             for m in ALL_MODULES]))
        m = module.sub_object(**options)

        sp = options.get('spacing', '30.0pt')
        if sp == 'newline':
            self.q_spacing = shared.machine.write_new_line()
        elif sp == 'newline_twice':
            self.q_spacing = shared.machine.write_new_line() \
                + shared.machine.write_new_line()
        elif sp == '':
            self.q_spacing = ''
        else:
            self.q_spacing = shared.machine.addvspace(height=sp)

        asp = options.get('answers_spacing', '')
        if asp == 'newline':
            self.a_spacing = shared.machine.write_new_line()
        elif asp == 'newline_twice':
            self.a_spacing = shared.machine.write_new_line() \
                + shared.machine.write_new_line()
        elif asp == '':
            self.a_spacing = ''
        else:
            self.a_spacing = shared.machine.addvspace(height=asp)

        self.q_text = m.q(**options)
        self.q_answer = m.a(**options)
        if hasattr(m, 'h'):
            self.q_hint = m.h(**options)
        else:
            self.q_hint = ''
        self.q_nb_included_in_wording = False
        if hasattr(m, 'q_nb_included_in_wording'):
            self.q_nb_included_in_wording = m.q_nb_included_in_wording
        self.transduration = None
        if hasattr(m, 'transduration'):
            self.transduration = m.transduration
        if 'transduration' in options:
            self.transduration = options['transduration']
        self.substitutable_question_mark = False
        if hasattr(m, 'substitutable_question_mark'):
            self.substitutable_question_mark = m.substitutable_question_mark

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
            raise ValueError('Got ' + str(ex_or_answers)
                             + ' instead of \'exc\'|\'ans\'|\'hint\'')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the text of the question as a str
    def text_to_str(self):
        text = str(self.q_text) + self.q_spacing
        if not self.q_nb_included_in_wording:
            text = str(self.displayable_number) + text
        return text

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        return str(self.displayable_number) + str(self.q_answer) \
            + str(self.a_spacing)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def hint_to_str(self):
        return self.q_hint
