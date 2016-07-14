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

import decimal


# --------------------------------------------------------------------------
##
#   @brief True if argument is a string
#   @param objct The object to test
#   @return True if argument is a string
def a_string(objct):
    if type(objct) == str:
        return True
    else:
        return False


# --------------------------------------------------------------------------
##
#   @brief True if argument is a string containing only numbers 0-9, -, + or .
#   @param objct The object to test
#   @return True if argument is a string
def a_numerical_string(objct):
    if type(objct) == str and objct != "" and objct != '...':
        return all(o in ['+', '-', '.', '0', '1', '2', '3', '4', '5',
                         '6', '7', '8', '9'] for o in objct)
    else:
        return False


# --------------------------------------------------------------------------
##
#   @brief True if argument is a list containing only strings
#   @param objct The object to test
#   @return True if argument is a list containing only strings
def a_string_list(objct):
    if type(objct) != list:
        return False

    for i in range(len(objct)):
        if type(objct[i]) != str:
            return False

    return True


# --------------------------------------------------------------------------
##
#   @brief True if argument is an ordered Exponented objects list
#   @param provided_list The list to check
#   @return True if argument is an ordered Exponented objects list
def an_ordered_calculable_objects_list(provided_list):
    # Caution, the provided list must contain only Exponented objects that
    # can be ordered with the Exponented.alphabetical_order_cmp() function
    for i in range(len(provided_list)):
        if i < len(provided_list) - 1:
            if (provided_list[i].alphabetical_order_cmp(
                provided_list[i + 1]) > 0):
                # __
                return False

    return True


# --------------------------------------------------------------------------
##
#   @brief True if argument is a sign ('+' or '-')
#   @param objct The object to test
#   @return True if argument is a sign ('+' or '-')
def a_sign(objct):
    if (objct == '+') or (objct == '-'):
        return True
    else:
        return False


# --------------------------------------------------------------------------
##
#   @brief True if the argument is a number
#   @param objct The object to test
#   @todo Maybe add other kind of objects like fractions ??...
#   @return True if the argument is a number
def a_number(objct):
    return type(objct) in [float, int, decimal.Decimal]


# --------------------------------------------------------------------------
##
#   @brief True if argument is an int or a decimal.Decimal containing an int
#   @param objct The object to test
#   @return True if argument is an int or a decimal.Decimal containing an int
def an_integer(objct):
    if (type(objct) == int):
        return True
    elif isinstance(objct, decimal.Decimal):
        return objct - objct.to_integral_exact() == 0
    else:
        return False


# --------------------------------------------------------------------------
##
#   @brief True if argument is an int
#   @param objct The object to test
#   @return True if argument is an int
def an_int(objct):
    if (type(objct) == int):
        return True
    else:
        return False


# --------------------------------------------------------------------------
##
#   @brief True if the argument is a natural int (e.g. positive)
#   @param objct The object to test
#   @return True if the argument is a natural int (e.g. positive)
def a_natural_int(objct):
    if (type(objct) == int):
        if objct >= 0:
            return True
        else:
            return False
    else:
        return False
