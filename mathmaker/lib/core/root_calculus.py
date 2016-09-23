# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets with their answers
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
# @package core.root_calculus
# @brief Mostly abstract classes for mathematical calculus objects.

import copy
import locale
from decimal import Decimal, getcontext, Rounded, ROUND_HALF_UP, ROUND_DOWN

from mathmaker.lib.maths_lib import round
from mathmaker.lib.common.cst import (UNIT, TENTH, HUNDREDTH, THOUSANDTH,
                                      TEN_THOUSANDTH, PRECISION,
                                      PRECISION_REVERSED,
                                      VALUE_AND_UNIT_SEPARATOR)
from mathmaker.lib.common import alphabet
from mathmaker.lib.core.base import Printable
from mathmaker.lib import is_, error
from mathmaker.lib.common.latex import MARKUP


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Evaluable
# @brief Abstract mother class of all (evaluable) mathematical objects
# It is not possible to implement any Evaluable object
class Evaluable(Printable):

    # --------------------------------------------------------------------------
    ##
    #   @brief If the object is literal, returns the first letter
    # The first term of a Sum, the first factor of a Product etc.
    def get_first_letter(self):
        raise error.MethodShouldBeRedefined(self, 'get_first_letter')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the numeric value of the object
    def evaluate(self):
        raise error.MethodShouldBeRedefined(self, 'evaluate')

    # --------------------------------------------------------------------------
    ##
    #   @brief To check if this contains a rounded number...
    #   @return True or False
    def contains_a_rounded_number(self):
        raise error.MethodShouldBeRedefined(self, 'contains_a_rounded_number')

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object contains exactly the given objct
    #   It can be used to detect objects embedded in a Sum or a Product that
    #   contain only one term (or factor)
    #   @param objct The object to search for
    #   @return True if the object contains exactly the given objct
    def contains_exactly(self, objct):
        raise error.MethodShouldBeRedefined(self, 'contains_exactly')

    # --------------------------------------------------------------------------
    ##
    #   @brief Sort order: numerics < sorted literals
    #   @return -1, 0 or +1
    def alphabetical_order_cmp(self, other_objct):

        if self.is_numeric() and other_objct.is_numeric():
            return 0

        elif self.is_literal() and other_objct.is_numeric():
            return 1

        elif self.is_numeric() and other_objct.is_literal():
            return -1

        elif self.is_literal() and other_objct.is_literal():
            self_value = self.get_first_letter()
            other_value = other_objct.get_first_letter()

            # let's compare
            if self_value == other_value:
                return 0
            elif alphabet.order[self_value] > alphabet.order[other_value]:
                return 1
            else:
                return -1

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object only contains numeric objects
    def is_numeric(self):
        raise error.MethodShouldBeRedefined(self, 'is_numeric')

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object only contains literal objects
    def is_literal(self):
        raise error.MethodShouldBeRedefined(self, 'is_literal')

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the evaluated value of an object is null
    def is_null(self):
        raise error.MethodShouldBeRedefined(self, 'is_null')


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Calculable
# @brief Abstract mother class of all (calculable) mathematical objects
# It is not possible to implement any Calculable object
class Calculable(Evaluable):

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the list of elements to iter over
    def get_iteration_list(self):
        raise error.MethodShouldBeRedefined(self, 'get_iteration_list')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the next Calculable object during a numeric calculation
    def calculate_next_step(self, **options):
        raise error.MethodShouldBeRedefined(self, 'calculate_next_step')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the next step of expansion/reduction of the Sum
    #   So, either the Sum of its expanded/reduced terms,
    #   or the Sum itself reduced, or None
    #   @return Exponented
    def expand_and_reduce_next_step(self, **options):
        raise error.MethodShouldBeRedefined(self,
                                            'expand_and_reduce_next_step')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the number of elements of the Exponented
    def __len__(self):
        raise error.MethodShouldBeRedefined(self, "__len__()")

    # --------------------------------------------------------------------------
    ##
    #   @brief This will iter over the content of the Calculable
    def __iter__(self):
        return iter(self.get_iteration_list())

    def __next__(self):
        return next(self.get_iteration_list())

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the usual writing rules require a × between two factors
    #   @param objct The other one
    #   @param position The position (integer) of self in the Product
    #   @return True if the writing rules require × between self & obj
    def multiply_symbol_is_required(self, objct, position):
        raise error.MethodShouldBeRedefined(self,
                                            'multiply_symbol_is_required')

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the argument requires brackets in a product
    #   For instance, a Sum with several terms or a negative Item
    #   @param position The position of the object in the Product
    #   @return True if the object requires brackets in a Product
    def requires_brackets(self, position):
        raise error.MethodShouldBeRedefined(self, 'requires_brackets')

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the argument requires inner brackets
    #   The reason for requiring them is having an exponent different
    #   from 1 and several terms or factors (in the case of Products & Sums)
    #   @return True if the object requires inner brackets
    def requires_inner_brackets(self):
        raise error.MethodShouldBeRedefined(self,
                                            'requires_innner_brackets')

    # --------------------------------------------------------------------------
    ##
    #   @brief Uses the given lexicon to substitute literal Values in self
    def substitute(self, subst_dict):
        for elt in self:
            elt.substitute(subst_dict)

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single 1
    # For instance, the Product 1×1×1×1 or the Sum 0 + 0 + 1 + 0
    def is_displ_as_a_single_1(self):
        raise error.MethodShouldBeRedefined(self,
                                            'is_displ_as_a_single_1')

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single int
    def is_displ_as_a_single_int(self):
        raise error.MethodShouldBeRedefined(self,
                                            'is_displ_as_a_single_1')

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single -1
    # For instance, the Product 1×1×(-1)×1 or the Sum 0 + 0 - 1 + 0
    def is_displ_as_a_single_minus_1(self):
        raise error.MethodShouldBeRedefined(self,
                                            'is_displ_as_a_single_minus_1')

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single 0
    # For instance, the Product 0×0×0×0 (but not 0×1)
    # or the Sum 0 + 0 + 0 (but not 0 + 1 - 1)
    def is_displ_as_a_single_0(self):
        raise error.MethodShouldBeRedefined(self,
                                            'is_displ_as_a_single_0')

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object is or only contains one numeric Item
    def is_displ_as_a_single_numeric_Item(self):
        raise error.MethodShouldBeRedefined(self, 'is_displ_as_a_single'
                                                  '_numeric_Item')

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be considered as a neutral element
    def is_displ_as_a_single_neutral(self, elt):
        raise error.MethodShouldBeRedefined(self, 'is_displ_as_a_single'
                                                  '_neutral')


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Signed
# @brief Signed objects: CommutativeOperations (Sums&Products), Items,
#        Quotients...
# Any Signed must have a sign field
class Signed(Calculable):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @return A Signed, though it can't really be used as is
    def __init__(self):
        self._sign = '+'

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the number of minus signs in the object
    def get_minus_signs_nb(self):
        raise error.MethodShouldBeRedefined(self, 'get_minus_signs_nb')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the sign of the object
    def get_sign(self):
        return self._sign
    # --------------------------------------------------------------------------
    sign = property(get_sign,
                    doc="Sign of the object")

    # --------------------------------------------------------------------------
    ##
    #   @brief Set the sign of the object
    #   @param  arg String being '+' or '-' or number being +1 or -1
    #   @warning Relays an exception if arg is not of the types described
    def set_sign(self, arg):
        if is_.a_sign(arg):
            self._sign = arg
        elif arg == 1:
            self._sign = '+'
        elif arg == -1:
            self._sign = '-'
        elif isinstance(arg, Calculable):
            if arg.is_displ_as_a_single_1():
                self._sign = '+'
            elif arg.is_displ_as_a_single_minus_1():
                self._sign = '-'
        else:
            raise error.UncompatibleType(self, "'+' or '-' or 1 or -1")

    # --------------------------------------------------------------------------
    ##
    #   @brief Changes the sign of the object
    def set_opposite_sign(self):
        if self.get_sign() == '-':
            self.set_sign('+')
        elif self.get_sign() == '+':
            self.set_sign('-')
        else:
            # this case should never happen, just to secure the code
            raise error.WrongObject("The sign of the object "
                                    + repr(self)
                                    + " is "
                                    + str(self.sign)
                                    + " instead of '+' or '-'.")

    # --------------------------------------------------------------------------
    ##
    #   @brief True if object's *sign* is '-' (ie -(-1) would be "negative")
    def is_negative(self):
        return self.sign == '-'

    # --------------------------------------------------------------------------
    ##
    #   @brief True if object's *sign* is '+'
    def is_positive(self):
        return self.sign == '+'


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Value
# @brief This class embedds Numbers & Strings into a basic object. It doesn't
#        have any exponent field (always set to 1), so does not belong to
#        Exponenteds. This is the only place where numbers are used directly.
#        The Item class for instance, contains Values in its fields, not
#        numbers.
#        This to be sure any content of any field (even if only a simple
#        number is to be saved in the field) can be tested & managed
#        as an object in any other class than Value.
#        Up from 2010/11/19, it is decided that all numeric Values will contain
#        a Decimal.decimal number.
class Value(Signed):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @warning Might raise an UncompatibleType exception
    #            or InvalidOperation
    #   @param arg Number|String
    #   If the argument is not of one of these kinds, an exception
    #   will be raised.
    #   @return One instance of Value
    def __init__(self, arg, **options):
        Signed.__init__(self)

        self._has_been_rounded = False

        self._unit = ""

        if 'unit' in options:
            self._unit = Unit(options['unit'])

        if (type(arg) == float
            or type(arg) == int
            or type(arg) == Decimal):
            # __
            self._raw_value = Decimal(str(arg))
            if arg >= 0:
                self._sign = '+'
            else:
                self._sign = '-'

        elif type(arg) == str:
            if is_.a_numerical_string(arg):
                self._raw_value = Decimal(arg)
            else:
                self._raw_value = arg

            if len(arg) >= 1 and arg[0] == '-':
                self._sign = '-'

        elif isinstance(arg, Value):
            self._raw_value = arg.raw_value
            self._has_been_rounded = arg.has_been_rounded
            self._unit = arg.unit
            self._sign = arg.sign

        # All other unforeseen cases: an exception is raised.
        else:
            raise error.UncompatibleType(arg, "Number|String")

        if self._sign == '-':
            if isinstance(self._raw_value, str):
                self._abs_value = self._raw_value[1:]
            else:
                self._abs_value = - self._raw_value
        else:
            self._abs_value = self._raw_value

    # --------------------------------------------------------------------------
    ##
    #   @brief If the object is literal, returns the value
    def get_first_letter(self):
        if self.is_literal():
            return self.raw_value
        else:
            raise error.UncompatibleType(self, "str, i.e. literal Value")

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the "has been rounded" state of the Value
    def get_has_been_rounded(self):
        return self._has_been_rounded

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the list of elements to iter over
    def get_iteration_list(self):
        return [self.raw_value]

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the number of minus signs in the object
    def get_minus_signs_nb(self):
        raise error.MethodShouldBeRedefined(self, 'get_minus_signs_nb')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the raw value contained in the Value
    def get_raw_value(self):
        return self._raw_value

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the sign of the Value
    def get_sign(self):
        return self._sign

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the unit of the Value
    def get_unit(self):
        return self._unit

    @property
    def abs_value(self):
        return self._abs_value

    raw_value = property(get_raw_value,
                         doc="Raw value of the object")
    has_been_rounded = property(get_has_been_rounded,
                                doc="'has been rounded' state of the Value")
    sign = property(get_sign,
                    doc="Sign of the Value")

    unit = property(get_unit,
                    doc="Unit of the Value")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the "has been rounded" state of the Value
    def set_has_been_rounded(self, arg):
        if arg not in [True, False]:
            raise error.WrongArgument(str(type(arg)), "True|False")
        else:
            self._has_been_rounded = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Set the sign of the object
    #   @param  arg String being '+' or '-' or number being +1 or -1
    #   @warning Relays an exception if arg is not of the types described
    def set_sign(self, arg):
        if is_.a_sign(arg):
            self._sign = arg
        elif arg == 1:
            self._sign = '+'
        elif arg == -1:
            self._sign = '-'
        elif isinstance(arg, Calculable):
            if arg.is_displ_as_a_single_1():
                self._sign = '+'
            elif arg.is_displ_as_a_single_minus_1():
                self._sign = '-'
        else:
            raise error.UncompatibleType(self, "'+' or '-' or 1 or -1")

    # --------------------------------------------------------------------------
    ##
    #   @brief Set the unit of the Value
    #   @param  arg String
    def set_unit(self, arg):
        self._unit = Unit(arg)

    # --------------------------------------------------------------------------
    ##
    #   @brief Changes the sign of the object
    def set_opposite_sign(self):
        if self.get_sign() == '-':
            self.set_sign('+')
        elif self.get_sign() == '+':
            self.set_sign('-')
        else:
            # this case should never happen, just to secure the code
            raise error.WrongObject("The sign of the object "
                                    + repr(self)
                                    + " is "
                                    + str(self.sign)
                                    + " instead of '+' or '-'.")

    # --------------------------------------------------------------------------
    ##
    #   @brief Temporary shortcut for into_str()
    def __str__(self, **options):
        return self.into_str(**options)

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        sign = ''
        if self._sign == '-':
            sign = '-'

        if self.is_numeric():
            if 'display_unit' in options and options['display_unit']:
                unit_str = self.unit.into_str(**options) \
                    if isinstance(self.unit, Unit) \
                    else str(self.unit)
                return sign + locale.str(self.abs_value) + unit_str
            elif 'display_SI_unit' in options and options['display_SI_unit']:
                unit_str = self.unit.into_str(**options) \
                    if isinstance(self.unit, Unit) \
                    else str(self.unit)
                return sign + "\SI{" + locale.str(self.abs_value) + "}"\
                    "{" + unit_str + "}"
            else:
                return sign + MARKUP['open_text_in_maths'] \
                    + locale.str(self.abs_value) \
                    + MARKUP['close_text_in_maths']

        elif (self.raw_value in ["", " "] and 'display_SI_unit' in options
              and options['display_SI_unit']):
            # __
            unit_str = self.unit.into_str(**options) \
                if isinstance(self.unit, Unit) \
                else str(self.unit)
            return sign + "\SI{" + self.abs_value + "}"\
                "{" + unit_str + "}"

        else:  # self.is_literal()
            if (len(self.get_first_letter()) >= 2
                and not self.get_first_letter()[0] in ["-", "+"]):
                # __
                return sign + MARKUP['open_text_in_maths'] \
                    + str(self.abs_value) \
                    + MARKUP['close_text_in_maths']
            else:
                return str(self.raw_value)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the value of a numeric Value
    #   @warning Raise an exception if not numeric
    def evaluate(self):
        if not self.is_numeric():
            raise error.UncompatibleType(self, "numeric Value")
        else:
            return self.raw_value

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns None
    def calculate_next_step(self, **options):
        return None

    # --------------------------------------------------------------------------
    ##
    #   @brief Debugging method to print the Value
    def __repr__(self, **options):
        return "." + str(self.raw_value) + "."

    # --------------------------------------------------------------------------
    ##
    #   @brief Compares two Values
    #   @todo check if __eq__ shouldn't return +1 if value of self > objct
    #   @todo comparison directly with numbers... (see alphabetical_order_cmp)
    #   @return True if they're equal
    def __eq__(self, other_value):
        if not isinstance(other_value, Value):
            return False

        if self.raw_value == other_value.raw_value:
            return True
        else:
            return False

    def __ne__(self, other_value):
        """Basically the contrary of __eq__, to allow comparisons with !="""
        return not self.__eq__(other_value)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Value's length
    #   @return 1
    def __len__(self):
        return 1

    # --------------------------------------------------------------------------
    ##
    #   @brief Makes Values hashable (so, usable as dictionnary keys)
    def __hash__(self):
        return hash(str(self.sign) + str(self.raw_value)
                    + str(self.has_been_rounded) + str(self.unit))

    # --------------------------------------------------------------------------
    ##
    #   @brief Executes the multiplication with another object
    #   @warning Will raise an error if you try to multiply a literal
    #            with a number
    def __mul__(self, objct):
        if isinstance(objct, Calculable):
            return self.raw_value * objct.evaluate()
        else:
            return self.raw_value * objct

    # --------------------------------------------------------------------------
    ##
    #   @brief Executes the addition with another object
    #   @warning Will raise an error if you try to add a literal with a number
    def __add__(self, objct):
        if isinstance(objct, Calculable):
            return self.raw_value + objct.evaluate()
        else:
            return self.raw_value + objct

    def __sub__(self, v):
        """
        Return the difference between self and another Value, as a Value.

        :param v: the Value to substract of self
        :type v: Value
        :rtype: Value
        """
        if isinstance(v, Value):
            return Value(self.raw_value - v.raw_value)
        else:
            raise TypeError('TypeError: unsupported operand type(s) for -:'
                            ' \'Value\' and \'{}\''
                            .format(str(type(v))))

    # --------------------------------------------------------------------------
    ##
    #   @brief Uses the given lexicon to substitute literal Values in self
    def substitute(self, subst_dict):
        if self.is_literal():
            for key in subst_dict:
                if self == key:
                    self.__init__(subst_dict[key])
        else:
            pass

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns a Value containing the square root of self
    def sqrt(self):
        if self.is_numeric():
            return Value(self.raw_value.sqrt())
        else:
            raise error.UncompatibleType(self, "numeric Value")

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the value once rounded to the given precision
    def round(self, precision):
        if not self.is_numeric():
            raise error.UncompatibleType(self, "numeric Value")
        elif (not (precision in [UNIT, TENTH, HUNDREDTH, THOUSANDTH,
                                 TEN_THOUSANDTH]
              or (type(precision) == int and 0 <= precision <= 4))):
            # __
            raise error.UncompatibleType(precision, "must be UNIT or"
                                                    + "TENTH, "
                                                    + "HUNDREDTH, "
                                                    + "THOUSANDTH, "
                                                    + "TEN_THOUSANDTH, "
                                                    + "or 0, 1, 2, 3 or 4.")
        else:
            result_value = None

            if type(precision) == int:
                result_value = Value(round(self.raw_value,
                                           Decimal(PRECISION[precision]),
                                           rounding=ROUND_HALF_UP))
            else:
                result_value = Value(round(self.raw_value,
                                           Decimal(precision),
                                           rounding=ROUND_HALF_UP))

            if self.needs_to_get_rounded(precision):
                result_value.set_has_been_rounded(True)

            return result_value

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the number of digits of a numerical value
    def digits_number(self):
        if not self.is_numeric():
            raise error.UncompatibleType(self, "numeric Value")
        else:
            temp_result = len(str((self.raw_value
                                   - round(self.raw_value,
                                           Decimal(UNIT),
                                           rounding=ROUND_DOWN)))) - 2
            if temp_result < 0:
                return 0
            else:
                return temp_result

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns True/False depending on the need of the value to get
    #          rounded (for instance 2.68 doesn't need to get rounded if
    #          precision is HUNDREDTH or more, but needs it if it is less)
    def needs_to_get_rounded(self, precision):
        if (not (precision in [UNIT, TENTH, HUNDREDTH, THOUSANDTH,
                               TEN_THOUSANDTH]
            or (type(precision) == int and 0 <= precision <= 4))):
            # __
            raise error.UncompatibleType(precision, "must be UNIT or"
                                                    + "TENTH, "
                                                    + "HUNDREDTH, "
                                                    + "THOUSANDTH, "
                                                    + "TEN_THOUSANDTH, "
                                                    + "or 0, 1, 2, 3 or 4.")

        precision_to_test = 0

        if type(precision) == int:
            precision_to_test = precision
        else:
            precision_to_test = PRECISION_REVERSED[precision]

        return self.digits_number() > precision_to_test

    # --------------------------------------------------------------------------
    ##
    #   @brief To check if this contains a rounded number...
    #   @return True or False depending on the Value inside
    def contains_a_rounded_number(self):
        return self.has_been_rounded

    # --------------------------------------------------------------------------
    ##
    #   @brief Always False for a Value
    #   @param objct The object to search for
    #   @return False
    def contains_exactly(self, objct):
        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief  True if the object contains a perfect square
    #           (integer or decimal)
    def is_a_perfect_square(self):
        if not self.is_numeric():
            raise error.UncompatibleType(self, "numeric Value")

        if self.is_an_integer():
            return not self.sqrt().needs_to_get_rounded(0)
        else:
            return len(str(self.raw_value)) > len(str(self.raw_value.sqrt()))

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object contains an integer (numeric)
    def is_an_integer(self):
        if not self.is_numeric():
            raise error.UncompatibleType(self, "numeric Value")
        getcontext().clear_flags()
        self.raw_value.to_integral_exact()
        return getcontext().flags[Rounded] == 0

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object only contains numeric objects
    def is_numeric(self):
        return type(self.raw_value) in [float, int, Decimal]

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object only contains literal objects
    def is_literal(self):
        if type(self.raw_value) == str:
            # __
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the evaluated value of an object is null
    def is_null(self):
        if self.is_numeric() and self.raw_value == 0:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single 1
    def is_displ_as_a_single_1(self):
        if self.is_numeric() and self.raw_value == 1:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single -1
    def is_displ_as_a_single_minus_1(self):
        if self.is_numeric() and self.raw_value == -1:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single 0
    def is_displ_as_a_single_0(self):
        if self.is_numeric() and self.raw_value == 0:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object is or only contains one numeric Item
    def is_displ_as_a_single_numeric_Item(self):
        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single int
    def is_displ_as_a_single_int(self):
        return self.is_numeric() and self.is_an_integer()


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Exponented
# @brief Exponented objects: CommutativeOperations (Sums&Products), Items,
#           Quotients...
# Any Exponented must have a exponent field and should reimplement the
# methods that are not already defined hereafter
class Exponented(Signed):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @return An Exponented, though it can't really be used as is
    def __init__(self):
        Signed.__init__(self)
        self._exponent = Value(1)

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the exponent of the Function
    #   @brief this should be already done by Item.get_exponent()...
    def get_exponent(self):
        return self._exponent
    # --------------------------------------------------------------------------
    exponent = property(get_exponent, doc="Exponent of the Function")

    # --------------------------------------------------------------------------
    ##
    #   @brief Set the value of the exponent
    #   @param  arg Calculable|Number|String
    #   @warning Relays an exception if arg is not of the types described
    def set_exponent(self, arg):
        if isinstance(arg, Calculable):
            self._exponent = arg.clone()
        else:
            self._exponent = Value(arg)

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the exponent isn't equivalent to a single 1
    #   @return True if the exponent is not equivalent to a single 1
    def exponent_must_be_displayed(self):
        if not self.exponent.is_displ_as_a_single_1():
            return True
        else:
            return False


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Unit
# @brief This class is used to handle with units.
class Unit(Exponented):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @return One instance of Unit
    def __init__(self, arg, **options):
        Exponented.__init__(self)

        if type(arg) == str:
            self._name = arg
            if 'exponent' in options:
                self._exponent = Value(options['exponent'])

        elif type(arg) == Unit:
            self._name = copy.deepcopy(arg.name)
            self._exponent = copy.deepcopy(arg.exponent)

        else:
            raise error.WrongArgument(arg, "a string or a Unit")

    @property
    def name(self):
        return self._name

    @property
    def exponent(self):
        return self._exponent

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):

        text_box_open = MARKUP['open_text_in_maths']
        text_box_close = MARKUP['close_text_in_maths']

        if ('graphic_display' in options and options['graphic_display']
            or 'display_SI_unit' in options):
            # __
            text_box_open = ""
            text_box_close = ""

        exponent = ""

        if self.exponent != Value(1):
            exponent = MARKUP['opening_exponent'] \
                + str(self.exponent) \
                + MARKUP['closing_exponent']

        separator = VALUE_AND_UNIT_SEPARATOR[self.name] \
            if 'display_SI_unit' not in options \
            else ""

        return separator + text_box_open + self.name \
            + text_box_close + exponent
