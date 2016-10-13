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
from . import algebra_modules, mc_modules, geometry_modules

ALL_MODULES = (algebra_modules, mc_modules, geometry_modules)

SUBKINDS_TO_UNPACK = {'simple_parts_of_a_number': {'half', 'third', 'quarter'},
                      'simple_multiples_of_a_number': {'double', 'triple',
                                                       'quadruple'},
                      'simple_parts_or_multiples_of_a_number': {'half',
                                                                'third',
                                                                'quarter',
                                                                'double',
                                                                'triple',
                                                                'quadruple'},
                      'operation': {'multi', 'divi', 'addi', 'subtr'}}

UNPACKABLE_SUBKINDS = {'half', 'third', 'quarter',
                       'double', 'triple', 'quadruple',
                       'multi', 'divi', 'addi', 'subtr'}

SOURCES_TO_UNPACK = {'auto_table': {'half': {'table_2'},
                                    'third': {'table_3'},
                                    'quarter': {'table_4'},
                                    'double': {'table_2'},
                                    'triple': {'table_3'},
                                    'quadruple': {'table_4'},
                                    'multi': {'intpairs_2to9'},
                                    'divi': {'intpairs_2to9'},
                                    'addi': {'intpairs_2to9'},
                                    'subtr': {'intpairs_2to9'}},
                     'auto_11_50': {'half': {'multiplesof2_11to50'},
                                    'third': {'multiplesof3_11to50'},
                                    'quarter': {'multiplesof4_11to50'},
                                    'double': {'multiplesof2_11to50'},
                                    'triple': {'multiplesof3_11to50'},
                                    'quadruple': {'multiplesof4_11to50'}},
                     'auto_vocabulary':
                     {'half': {'table_2', 'multiplesof2_11to50'},
                      'third': {'table_3', 'multiplesof3_11to50'},
                      'quarter': {'table_4', 'multiplesof4_11to50'},
                      'double': {'table_2', 'multiplesof2_11to50'},
                      'triple': {'table_3', 'multiplesof3_11to50'},
                      'quadruple': {'table_4', 'multiplesof4_11to50'},
                      'multi': {'intpairs_2to9'},
                      'divi': {'intpairs_2to9'},
                      # The 'intpairs_2to200' below will get divided
                      # by 10 to produce two decimals between 0.2
                      # and 20.
                      'addi': {'intpairs_10to100', 'intpairs_2to200'},
                      'subtr': {'intpairs_10to100', 'intpairs_2to200'}},
                     'decimal_and_10_100_1000':
                     {'multi_direct': {'decimal_and_10_100_1000_for_multi'},
                      'divi_direct': {'decimal_and_10_100_1000_for_divi'},
                      'area_rectangle': {'decimal_and_10_100_1000_for_multi'},
                      'perimeter_rectangle': {'decimal_and_10_100_1000_for'
                                              '_multi'},
                      'multi_hole': {'decimal_and_10_100_1000_for_multi'},
                      'vocabulary_multi': {'decimal_and_10_100_1000_for'
                                           '_multi'},
                      'vocabulary_divi': {'decimal_and_10_100_1000_for_divi'}},
                     'decimal_and_one_digit': \
                     {'multi_direct': {'decimal_and_one_digit_for_multi'},
                      'divi_direct': {'decimal_and_one_digit_for_divi'},
                      'area_rectangle': {'decimal_and_one_digit_for_multi'},
                      'multi_hole': {'decimal_and_one_digit_for_multi'},
                      'vocabulary_multi': {'decimal_and_one_digit_for_multi'},
                      'vocabulary_divi': {'decimal_and_one_digit_for_divi'}}}


# --------------------------------------------------------------------------
##
#   @brief  Tells if the given question's type and source number do match
#   @todo   The 'integer_3_10_decimal_3_10' may be later turned into
#           'intpairs_3to10' with variant='decimal1', so this condition can
#           certainly be removed.
def match_qtype_sourcenb(q_type, source_nb):
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
    elif q_type == 'multi_reversed':
        return any([(source_nb.startswith('intpairs_')
                     and source_nb.endswith('to9')),
                    source_nb == 'table_2',
                    source_nb == 'table_3',
                    source_nb == 'table_4',
                    source_nb == 'bypass'])


# --------------------------------------------------------------------------
##
#   @brief Returns a dictionary to give some special informations needed for
#          certain questions.
def get_modifier(q_type, nb_source):
    d = {}
    if q_type == 'multi_reversed':
        d.update({'multi_reversed': True,
                  'info_multirev': {(2, 6): [(2, 6), (3, 4)],
                                    (3, 4): [(2, 6), (3, 4)],
                                    (2, 8): [(2, 8), (4, 4)],
                                    (4, 4): [(2, 8), (4, 4)],
                                    (3, 6): [(3, 6), (2, 9)],
                                    (2, 9): [(3, 6), (2, 9)],
                                    (3, 8): [(3, 8), (4, 6)],
                                    (4, 6): [(3, 8), (4, 6)],
                                    (4, 9): [(4, 9), (6, 6)],
                                    (6, 6): [(4, 9), (6, 6)]}})
    elif q_type == 'subtr_direct' and nb_source.startswith('intpairs_10'):
        d.update({'diff7atleast': True})
    elif any(['rectangle' in q_type,
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

        self.add_new_line_to_text = shared.machine.write_new_line() \
            + shared.machine.write_new_line()

        # modules
        if self.q_kind in ['vocabulary_half', 'vocabulary_third',
                           'vocabulary_quarter', 'vocabulary_double',
                           'vocabulary_triple', 'vocabulary_quadruple']:
            # __
            module = getattr(mc_modules,
                             'vocabulary_simple_multiple_of_a_number')
            self.add_new_line_to_text = ''

        else:
            for m in ALL_MODULES:
                if hasattr(m, self.q_kind):
                    module = getattr(m, self.q_kind)
                    if m is mc_modules:
                        self.add_new_line_to_text = ''
                    break
            else:
                raise AttributeError(self.q_kind + ' not found in '
                                     'ALL_MODULES: '
                                     + ', '.join([m.__name__
                                                 for m in ALL_MODULES]))
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
        return str(self.displayable_number) + str(self.q_text) \
            + self.add_new_line_to_text

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        return str(self.displayable_number) + str(self.q_answer)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the answer of the question as a str
    def hint_to_str(self):
        return self.q_hint
