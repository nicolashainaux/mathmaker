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

from base import *
from lib.common import alphabet
from lib import is_
from lib.maths_lib import *
from decimal import *
from lib.common.cst import *
import locale

markup_choice = cfg.get_value_from_file('MARKUP', 'USE')

if markup_choice == 'latex':
    from lib.common.latex import MARKUP

try:
    locale.setlocale(locale.LC_ALL, LANGUAGE + '.' + ENCODING)
except:
    locale.setlocale(locale.LC_ALL, '')

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





    # -------------------------- IS EQUIVALENT TO A SINGLE NEUTRAL ? ----------
    ##
    #   @brief True if the object can be considered as a neutral element
    def is_displ_as_a_single_neutral(self, elt):
        raise error.MethodShouldBeRedefined(self,
                                      'is_displ_as_a_single_neutral')





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





# -----------------------------------------------------------------------------
# ------------------------------------------------- CLASS: Evaluable ----------
# -----------------------------------------------------------------------------
##
# @class Evaluable
# @brief Abstract mother class of all (evaluable) mathematical objects
# It is not possible to implement any Evaluable object
class Evaluable(Displayable):





    # ----------------------------------------------------- EVALUATE ----------
    ##
    #   @brief Returns the numeric value of the object
    def evaluate(self):
        raise error.MethodShouldBeRedefined(self, 'evaluate')





    # ------------------------------------------------- IS NUMERIC ? ----------
    ##
    #   @brief True if the object only contains numeric objects
    def is_numeric(self):
        raise error.MethodShouldBeRedefined(self, 'is_numeric')





    # ------------------------------------------------- IS LITERAL ? ----------
    ##
    #   @brief True if the object only contains literal objects
    def is_literal(self):
        raise error.MethodShouldBeRedefined(self, 'is_literal')





    # ---------------------------------------------------- IS NULL ? ----------
    ##
    #   @brief True if the evaluated value of an object is null
    def is_null(self):
        raise error.MethodShouldBeRedefined(self, 'is_null')





    # ------------------------------------- CONTAINS A ROUNDED NUMBER ----------
    ##
    #   @brief To check if this contains a rounded number...
    #   @return True or False
    def contains_a_rounded_number(self):
        raise error.MethodShouldBeRedefined(self, 'contains_a_rounded_number')





    # ------------------------------------------- CONTAINS EXACTLY ? ----------
    ##
    #   @brief True if the object contains exactly the given objct
    #   It can be used to detect objects embedded in a Sum or a Product that
    #   contain only one term (or factor)
    #   @param objct The object to search for
    #   @return True if the object contains exactly the given objct
    def contains_exactly(self, objct):
        raise error.MethodShouldBeRedefined(self, 'contains_exactly')





    # -------------------------------- ALPHABETICAL ORDER COMPARISON ----------
    ##
    #   @brief Sort order : numerics < sorted literals
    #   @return -1, 0 or +1
    def alphabetical_order_cmp(self, other_objct):

        if self.is_numeric() and other_objct.is_numeric():
            return 0

        elif self.is_literal() and other_objct.is_numeric():
            return 1

        elif self.is_numeric() and other_objct.is_literal():
            return -1

        elif self.is_literal() and other_objct.is_literal():
            self_value = self.get_letter()
            other_value = other_objct.get_letter()

            # let's compare
            if self_value == other_value:
                return 0
            elif alphabet.order[self_value] > alphabet.order[other_value]:
                return 1
            else:
                return -1





    # --------------------------------------------------- GET LETTER ----------
    ##
    #   @brief If the object is literal, returns the first letter
    # The first term of a Sum, the first factor of a Product etc.
    def get_letter(self):
        raise error.MethodShouldBeRedefined(self, 'get_letter')





