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

import sys
import math
import random
from decimal import Decimal

from mathmakerlib.calculus import is_integer, is_number


# DIVISORS frequently used by the children
# (the most "exotic" couples (like 4×16) have been withdrawn so that the
# the fractions can be reduced in a way that will look natural to children.
# There should be enough couples left to bring the reduction to fruition, even
# if in several steps. Some "exotic" couples have been kept because they are
# necessary (like 7×13, 5×17...)
# The divisor 1 in the divisors of 0 and 1 has been written twice to avoid
# getting an error on asking the length of an unsized object
DIVISORS = [(1, 1), (1, 1), (2, 1), (3, 1), (4, 2, 1), (5, 1), (6, 3, 2, 1),
            (7, 1), (8, 4, 2, 1), (9, 3, 1), (10, 5, 2, 1), (11, 1),
            (12, 6, 4, 3, 2, 1), (13, 1), (14, 7, 2, 1),
            (15, 5, 3, 1), (16, 8, 4, 2, 1), (17, 1), (18, 9, 6, 3, 2, 1),
            (19, 1), (20, 10, 5, 4, 2, 1), (21, 7, 3, 1), (22, 11, 2, 1),
            (23, 1), (24, 12, 8, 6, 4, 3, 2, 1), (25, 5, 1), (26, 13, 2, 1),
            (27, 9, 3, 1), (28, 7, 4, 2, 1), (29, 1),
            (30, 15, 10, 6, 5, 3, 2, 1), (31, 1), (32, 16, 8, 4, 2, 1),
            (33, 11, 3, 1), (34, 17, 2, 1), (35, 7, 5, 1),
            (36, 18, 12, 9, 6, 4, 3, 2, 1), (37, 1), (38, 19, 2, 1),
            (39, 13, 3, 1), (40, 20, 10, 8, 5, 4, 2, 1), (41, 1),
            (42, 21, 7, 6, 2, 1), (43, 1), (44, 22, 11, 4, 2, 1),
            (45, 9, 5, 1), (46, 23, 2, 1), (47, 1), (48, 24, 8, 6, 2, 1),
            (49, 7, 1), (50, 25, 10, 5, 2, 1), (51, 17, 3, 1),
            (52, 26, 13, 4, 2, 1), (53, 1), (54, 27, 9, 6, 2, 1),
            (55, 11, 5, 1), (56, 28, 8, 7, 2, 1), (57, 19, 3, 1),
            (58, 29, 2, 1), (59, 1),
            (60, 30, 20, 15, 12, 10, 6, 5, 4, 3, 2, 1), (61, 1),
            (62, 31, 2, 1), (63, 21, 9, 7, 3, 1), (64, 32, 8, 2, 1),
            (65, 13, 5, 1), (66, 33, 2, 1), (67, 1), (68, 34, 17, 4, 2, 1),
            (69, 23, 3, 1), (70, 35, 10, 7, 5, 2, 1), (71, 1),
            (72, 12, 9, 8, 6, 2, 1), (73, 1), (74, 37, 2, 1), (75, 15, 5, 1),
            (76, 38, 2, 1), (77, 11, 7, 1), (78, 39, 26, 3, 2, 1), (79, 1),
            (80, 40, 20, 10, 8, 4, 2, 1), (81, 9, 1), (82, 41, 2, 1), (83, 1),
            (84, 42, 2, 1), (85, 17, 5, 1), (86, 43, 2, 1), (87, 29, 3, 1),
            (88, 44, 22, 11, 8, 4, 2, 1), (89, 1),
            (90, 45, 30, 10, 9, 3, 2, 1), (91, 13, 7, 1), (92, 46, 2, 1),
            (93, 31, 3, 1), (94, 47, 2, 1), (95, 19, 5, 1), (96, 48, 2, 1),
            (97, 1), (98, 49, 2, 1), (99, 33, 11, 9, 3, 1),
            (100, 50, 25, 10, 4, 2, 1)]


POLYGONS_NATURES = {3: 'Triangle', 4: 'Quadrilatere', 5: 'Pentagon',
                    6: 'Hexagon', 7: 'Heptagon', 8: 'Octogon',
                    9: 'Enneagon', 10: 'Decagon'}

# CONSTANTS CONCERNING MATH OBJECTS
ZERO_POLYNOMIAL_DEGREE = -sys.maxsize


