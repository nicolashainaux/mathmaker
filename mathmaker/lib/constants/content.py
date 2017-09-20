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
                     # TODO: remove auto_11_50 when XML sheets are removed
                     'auto_11_50': {'half': {'multiplesof2_11to50'},
                                    'third': {'multiplesof3_11to50'},
                                    'quarter': {'multiplesof4_11to50'},
                                    'double': {'multiplesof2_11to50'},
                                    'triple': {'multiplesof3_11to50'},
                                    'quadruple': {'multiplesof4_11to50'}},
                     'auto_multiples': {'half': {'multiplesof2_11to50',
                                                 'multiplesof20_2to10'},
                                        'third': {'multiplesof3_8to13',
                                                  'multiplesof30_2to10'},
                                        'quarter': {'multiplesof4_8to13',
                                                    'multiplesof40_2to10'},
                                        'double': {'multiplesof2_11to50'},
                                        'triple': {'multiplesof3_11to30'},
                                        'quadruple': {'multiplesof4_11to20'}},
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