# -----------------------------------------------------------------------------
# ------------------------------------------------ CLASS: Calculable ----------
# -----------------------------------------------------------------------------
##
# @class Calculable
# @brief Abstract mother class of all (calculable) mathematical objects
# It is not possible to implement any Calculable object
class Calculable(Evaluable):




    # ---------------------------------------------------- ITERATION ----------
    ##
    #   @brief This will iter over the content of the Calculable
    def __iter__(self):
        return iter(self.get_iteration_list())

    def next(self):
        return self.get_iteration_list().next()





    # ------------------------------------------- CALCULATE ONE STEP ----------
    ##
    #   @brief Returns the next Calculable object during a numeric calculation
    def calculate_next_step(self, **options):
        raise error.MethodShouldBeRedefined(self, 'calculate_next_step')





    # -------------------------------- EXPAND AND REDUCE : NEXT STEP ----------
    ##
    #   @brief Returns the next step of expansion/reduction of the Sum
    #   So, either the Sum of its expanded/reduced terms,
    #   or the Sum itself reduced, or None
    #   @return Exponented
    def expand_and_reduce_next_step(self, **options):
        raise error.MethodShouldBeRedefined(self,
                                            'expand_and_reduce_next_step')





    # ------------------------------------------ EXPONENTED'S LENGTH ----------
    ##
    #   @brief Returns the number of elements of the Exponented
    def __len__(self):
        raise error.MethodShouldBeRedefined(self, "__len__()")





    # --------------------------------------------------- SUBSTITUTE ----------
    ##
    #   @brief Uses the given lexicon to substitute literal Values in self
    def substitute(self, subst_dict):
        for elt in self:
            elt.substitute(subst_dict)





# -----------------------------------------------------------------------------
# ---------------------------------------------------- CLASS: Signed ----------
# -----------------------------------------------------------------------------
##
# @class Signed
# @brief Signed objects: Operations (Sums&Products), Items, Quotients...
# Any Signed must have a sign field
class Signed(Calculable):



    # -------------------------------------------------- CONSTRUCTOR ----------
    ##
    #   @brief Constructor
    #   @return A Signed, though it can't really be used as is
    def __init__(self):
        self._sign = '+'





    # ------------------------------------------------------ GET SIGN ----------
    ##
    #   @brief Returns the sign of the object
    def get_sign(self):
        return self._sign
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    sign = property(get_sign,
                    doc = "Sign of the object")





    # --------------------------------------- GET MINUS SIGNS NUMBER ----------
    ##
    #   @brief Returns the number of minus signs in the object
    def get_minus_signs_nb(self):
        raise error.MethodShouldBeRedefined(self, 'get_minus_signs_nb')





    # ------------------------------------------------------ SET SIGN ----------
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





    # --------------------------------------------- SET OPPOSITE SIGN ----------
    ##
    #   @brief Changes the sign of the object
    def set_opposite_sign(self):
        if self.get_sign() == '-':
            self.set_sign('+')
        elif self.get_sign() == '+':
            self.set_sign('-')
        else:
            # this case should never happen, just to secure the code
            raise error.WrongObject("The sign of the object " \
                                    + self.dbg_str() \
                                    + " is " \
                                    + str(self.sign) \
                                    + " instead of '+' or '-'.")





