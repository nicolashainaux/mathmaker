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


##
#   @brief  Will tell if the tag belongs to int pairs, decimal numbers etc.
def classify_tag(tag):
    if (tag.startswith('intpairs_') or tag.startswith('table_')
        or tag.startswith('multiplesof')):
        # __
        return 'int_pairs'
    elif tag.startswith('singleint_'):
        return 'single_int'
    elif tag in ['int_deci_clever_pairs', 'rank_words',
                 'int_irreducible_frac', 'nothing',
                 'decimal_and_10_100_1000_for_multi',
                 'decimal_and_10_100_1000_for_divi',
                 'decimal_and_one_digit_for_multi',
                 'decimal_and_one_digit_for_divi']:
        # __
        return tag
    raise ValueError(tag + " is not recognized as a valid 'tag' that can be "
                     "used in a mathmaker xml file.")


##
#   @brief  Will turn the tag into the matching conditions for the db query.
#           Note that any value matching a 'nbN' key (like 'nb1': '11') will
#           be automatically removed from any "NOT IN(...)" condition in a
#           query. The "raw" keyword allows to give more complex queries but
#           as the 'nbN' keys are then "buried" inside the query string, it's
#           possible to add a "prevail": 'value' in the returned dictionary
#           to allow this very same behaviour (as directly adding a
#           'nbN': 'value' may change the query).
#   @return A dictionary
def translate_int_pairs_tag(tag):
    d = {}
    # 'table_11' is a shortcut for a special range
    if tag == 'table_11':
        d = {'nb2_in': ['11', '12', '13', '14', '15', '16', '17', '18', '21',
                        '22', '23', '24', '25', '26', '27', '31', '32', '33',
                        '34', '35', '36', '41', '42', '43', '44', '45', '51',
                        '52', '53', '54', '61', '62', '63', '71', '72', '81'],
             'nb1': '11'}
    # 'table_N' is a shortcut for 'multiplesofN_2to9' if N <= 10
    # and for 'multiplesofN_2to6' if N >= 12 (11 is managed separately)
    elif tag.startswith('table_'):
        n = int(tag[6:])
        r = "_2to9" if n <= 10 else "_2to6"
        tag = 'multiplesof' + str(n) + r

    if tag.startswith('intpairs_'):
        n1, n2 = tag[9:].split(sep='to')
        d = {'nb1_min': n1, 'nb1_max': n2,
             'nb2_min': n1, 'nb2_max': n2}
    elif tag.startswith('multiplesof'):
        N, r = tag[11:].split(sep='_')
        mini, maxi = r.split(sep='to')
        d = {'raw': '(nb1 = ' + N + ' and (nb2 >= ' + mini
                    + ' and nb2 <= ' + maxi + ')) or (nb2 = ' + N
                    + ' and (nb1 >= ' + mini + ' and nb1 <= ' + maxi + '))',
             'prevails': [N]}

    return d


def translate_single_int_tag(tag):
    if tag.startswith('singleint_'):
        n1, n2 = tag[10:].split(sep='to')
        d = {'nb1_min': n1, 'nb1_max': n2}
    return d
