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

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @package error
# @brief This contains all exceptions used by this software.

import sys
sdt_err_output = sys.stderr.fileno()


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception UnreachableData
# @brief Raised if a searched for data can't be found.
class UnreachableData(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "Can't find: " + str(self.data)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception MethodShouldBeRedefined
# @brief Raised if one tries to use a method that should have been redefined.
class MethodShouldBeRedefined(Exception):
    def __init__(self, objct, method):
        self.objct = objct
        self.method = method

    def __str__(self):
        return "The method " + str(self.method)                              \
               + " has just been called by this type of object "              \
               + str(type(self.objct)) \
               + " that should have redefined it in order to use it."


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception NotImplementedYet
# @brief Raised if one tries to use a portion of code that is not written yet.
class NotImplementedYet(Exception):
    def __init__(self, method):
        self.method = method

    def __str__(self):
        return "The method " + str(self.method)                              \
               + " must handle with a case that is not implemented yet!"


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception NotInstanciableObject
# @brief Raised if one tries to instanciate a non instanciable object.
class NotInstanciableObject(Exception):
    def __init__(self, objct):
        self.objct = objct

    def __str__(self):
        return "It is not allowed to instanciate this type of objects: "     \
               + str(type(self.objet))


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception OutOfRangeArgument
# @brief Raised if the value of an argument is out of the expected range.
class OutOfRangeArgument(Exception):
    def __init__(self, objct, expected_range):
        self.objct = objct
        self.expected_range = expected_range

    def __str__(self):
        return "\nValue of the given argument is out " \
               + "of expected range or values: "      \
               + str(self.objct)                                        \
               + ".\nExpected range is: "                                    \
               + str(self.expected_range)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception UncompatibleObjects
# @brief Raised if one tries to manage two objects in a unconvenient way
# For example if you try to add an Equation and a Number
class UncompatibleObjects(Exception):
    def __init__(self, objct1, objct2, given_action, expected_result):
        self.objct1 = objct1
        self.objct2 = objct2
        self.given_action = given_action
        self.expected_result = self.expected_result

    def __str__(self):
        return "The following action is attempted: " + str(self.given_action)\
               + " on " + str(self.objct1)                                    \
               + " and " + str(self.objct2)                                   \
               + " and expects this result: " + str(self.expected_result)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception UncompatibleType
# @brief Raised if an object isn't from the expected type.
class UncompatibleType(Exception):
    def __init__(self, objct, possible_types):
        self.objct = objct
        self.possible_types = possible_types

    def __str__(self):
        return "One tries to use an object from unexpected type: "           \
               + str(type(self.objct))                                        \
               + ". Usable types here are: "                                 \
               + str(self.possible_types)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception UncompatibleOptions
# @brief Raised if two options are used together when it's not desired
class UncompatibleOptions(Exception):
    def __init__(self, opt1, opt2):
        self.opt1 = opt1
        self.opt2 = opt2

    def __str__(self):
        return "One tries to use these two uncompatible options: #1: "      \
               + str(self.opt1)                                        \
               + " and #2: "                                 \
               + str(self.opt2)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception UnknownOutputFormat
# @brief Raised if the given format isn't available yet.
class UnknownOutputFormat(Exception):
    def __init__(self, given_format):
        self.given_format = given_format

    def __str__(self):
        return str(self.given_format) + " isn't available yet."


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception ArgumentNeeded
# @brief Raised if an argument was expected.
class ArgumentNeeded(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "Expected: " + str(self.data)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception ImpossibleAction
# @brief Raised if the programm is asked something impossible.
class ImpossibleAction(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "Impossible to " + str(self.data)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception WrongObject
# @brief Raised if an error in an object has been found.
class WrongObject(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "Cause of the error: " + str(self.data)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception WrongArgument
# @brief Raised if a given argument doesn't match what was expected.
class WrongArgument(Exception):
    def __init__(self, given_arg, expected_arg):
        self.given_arg = given_arg
        self.expected_arg = expected_arg

    def __str__(self):
        return "This kind of argument was given: " + str(self.given_arg) \
               + "\nbut this argument was expected: " + str(self.expected_arg)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception UnknownXMLTag
# @brief Raised when a tag out of the expected list is read from an XML file.
class UnknownXMLTag(Exception):
    def __init__(self, given_tag):
        self.given_tag = given_tag

    def __str__(self):
        return "This unknown tag was read from the file: "\
               + str(self.given_tag)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @exception XMLFileFormatError
# @brief Raised when something is wrong in an XML file.
class XMLFileFormatError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