# -----------------------------------------------------------------------------
# ----------------------------------------------------- CLASS: Value ----------
# -----------------------------------------------------------------------------
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
#        a Decimal number.
class Value(Calculable):





    # -------------------------------------------------- CONSTRUCTOR ----------
    ##
    #   @brief Constructor
    #   @warning Might raise an UncompatibleType exception
    #            or InvalidOperation
    #   @param arg Number|String
    #   If the argument is not of one of these kinds, an exception
    #   will be raised.
    #   @return One instance of Value
    def __init__(self, arg, **options):
        self.has_been_rounded = False

        self.unit = ""

        if 'unit' in options and options['unit'] in AVAILABLE_UNITS:
            self.unit = options['unit']

        if type(arg) == float                                             \
            or type(arg) == int                                          \
            or type(arg) == long                                        \
            or type(arg) == Decimal:
        #___
            self.value = Decimal(str(arg))

        elif type(arg) == str:
            if is_.a_numerical_string(arg):
                self.value = Decimal(arg)
            else:
                self.value = arg

        elif isinstance(arg, Value):
            self.value = arg.value
            self.has_been_rounded = arg.has_been_rounded
            self.unit = arg.unit

        # All other unforeseen cases : an exception is raised.
        else:
            raise error.UncompatibleType(arg, "Number|String")



    # -------------------------------------------------- RAW DISPLAY ----------
    ##
    #   @brief Debugging method to print the Value
    def dbg_str(self, **options):
        return "." + str(self.value) + "."





    # ------------------------------------------- OBJECTS COMPARISON ----------
    ##
    #   @brief Compares two Values
    #   @todo check if __cmp__ shouldn't return +1 if value of self > objct
    #   @todo comparison directly with numbers... (see alphabetical_order_cmp)
    #   @return 0 (i.e. they're equal)
    def __cmp__(self, other_value):
        if not isinstance(other_value, Value):
            return -1

        if self.value == other_value.value:
            return 0
        else:
            return -1





    # ----------------------------------------------- VALUE'S LENGTH ----------
    ##
    #   @brief Returns the Value's length
    #   @return 1
    def __len__(self):
        return 1




    # ----------------------------------------------- MULTIPLICATION ----------
    ##
    #   @brief Executes the multiplication with another object
    #   @warning Will raise an error if you try to multiply a literal
    #            with a number
    def __mul__(self, objct):
        if isinstance(objct, Calculable):
            return self.value * objct.evaluate()
        else:
            return self.value * objct





    # ----------------------------------------------------- ADDITION ----------
    ##
    #   @brief Executes the addition with another object
    #   @warning Will raise an error if you try to add a literal with a number
    def __add__(self, objct):
        if isinstance(objct, Calculable):
            return self.value + objct.evaluate()
        else:
            return self.value + objct





    # ------------------------------------------------- IS NUMERIC ? ----------
    ##
    #   @brief True if the object only contains numeric objects
    def is_numeric(self):
        if type(self.value) == float                \
            or type(self.value) == int              \
            or type(self.value) == long             \
            or type(self.value) == Decimal:
        #___
            return True
        else:
            return False





    # ------------------------------------------------- IS LITERAL ? ----------
    ##
    #   @brief True if the object only contains literal objects
    def is_literal(self):
        if type(self.value) == str:
        #___
            return True
        else:
            return False





    # ------------------------------------- CONTAINS A ROUNDED NUMBER ----------
    ##
    #   @brief To check if this contains a rounded number...
    #   @return True or False depending on the Value inside
    def contains_a_rounded_number(self):
        return self.has_been_rounded






    # ------------------------------------------- CONTAINS EXACTLY ? ----------
    ##
    #   @brief Always False for a Value
    #   @param objct The object to search for
    #   @return False
    def contains_exactly(self, objct):
        return False






    # ---------------------------------------------------- IS NULL ? ----------
    ##
    #   @brief True if the evaluated value of an object is null
    def is_null(self):
        if self.is_numeric() and self.value == 0:
            return True
        else:
            return False





    # ------------------------------------------------ GET ITER LIST ----------
    ##
    #   @brief Returns the list of elements to iter over
    def get_iteration_list(self):
        return [self.value]






    # --------------------------------------------------- GET LETTER ----------
    ##
    #   @brief If the object is literal, returns the value
    def get_letter(self):
        if self.is_literal():
            return self.value
        else:
            raise error.UncompatibleType(self, "str, i.e. literal Value")






    # -------------------------------- IS EQUIVALENT TO A SINGLE 1 ? ----------
    ##
    #   @brief True if the object can be displayed as a single 1
    def is_displ_as_a_single_1(self):
        if self.is_numeric() and self.value == 1:
            return True
        else:
            return False





    # ------------------------------- IS EQUIVALENT TO A SINGLE -1 ? ----------
    ##
    #   @brief True if the object can be displayed as a single -1
    def is_displ_as_a_single_minus_1(self):
        if self.is_numeric() and self.value == -1:
            return True
        else:
            return False





    # -------------------------------- IS EQUIVALENT TO A SINGLE 0 ? ----------
    ##
    #   @brief True if the object can be displayed as a single 0
    def is_displ_as_a_single_0(self):
        if self.is_numeric() and self.value == 0:
            return True
        else:
            return False





    # --------------------- IS EQUIVALENT TO A SINGLE NUMERIC ITEM ? ----------
    ##
    #   @brief True if the object is or only contains one numeric Item
    def is_displ_as_a_single_numeric_Item(self):
        return False





    # ---------------------------- IS EQUIVALENT TO A SINGLE INT ? ----------
    ##
    #   @brief True if the object can be displayed as a single int
    def is_displ_as_a_single_int(self):
        return self.is_numeric() and self.is_an_integer()




    # ---------------------------------------- IS A PERFECT SQUARE ? ----------
    ##
    #   @brief True if the object contains a perfect square (integer or decimal)
    def is_a_perfect_square(self):
        if not self.is_numeric():
            raise error.UncompatibleType(self, "numeric Value")

        if self.is_an_integer():
            return not self.sqrt().needs_to_get_rounded(0)
        else:
            return len(str(self.value)) > len(str(self.value.sqrt()))




    # --------------------------------------------- IS AN INTEGER ? ----------
    ##
    #   @brief True if the object contains an integer (numeric)
    def is_an_integer(self):
        if not self.is_numeric():
            raise error.UncompatibleType(self, "numeric Value")

        getcontext().clear_flags()

        trash = self.value.to_integral_exact()

        return getcontext().flags[Rounded] == 0




    # ----------------------------------------------------- EVALUATE ----------
    ##
    #   @brief Returns the value of a numeric Value
    #   @warning Raise an exception if not numeric
    def evaluate(self):
        if not self.is_numeric():
            raise error.UncompatibleType(self, "numeric Value")
        else:
            return self.value






    # ------------------------------------------- CALCULATE ONE STEP ----------
    ##
    #   @brief Returns None
    def calculate_next_step(self, **options):
        return None





    # --------------------------------------------------- SUBSTITUTE ----------
    ##
    #   @brief Uses the given lexicon to substitute literal Values in self
    def substitute(self, subst_dict):
        if self.is_literal():
            for key in subst_dict:
                if self == key:
                    self.__init__(subst_dict[key])
                    #done = True

            #if not done:
            #    raise error.ImpossibleAction("substitute because the numeric "\
            #                + "value matching the literal here is not in the "\
            #                + "substitution dictionnary")

        else:
            pass





    # --------------------------------------------------- SQUARE ROOT ----------
    ##
    #   @brief Returns a Value containing the square root of self
    def sqrt(self):
        if self.is_numeric():
            return Value(self.value.sqrt())
        else:
            raise error.UncompatibleType(self, "numeric Value")



    # --------------------------------------------------------- ROUND ----------
    ##
    #   @brief Returns the value once rounded to the given precision
    def round(self, precision):
        if not self.is_numeric():
            raise error.UncompatibleType(self, "numeric Value")
        elif not (precision in [UNIT,
                                TENTH,
                                HUNDREDTH,
                                THOUSANDTH,
                                TEN_THOUSANDTH] \
             or (type(precision) == int and precision >= 0 and precision <= 4)):
        #___
            raise error.UncompatibleType(precision, "must be UNIT or" \
                                                    + "TENTH, " \
                                                    + "HUNDREDTH, " \
                                                    + "THOUSANDTH, " \
                                                    + "TEN_THOUSANDTH, "\
                                                    + "or 0, 1, 2, 3 or 4.")
        else:
            result_value = None

            if type(precision) == int:
                result_value = Value(round(self.value,
                                           Decimal(PRECISION[precision]),
                                           rounding=ROUND_HALF_UP
                                          )
                                    )
            else:
                result_value = Value(round(self.value,
                                           Decimal(precision),
                                           rounding=ROUND_HALF_UP
                                          )
                                    )

            if self.needs_to_get_rounded(precision):
                result_value.has_been_rounded = True

            return result_value




    # ------------------------------------------------- DIGITS NUMBER ----------
    ##
    #   @brief Returns the number of digits of a numerical value
    def digits_number(self):
        if not self.is_numeric():
            raise error.UncompatibleType(self, "numeric Value")
        else:
            temp_result = len(str((self.value \
                                   - round(self.value,
                                           Decimal(UNIT),
                                           rounding=ROUND_DOWN
                                          )
                                  ))
                              ) \
                           - 2

            if temp_result < 0:
                return 0
            else:
                return temp_result





    # ------------------------------------------ NEEDS TO GET ROUNDED ----------
    ##
    #   @brief Returns True/False depending on the need of the value to get
    #          rounded (for instance 2.68 doesn't need to get rounded if
    #          precision is HUNDREDTH or more, but needs it if it is less)
    def needs_to_get_rounded(self, precision):
        if not (precision in [UNIT,
                              TENTH,
                              HUNDREDTH,
                              THOUSANDTH,
                              TEN_THOUSANDTH] \
             or (type(precision) == int and precision >= 0 and precision <= 4)):
        #___
            raise error.UncompatibleType(precision, "must be UNIT or" \
                                                    + "TENTH, " \
                                                    + "HUNDREDTH, " \
                                                    + "THOUSANDTH, " \
                                                    + "TEN_THOUSANDTH, "\
                                                    + "or 0, 1, 2, 3 or 4.")

        precision_to_test = 0

        if type(precision) == int:
            precision_to_test = precision
        else:
            precision_to_test = PRECISION_REVERSED[precision]

        return self.digits_number() > precision_to_test





    # ----------------- FUNCTION CREATING THE ML STRING OF THE OBJECT ---------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):

        if 'display_unit' in options and options['display_unit'] in YES \
            and self.unit != None and self.unit != '':
        #___
            unit_str = VALUE_AND_UNIT_SEPARATOR[self.unit] + self.unit

        if self.is_numeric():
            if 'display_unit' in options and options['display_unit'] in YES:
                if 'graphic_display' in options\
                    and options['graphic_display'] in YES:
                #___
                    return locale.str(self.value)\
                           + unit_str
                else:
                    return locale.str(self.value)\
                           + MARKUP['open_text_in_maths']\
                           + unit_str \
                           + MARKUP['close_text_in_maths']
            else:
                return locale.str(self.value)
        else:
            if len(self.get_letter()) >= 2 \
                and not (self.get_letter()[0] == "-" \
                         or self.get_letter()[0] == "+"):
            #___
                return MARKUP['open_text_in_maths'] \
                       + str(self.value) \
                       + MARKUP['close_text_in_maths']
            else:
                return str(self.value)