# --------------------------------------------------------------------------
##
#   @brief Returns the sign of the product of relatives numbers
#   @param signed_objctlist A list of any objects having a sign
#   @return A sign ('+' ou '-')
def sign_of_product(signed_objctlist):
    from mathmaker.lib.core.base_calculus import Exponented

    if not(type(signed_objctlist) == list):
        raise TypeError('Expected a list, got a '
                        + str(type(signed_objctlist)) + 'instead')

    if not(len(signed_objctlist) >= 1):
        raise ValueError('This list shouldn\'t be empty')

    minus_signs_nb = 0

    for i in range(len(signed_objctlist)):

        if not (signed_objctlist[i] in ['+', '-']
                or is_number(signed_objctlist[i])
                or isinstance(signed_objctlist[i], Exponented)):
            # __
            raise TypeError('Expected a sign + or -, or a number, or an '
                            'Exponented. Got a '
                            + str(type(signed_objctlist[i])) + ' instead')

        elif signed_objctlist[i] == '-':
            minus_signs_nb += 1

        elif is_number(signed_objctlist[i]) and signed_objctlist[i] < 0:
            minus_signs_nb += 1

        elif isinstance(signed_objctlist[i], Exponented):
            minus_signs_nb += signed_objctlist[i].get_minus_signs_nb()

    if is_even(minus_signs_nb):
        return '+'
    else:
        return '-'


# --------------------------------------------------------------------------
##
#   @brief Returns the GCD of two integers
def gcd(a, b):
    if not is_integer(a):
        raise TypeError('Expected an Integer, got a '
                        + str(type(a)) + ' instead')

    if not is_integer(b):
        raise TypeError('Expected an Integer, got a '
                        + str(type(b)) + ' instead')

    if b == 0:
        raise ValueError('Expected a value different from 0.')

    if a % b == 0:
        return int(math.fabs(b))

    return gcd(b, a % b)


# --------------------------------------------------------------------------
##
#   @brief Returns the GCD that a pupil would think of
#   If the numbers are too high, the real gcd will be returned to avoid having
#   reducible fractions found irreducible.
def pupil_gcd(a, b):
    if not is_integer(a):
        raise TypeError('Expected an Integer, got a '
                        + str(type(a)) + ' instead')

    if not is_integer(b):
        raise TypeError('Expected an Integer, got a '
                        + str(type(b)) + ' instead')

    if b == 0:
        raise ValueError('Expected a value different from 0.')

    if a == b:
        return a

    if a >= len(DIVISORS) or b >= len(DIVISORS):
        if a % 10 == 0 and b % 10 == 0:
            return 10 * ten_power_gcd(a / 10, b / 10)

        elif a % 5 == 0 and b % 5 == 0:
            return 5

        elif a % 2 == 0 and b % 2 == 0:
            return 2

        elif a % 3 == 0 and b % 3 == 0:
            return 3

        else:
            return gcd(a, b)

    result = 1

    for i in range(len(DIVISORS[int(a)])):
        if ((DIVISORS[int(a)][i] in DIVISORS[int(b)])
            and DIVISORS[int(a)][i] > result):
            # __
            result = DIVISORS[int(a)][i]

    # to finally get the fraction reduced even if the gcd isn't in the
    # pupil's divisors table:
    if gcd(a, b) != 1 and result == 1:
        result = gcd(a, b)

    return result


