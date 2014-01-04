# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2013 Nicolas Hainaux <nico_h@users.sourceforge.net>

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
from decimal import *
import core
import is_
import randomly
import utils


# DIVISORS frequently used by the children
# (the most "exotic" couples (like 4×16) have been withdrawn so that the
# the fractions can be reduced in a way that will look natural to children.
# There should be enough couples left to bring the reduction to fruition, even
# if in several steps. Some "exotic" couples have been kept because they are
# necessary (like 7×13, 5×17...)
# The divisor 1 in the divisors of 0 and 1 has been written twice to avoid
# getting an error on asking the length of an unsized object
DIVISORS = [(1,1), (1,1), (2,1), (3,1), (4,2,1), (5,1), (6,3,2,1), (7,1),
            (8,4,2,1),
            (9,3,1), (10,5,2,1), (11,1), (12,6,4,3,2,1), (13,1), (14,7,2,1),
            (15,5,3,1), (16,8,4,2,1), (17,1), (18,9,6,3,2,1), (19,1),
            (20,10,5,4,2,1), (21,7,3,1), (22,11,2,1), (23,1),
            (24,12,8,6,4,3,2,1), (25,5,1), (26,13,2,1), (27,9,3,1),
            (28,7,4,2,1), (29,1), (30,15,10,6,5,3,2,1), (31,1),
            (32,16,8,4,2,1), (33,11,3,1), (34,17,2,1), (35,7,5,1),
            (36,18,12,9,6,4,3,2,1), (37,1), (38,19,2,1), (39,13,3,1),
            (40,20,10,8,5,4,2,1), (41,1), (42,21,7,6,2,1), (43,1),
            (44,22,11,4,2,1), (45,9,5,1), (46,23,2,1), (47,1),
            (48,24,8,6,2,1), (49,7,1), (50,25,10,5,2,1), (51,17,3,1),
            (52,26,13,4,2,1), (53,1), (54,27,9,6,2,1), (55,11,5,1),
            (56,28,8,7,2,1), (57,19,3,1), (58,29,2,1), (59,1),
            (60,30,20,15,12,10,6,5,4,3,2,1), (61,1), (62,31,2,1),
            (63,21,9,7,3,1), (64,32,8,2,1), (65,13,5,1), (66,33,2,1), (67,1),
            (68,34,17,4,2,1), (69,23,3,1), (70,35,10,7,5,2,1), (71,1),
            (72,12,9,8,6,2,1), (73,1), (74,37,2,1), (75,15,5,1), (76,38,2,1),
            (77,11,7,1), (78,39,26,3,2,1), (79,1), (80,40,20,10,8,4,2,1),
            (81,9,1), (82,41,2,1), (83,1), (84,42,2,1), (85,17,5,1),
            (86,43,2,1), (87,29,3,1), (88,44,22,11,8,4,2,1), (89,1),
            (90,45,30,10,9,3,2,1), (91,13,7,1), (92,46,2,1), (93,31,3,1),
            (94,47,2,1), (95,19,5,1), (96,48,2,1), (97,1), (98,49,2,1),
            (99,33,11,9,3,1), (100,50,25,10,4,2,1)]



# CONSTANTS CONCERNING MATH OBJECTS
ZERO_POLYNOMIAL_DEGREE = -sys.maxint


def abs(nb):
    if nb >= 0:
        return nb
    else:
        return -nb




# ------------------------------------------------ SIGN OF A PRODUCT ----------
##
#   @brief Returns the sign of the product of relatives numbers
#   @param signed_objctlist A list of any objects having a sign
#   @return A sign ('+' ou '-')
def sign_of_product(signed_objctlist):

    if not(type(signed_objctlist) == list) or not(len(signed_objctlist) >= 1):
        raise error.UncompatibleType(signed_objctlist, "non empty list")

    minus_signs_nb = 0

    for i in xrange(len(signed_objctlist)):

        if not (is_.a_sign(signed_objctlist[i])                               \
           or is_.a_number(signed_objctlist[i])                               \
           or isinstance(signed_objctlist[i], core.base_calculus.Exponented)):
        #___
            raise error.UncompatibleType(signed_objctlist[i],                 \
                                         "'+' or '-'|number|Exponented")

        elif signed_objctlist[i] == '-':
            minus_signs_nb += 1

        elif is_.a_number(signed_objctlist[i]) and signed_objctlist[i] < 0:
            minus_signs_nb += 1

        elif isinstance(signed_objctlist[i], core.base_calculus.Exponented):
            minus_signs_nb += signed_objctlist[i].get_minus_signs_nb()

    if is_even(minus_signs_nb):
        return '+'
    else:
        return '-'





# ------------------------------------------------ TWO INTEGER'S GCD ----------
##
#   @brief Returns the GCD of two integers
def gcd(a, b):
    if not is_.an_integer(a):
        raise error.UncompatibleType(a, "Integer")

    if not is_.an_integer(b):
        raise error.UncompatibleType(b, "Integer")

    if b == 0:
        raise error.OutOfRangeArgument(b, "Integer but not zero !")

    if a % b == 0:
        return int(math.fabs(b))

    return gcd(b, a % b)





# ---------------------------------------- GCD OF A LIST OF INTEGERS ----------
##
#   @brief Returns the GCD of a list of integers
def gcd_of_the_list(l):
    if len(l) == 2:
        return gcd(l[0], l[1])
    else:
        return gcd(l.pop(), gcd_of_the_list(l))





