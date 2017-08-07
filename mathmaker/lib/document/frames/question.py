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

import warnings

from mathmaker.lib import shared
from mathmaker.lib.constants import EQUAL_PRODUCTS
from mathmaker.lib.document.content import algebra, calculation, geometry

ALL_MODULES = (algebra, calculation, geometry)


def match_qtype_sourcenb(q_type: str, source_nb: str, variant: str):
    """
    Tell if the given question's type and source number do match.

    This is used in mix sections only, yet.

    :param q_type: the question's type (kind_subkind)
    :param source_nb: the source of the numbers
    :param variant: the variant of the numbers' source / question, if available
    """
    #   @todo   The 'integer_3_10_decimal_3_10' may be later turned into
    #           'intpairs_3to10' with variant='decimal1', so this condition can
    #           certainly be removed.
    source_nb = source_nb[0]
    if q_type in ['multi_direct', 'area_rectangle', 'multi_hole',
                  'rectangle_length_or_width_from_area', 'divi_direct',
                  'vocabulary_multi', 'vocabulary_divi']:
        # __
        return any([source_nb.startswith('intpairs_'),
                    source_nb.startswith('multiplesof'),
                    source_nb.startswith('table_'),
                    source_nb == 'decimal_and_10_100_1000',
                    source_nb == 'decimal_and_one_digit',
                    source_nb == 'bypass'])
    elif q_type in ['addi_direct', 'subtr_direct', 'perimeter_rectangle',
                    'rectangle_length_or_width_from_perimeter',
                    'vocabulary_addi', 'vocabulary_subtr']:
        # __
        return any([source_nb.startswith('intpairs_'),
                    source_nb.startswith('multiplesof'),
                    source_nb.startswith('table_'),
                    source_nb == 'decimal_and_10_100_1000',
                    source_nb == 'integer_3_10_decimal_3_10',
                    source_nb == 'decimals_0_20_1',
                    source_nb == 'bypass'])
    elif q_type.startswith('rank_'):
        return any([source_nb == 'rank_words', source_nb == 'bypass'])
    elif q_type in ['perimeter_square', 'area_square']:
        return any([source_nb.startswith('intpairs_'),
                    source_nb.startswith('multiplesof'),
                    source_nb.startswith('table_'),
                    source_nb == 'bypass'])
    elif q_type in ['vocabulary_half', 'vocabulary_double']:
        return any([source_nb.startswith('multiplesof2'),
                    source_nb == 'table_2',
                    source_nb == 'bypass'])
    elif q_type in ['vocabulary_third', 'vocabulary_triple']:
        return any([source_nb.startswith('multiplesof3'),
                    source_nb == 'table_3',
                    source_nb == 'bypass'])
    elif q_type in ['vocabulary_quarter', 'vocabulary_quadruple']:
        return any([source_nb.startswith('multiplesof4'),
                    source_nb == 'table_4',
                    source_nb == 'bypass'])
    elif q_type in ['multi_reversed', 'fraction_of_rectangle']:
        return any([source_nb.startswith('intpairs_'),
                    source_nb == 'table_2',
                    source_nb == 'table_3',
                    source_nb == 'table_4',
                    source_nb == 'bypass'])
    elif q_type == 'calculation_order_of_operations':
        # We only check there are two sources
        return len(source_nb.split(sep=';;')) == 2
    else:
        warnings.warn('Could not check if the question\'s type and numbers\'s '
                      'source do match or not: {} and {}'
                      .format(q_type, source_nb))
        return True


# --------------------------------------------------------------------------
##
#   @brief Returns a dictionary to give some special informations needed for
#          certain questions.
def get_modifier(q_type, nb_source):
    d = {}
    if (q_type in ['multi_reversed', 'fraction_of_a_rectangle']
        and nb_source.startswith('intpairs')):
        d.update({'lock_equal_products': True,
                  'info_lock': EQUAL_PRODUCTS})
    elif q_type == 'subtr_direct' and nb_source.startswith('intpairs_10'):
        d.update({'diff7atleast': True})
    elif any(['rectangle' in q_type and q_type != 'fraction_of_a_rectangle',
              q_type.startswith('addi_'), q_type.endswith('_addi'),
              q_type.startswith('subtr_'), q_type.endswith('_subtr')]):
        # __
        d.update({'rectangle': True})
    elif 'square' in q_type:
        d.update({'square': True})
    return d


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