# --------------------------------------------------------------------------
##
#   @brief Returns the GCD among powers of 10
#   For instance, ten_power_gcd(20, 300) returns 10,
#   ten_power_gcd(3000, 6000) returns 1000.
def ten_power_gcd(a, b):
    if not is_integer(a):
        raise TypeError('Expected an Integer, got a '
                        + str(type(a)) + ' instead')

    if not is_integer(b):
        raise TypeError('Expected an Integer, got a '
                        + str(type(b)) + ' instead')

    if b == 0:
        raise ValueError('Expected a value different from 0.')

    if a % 10 == 0 and b % 10 == 0:
        return 10 * ten_power_gcd(a // 10, b // 10)
    else:
        return 1


# --------------------------------------------------------------------------
##
#   @brief Returns the lcm of two integers
def lcm(a, b):
    return int(math.fabs(a * b / gcd(a, b)))


# --------------------------------------------------------------------------
##
#   @brief Returns the LCM of a list of integers
def lcm_of_the_list(l):
    if len(l) == 2:
        return lcm(l[0], l[1])
    else:
        return lcm(l.pop(), lcm_of_the_list(l))


# --------------------------------------------------------------------------
##
#   @brief True if objct is an even number|numeric Item. Otherwise, False
#   @param objct The object to test
#   @return True if objct is an even number|numeric Item. Otherwise, False
def is_even(objct):
    from mathmaker.lib.core.base_calculus import Item, Function
    from mathmaker.lib.core.root_calculus import Value

    if is_number(objct) and is_integer(objct):
        if objct % 2 == 0:
            return True
        else:
            return False

    elif (isinstance(objct, Item) and objct.is_numeric()
          and not isinstance(objct, Function)):
        return is_even(objct.raw_value)

    elif isinstance(objct, Value) and objct.is_numeric():
        return is_even(objct.raw_value)

    else:
        return False


# --------------------------------------------------------------------------
##
#   @brief True if objct is an uneven number|numeric Item. Otherwise, False
#   @param objct The object to test
#   @return True if objct is an uneven number|numeric Item. Otherwise, False
def is_uneven(objct):
    return not is_even(objct)


# --------------------------------------------------------------------------
##
#   @brief Mean of a list of numbers
def mean(numberList, weights=None):
    if not type(numberList) == list:
        raise TypeError('Expected a list, got a '
                        + str(type(numberList)) + 'instead')

    if len(numberList) == 0:
        raise ValueError('This list shouldn\'t be empty')

    for i in range(len(numberList)):
        if not is_number(numberList[i]):
            raise TypeError('Expected a number, got a '
                            + str(type(numberList[i])) + ' instead')

    decimalNums = [Decimal(str(x)) for x in numberList]
    if weights is None:
        weights = [1 for n in decimalNums]

    if len(weights) != len(decimalNums):
        raise ValueError('There should be as many weights as numbers, but '
                         'there are {w} weights and {n} numbers.'
                         .format(w=len(weights), n=len(decimalNums)))

    total_weight = Decimal(str(sum(weights)))
    terms = [Decimal(str(w)) * d for w, d in zip(weights, decimalNums)]

    return Decimal(str(sum(terms) / total_weight))


# --------------------------------------------------------------------------
##
#   @brief Barycenter of a list of Points
def barycenter(points_list, barycenter_name, weights=None):
    from mathmaker.lib.core.base_geometry import Point
    if not type(points_list) == list:
        raise TypeError('Expected a list, got a '
                        + str(type(points_list)) + 'instead')

    if len(points_list) == 0:
        raise ValueError('This list shouldn\'t be empty')

    for i in range(len(points_list)):
        if not isinstance(points_list[i], Point):
            raise TypeError('Expected a Point, got a '
                            + str(type(points_list[i])) + ' instead')

    if not type(barycenter_name) == str:
        raise TypeError('Expected a str, got a '
                        + str(type(barycenter_name)) + 'instead')
    if weights is None:
        weights = [1 for p in points_list]

    abscissas_list = [P.x_exact for P in points_list]
    ordinates_list = [P.y_exact for P in points_list]

    return Point(barycenter_name,
                 mean(abscissas_list, weights=weights),
                 mean(ordinates_list, weights=weights))


# --------------------------------------------------------------------------
##
#   @brief Generator of coprime numbers
def coprime_generator(n):
    for i in range(20):
        if gcd(i, n) == 1:
            yield i


# --------------------------------------------------------------------------
##
#   @brief Returns a list of numbers of the given kind
def generate_decimal(width, places_scale, start_place):
    # Probability to fill a higher place rather than a lower one
    php = 0.5
    hp = lr = start_place
    places = [start_place]

    for i in range(width - 1):
        if lr == 0:
            php = 1
        elif hp == len(places_scale) - 1:
            php = 0
        if random.random() < php:
            hp += 1
            places += [hp]
            php *= 0.4
        else:
            lr -= 1
            places += [lr]
            php *= 2.5

    figures = [str(i + 1) for i in range(9)]
    random.shuffle(figures)
    deci = Decimal('0')
    for p in places:
        figure = figures.pop()
        deci += Decimal(figure) * places_scale[p]
    return deci


def prime_factors(n):
    """
    Return all the prime factors of a positive integer

    Taken from https://stackoverflow.com/a/412942/3926735.
    """
    try:
        n = int(n)
    except ValueError:
        raise TypeError('n must be an int')
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d = d + 1
        if d * d > n:
            if n > 1:
                factors.append(n)
            break
    return factors


def coprimes_to(n, span):
    """
    List numbers coprime to n inside provided span.

    :param n: integer number
    :type n: int
    :param span: a list of integer numbers
    :type span: list
    :rtype: list
    """
    return [x for x in span if gcd(n, x) == 1]


def not_coprimes_to(n, span, exclude=None):
    """
    List numbers NOT coprime to n inside provided span.

    :param n: integer number
    :type n: int
    :param span: a list of integer numbers
    :type span: list
    :param exclude: a list of number to always exclude from the results
    :type exclude: list
    :rtype: list
    """
    if exclude is None:
        exclude = []

    return [x for x in span if (x not in exclude and gcd(n, x) != 1)]