# ------------------------------------------------------ PUPIL'S GCD ----------
##
#   @brief Returns the GCD that a pupil would think of
#   If the numbers are too high, the real gcd will be returned to avoid having
#   reducible fractions found irreducible.
def pupil_gcd(a, b):
    if not is_.an_integer(a):
        raise error.UncompatibleType(a, "Integer")

    if not is_.an_integer(b):
        raise error.UncompatibleType(b, "Integer")

    if b == 0:
        raise error.OutOfRangeArgument(b, "Integer but not zero !")

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
            return gcd(a,b)

    result = 1

    for i in xrange(len(DIVISORS[int(a)])):
        if (DIVISORS[int(a)][i] in DIVISORS[int(b)]) \
            and DIVISORS[int(a)][i] > result:
        #___
            result = DIVISORS[int(a)][i]

    # to finally get the fraction reduced even if the gcd isn't in the
    # pupil's divisors table :
    if gcd(a,b) != 1 and result == 1:
        result = gcd(a,b)

    return result





# ------------------------------------------------------ PUPIL'S GCD ----------
##
#   @brief Returns the GCD among powers of 10
#   For instance, ten_power_gcd(20, 300) returns 10,
#   ten_power_gcd(3000, 6000) returns 1000.
def ten_power_gcd(a, b):
    if not is_.an_integer(a):
        raise error.UncompatibleType(a, "Integer")

    if not is_.an_integer(b):
        raise error.UncompatibleType(b, "Integer")

    if b == 0:
        raise error.OutOfRangeArgument(b, "Integer but not zero !")

    if a % 10 == 0 and b % 10 == 0:
        return 10 * ten_power_gcd(a / 10, b / 10)
    else:
        return 1




# ------------------------------------------------ TWO INTEGER'S LCM ----------
##
#   @brief Returns the lcm of two integers
def lcm(a, b):
    return int(math.fabs(a*b/gcd(a,b)))





# ---------------------------------------- LCM OF A LIST OF INTEGERS ----------
##
#   @brief Returns the LCM of a list of integers
def lcm_of_the_list(l):
    if len(l) == 2:
        return lcm(l[0], l[1])
    else:
        return lcm(l.pop(), lcm_of_the_list(l))





# -------------------------------------------------------- IS EVEN ? ----------
##
#   @brief True if objct is an even number|numeric Item. Otherwise, False
#   @param objct The object to test
#   @return True if objct is an even number|numeric Item. Otherwise, False
def is_even(objct):
    if is_.an_integer(objct) or isinstance(objct, Decimal):
        if objct % 2 == 0:
            return True
        else:
            return False

    elif isinstance(objct, core.base_calculus.Item) and objct.is_numeric():
        return is_even(objct.value)

    elif isinstance(objct, core.base_calculus.Value) and objct.is_numeric():
        return is_even(objct.value)

    else:
        return False





# ------------------------------------------------------ IS UNEVEN ? ----------
##
#   @brief True if objct is an uneven number|numeric Item. Otherwise, False
#   @param objct The object to test
#   @return True if objct is an uneven number|numeric Item. Otherwise, False
def is_uneven(objct):
    if is_.an_integer(objct):
        if objct % 2 == 0:
            return False
        else:
            return True

    elif isinstance(objct, core.base_calculus.Item) and objct.is_numeric():
        return is_uneven(objct.value)

    elif isinstance(objct, core.base_calculus.Value) and objct.is_numeric():
        return is_uneven(objct.value)

    else:
        return False





# ------------------------------- ANGLES' UNITS CONVERSION FUNCTIONS ----------
##
#   @brief Conversions between degrees and radians
def deg_to_rad(arg):
    if not is_.a_number(arg):
        raise error.WrongArgument(' a number ', str(type(arg)))

    return arg*math.pi/180





# ------------------------------- ANGLES' UNITS CONVERSION FUNCTIONS ----------
##
#   @brief Conversions between degrees and radians
def rad_to_deg(arg):
    if not is_.a_number(arg):
        raise error.WrongArgument(' a number ', str(type(arg)))

    return arg*180/math.pi





# ---------------------------------------- MEAN OF A LIST OF NUMBERS ----------
##
#   @brief Mean of a list of numbers
def mean(numberList):
    if not type(numberList) == list:
        raise error.WrongArgument(' a list ', str(type(arg)))

    if len(numberList) == 0:
        raise error.WrongArgument(' a list of length > 0 ', ' an empty list ')

    for i in xrange(len(numberList)):
        if not is_.a_number(numberList[i]):
            raise error.WrongArgument(' a number ', str(type(numberList[i])))

    decimalNums = [Decimal(str(x)) for x in numberList]

    return Decimal(str(sum(decimalNums) / len(numberList)))





# ------------------------------------------- BARYCENTER OF n POINTS ----------
##
#   @brief Barycenter of a list of Points
def barycenter(points_list, barycenter_name):
    if not type(points_list) == list:
        raise error.WrongArgument(' a list ', str(type(points_list)))

    if len(points_list) == 0:
        raise error.WrongArgument(' a list of length > 0 ', ' an empty list ')

    for i in xrange(len(points_list)):
        if not isinstance(points_list[i], core.base_geometry.Point):
            raise error.WrongArgument(' a Point ', str(type(points_list[i])))

    if not type(barycenter_name) == str:
        raise error.WrongArgument(' a str ', str(type(barycenter_name)))

    abscissas_list = [P.x_exact for P in points_list]
    ordinates_list = [P.y_exact for P in points_list]

    return core.base_geometry.Point([barycenter_name, (mean(abscissas_list),
                                    mean(ordinates_list)
                                   )
                 ])





# ----------------------------------------------- ROUNDING A DECIMAL ----------
##
#   @brief Rounds correctly a Decimal
#   @options They are the same as the decimal's module quantize() method
def round(d, precision, **options):
    if not isinstance(d, Decimal):
        raise error.WrongArgument(str(type(d)), "a Decimal")

    return utils.correct_normalize_results(d.quantize(precision, **options))