# -----------------------------------------------------------------------------
# ------------------------------------------------ CLASS: Exponented ----------
# -----------------------------------------------------------------------------
##
# @class Exponented
# @brief Exponented objects: Operations (Sums&Products), Items, Quotients...
# Any Exponented must have a exponent field and should reimplement the
# methods that are not already defined hereafter
class Exponented(Signed):



    # -------------------------------------------------- CONSTRUCTOR ----------
    ##
    #   @brief Constructor
    #   @return An Exponented, though it can't really be used as is
    def __init__(self):
        Signed.__init__(self)
        self._exponent = Value(1)





    # ------------------------------------------------- GET EXPONENT ----------
    ##
    #   @brief Gets the exponent of the FunctionalItem
    #   @brief this should be already done by Item.get_exponent()...
    def get_exponent(self):
        return self._exponent
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    exponent = property(get_exponent,
                        doc = "Exponent of the FunctionalItem")




    # ------------------------------------------------- SET EXPONENT ----------
    ##
    #   @brief Set the value of the exponent
    #   @param  arg Calculable|Number|String
    #   @warning Relays an exception if arg is not of the types described
    def set_exponent(self, arg):
        if isinstance(arg, Calculable):
            self._exponent = arg.deep_copy()
        else:
            self._exponent = Value(arg)





    # ----------------------------- MUST THE EXPONENT BE DISPLAYED ? ----------
    ##
    #   @brief True if the exponent isn't equivalent to a single 1
    #   @return True if the exponent is not equivalent to a single 1
    def exponent_must_be_displayed(self):
        if not self.exponent.is_displ_as_a_single_1():
            return True
        else:
            return False










