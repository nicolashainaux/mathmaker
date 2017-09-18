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

import copy
import random
import warnings
from decimal import Decimal, ROUND_DOWN


def is_number(n):
    """Check if n is a number."""
    return any(isinstance(n, c) for c in [float, int, Decimal])


def is_integer(n):
    """Check if number n is an integer."""
    if isinstance(n, int):
        return True
    elif isinstance(n, float):
        return n.is_integer()
    elif isinstance(n, Decimal):
        return n % 1 == 0
    else:
        raise TypeError('Expected a number, either float, int or Decimal,'
                        'got {} instead.'.format(str(type(n))))


def is_natural(n):
    """Check if number n is a natural number."""
    return is_integer(n) and n >= 0


class Number(Decimal):
    """Extend Decimal with a bunch of useful methods."""

    def standardized(self):
        """Turn 8.0 to 8 and 1E+1 to 10"""
        return Number(self.quantize(Decimal(1))) \
            if self == self.to_integral() \
            else Number(self.normalize())

    def nonzero_digits_nb(self):
        """Return the number of nonzero digits."""
        n = str(abs(self.standardized()))
        return len(n) - n.count('0') - n.count('.')

    def round(self, precision, **options):
        """Round the number. Return a standardized result."""
        return Number(self.quantize(precision, **options)).standardized()

    def decimal_places_nb(self):
        """Return the number of decimal places."""
        n = Number(abs(self)).standardized()
        temp = len(str((n - n.round(Decimal(1), rounding=ROUND_DOWN)))) - 2
        return temp if temp >= 0 else 0

    def is_power_of_10(self):
        """Check if n is a power of ten."""
        n = Number(abs(self))
        if Decimal(10) <= n:
            return Number(n / Number(10)).is_power_of_10()
        if Decimal(1) < n < Decimal(10):
            return False
        elif n == Decimal(1):
            return True
        elif Decimal('0.1') < n < Decimal(1):
            return False
        elif 0 < n <= Decimal('0.1'):
            return Number(n * Number(10)).is_power_of_10()
        elif n == 0:
            return False

    def atomized(self, keep_zeros=False):
        """Split abs(self) in as many Numbers as digits."""
        _, digits, e = self.standardized().as_tuple()
        digits = list(digits)
        result = []
        for i, d in enumerate(digits):
            if d != 0 or keep_zeros:
                result += [Number(d) * Number(10) ** (e + len(digits) - 1 - i)]
        if not len(result):
            return [Number(0)]
        return result

    def overlap_level(self):
        """
        Calculate the maximum overlap possible.

        For instance, 0.724 has an overlap level of 1 (can be split as
        0.71 + 0.14) but 0.714 has an overlap level of only 0 (can be split as
        0.7 + 0.014 or 0.71 + 0.004, but not as two decimals having a nonzero
        digits at tenths' position.)
        """
        base_level = self.standardized().nonzero_digits_nb() - 2
        digits = list(self.as_tuple().digits)
        level = base_level - digits[1:-1].count(1)
        return level

    def cut(self, overlap=0, return_all=False):
        """
        Cut self as a + b, a and b having only 0, 1... positions in common.

        For instance:
        Number('5.6').cut() == (Number('5'), Number('0.6'))
        Number('5.36').cut(return_all=True) == \
            [(Number('5'), Number('0.36')),
             (Number('5.3'), Number('0.06'))]
        Number('5.36').cut(overlap=1, return_all=True) == \
            [(Number('5.1'), Number('0.26')),
             (Number('5.2'), Number('0.16'))]

        :param overlap: tells how many decimal places in common the terms a
                        and b should have when splitting as a sum.
                        Values of overlap >= 1 are not handled yet
        :type overlap: int (only 0 is handled yet)
        :param return_all: if True, then all possibilities are returned, as a
                           list.
        :type return_all: bool
        :rtype: tuple (or a list of tuples)
        """
        if not isinstance(overlap, int):
            raise TypeError('When overlap is used, it must be an int. Got '
                            'a {} instead.'.format(type(overlap)))
        if overlap < 0:
            raise ValueError('overlap must be a positive int. Got a '
                             'negative int instead.')
        if self.overlap_level() < overlap:
            raise ValueError('Given overlap is too high.')
        if overlap != 0:
            raise ValueError('Only overlap=0 is implemented yet.')
        results = []
        digits = self.atomized()
        for n in range(len(digits) - 1):
            results += [(sum(digits[0:n + 1]), sum(digits[n + 1:]))]
        if return_all:
            return results
        else:
            return random.choice(results)

    def split(self, operation='sum', dig=0):
        """
        Split self as a sum or difference, e.g. self = a + b or self = a - b

        By default, a and b have as many fractional digits as n does.
        The 'dig' keyword tells how many extra digits must have a and b
        (compared to self). For instance, if n=Decimal('4.5'), operation='sum',
        dig=1, then self will be split into 2-fractional-digits numbers,
        like 2.14 + 2.36.

        :param operation: must be 'sum', 'difference', '+' or '-'
        :type operation: str
        :param dig: extra depth level to use
        :type dig: int
        :rtype: tuple (of numbers)
        """
        if operation not in ['sum', 'difference', '+', '-']:
            raise ValueError('Argument "operation" should be either \'sum\' '
                             'or \'difference\'.')
        n_depth = self.decimal_places_nb()
        depth = dig + self.decimal_places_nb()
        n = self
        if operation in ['sum', '+']:
            if self.is_power_of_10() and abs(self) <= 1 and dig == 0:
                # This case is impossible: write 1 as a sum of two natural
                # numbers bigger than 1, or 0.1 as a sum of two positive
                # decimals having 1 digit either, etc. so we arbitrarily
                # replace self by a random number between 2 and 9
                warnings.warn('mathmaker is asked something impossible (split '
                              '{} as a sum of two numbers having as many '
                              'digits)'.format(self))
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
            seq = [i for i in seq
                   if not is_integer(i * (10 ** (depth - 1)))]
        if operation in ['sum', '+']:
            a = random.choice(seq)
            b = n - a
        elif operation in ['difference', '-']:
            b = random.choice(seq)
            a = n + b
        return (a, b)


