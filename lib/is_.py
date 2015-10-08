# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

from . import error
from .common import cfg
import math
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
        for i in range(len(objct)):
            if not(objct[i] == '+' \
               or objct[i] == '-' \
               or objct[i] == '.' \
               or objct[i] == '0' \
               or objct[i] == '1' \
               or objct[i] == '2' \
               or objct[i] == '3' \
               or objct[i] == '4' \
               or objct[i] == '5' \
               or objct[i] == '6' \
               or objct[i] == '7' \
               or objct[i] == '8' \
               or objct[i] == '9'):
            #___
                return False

        return True

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
            if provided_list[i].alphabetical_order_cmp(provided_list[i+1]) > 0:
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
    if (type(objct) == float)                                                 \
      or (type(objct) == int)                                                 \
      or (type(objct) == decimal.Decimal):
        return True
    else:
        return False





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
