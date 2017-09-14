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

import random
import warnings
from decimal import Decimal, ROUND_DOWN


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
            from mathmaker.lib.tools import is_integer
            seq = [i for i in seq
                   if not is_integer(i * (10 ** (depth - 1)))]
        if operation in ['sum', '+']:
            a = random.choice(seq)
            b = n - a
        elif operation in ['difference', '-']:
            b = random.choice(seq)
            a = n + b
        return (a, b)
