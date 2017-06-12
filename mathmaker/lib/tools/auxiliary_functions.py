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
"""Various auxiliary functions."""

from decimal import Decimal


def rotate(l, n):
    """Rotate list l of n places, to the right if n > 0; else to the left."""
    return l[-n:] + l[:-n]


def check_unique_letters_words(words_list, n):
    """
    Check if each word of the list contains exactly n letters, all unique.
    """
    for w in words_list:
        if len(w) != n:
            raise ValueError('Expected words of length {}, but {} contains '
                             '{} letters.'.format(str(n), w, str(len(w))))
        if len(w) != len(set(w)):
            raise ValueError('{} contains duplicate letters, but it '
                             'shouldn\'t.'
                             .format(w))
    return True


def is_integer(n):
    """Check if number n is an integer."""
    if type(n) is int:
        return True
    elif type(n) is float:
        return n.is_integer()
    elif type(n) is Decimal:
        return n % 1 == 0
    else:
        raise TypeError('Expected a number, either float, int or Decimal,'
                        'got {} instead.'.format(str(type(n))))


def is_natural(n):
    """Check if number n is a natural number."""
    return is_integer(n) and n >= 0
