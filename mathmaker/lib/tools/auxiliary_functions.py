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
from decimal import Decimal, ROUND_DOWN


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


def correct_normalize_results(d):
    """Transform the xE+n results in decimal form (ex. 1E+1 -> 10)"""
    if not isinstance(d, Decimal):
        raise TypeError('Expected a Decimal, got a '
                        + str(type(d)) + 'instead')
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def round_deci(d, precision, **options):
    """Correctly round a Decimal"""
    if not isinstance(d, Decimal):
        raise TypeError('Expected a Decimal, got a '
                        + str(type(d)) + 'instead')

    return correct_normalize_results(d.quantize(precision, **options))


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


def digits_nb(n):
    """
    Return the number of significant digits of an int or decimal.Decimal.

    :param n: the number to test
    :type n: int or decimal.Decimal
    :rtype: int
    """
    if is_integer(n):
        return 0
    n = Decimal(n)
    n = n.quantize(Decimal(1)) if n == n.to_integral() else n.normalize()
    temp = len(str((n - round_deci(n, Decimal(1), rounding=ROUND_DOWN)))) - 2
    return temp if temp >= 0 else 0


def is_power_of_10(n):
    """
    Check if n is a power of ten.

    :param n: the number to test
    :type n: int or decimal.Decimal
    :rtype: boolean
    """
    if not is_number(n) or type(n) is float:
        raise TypeError('Argument n must be either int or decimal.Decimal.')
    n = Decimal(abs(n))
    if Decimal(10) <= n:
        return is_power_of_10(n / 10)
    if Decimal(1) < n < Decimal(10):
        return False
    elif n == Decimal(1):
        return True
    elif Decimal('0.1') < n < Decimal(1):
        return False
    elif 0 < n <= Decimal('0.1'):
        return is_power_of_10(n * 10)
    elif n == 0:
        return False


def split_nb(n, operation='sum', dig=0):
    """
    Split n as a sum, like a + b = n; or a difference, like a - b = n

    By default, a and b have as many digits as n does. The 'dig' keyword tells
    how many extra digits must have a and b (compared to n).
    For instance, if n=Decimal('2.5'), operation='sum', dig=1, then
    n will be split into 2-digits numbers, like 2.14 + 2.36.

    :param n: the number to split
    :type n: a number (preferably an int or a Decimal, but can be a float too)
    :param operation: must be 'sum', 'difference', '+' or '-'
    :type operation: str
    :param dig: extra depth level to use
    :type dig: int
    :rtype: tuple (of numbers)
    """
    if operation not in ['sum', 'difference', '+', '-']:
        raise ValueError('Argument "operation" should be either \'sum\' or '
                         '\'difference\'.')
    n_depth = digits_nb(n)
    depth = dig + digits_nb(n)
    if operation in ['sum', '+']:
        if is_power_of_10(n) and abs(n) <= 1 and dig == 0:
            # This case is impossible: write 1 as a sum of two natural
            # numbers bigger than 1, or 0.1 as a sum of two positive decimals
            # having 1 digit either, etc. so we arbitrarily replace n by
            # a random number between 2 and 9
            warnings.warn('mathmaker is asked something impossible (split {}'
                          'as a sum of two numbers having as many digits)'
                          .format(n))
            n = random.choice([i + 2 for i in range(7)])
            n = n * (10 ** (Decimal(- n_depth)))
        amplitude = n
    elif operation in ['difference', '-']:
        amplitude = max(10 ** (n_depth), n)
    start, end = 0, int((amplitude) * 10 ** depth - 1)
    if start > end:
        start, end = end + 1, -1
    # default: all numbers, including integers
    seq = [(Decimal(i) + 1) / Decimal(10) ** Decimal(depth)
           for i in range(start, end)]
    # then if decimals are wanted, we remove the results that do not match
    # the wanted "depth" (if depth == 2, we remove 0.4 for instance)
    if depth >= 1:
            seq = [n for n in seq
                   if not is_integer(n * (10 ** (depth - 1)))]
    if operation in ['sum', '+']:
        a = random.choice(seq)
        b = n - a
    elif operation in ['difference', '-']:
        b = random.choice(seq)
        a = n + b
    return (a, b)