def move_fracdigits_to(n, from_nb=None):
    """
    Turn n into decimal instead of all decimals found in the from_nb list.

    Each decimal found in the numbers' list will be recursively replaced by
    10 times itself (until it is no decimal anymore) while in the same time
    n will be divided by 10.

    This is useful for the case division by a decimal is unwanted.

    :param n: the number who will be divided by 10 instead of the others
    :type n: any number (int, Decimal, float though they're not advised)
    :param from_nb: an iterable containing the numbers that must be integers
    :type from_nb: a list (of numbers)
    :rtype: a list (of numbers)
    """
    if type(from_nb) is not list:
        raise TypeError('A list of numbers must be given as argument '
                        '\'numbers\'.')
    if not is_number(n):
        raise TypeError('The first argument must be a number.')
    n = Decimal(str(n))
    if all([is_integer(i) for i in from_nb]):
        return [n, ] + [i for i in from_nb]
    numbers_copy = copy.deepcopy(from_nb)
    for i, j in enumerate(from_nb):
        if not is_number(j):
            raise TypeError('Each variable of the list must be a number.')
        if not is_integer(j):
            numbers_copy[i] = j * 10
            return move_fracdigits_to(n / 10, from_nb=numbers_copy)
    return [n, ] + [i for i in from_nb]


def remove_fracdigits_from(number, to=None):
    """
    Turn a number of the to list into a decimal, instead of number.

    In some cases this is not possible (for instance when all numbers of the
    to list are multiples of 10), then a ValueError is raised.

    :param number: the number that must be turned into integer
    :type number: decimal.Decimal
    :param to: the list of numbers where to find an integer that must be
               turned into a decimal
    :type to: list
    :rtype: a list (of numbers)
    """
    if not isinstance(number, Decimal):
        raise TypeError('The first argument must be a Decimal number.')
    if is_integer(number):
        raise TypeError('The first argument must be a decimal number.')
    if type(to) is not list:
        raise TypeError('Argument to: must be a list.')
    n = Number(number).decimal_places_nb()
    try:
        i = to.index(next(x for x in to
                          if not is_integer(x / 10 ** n)))
    except StopIteration:
        raise ValueError('None of the numbers of to can be turned into '
                         'decimal.')
    to[i] = Number(to[i]) / Number(10) ** n
    return [Number(number * 10 ** n).standardized(), ] + [x for x in to]


def fix_fracdigits(n1, *n2):
    """Ensure digits from n1 are removed. Change n2 if necessary."""
    n2 = list(n2)
    try:
        n1, *n2 = remove_fracdigits_from(n1, to=n2)
    except ValueError:
        j = random.choice([j for j in range(len(n2))])
        n2[j] += random.choice([i for i in range(-4, 5) if i != 0])
        n1, *n2 = remove_fracdigits_from(n1, to=n2)
    return (n1, *n2)
