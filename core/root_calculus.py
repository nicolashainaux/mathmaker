# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets with their answers
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

# -----------------------------------------------------------------------------
# ---------------------------------- PACKAGE:  core.root_calculus -------------
# -----------------------------------------------------------------------------
##
# @package core.root_calculus
# @brief Mostly abstract classes for mathematical calculus objects.
import locale
import math
from decimal import *

import core
from base import *

# -----------------------------------------------------------------------------
# ----------------------------------------------- CLASS: Displayable ----------
# -----------------------------------------------------------------------------
##
# @class Displayable
# @brief Abstract mother class of all (displayable) mathematical objects
# It is not possible to implement any Displayable object
class Displayable(Printable):




    # -------------------------------- IS EQUIVALENT TO A SINGLE 1 ? ----------
    ##
    #   @brief True if the object can be displayed as a single 1
    # For instance, the Product 1×1×1×1 or the Sum 0 + 0 + 1 + 0
    def is_displ_as_a_single_1(self):
        raise error.MethodShouldBeRedefined(self,
                                            'is_displ_as_a_single_1')





    # ---------------------------- IS EQUIVALENT TO A SINGLE INT ? ----------
    ##
    #   @brief True if the object can be displayed as a single int
    def is_displ_as_a_single_int(self):
        raise error.MethodShouldBeRedefined(self,
                                            'is_displ_as_a_single_1')





    # ------------------------------- IS EQUIVALENT TO A SINGLE -1 ? ----------
    ##
    #   @brief True if the object can be displayed as a single -1
    # For instance, the Product 1×1×(-1)×1 or the Sum 0 + 0 - 1 + 0
    def is_displ_as_a_single_minus_1(self):
        raise error.MethodShouldBeRedefined(self,
                                           'is_displ_as_a_single_minus_1')





    # -------------------------------- IS EQUIVALENT TO A SINGLE 0 ? ----------
    ##
    #   @brief True if the object can be displayed as a single 0
    # For instance, the Product 0×0×0×0 (but not 0×1)
    # or the Sum 0 + 0 + 0 (but not 0 + 1 - 1)
    def is_displ_as_a_single_0(self):
        raise error.MethodShouldBeRedefined(self,
                                            'is_displ_as_a_single_0')





    # --------------------- IS EQUIVALENT TO A SINGLE NUMERIC ITEM ? ----------
    ##
    #   @brief True if the object is or only contains one numeric Item
    def is_displ_as_a_single_numeric_Item(self):
        raise error.MethodShouldBeRedefined(self,
                                      'is_displ_as_a_single_numeric_Item')





    # ------- CHECK IF A × IS REQUIRED BETWEEN SELF & ANOTHER FACTOR ----------
    ##
    #   @brief True if the usual writing rules require a × between two factors
    #   @param objct The other one
    #   @param position The position (integer) of self in the Product
    #   @return True if the writing rules require × between self & obj
    def multiply_symbol_is_required(self, objct, position):
        raise error.MethodShouldBeRedefined(self,
                                            'multiply_symbol_is_required')





    # ----------------------- CHECK IF A FACTOR REQUIRES PARENTHESIS ----------
    ##
    #   @brief True if the argument requires brackets in a product
    #   For instance, a Sum with several terms or a negative Item
    #   @param position The position of the object in the Product
    #   @return True if the object requires brackets in a Product
    def requires_brackets(self, position):
        raise error.MethodShouldBeRedefined(self, 'requires_brackets')





    # --------------------------------- REQUIRES INNER PARENTHESIS ? ----------
    ##
    #   @brief True if the argument requires inner brackets
    #   The reason for requiring them is having an exponent different
    #   from 1 and several terms or factors (in the case of Products & Sums)
    #   @return True if the object requires inner brackets
    def requires_inner_brackets(self):
        raise error.MethodShouldBeRedefined(self,
                                            'requires_innner_brackets')





