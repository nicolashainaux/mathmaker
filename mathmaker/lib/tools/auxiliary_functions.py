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

import copy
import warnings
import random
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


def is_number(n):
    """Check if n is a number."""
    return type(n) in [float, int, Decimal]


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


def remove_division_by_decimal(N, numbers=None):
    """
    Turn N into decimal instead of the numbers of the list.

    Each decimal of the numbers' list will be recursively replaced by
    10 times itself while N will be divided by 10.

    This is useful for the case division by a decimal is unwanted.

    :param N: the number who will be divided by 10 instead of the others
    :type N: any number (int, Decimal, float though they're not advised)
    :param numbers: an iterable containing the numbers that must be integers
    :type numbers: a list (of numbers)
    :rtype: a list (of numbers)
    """
    if type(numbers) is not list:
        raise TypeError('A list of numbers must be given as argument '
                        '\'numbers\'.')
    if not is_number(N):
        raise TypeError('The first argument must be a number.')
    N = Decimal(str(N))
    if all([is_integer(n) for n in numbers]):
        return [N, ] + [n for n in numbers]
    numbers_copy = copy.deepcopy(numbers)
    for i, n in enumerate(numbers):
        if not is_number(n):
            raise TypeError('Each variable of the list must be a number.')
        if not is_integer(n):
            numbers_copy[i] = n * 10
            return remove_division_by_decimal(N / 10, numbers=numbers_copy)
    return [N, ] + [n for n in numbers]


def split_nb_into(operation, n, nb_variant='',
                  deci_restriction='', extra_digits=0):
    """
    Split n as a sum, like a + b = n; or a difference, like a - b = n

    By default, a and b are integers, or decimals with as many digits as
    shown in nb_variant (if it is in the form of 'decimalN').
    Extra_digits are useful when one want a and b to be "deeper" than planned.
    For instance, with arguments 'sum', Decimal('2.5'), 'decimal1', '', 1
    it's possible to decompose split 2.5 in 2.14 + 2.36.

    The variable 'depth' finally represents how many digits will have the
    final numbers a and b.

    :param operation: must be either 'sum' or 'difference'
    :type operation: str
    :param n: the number to split
    :type n: a number (preferably an int or a Decimal, but can be a float too)
    :param nb_variant: can be 'decimal1', 'decimal2' -> 'decimal9', or
                       any other string that won't be taken into account
    :type nb_variant: str
    :param deci_restriction: can contain '+' or '-' or any other string
                             that won't be taken into account
    :type deci_restriction: str
    :param extra_digits: extra depth level to use
    :type extra_digits: int
    :rtype: tuple (of numbers)
    """
    if operation not in ['sum', 'difference']:
        raise ValueError('Argument "operation" should be either \'sum\' or '
                         '\'difference\'.')
    depth = 0  # default value (matches integers)
    if nb_variant.startswith('decimal'):
        if (not is_integer(n)
            or ('+' in deci_restriction and operation is 'sum')
            or ('-' in deci_restriction and operation is 'difference')):
            # e.g. decimals_restricted_to contains '+-'
            # or nb_variant is 'decimalN' (where 1 <= N <= 9) and nb1 is no int
            depth = int(nb_variant[-1]) + extra_digits
    if operation is 'sum':
        if not (nb_variant.startswith('decimal') and depth >= 1) and n == 1:
            # This case is impossible: write 1 as a sum of two natural
            # numbers bigger than 1, so we arbitrarily replace 1 by
            # a random number between 2 and 10
            warnings.warn('mathmaker is asked to split 1 as a sum of two '
                          'naturals bigger than 1. As this is impossible, '
                          '1 will be replaced by a random natural between '
                          '2 and 10.')
            n = random.choice([i + 2 for i in range(8)])
        amplitude = n
    elif operation is 'difference':
        amplitude = max(10, n)
    start, end = 0, int((amplitude) * 10 ** depth - 1)
    if start > end:
        start, end = end + 1, -1
    # default: all numbers, including integers
    seq = [(Decimal(i) + 1) / Decimal(10) ** Decimal(depth)
           for i in range(start, end)]
    # then if decimals are wanted, we remove the results that do not match
    # the wanted "depth" (if depth == 2, we remove 0.4 for instance)
    if nb_variant.startswith('decimal') and depth >= 1:
            seq = [n for n in seq
                   if not is_integer(n * (10 ** (depth - 1)))]
    if operation == 'sum':
        a = random.choice(seq)
        b = n - a
    elif operation == 'difference':
        b = random.choice(seq)
        a = n + b
    return (a, b)
