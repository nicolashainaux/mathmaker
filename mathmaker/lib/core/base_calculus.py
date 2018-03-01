# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets with their answers
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

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @package core.base_calculus
# @brief Mathematical elementary arithmetic and algebraic objects.

import math
import random
import types
from decimal import Decimal
from abc import ABCMeta, abstractmethod

from mathmakerlib import required
from mathmakerlib.calculus import Number
from mathmakerlib.calculus import is_integer, is_natural, is_number

from mathmaker import settings
from mathmaker.lib.core.root_calculus import Calculable, Value, Exponented
from mathmaker.lib.tools.maths import (sign_of_product, pupil_gcd,
                                       lcm_of_the_list, is_even, is_uneven,
                                       prime_factors,
                                       ZERO_POLYNOMIAL_DEGREE)
from mathmaker.lib.constants import (DEFAULT, RANDOMLY, NUMERIC, LITERALS,
                                     OTHERS)
from .utils import reduce_literal_items_product, put_term_in_lexicon
from mathmaker.lib.constants.latex import MARKUP


# Maximum ratio of constant terms accepted during the creation of random
# polynomials
CONSTANT_TERMS_MAXIMUM_RATIO = 0.4
# Minimum always authorized number of constant terms during the creation of
# random polynomials. This minimum is necessary to still have constant terms
# in short polynomials, like the ones having only 1 ou 2 terms
CONSTANT_TERMS_MINIMUM_NUMBER = 1

# GLOBAL
expression_begins = True


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
#   @class Item
#   @brief It's the smallest displayable element (sign, value, exponent)
#   The value can be either numeric or literal
class Item(Exponented):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg None|Number|String|Item|(sign,value,exponent)|
    #              (sign,number|letter|Value)|0-degree Monomial|Value
    #   Possible arguments can be:
    #   - a number which will will be the same as (sign_number, number, 1)
    #   - a letter: for example, passing 'a' is equivalent to ('+', 'a', 1)
    #                but passing '-x' is equivalent to ('-', 'x', 1)
    #                further characters are ignored ('ax' is equivalent to 'a')
    #   - another Item which will be copied
    #   - a tuple ('+'|'-', number|string)
    #   - a tuple ('+'|'-', number|string, <exponent as number|Exponented>)
    #   - None which will be the same as giving 1
    #   - a Monomial of degree zero and coefficient is an Item
    #   The is_out_striked field will always be initialized at False but will
    #   be copied in the case of an Item given as argument.
    #   If the argument is not of one of these kinds, an exception
    #   will be raised.
    #   @return One instance of Item
    def __init__(self, arg, **options):
        Exponented.__init__(self)
        self._is_out_striked = False
        self._force_display_sign_once = False
        self._value_inside = Value(1)

        unit = options.get('unit', None)
        if unit is not None:
            self.set_unit(unit)

        # 1st CASE: number
        # Item's sign will be number's sign
        # Item's value will be abs(number)
        # Item's exponent will be 1
        if is_number(arg):
            if arg > 0:
                self._value_inside = Value(arg, **options)
            else:
                self._sign = '-'
                self._value_inside = Value(-arg, **options)

        # 2d CASE: string
        # Item's sign will be either '-' if given, or '+'
        # Item's value will be the next letters
        # Item's exponent will be 1
        elif type(arg) is str and len(arg) >= 1:
            if arg[0] in ['+', '-'] and len(arg) >= 2:
                self._sign = arg[0]
                self._value_inside = Value(arg[1:len(arg)], **options)
            else:
                self._sign = '+'
                self._value_inside = Value(arg, **options)

        # 3d CASE: Item
        elif isinstance(arg, Item):
            self._sign = arg.sign
            self._value_inside = arg.value_inside.clone()
            self._exponent = arg.exponent.clone()
            self._is_out_striked = arg.is_out_striked
            self._force_display_sign_once = arg.force_display_sign_once
            if arg.get_unit() is not None:
                self.set_unit(arg.get_unit())

        # 4th CASE: (sign, number|letter, <exponent as number|Exponented>)
        elif (type(arg) == tuple and len(arg) == 3 and arg[0] in ['+', '-']
              and (is_number(arg[1]) or type(arg[1]) is str)
              and (is_number(arg[2]) or isinstance(arg[2], Exponented)
                   or isinstance(arg[2], Value))):
            # __
            self._sign = arg[0]
            self._value_inside = Value(arg[1], **options)
            if isinstance(arg[2], Exponented):
                self._exponent = arg[2].clone()
            else:
                self._exponent = Value(arg[2], **options)

        # 5th CASE: (sign, number|letter)
        elif (type(arg) == tuple and len(arg) == 2 and arg[0] in ['+', '-']
              and (is_number(arg[1]) or type(arg[1]) is str)):
            # __
            self._sign = arg[0]
            self._value_inside = Value(arg[1], **options)

        # 6th CASE: None
        elif arg is None:
            self._value_inside = Value(1, **options)

        # 7th CASE: A zero-degree Monomial having an Item as coefficient
        elif (isinstance(arg, Monomial) and arg.is_numeric()
              and isinstance(arg.factor[0], Item)):
            # __
            self._sign = arg.get_sign()
            self._value_inside = Value(arg.factor[0].raw_value, **options)

        # 8th CASE: A Value (the exponent will be one)
        elif isinstance(arg, Value):
            if arg.is_numeric():
                if arg.raw_value < 0:
                    self._sign = '-'
                    self._value_inside = Value(-arg.raw_value, **options)
                else:
                    self._sign = '+'
                    self._value_inside = Value(arg.raw_value, **options)
            else:
                self._sign = '+'
                self._value_inside = Value(arg.raw_value, **options)

            self._value_inside.set_has_been_rounded(arg.has_been_rounded)

        # All other unforeseen cases: an exception is raised.
        else:
            raise TypeError('Got: ' + str(type(arg)) + ' instead of '
                            'a Number|String|Item|'
                            '(sign, Number|String, exponent)|'
                            '(sign, Number|String)')

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the raw value of the Item
    #   @return value_inside.raw_value
    def get_is_out_striked(self):
        return self._is_out_striked

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets force_display_sign_once field
    #   @return Item's force_display_sign_once field
    def get_force_display_sign_once(self):
        return self._force_display_sign_once

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the raw value of the Item
    #   @return value_inside.raw_value
    def get_raw_value(self):
        return self.value_inside.raw_value

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the Value of the Item
    #   @return value_inside
    def get_value_inside(self):
        return self._value_inside

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the unit of the Item
    def get_unit(self):
        return self._value_inside.unit

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the number of '-' signs of the Item
    #   @return The number of '-' signs of the Item (either 0, 1 or 2)
    def get_minus_signs_nb(self):
        nb = 0

        if self.is_negative() and not self.is_null():
            nb += 1

        if self.is_numeric():
            if (Decimal(str(self.raw_value)) < Decimal("0")
                and is_uneven(self.exponent)):
                # __
                nb += 1

        return nb

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the list of elements to iter over
    def get_iteration_list(self):
        return [self.value_inside, self.exponent]

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the letter of the Item, in case it's a literal
    def get_first_letter(self):
        if self.is_literal():
            return self.raw_value

        else:
            raise TypeError('Cannot get first letter of a non liteal Item')

    is_out_striked = property(get_is_out_striked,
                              doc="Item's is_out_striked field")

    force_display_sign_once = property(get_force_display_sign_once,
                                       doc="Item's force_display_sign_once"
                                       " field")

    raw_value = property(get_raw_value, doc="Item's raw value")

    value_inside = property(get_value_inside, doc="Item's Value")

    unit = property(get_unit, doc="Unit of the Item")

    # --------------------------------------------------------------------------
    ##
    #   @brief Set the unit of the Item
    #   @param  arg String
    def set_unit(self, arg):
        self._value_inside.set_unit(arg)

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets a value to the "is_out_striked" field
    # If is_out_striked is set to True, the Item will be displayed out striked
    def set_is_out_striked(self, arg):
        if arg in [True, False]:
            self._is_out_striked = arg
        else:
            raise ValueError("arg should be True|False")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets a True|False value to the "force_display_sign_once" field
    def set_force_display_sign_once(self, arg):
        if arg in [True, False]:
            self._force_display_sign_once = arg
        else:
            raise ValueError("arg should be True|False")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the Value inside
    def set_value_inside(self, arg):
        if isinstance(arg, Value):
            self._value_inside = arg.clone()
        else:
            raise ValueError("arg should be a Value")

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        global expression_begins
        log = settings.dbg_logger.getChild('Item.into_str')
        # Displaying the + sign depends on the expression_begins flag of the
        # machine:
        #  - either it's True: + won't be displayed
        #  - or it's False: + will be displayed
        # "Normal" state of this flag is False.
        # It is set to True outside of this section of into_str, every time
        # it's necessary (for example, as soon as a bracket has been
        # displayed the next object should be displayed like at the beginning
        # of an expression).
        # Everytime an Item is written, expression_begins is set to False again

        if ('force_expression_begins' in options
            and options['force_expression_begins']):
            # __
            expression_begins = options['force_expression_begins']
            options['force_expression_begins'] = False

        log.debug("Entering with force_display_sign_once == "
                  + str(self.force_display_sign_once))

        resulting_string = ""

        sign = ''

        inner_bracket_1 = ''
        inner_bracket_2 = ''

        if self.requires_inner_brackets():
            inner_bracket_1 = MARKUP['opening_bracket']
            inner_bracket_2 = MARKUP['closing_bracket']

        if (not expression_begins
            or ('force_display_sign' in options and self.is_numeric())
            or self.force_display_sign_once):
            # __
            if self.sign == '+' or self.is_null():
                sign = MARKUP['plus']
            else:
                sign = MARKUP['minus']
            if self.force_display_sign_once:
                self.set_force_display_sign_once(False)
        else:
            if self.sign == '-' and not self.is_null():
                sign = MARKUP['minus']

        if self.exponent.is_displ_as_a_single_0():
            # __
            if ('force_display_exponent_0' in options
                or 'force_display_exponents' in options):
                # __
                resulting_string += inner_bracket_1\
                    + self.value_inside.into_str(**options)\
                    + inner_bracket_2\
                    + MARKUP['opening_exponent']\
                    + MARKUP['zero']\
                    + MARKUP['closing_exponent']
            else:
                resulting_string += MARKUP['one']

        elif self.exponent_must_be_displayed():
            if isinstance(self.exponent, Exponented):
                expression_begins = True

            resulting_string += inner_bracket_1\
                + self.value_inside.into_str(**options)\
                + inner_bracket_2\
                + MARKUP['opening_exponent']\
                + self.exponent.into_str(**options)\
                + MARKUP['closing_exponent']

        else:   # that should only concern cases where the exponent
                # is equivalent to 1
            if ('force_display_exponent_1' in options
                or 'force_display_exponents' in options):
                # __
                resulting_string += inner_bracket_1\
                    + self.value_inside.into_str(**options)\
                    + inner_bracket_2\
                    + MARKUP['opening_exponent']\
                    + MARKUP['one']\
                    + MARKUP['closing_exponent']
            else:
                resulting_string += inner_bracket_1\
                    + self.value_inside.into_str(**options) + inner_bracket_2

        if self.is_out_striked:
            resulting_string = MARKUP['opening_out_striked']\
                + resulting_string + MARKUP['closing_out_striked']
            required.package['cancel'] = True

        # if self.unit is not None and 'display_unit' in options \
        #    and options['display_unit']:
            # __
        #    resulting_string += "~" + str(self.unit)

        expression_begins = False
        return sign + resulting_string

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the value of a numerically evaluable Item
    #   @warning Relays an exception if the exponent is not Exponented|Value
    def evaluate(self, **options):
        expon = self.exponent.evaluate()

        if self.is_numeric():
            if self.is_positive():
                return (self.raw_value)**expon
            else:
                return -(self.raw_value)**expon

        else:
            raise TypeError('Cannot evaluate a non numeric Item')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns None|an Item
    #   @todo Manage the case when the exponent is a calculable that should
    #   be calculated itself.
    #   @warning Relays an exception if the exponent is not Exponented|Value
    # If the Item has an exponent equivalent to a single 1, then nothing
    # can be calculated, so this method returns None
    # In another case, it returns the evaluated Item
    def calculate_next_step(self, **options):
        log = settings.dbg_logger.getChild(
            'Item.calculate_next_step')
        if not self.is_numeric():
            raise TypeError('Cannot calculate next step of a non numeric Item')

        log.debug("Entered; current Item is: " + repr(self))

        # First, either get the exponent as a Number or calculate it further
        expon_test = self.exponent.calculate_next_step(**options)

        log.debug("expon_test = " + str(expon_test))

        if expon_test is not None:
            return Item((self.sign, self.raw_value, expon_test))

        expon = self.exponent.evaluate()

        log.debug("expon = " + str(expon))

        # Now the exponent is a number (saved in "expon")

        # If it is different from 1, then the next step is to calculate
        # a new Item using this exponent (for example,
        # the Item 4² would return the Item 16)
        if expon != 1:
            log.debug("expon is != 1")
            # Intricated case where the inner sign is negative
            # (like in ±(-5)³)
            if self.raw_value < 0:
                log.debug("self.raw_value < 0")

                aux_inner_sign = Item(('+', -1, expon))
                return Item((sign_of_product([self.sign, aux_inner_sign]),
                             (- self.raw_value)**expon,
                             1))
            # Simple case like -3² or 5³
            else:
                log.debug("self.raw_value >= 0")
                return Item((self.sign,
                             self.raw_value ** expon,
                             1))

        # Now the exponent is 1
        else:
            log.debug("expon is == 1")
            # Case of -(-something)
            if self.raw_value < 0 and self.sign == '-':
                return Item(('+',
                             - self.raw_value,
                             expon))

            # Other cases like ±number where ± is either external or
            # inner sign
            else:
                return None

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns None (an Item can't get expanded nor reduced !)
    #   @return Exponented
    def expand_and_reduce_next_step(self, **options):
        if self.is_numeric():
            return self.calculate_next_step(**options)
        else:
            return None

    # --------------------------------------------------------------------------
    ##
    #   @brief Shortcut for into_str
    def __str__(self, **options):
        return self.into_str(**options)

    # --------------------------------------------------------------------------
    ##
    #   @brief Raw display of the Item (debugging method)
    #   @param options No option available so far
    #   @return A string containing "{sign value ^ exponent}"
    def __repr__(self, **options):
        if self.is_out_striked:
            begining = " s{"
        else:
            begining = " {"

        unit_str = ''

        if self.unit is not None:
            unit_str = ' (unit={u}) '.format(u=repr(self.unit))

        return begining + self.sign + str(self.raw_value) + unit_str \
            + "^" + repr(self.exponent) + "} "

    # --------------------------------------------------------------------------
    ##
    #   @brief Compares two Items
    #   @return True if they're equal
    def __eq__(self, other_item):
        log = settings.dbg_logger.getChild('Item.eq')
        if not isinstance(other_item, Item):
            log.debug("the other object is not an Item => returning False")
            return False

        if (self.sign == other_item.sign
            and self.raw_value == other_item.raw_value
            and self.exponent == other_item.exponent):
            # __
            log.debug("everything found equal")
            return True
        else:
            log.debug("self.sign is " + str(self.sign) + " "
                      "other_item.sign is " + str(other_item.sign) + " "
                      " and they're equal? "
                      + str(self.sign == other_item.sign)
                      + "\n          self.raw_value is "
                      + str(self.raw_value) + " "
                      "other_item.raw_value is "
                      + str(other_item.raw_value) + " "
                      " and they're equal? "
                      + str(self.raw_value == other_item.raw_value)
                      + "\n          self.exponent is "
                      + str(self.exponent) + " "
                      "other_item.exponent is " + str(other_item.exponent)
                      + " and they're equal? "
                      + str(self.exponent == other_item.exponent))
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief Compares an Item to something else ; it's a reimplementing of
    #          alphabetical_order_cmp(), since we need this comparison
    #   @return True if self is lower than the other_item
    def __lt__(self, other_objct):
        if self.is_numeric() and other_objct.is_numeric(displ_as=True):
            return False

        elif self.is_literal() and other_objct.is_numeric(displ_as=True):
            return False

        elif self.is_numeric() and other_objct.is_literal(displ_as=True):
            return True

        elif self.is_literal() and other_objct.is_literal(displ_as=True):
            self_value = self.get_first_letter()
            other_value = other_objct.get_first_letter()

            # let's compare
            if self_value == other_value:
                return False
            elif self_value > other_value:
                return False
            else:
                return True

    # --------------------------------------------------------------------------
    ##
    #   @brief Compares an Item to something else ; it's a reimplementing of
    #          alphabetical_order_cmp(), since we need this comparison
    #   @return True if self is lower than the other_item
    def __gt__(self, other_objct):
        if self.is_numeric() and other_objct.is_numeric(displ_as=True):
            return True

        elif self.is_literal() and other_objct.is_numeric(displ_as=True):
            return True

        elif self.is_numeric() and other_objct.is_literal(displ_as=True):
            return False

        elif self.is_literal() and other_objct.is_literal(displ_as=True):
            self_value = self.get_first_letter()
            other_value = other_objct.get_first_letter()

            # let's compare
            if self_value == other_value:
                return False
            elif self_value > other_value:
                return True
            else:
                return False

    # --------------------------------------------------------------------------
    ##
    #   @brief Makes Items hashable (so, usable as dictionnary keys)
    def __hash__(self):
        return hash(str(self.raw_value) + str(self.sign)
                    + repr(self.exponent))

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Item's length
    #   @return 1
    def __len__(self):
        return 1

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the usual writing rules require a × between two factors
    #   @param objct The other one
    #   @param position The position (integer) of self in the Product
    #   @return True if the writing rules require × between self & obj
    def multiply_symbol_is_required(self, objct, position):
        # 1st CASE: Item × Item
        # and other cases inside: numeric × numeric or numeric × literal etc.
        # The code could be shortened but will not, for better comprehension.
        if isinstance(objct, Item):
            # ex: 2 × 4
            if ((self.is_numeric() or self.is_displ_as_a_single_1())
                and (objct.is_numeric(displ_as=True)
                     or objct.is_displ_as_a_single_1())):
                # __
                return True

            # ex: a × 3 (writing a3 isn't OK)
            elif (self.is_literal()
                  and (objct.is_numeric(displ_as=True)
                       or objct.is_displ_as_a_single_1())):
                # __
                return True

            elif self.is_numeric() and objct.is_literal(displ_as=True):
                if (self.raw_value == 1
                    or self.requires_brackets(position)
                    or objct.requires_brackets(position + 1)):
                    # __
                    return True
                else:
                    return False

            elif self.is_literal() and objct.is_literal(displ_as=True):
                if (self.requires_brackets(position)
                    or objct.requires_brackets(position + 1)):
                    # __
                    return True
                else:
                    if (not self.exponent_must_be_displayed()
                        and self.raw_value == objct.raw_value):
                        # __
                        return True
                    else:
                        return False

        # 2d CASE: Item × Product
        if isinstance(objct, Product):
            return self.multiply_symbol_is_required(objct.factor[0],
                                                    position)

        # 3d CASE: Item × Sum
        if isinstance(objct, Sum):
            if len(objct.throw_away_the_neutrals()) >= 2:
                if self.is_numeric() and self.raw_value == 1:
                    return True
                else:
                    return False
            else:
                return self\
                    .multiply_symbol_is_required(objct.
                                                 throw_away_the_neutrals()
                                                 .term[0],
                                                 position)

        # 4th CASE: Item × Quotient
        if isinstance(objct, Quotient):
            return True

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the argument requires brackets in a product
    #   For instance, a Sum with several terms or a negative Item
    #   @param position The position of the object in the Product
    #   @return True if the object requires brackets in a Product
    def requires_brackets(self, position):
        # an Item at first position doesn't need brackets
        if position == 0:
            return False
        # if the Item isn't at first position, then it depends on its sign
        elif self.sign == '+':
            # The case of literals which don't need inner brackets but
            # do have a minus sign "inside" is quite tricky. Maybe should
            # be managed better than that ; check the requires_inner_bracket()
            # and take care that it already calls requires_brackets() !
            if self.is_literal() and self.raw_value[0] == '-':
                return True
            else:
                return False
        elif self.sign == '-':
            return True

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object requires inner brackets
    #   The reason for requiring them is having a negative *value* and
    #   if the exponent is either:
    #   - (numeric Item | number) and even
    #   - (numeric Item | number) equivalent to 1 the object has a '-' *sign*
    #   - litteral Item
    #   - any Exponented apart from Items.
    #   @todo Case of non-Item-Exponented exponents probably is to be improved
    #   @todo Case of numerator-only equivalent Quotients not made so far
    #   @return True if the object requires inner brackets
    def requires_inner_brackets(self):
        # CHECK if the *value* is negative (not the sign !):
        if (self.is_numeric() and self.raw_value < 0)                  \
           or (self.is_literal() and self.raw_value[0] == '-'):
            # __
            # To avoid two - signs in a row, inner brackets must be displayed
            if self.is_negative():
                return True

            # First, check the most common cases of Item/number/string
            # exponents...

            # NUMERIC exponents (with a positive *sign*, the negative ones
            #                    having already be managed just above)
            if ((isinstance(self.exponent, Value)
                 or isinstance(self.exponent, Item))
                and self.exponent.is_numeric(displ_as=True)):
                # __
                if is_even(self.exponent):
                    return True

            # LITERAL exponents
            elif self.exponent.is_literal(displ_as=True):
                return True

            # Now the cases of non-Item-but-though-(numeric) Exponented
            # exponents:
            # General rule is the brackets will be required as long as the
            # displayed value is not simple. In something like (-4)^{2 - 1},
            # the inner brackets must be displayed although they are not
            # necessary
            elif (isinstance(self.exponent, Exponented)
                  and not isinstance(self.exponent, Item)):
                # __
                if self.exponent.is_displ_as_a_single_1():
                    return False
                elif (isinstance(self.exponent, CommutativeOperation)
                      and len(self.exponent) == 1
                      and not self.exponent.exponent_must_be_displayed()):
                    # __
                    aux_item = Item((self.sign,
                                     self.raw_value,
                                     self.exponent.element[0]))
                    return aux_item.requires_inner_brackets()

                else:
                    return True

        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief Always False for an Item
    #   @param objct The object to search for
    #   @return False
    def contains_exactly(self, objct):
        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief To check if this contains a rounded number...
    #   @return True or False depending on the Value inside
    def contains_a_rounded_number(self):
        return self.value_inside.has_been_rounded

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the (numeric) Item once rounded to the given precision
    def rounded(self, precision):
        if not self.exponent.is_displ_as_a_single_1():
            raise TypeError('In order to round an Item, its exponent should be'
                            ' equivalent to a single 1')
        else:
            result = self.clone()
            result.set_value_inside(self.value_inside.rounded(precision))
            return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the number of digits of a numerical Item
    def digits_number(self):
        if not self.exponent.is_displ_as_a_single_1():
            raise TypeError('In order to get the number of digits of an Item, '
                            'its exponent should be equivalent to a single 1')
        else:
            return self.value_inside.digits_number()

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns True/False depending on the need of the value to get
    #          rounded (for instance 2.68 doesn't need to get rounded if
    #          precision is HUNDREDTH or more, but needs it if it is less)
    #          If the Item is not numeric, or if the given precision is
    #          incorrect, the matching call to the Value
    #          will raise an exception.
    def needs_to_get_rounded(self, precision):
        if not self.exponent.is_displ_as_a_single_1():
            raise TypeError('In order to know if an Item needs to get rounded,'
                            ' its exponent should be equivalent to a single 1')

        return self.value_inside.needs_to_get_rounded(precision)

    # --------------------------------------------------------------------------
    ##
    #   @brief Turns the Item into the fraction item itself over item 1
    def turn_into_fraction(self):
        return Fraction(('+', self, Item(1)))

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's a numeric Item
    def is_numeric(self, displ_as=False):
        if (self.value_inside.is_numeric()
            and self.exponent.is_numeric(displ_as=displ_as)):
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's a literal Item
    def is_literal(self, displ_as=False) -> bool:
        """
        Return True if Item is to be considered literal.

        :param displ_as: not applicable to Items
        """
        return (self.value_inside.is_literal()
                or self.exponent.is_literal(displ_as=displ_as))

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's the null Item
    def is_null(self):
        if self.exponent.evaluate() == ZERO_POLYNOMIAL_DEGREE \
           or (self.value_inside.is_null()):
            # __
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's positive w/ (exponent 0 or numeric w/ value 1)
    def is_displ_as_a_single_1(self):
        if self.sign == '+':
            if (self.exponent.is_null()) \
               or (self.value_inside.is_displ_as_a_single_1()):
                # __
                return True

        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's negative w/ (exponent 0 or numeric w/ value 1)
    def is_displ_as_a_single_minus_1(self):
        if self.sign == '-':
            if self.exponent.is_null() \
               or (self.value_inside.is_displ_as_a_single_1()):
                # __
                return True

        if self.sign == '+':
            if self.value_inside.is_displ_as_a_single_minus_1()   \
               and is_uneven(self.exponent):
                # __
                return True

        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if self.is_null()
    def is_displ_as_a_single_0(self):
        return self.is_null()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Item is numeric
    def is_displ_as_a_single_numeric_Item(self):
        return self.is_numeric(displ_as=True)

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single int
    def is_displ_as_a_single_int(self):
        return self.value_inside.is_displ_as_a_single_int() \
            and self.exponent.is_displ_as_a_single_1()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be considered as a neutral element
    def is_displ_as_a_single_neutral(self, elt):
        if elt == Item(0):
            return self.is_displ_as_a_single_0()
        elif elt == Item(1):
            return self.is_displ_as_a_single_1()
        else:
            raise TypeError('elt must be a neutral element for addition '
                            'or multiplication, i.e. Item(1) | Item(0), '
                            'yet it is {} '.format(repr(elt)))

    # --------------------------------------------------------------------------
    ##
    #   @brief False
    #   @return False
    def is_expandable(self):
        return False


class Function(Item):
    """
    Represent the image of a number under a function like f(x) or cos(ABC).
    """

    def __init__(self, copy_this=None, name='f', var=Item('x'),
                 fct=lambda x: x, num_val=Value(1), display_mode='literal',
                 inv_fct=None, unlocked=False):
        from mathmaker.lib.core.base_geometry import Angle
        if copy_this is None:
            if not type(name) == str:
                raise TypeError('name should be a str')

            if not (isinstance(var, Angle)
                    or (isinstance(var, Calculable) and var.is_literal())):
                # __
                raise TypeError('var should be a literal Calculable '
                                'or an Angle')

            if not ((isinstance(num_val, Value)
                    or isinstance(num_val, Item))
                    and num_val.is_numeric()):
                raise TypeError('num_val should be a numeric Value or Item')

            if display_mode not in ['literal', 'numeric']:
                raise TypeError("display_mode should be 'literal' "
                                "or 'numeric'")

            for elt in [fct, inv_fct]:
                if not (elt is None or isinstance(elt, types.LambdaType)):
                    # __
                    raise TypeError('fct and inv_fct must both be None or '
                                    'types.LambdaType')

            if unlocked not in [True, False]:
                raise TypeError('unlocked should be a boolean')

            if isinstance(var, Angle):
                var = AngleItem(from_this_angle=var)

            Exponented.__init__(self)
            self._force_display_sign_once = False
            self._image_notations = \
                {'literal': Value(name
                                  + MARKUP['opening_bracket']
                                  + var.printed
                                  + MARKUP['closing_bracket'],
                                  text_in_maths=False),
                 'numeric': Value(name
                                  + MARKUP['opening_bracket']
                                  + num_val.printed
                                  + MARKUP['closing_bracket'],
                                  text_in_maths=False)}
            self._arguments = {'literal': var, 'numeric': num_val}
            self._name = name
            self._var = var
            self._fct = fct
            self._inv_fct = inv_fct
            self._num_val = num_val
            self._display_mode = display_mode
            self._image_notation = self._image_notations[display_mode]
            self._unlocked = unlocked
        else:
            if not isinstance(copy_this, Function):
                raise TypeError('If copy_this is not None, it should be '
                                'a Function')
            Exponented.__init__(self)
            self._sign = copy_this._sign
            self._force_display_sign_once = copy_this._force_display_sign_once
            self._arguments = copy_this._arguments
            self._name = copy_this._name
            self._var = copy_this._var
            self._fct = copy_this._fct
            self._inv_fct = copy_this._inv_fct
            self._num_val = copy_this._num_val
            self._display_mode = copy_this._display_mode
            self._image_notations = copy_this._image_notations
            self._image_notation = copy_this._image_notation
            self._unlocked = copy_this._unlocked

    @property
    def image_notation(self):
        return self._image_notations[self._display_mode]

    @property
    def argument(self):
        return self._arguments[self._display_mode]

    @property
    def unlocked(self):
        return self._unlocked

    @unlocked.setter
    def unlocked(self, arg):
        if arg not in [True, False]:
            raise TypeError('arg should be a boolean')
        else:
            self._unlocked = arg

    @property
    def var(self):
        return self._var

    @property
    def num_val(self):
        return self._num_val

    @num_val.setter
    def num_val(self, arg):
        if not (isinstance(arg, Item) or isinstance(arg, Value)):
            raise TypeError("arg should be an Item or Value")
        if not arg.is_numeric():
            raise TypeError("arg should be a numeric Item or Value")
        self._num_val = Item(arg)
        self._image_notations['numeric'] = Value(self._name
                                                 + MARKUP['opening_bracket']
                                                 + self.num_val.printed
                                                 + MARKUP['closing_bracket'],
                                                 text_in_maths=False)

    @property
    def fct(self):
        """The lambda function to use for evaluation."""
        return self._fct

    @property
    def inv_fct(self):
        """The lambda function to use for evaluation."""
        if self._inv_fct is None:
            raise RuntimeError('The inverse function is required but has '
                               'not been defined yet!')
        return self._inv_fct

    def get_first_letter(self):
        """Return the first letter of Function's name."""
        return self._name[0]

    def get_minus_signs_nb(self):
        """
        1 if Function object has a negative sign and no even exponent, else 0.
        """
        if (self.is_negative() and not self.is_null()
            and is_uneven(self.exponent)):
            return 1
        return 0

    def get_iteration_list(self):
        """Return [variable, exponent]."""
        return [self.var, self.exponent]

    def contains_a_rounded_number(self):
        """f(...) neither its argument never have any reason to be rounded."""
        return False

    def contains_exactly(self, objct):
        """True if the looked for object is self."""
        return self == objct

    def set_literal_mode(self):
        """Set the display mode to 'literal'."""
        self._display_mode = 'literal'

    def set_numeric_mode(self):
        """Set the display mode to 'numeric'."""
        self._display_mode = 'numeric'

    def __hash__(self):
        """A hash value for Function"""
        return hash(str(self.name) + str(self.sign) + str(self.var)
                    + str(self.fct))

    def __len__(self):
        """Function's length."""
        return 1

    def __repr__(self, **options):
        """Function's string representation for debugging."""
        return '{fct ' + self.sign + self.name + '(' \
            + repr(self.argument) \
            + ')' + '^' + repr(self.exponent) + ' fct} '

    def __eq__(self, other_fct):
        """True if self 'equals' other_fct."""
        if not isinstance(other_fct, Function):
            return False
        else:
            return (self._sign == other_fct._sign
                    and self._exponent == other_fct._exponent
                    and self._force_display_sign_once ==
                    other_fct._force_display_sign_once
                    and self._image_notations == other_fct._image_notations
                    and self._arguments == other_fct._arguments
                    and self._name == other_fct._name
                    and self._var == other_fct._var
                    and self._fct == other_fct._fct
                    and self._inv_fct == other_fct._inv_fct
                    and self._num_val == other_fct._num_val
                    and self._display_mode == other_fct._display_mode
                    and self._image_notation == other_fct._image_notation)

    def requires_brackets(self, position):
        """True if Function requires brackets inside a Product."""
        if position == 0:
            return False
        else:
            return self.sign == '-'

    def requires_inner_brackets(self):
        """Return True for cases like (-f(x))^2"""
        return self.sign == '-' and is_uneven(self.exponent)

    def multiply_symbol_is_required(self, objct, position):
        """True if × is required between self and next objct in a Product."""
        # 1st CASE: a) Function × Function
        if isinstance(objct, Function):
            return False

        # 1st CASE: b) Function × Item
        if isinstance(objct, Item):
            return True

        # 2d CASE: Function × Product
        if isinstance(objct, Product):
            return self.multiply_symbol_is_required(objct.factor[0], position)

        # 3d CASE: Function × Sum
        if isinstance(objct, Sum):
            if len(objct.throw_away_the_neutrals()) >= 2:
                # This is not exactly necessary, but more readable
                return True
            else:
                return self\
                    .multiply_symbol_is_required(objct.
                                                 throw_away_the_neutrals()
                                                 .term[0],
                                                 position)

        # 4th CASE: Function × Quotient
        if isinstance(objct, Quotient):
            return True

    def calculate_next_step(self, **options):
        """Will only swap to numeric argument, no automatic evaluation."""
        if self._display_mode == 'literal' and self.unlocked:
            self.set_numeric_mode()
            return self
        force_eval = options.get('force_evaluation', False)
        if force_eval:
            return self.evaluate()
        else:
            return None

    def expand_and_reduce_next_step(self, **options):
        """Same as calculate_ntext_step(), for Functions."""
        return self.calculate_next_step(**options)

    def is_numeric(self, displ_as=False):
        """Return True if current display mode is numeric.

        :param displ_as: if displ_as is True, it's about knowing whether the
                         object should be considered numeric for display,
                         otherwise, it's about knowing wether it can be
                         numerically evaluated (directly, without replacing
                         its variable by a Value)."""
        if displ_as:
            return False
        else:
            return self._display_mode == 'numeric'

    def is_literal(self, displ_as=False) -> bool:
        """
        Return True if Function is to be considered literal.

        :param displ_as: if displ_as is True, it's about knowing whether the
                         object should be considered literal for display,
                         otherwise, it's about knowing wether it can be
                         numerically evaluated (directly, without replacing
                         its variable by a Value).
        """
        if displ_as:
            return True
        else:
            return self._display_mode == 'literal'

    def is_null(self):
        """True if self evaluates to 0."""
        return self.evaluate() == 0

    def is_displ_as_a_single_1(self):
        """f(x) is never a single 1."""
        return False

    def is_displ_as_a_single_int(self):
        """f(x) is never a single int."""
        return False

    def is_displ_as_a_single_minus_1(self):
        """f(x) is never a single -1."""
        return False

    def is_displ_as_a_single_0(self):
        """f(x) is never a single 0."""
        return False

    def is_displ_as_a_single_numeric_Item(self):
        """f(x) is never a single numeric Item (like any single number)."""
        return False

    def is_displ_as_a_single_neutral(self, elt):
        """f(x) is never a single neutral element."""
        return False

    def is_expandable(self):
        """f(x) is not expandable."""
        return False

    def substitute(self, subst_dict):
        """Substitute the argument by its value, if available in subst_dict."""
        log = settings.dbg_logger.getChild('Function.substitute')
        substituted = False
        var = self.var.clone()
        if isinstance(var, Calculable) and var.substitute(subst_dict):
            log.debug('Case 1')
            substituted = True
            self.num_val = var
            self.set_numeric_mode()
            self._arguments['numeric'] = self.num_val
        elif self.var in subst_dict:
            log.debug('Case 2')
            substituted = True
            self.num_val = subst_dict[self.var]
            self.set_numeric_mode()
            self._arguments['numeric'] = self.num_val
        if self.exponent.substitute(subst_dict):
            substituted = True
        return substituted

    def into_str(self, **options):
        """Creates the str version of the Function."""
        # Very similar to Item's into_str()...
        global expression_begins
        log = settings.dbg_logger.getChild('Function.into_str')
        log.debug('Entering with options: ' + str(options))

        if ('force_expression_begins' in options
            and options['force_expression_begins']):
            # __
            expression_begins = options['force_expression_begins']
            options['force_expression_begins'] = False

        log.debug('expression_begins set to: '
                  + str(expression_begins))

        resulting_string = ""
        sign = ''
        inner_bracket_1 = ''
        inner_bracket_2 = ''

        if self.requires_inner_brackets():
            inner_bracket_1 = MARKUP['opening_bracket']
            inner_bracket_2 = MARKUP['closing_bracket']

        if (not expression_begins
            or ('force_display_sign' in options and self.is_numeric())
            or self._force_display_sign_once):
            # __
            if self.sign == '+' or self.is_null():
                sign = MARKUP['plus']
            else:
                sign = MARKUP['minus']
            if self._force_display_sign_once:
                self._force_display_sign_once = False
        else:
            if self.sign == '-' and not self.is_null():
                sign = MARKUP['minus']

        if self.exponent.is_displ_as_a_single_0():
            # __
            if ('force_display_exponent_0' in options
                or 'force_display_exponents' in options):
                # __
                resulting_string += inner_bracket_1\
                    + self.image_notation.into_str(**options)\
                    + inner_bracket_2\
                    + MARKUP['opening_exponent']\
                    + MARKUP['zero']\
                    + MARKUP['closing_exponent']
            else:
                resulting_string += MARKUP['one']

        elif self.exponent_must_be_displayed():
            if isinstance(self.exponent, Exponented):
                expression_begins = True

            resulting_string += inner_bracket_1\
                + self.image_notation.into_str(**options)\
                + inner_bracket_2\
                + MARKUP['opening_exponent']\
                + self.exponent.into_str(**options)\
                + MARKUP['closing_exponent']

        else:   # that should only concern cases where the exponent
                # is equivalent to 1
            if ('force_display_exponent_1' in options
                or 'force_display_exponents' in options):
                # __
                resulting_string += inner_bracket_1\
                    + self.image_notation.into_str(**options)\
                    + inner_bracket_2\
                    + MARKUP['opening_exponent']\
                    + MARKUP['one']\
                    + MARKUP['closing_exponent']
            else:
                resulting_string += inner_bracket_1\
                    + self.image_notation.into_str(**options) + inner_bracket_2

        expression_begins = False
        log.debug('Leaving, returning ' + sign + resulting_string)
        return sign + resulting_string

    def evaluate(self, **options):
        """Return the value of f(number)."""
        num = Item((self.sign,
                    self.fct(self.num_val.evaluate()),
                    self._exponent))
        return num.evaluate()


class AngleItem(Item):
    """
    Represent Angles' names, like \widehat{ABC} (handled as Items).
    """

    def __init__(self, raw_value=None, copy_this=None, from_this_angle=None):
        """
        Initialize the AngleItem.

        One exactly of the optional arguments must be correctly set.

        :param copy_this: another AngleItem (to clone)
        :type copy_this: AngleItem
        :param from_this_angle: an Angle to turn into (Angle)Item
        :type from_this_angle: Angle
        :param raw_value: any value that Item.__init__() can use
        :type raw_value: see Item.__init__()
        """
        from mathmaker.lib.core.base_geometry import Angle
        i = iter([copy_this, from_this_angle, raw_value])
        # Check if exactly one of the options is not None (or False):
        if any(i) and not any(i):
            if copy_this is not None:
                if not isinstance(copy_this, AngleItem):
                    raise TypeError('copy_this should be an AngleItem.')
                Item.__init__(self, copy_this)
            elif from_this_angle is not None:
                if not isinstance(from_this_angle, Angle):
                    raise TypeError('from_this_angle should be an Angle.')
                Item.__init__(self,
                              from_this_angle.points[0].name
                              + from_this_angle.points[1].name
                              + from_this_angle.points[2].name)
            else:
                Item.__init__(self, raw_value, unit=MARKUP['text_degree'])
        else:
            raise ValueError('Exactly one of the optional arguments '
                             '(copy_this, from_this_angle or raw_value) '
                             'must be different from None (or False).')

    def __repr__(self, **options):
        """Raw representation of the AngleItem"""
        if self.is_out_striked:
            begining = " s{∡ "
        else:
            begining = " {∡ "

        unit_str = ''

        if self.unit is not None:
            unit_str = ' (unit={u}) '.format(u=repr(self.unit))

        return begining + self.sign + str(self.raw_value) + unit_str \
            + "^" + repr(self.exponent) + " ∡ } "

    def into_str(self, **options):
        """
        Return the printed version of the AngleItem.

        If the AngleItem is literal, it will be displayed like a literal Item
        yet wrapped in a 'wide hat'.
        If it is not numeric, the unit will be automatically discarded."""
        if 'display_SI_unit' in options and self.is_literal():
            del options['display_SI_unit']
        if 'display_unit' in options and self.is_literal():
            del options['display_unit']
        if self.is_literal():
            return MARKUP['opening_widehat']\
                + Item.into_str(self, **options)\
                + MARKUP['closing_widehat']
        else:
            return Item.into_str(self, **options)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
#   @class SquareRoot
#   @brief It's a Exponented under a square root
#   The Exponented can be either numeric or literal
class SquareRoot(Function):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg Exponented|(sign, Exponented)
    #           The given Exponented will be "embedded" in the SquareRoot
    #   @return One instance of SquareRoot
    def __init__(self, arg, **options):
        Exponented.__init__(self)
        self._force_display_sign_once = False
        self.radicand = Item(1)

        # 1st CASE: a SquareRoot
        if isinstance(arg, SquareRoot):
            if 'embbed' in options and options['embbed']:
                self.radicand = arg.clone()
            else:
                self._force_display_sign_once = arg.force_display_sign_once
                self._sign = arg.sign
                self.radicand = arg.radicand.clone()

        # 2d CASE: any other Exponented
        elif isinstance(arg, Exponented):
            self.radicand = arg.clone()

        # 3d CASE: a tuple (sign, Exponented)
        elif (isinstance(arg, tuple)
              and len(arg) == 2
              and arg[0] in ['+', '-']
              and isinstance(arg[1], Exponented)):
            # __
            self._sign = arg[0]
            self.radicand = arg[1].clone()

        # All other unforeseen cases: an exception is raised.
        else:
            raise TypeError('arg must be an Exponented, yet it is a {}'
                            .format(str(type(arg))))

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the list of elements to iter over
    def get_iteration_list(self):
        return [self.radicand, self.exponent]

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the number of '-' signs of the SquareRoot
    #   @return The number of '-' signs of the SquareRoot (either 0 or 1)
    def get_minus_signs_nb(self):
        if self.is_negative() and not self.is_null():
            return 1
        else:
            return 0

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets force_display_sign_once field
    #   @return Item's force_display_sign_once field
    def get_force_display_sign_once(self):
        return self._force_display_sign_once

    force_display_sign_once = property(get_force_display_sign_once,
                                       doc="Item's force_display_sign_once"
                                           " field")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets a True|False value to the "force_display_sign_once" field
    def set_force_display_sign_once(self, arg):
        if arg in [True, False]:
            self._force_display_sign_once = arg
        else:
            raise ValueError("arg should be True|False")

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        global expression_begins
        # Displaying the + sign depends on the expression_begins flag of the
        # machine:
        #  - either it's True: + won't be displayed
        #  - or it's False: + will be displayed
        # "Normal" state of this flag is False.
        # It is set to True outside of this section of into_str, every time
        # it's necessary (for example, as soon as a bracket has been
        # displayed the next object should be displayed like at the beginning
        # of an expression).
        # Everytime an SquareRoot is written,
        # expression_begins is set to False again

        if ('force_expression_begins' in options
            and options['force_expression_begins']):
            # __
            expression_begins = options['force_expression_begins']
            options['force_expression_begins'] = False

        resulting_string = ""

        sign = ''

        if (not expression_begins
            or ('force_display_sign' in options and self.is_numeric())
            or self.force_display_sign_once):
            # __
            if self.sign == '+' or self.is_null():
                sign = MARKUP['plus']
            else:
                sign = MARKUP['minus']
            if self.force_display_sign_once:
                self.set_force_display_sign_once(False)
        else:
            if self.sign == '-' and not self.is_null():
                sign = MARKUP['minus']

        resulting_string = sign + MARKUP['opening_sqrt']\
            + self.radicand.into_str()\
            + MARKUP['closing_sqrt']

        expression_begins = False

        return resulting_string

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns None|an SquareRoot
    #   @todo Manage the case when the exponent is a calculable that should
    #   be calculated itself.
    #   @warning Relays an exception if the content is negative
    def calculate_next_step(self, **options):
        if not self.is_numeric():
            return SquareRoot((self.sign,
                               self.radicand.expand_and_reduce_next_step()))

        # First, let's handle the case when a Decimal Result is awaited
        # rather than a SquareRoot's simplification
        if 'decimal_result' in options \
           and self.radicand.calculate_next_step() is None:
            # __
            result = Item(Value(self.radicand.evaluate()).sqrt()
                          .rounded(options['decimal_result']))
            result.set_sign(self.sign)
            return result

        # Now, decimal_resultat isn't awaited but the SquareRoot is one
        # of an integer perfect square
        # Case of "perfect decimal squares" (like 0.49) will be treated later.
        # For instance, 49×10^{-14} can be squarerooted...
        # the significant digits should be computed and checked if the
        # square root of them is right or must be rounded. Then check if the
        # matching exponent is even.
        # (this could be an improvement of the method is_a_perfect_square())
        elif (self.radicand.calculate_next_step() is None
              and Value(self.radicand.evaluate()).is_a_perfect_square()):
            # __
            result = Item(Value(self.radicand.evaluate()).sqrt())
            result.set_sign(self.sign)
            return result

        # There should be the code to handle the steps of SquareRoots'
        # simplification, in an analog way as by Fractions.
        else:
            # print "here + " + repr(self) + "\n"
            return None

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns SquareRoot(self.object.expand_and_reduce_next_step())
    def expand_and_reduce_next_step(self, **options):
        if self.is_numeric():
            return self.calculate_next_step(**options)
        else:
            return SquareRoot((self.sign,
                               self.radicand.
                               expand_and_reduce_next_step(**options)))

    # --------------------------------------------------------------------------
    ##
    #   @brief Raw display of the SquareRoot (debugging method)
    #   @param options No option available so far
    #   @return A string containing "signSQR{{str(object)}}"
    def __repr__(self, **options):
        return " " + self.sign \
               + "SQR{{ "   \
               + repr(self.radicand)  \
               + " }} "

    # --------------------------------------------------------------------------
    ##
    #   @brief Compares two SquareRoots
    #   @return 0 (i.e. they're equal) if sign, value & exponent are equal
    #   @obsolete ?
    def __eq__(self, other_item):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the SquareRoot's length
    #   @return 1
    def __len__(self):
        return 1

    # --------------------------------------------------------------------------
    ##
    #   @brief Turns the SquareRoot into the fraction item itself over item 1
    def turn_into_fraction(self):
        return Fraction(('+', self, Item(1)))

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the usual writing rules require a × between two factors
    #   @param objct The other one
    #   @param position The position (integer) of self in the Product
    #   @return True if the writing rules require × between self & obj
    def multiply_symbol_is_required(self, objct, position):
        raise NotImplementedError

        # 1st CASE: Item × Item

        # 2d CASE: Item × Product

        # 3d CASE: Item × Sum

        # 4th CASE: Item × Quotient

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the argument requires brackets in a product
    #   For instance, a Sum with several terms or a negative Item
    #   @param position The position of the object in the Product
    #   @return True if the object requires brackets in a Product
    def requires_brackets(self, position):
        # a SquareRoot at first position doesn't need brackets
        if position == 0:
            return False
        # if the SquareRoot isn't at first position,
        # then it depends on its sign
        elif self.sign == '+':
            if self.force_display_sign_once:
                return True
            else:
                return False
        elif self.sign == '-':
            return True

    # --------------------------------------------------------------------------
    ##
    #   @brief Always false for SquareRoots !
    def requires_inner_brackets(self):
        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief Always False for a SquareRoot ?
    #   @param objct The object to search for
    #   @return False
    def contains_exactly(self, objct):
        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief To check if this contains a rounded number...
    #   @return True or False depending on the Value inside
    def contains_a_rounded_number(self):
        return self.radicand.contains_a_rounded_number()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's a numeric SquareRoot
    def is_numeric(self, displ_as=False):
        return self.radicand.is_numeric(displ_as=displ_as)

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's a literal SquareRoot
    def is_literal(self, displ_as=False):
        """
        Return True if SquareRoot is to be considered literal.

        :param displ_as: not applicable to SquareRoots
        """
        return self.radicand.is_literal(displ_as=displ_as)

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's the null SquareRoot
    def is_null(self):
        return self.radicand.is_null()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's positive w/ radicand itself eq. to a single 1
    def is_displ_as_a_single_1(self):
        if self.sign == '+':
            return self.radicand.is_displ_as_a_single_1()

        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's negative w/ radicand itself eq. to a single 1
    def is_displ_as_a_single_minus_1(self):
        if self.sign == '-':
            return self.radicand.is_displ_as_a_single_1()

        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if self.is_null()
    def is_displ_as_a_single_0(self):
        return self.radicand.is_null()

    # --------------------------------------------------------------------------
    ##
    #   @brief Should never be True (if it is, then self is not a SquareRoot)
    def is_displ_as_a_single_numeric_Item(self):
        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single int
    def is_displ_as_a_single_int(self):
        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be considered as a neutral element
    def is_displ_as_a_single_neutral(self, elt):
        if elt == Item(0):
            return self.is_displ_as_a_single_0()
        elif elt == Item(1):
            return self.is_displ_as_a_single_1()
        else:
            raise TypeError('elt must be a neutral element for addition '
                            'or multiplication, i.e. Item(1) | Item(0), '
                            'yet it is {} '.format(repr(elt)))

    # --------------------------------------------------------------------------
    ##
    #   @brief Depends on the radicand
    #   @return True/False
    def is_expandable(self):
        return self.radicand.is_expandable()


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Operation
# @brief Abstract mother class of Quotient and of CommutativeOperation
class Operation(Exponented):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @warning Operation objects are not really usable
    #   @return An "instance" of Operation
    def __init__(self):
        # This is an "external" exponent (like ³ in (x + 5)³ or (3x²)³)
        Exponented.__init__(self)

        # The elements are terms for the Sum and factors for the Product,
        # the numerator and denominator for the Quotient
        self._element = list()

        # The neutral element for the Sum == Item(0)
        # The neutral element for the Product|Quotient == Item(1)
        self._neutral = None

        # The symbol for the Sum is '+' (should be taken from a markup list)
        # The symbol for the Product is '×' (idem)
        # The symbol for the Quotient is '÷' (idem) or a Fraction's bar
        self._symbol = None

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the list of elements
    def get_element(self):
        return self._element

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the list of elements to iter over
    def get_neutral(self):
        return self._neutral

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the symbol field of the Operation
    def get_symbol(self):
        return self._symbol

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the list of elements to iter over
    def get_iteration_list(self):
        return self.element + [self.exponent]

    element = property(get_element,
                       doc="element field of Operation")

    neutral = property(get_neutral,
                       doc="neutral field of Operation")

    symbol = property(get_symbol,
                      doc="symbol field of Operation")

    # --------------------------------------------------------------------------
    ##
    #   @brief
    #   @param n: number of the element to set
    #   @param arg: the object to put as n-th element
    def set_element(self, n, arg):
        if not isinstance(arg, Calculable):
            raise ValueError("arg should be a Calculable")

        self._element[n] = arg.clone()

    # --------------------------------------------------------------------------
    ##
    #   @brief Resets the element field
    def set_symbol(self, arg):
        if not type(arg) == str:
            raise ValueError('arg should be a str')

        else:
            self._symbol = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Resets the element field
    def reset_element(self):
        self._element = []

    # --------------------------------------------------------------------------
    ##
    #   @brief Makes any Operation hashable (so, usable as dictionnary keys)
    #   @warning    Seems that subclasses that redefine __eq__() are forgetting
    #               __hash__()
    def __hash__(self):
        return hash(self.symbol + str(self.sign)
                    + [repr(elt) for elt in self.element].join()
                    + repr(self.exponent))

    # --------------------------------------------------------------------------
    ##
    #   @brief It is possible to index an CommutativeOperation
    def __getitem__(self, i):
        return self._element[i]

    def __setitem__(self, i, data):
        self._element[i] = data

    # --------------------------------------------------------------------------
    ##
    #   @brief Defines the performed CommutativeOperation
    @abstractmethod
    def operator(self, arg1, arg2):
        pass

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Operation contains any Expandable
    #   @return True|False
    def is_expandable(self):
        for elt in self:
            if elt.is_expandable():
                return True

        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Operation contains only numeric elements
    def is_numeric(self, displ_as=False):
        for elt in self:
            if not elt.is_numeric(displ_as=displ_as):
                return False

        return True

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Operation contains only literal terms
    def is_literal(self, displ_as=False) -> bool:
        """
        Return True if Operation is to be considered literal.

        :param displ_as: not applicable to Operations
        """
        for elt in self:
            if not elt.is_literal(displ_as=displ_as):
                return False

        return True


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Quotient
# @brief Sign, Exponented numerator, Exponented denominator, exponent
class Quotient(Operation):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg Quotient|(sign, num, deno [, exponent [, symbol]])
    #   If the argument isn't of the kinds listed above, an exception will be
    #   raised. num and deno are expected to be Exponented ; nevertheless if
    #   they are only Values they get turned into Items.
    #   @param options Can be use_divide_symbol
    #   @todo Maybe: (RANDOMLY, num_max, deno_max) as possible argument ?
    #   @return One instance of Quotient
    def __init__(self, arg, ignore_1_denominator=False, **options):
        Operation.__init__(self)

        self._ignore_1_denominator = ignore_1_denominator
        # default initialization of other fields
        self._numerator = Value(1)
        self._denominator = Value(1)
        self._symbol = 'like_a_fraction'

        if 'use_divide_symbol' in options and options['use_divide_symbol']:
            self._symbol = 'use_divide_symbol'

        # 1st CASE: (sign, Exponented num, Exponented deno)
        if (type(arg) == tuple and len(arg) >= 3 and arg[0] in ['+', '-']
            and (isinstance(arg[1], Calculable) or is_number(arg[1])
                 or type(arg[1]) is str)
            and (isinstance(arg[2], Calculable) or is_number(arg[2]) or
                 type(arg[2]) is str)):
            # __
            self._sign = arg[0]
            if (is_number(arg[1]) or type(arg[1]) is str
                or isinstance(arg[1], Value)):
                # __
                self._numerator = Item(arg[1])
            else:
                self._numerator = arg[1].clone()

            if (is_number(arg[2]) or type(arg[2]) is str
                or isinstance(arg[2], Value)):
                # __
                self._denominator = Item(arg[2])
            else:
                self._denominator = arg[2].clone()

        # 2d CASE: imbricated in the 1st
            if len(arg) >= 4:
                if is_number(arg[3]):
                    self._exponent = Value(arg[3])
                else:
                    self._exponent = arg[3].clone()

            if len(arg) >= 5:
                self._symbol = arg[4]

        # 3d CASE: another Quotient to copy
        elif isinstance(arg, Quotient):
            self._exponent = arg.exponent.clone()
            self._numerator = arg.numerator.clone()
            self._denominator = arg.denominator.clone()
            self._sign = arg.sign
            self._symbol = arg.symbol
            self._ignore_1_denominator = arg._ignore_1_denominator

        # All other unforeseen cases: an exception is raised.
        else:
            raise TypeError('Got: ' + str(type(arg))
                            + 'instead of (sign, numerator, denominator)|'
                            '(sign, numerator, denominator, exponent)')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the sign of the object
    def get_sign(self):
        return self._sign

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the numerator of the object
    def get_numerator(self):
        return self._numerator

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the denominator of the object
    def get_denominator(self):
        return self._denominator

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the list of elements to iter over
    def get_iteration_list(self):
        return [self.numerator, self.denominator, self.exponent]

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the number of '-' signs of the Quotient
    #   @return The number of '-' signs of the Quotient
    def get_minus_signs_nb(self):
        answer = 0
        if self.sign == '-':
            answer += 1

        return answer + self.numerator.get_minus_signs_nb() \
            + self.denominator.get_minus_signs_nb()

    numerator = property(get_numerator,
                         doc="numerator field of Quotient")

    denominator = property(get_denominator,
                           doc="denominator field of Quotient")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the numerator of the object
    def set_numerator(self, arg):
        if not isinstance(arg, Exponented):
            raise ValueError("arg should be an Exponented")

        else:
            self._numerator = arg.clone()

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the denominator of the object
    def set_denominator(self, arg):
        if not isinstance(arg, Exponented):
            raise ValueError("arg should be an Exponented")

        else:
            self._denominator = arg.clone()

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        global expression_begins
        log = settings.dbg_logger.getChild('Quotient.into_str')

        if (self._ignore_1_denominator
            and self.denominator.is_displ_as_a_single_1()):
            if self.sign == '-':
                return Product([Value(-1), self.numerator]).into_str(**options)
            else:
                return Product([Value(1), self.numerator]).into_str(**options)

        log.debug("Entering with: " + repr(self))
        if ('force_expression_begins' in options
            and options['force_expression_begins']):
            # __
            expression_begins = True
            options['force_expression_begins'] = False

        if 'force_position' in options \
           and is_integer(options['force_position']):
            # __
            temp_options = dict()
            for key in options:
                if key != 'force_position':
                    temp_options[key] = options[key]
            options = temp_options

        # Quotient objects displaying
        sign = ''
        nume = ''
        deno = ''

        if self.sign == '+' and not expression_begins:
            sign = MARKUP['plus']
        elif self.sign == '-':
            sign = MARKUP['minus']

        expression_begins = True
        nume = self.numerator.into_str(force_position=0,
                                       **options)
        expression_begins = True
        deno = self.denominator.into_str(force_position=0,
                                         **options)

        if self.symbol == 'use_divide_symbol':
            if isinstance(self.numerator, Sum) \
               and len(self.numerator.throw_away_the_neutrals()) >= 2 \
               and not self.numerator.requires_inner_brackets():
                # __
                nume = MARKUP['opening_bracket'] \
                    + nume \
                    + MARKUP['closing_bracket']

            if isinstance(self.denominator, Sum) \
               and len(self.denominator.throw_away_the_neutrals()) >= 2 \
               and not self.denominator.requires_inner_brackets():
                # __
                deno = MARKUP['opening_bracket'] \
                    + deno + MARKUP['closing_bracket']

            # This is made to avoid having 4 ÷ -5
            # but to get 4 ÷ (-5) instead
            elif self.denominator.get_sign() == '-':
                # __
                deno = MARKUP['opening_bracket'] \
                    + deno + MARKUP['closing_bracket']

        if self.exponent_must_be_displayed():
            expression_begins = True
            exponent_string = self.exponent.into_str(**options)

            if self.symbol == 'like_a_fraction':
                return sign + MARKUP['opening_bracket']                       \
                            + MARKUP['opening_fraction']                      \
                            + nume                                            \
                            + MARKUP['fraction_vinculum']                     \
                            + deno                                            \
                            + MARKUP['closing_fraction']                      \
                            + MARKUP['closing_bracket']                       \
                            + MARKUP['opening_exponent']                      \
                            + exponent_string                                 \
                            + MARKUP['closing_exponent']

            else:
                return sign + MARKUP['opening_bracket']                       \
                            + nume                                            \
                            + MARKUP['divide']                                \
                            + deno                                            \
                            + MARKUP['closing_bracket']                       \
                            + MARKUP['opening_exponent']                      \
                            + exponent_string                                 \
                            + MARKUP['closing_exponent']

        else:
            if options.get('js_repr', False):
                return '{}{}/{}'.format(sign, nume, deno)
            if self.symbol == 'like_a_fraction':
                return sign + MARKUP['opening_fraction']                      \
                            + nume                                            \
                            + MARKUP['fraction_vinculum']                     \
                            + deno                                            \
                            + MARKUP['closing_fraction']

            else:
                return sign + nume                                            \
                            + MARKUP['divide']                                \
                            + deno

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the value of a numerically evaluable object
    def evaluate(self, **options):
        if not('stop_recursion' in options and options['stop_recursion']):
            next_step = self.calculate_next_step()

            if next_step is not None:
                return next_step.evaluate()

        if self.sign == '+':
            sign = 1
        else:
            sign = -1

        num = self.numerator.evaluate()
        deno = self.denominator.evaluate()

        return sign * (num / deno) ** self.exponent.evaluate()

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Quotient in the next step of simplification
    #   @todo The case where exponent has to be calculated as well.
    def calculate_next_step(self, **options):
        details_level = options.get('details_level', 'maximum')
        # First, check if any of numerator | denominator needs to be
        # calculated. If so, return the Quotient one step further.
        if isinstance(self.denominator, Fraction):
            if self.sign == '+':
                sign_item = Item(1)
            else:
                sign_item = Item(-1)

            next_step = Product([sign_item,
                                 self.numerator,
                                 self.denominator.invert()])
            next_step.set_exponent(self.exponent)
            return next_step.throw_away_the_neutrals()

        if 'decimal_result' in options:
            return Item(self.evaluate(**options))\
                .rounded(options['decimal_result'])

        if self.numerator.calculate_next_step(**options) is not None:
            if self.denominator.calculate_next_step(**options) is not None:
                return Quotient((self.sign,
                                 self.numerator.calculate_next_step(
                                     **options),
                                 self.denominator.calculate_next_step(
                                     **options),
                                 self.exponent,
                                 self.symbol))
            else:
                return Quotient((self.sign,
                                 self.numerator.calculate_next_step(**options),
                                 self.denominator,
                                 self.exponent,
                                 self.symbol))

        elif self.denominator.calculate_next_step(**options) is not None:
            return Quotient((self.sign,
                             self.numerator,
                             self.denominator.calculate_next_step(**options),
                             self.exponent,
                             self.symbol))

        # Now, neither the numerator nor the denominator can be calculated
        else:
            if self.sign == '+':
                sign_item = Item(1)
            else:
                sign_item = Item(-1)
            if isinstance(self.denominator, Quotient):

                next_step = Product([sign_item,
                                     self.numerator,
                                     self.denominator.invert()])
                next_step.set_exponent(self.exponent)
                return next_step

            elif isinstance(self.numerator, Quotient):
                if details_level == 'maximum':
                    c = Quotient
                    if isinstance(self.denominator, Item):
                        c = Fraction
                    next_step = Product([sign_item,
                                         self.numerator,
                                         c(('+', Item(1), self.denominator))])
                elif details_level == 'medium':
                    c = Quotient
                    if all([(isinstance(x, Item) or isinstance(x, Product))
                            for x in [self.numerator.numerator,
                                      self.numerator.denominator,
                                      self.denominator]]):
                        c = Fraction
                    next_step = c((self.sign, self.numerator.numerator,
                                   Product([self.numerator.denominator,
                                            self.denominator])))
                elif details_level == 'none':
                    c = Quotient
                    if all([(isinstance(x, Item) or isinstance(x, Product))
                            for x in [self.numerator.numerator,
                                      self.numerator.denominator,
                                      self.denominator]]):
                        c = Fraction
                    next_step = c((self.sign, self.numerator.numerator,
                                   Product([self.numerator.denominator,
                                            self.denominator]))) \
                        .calculate_next_step(**options)
                next_step.set_exponent(self.exponent)
                return next_step

            else:
                val = Item(self.evaluate(stop_recursion=True,
                                         **options)).rounded(3)
                return val

    def expand_and_reduce_next_step(self, **options):
        """If possible, expands Quotient's numerator and/or denominator."""
        next_nume = self.numerator.expand_and_reduce_next_step(**options)
        next_deno = self.denominator.expand_and_reduce_next_step(**options)
        if (next_nume, next_deno) != (None, None):
            if next_nume is None:
                next_nume = self.numerator.clone()
            if next_deno is None:
                next_deno = self.denominator.clone()
            result = Quotient(self)
            result.set_numerator(next_nume)
            result.set_denominator(next_deno)
            return result
        else:
            return self.calculate_next_step(**options)

    # --------------------------------------------------------------------------
    ##
    #   @brief Raw display of the Quotient (debugging method)
    #   @param options No option available so far
    #   @return A string: "Q# sign ( numerator / denominator )^{ exponent }#Q"
    def __repr__(self, **options):
        return "Q# " +                                       \
               str(self.sign) +                                               \
               " ( " +                                                        \
               repr(self.numerator) +                                     \
               " / " +                                                        \
               repr(self.denominator) +                                   \
               " ) ^ | " +                                                    \
               repr(self.exponent) +                                      \
               " }| #Q"

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Quotient's length
    #   It is used in Product.into_str(), changing it will have consequences
    #   on sheets like Fractions Products & Quotients...
    #   @return 1
    def __len__(self):
        return 1

    # --------------------------------------------------------------------------
    ##
    #   @brief Defines the performed Operation as a Quotient
    def operator(self, arg1, arg2):
        return arg1 / arg2

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the usual writing rules require a × between two factors
    #   @param objct The other one
    #   @param position The position (integer) of self in the Product
    #   @return True if the writing rules require × between self & obj
    def multiply_symbol_is_required(self, objct, position):
        # 1st CASE: Quotient × Quotient
        if isinstance(objct, Quotient):
            return True

        # 2d CASE: Quotient × <anything but a Quotient>
        if objct.is_literal(displ_as=True):
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the argument requires brackets in a product
    #   For instance, a Sum with several terms or a negative Item
    #   @param position The position of the object in the Product
    #   @return True if the object requires brackets in a Product
    def requires_brackets(self, position):
        if self.sign == '-' and position >= 1:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the argument requires inner brackets
    #   The reason for requiring them is having an exponent different from 1
    #   @return True if the object requires inner brackets
    def requires_inner_brackets(self):
        return self.exponent_must_be_displayed()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Quotient contains exactly the given objct
    #   It can be used to detect objects embedded in this Quotient (with
    #   a denominator equal to 1)
    #   @param objct The object to search for
    #   @return True if the Quotient contains exactly the given objct
    def contains_exactly(self, objct):
        if self.denominator.is_displ_as_a_single_1() \
           and self.sign == '+':
            # __
            if self.numerator == objct:
                return True
            else:
                return self.numerator.contains_exactly(objct)

        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief To check if this contains a rounded number...
    #   @return True or False
    def contains_a_rounded_number(self):
        if self.numerator.contains_a_rounded_number() \
           or self.denominator.contains_a_rounded_number():
            # __
            return True

        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the inverted Quotient
    def invert(self):
        new_quotient = Quotient(self)
        if isinstance(self, Fraction):
            new_quotient = Fraction(self)
        new_quotient.set_numerator(self.denominator)
        new_quotient.set_denominator(self.numerator)

        return new_quotient

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the numerator is null
    def is_null(self):
        return self.numerator.is_null()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Quotient contains only single 1-equivalent Calcs.
    # So, if the Quotient has a positive sign and if its numerator and
    # both are equivalent to single 1.
    def is_displ_as_a_single_1(self):
        return self.sign == '+'\
            and self.numerator.is_displ_as_a_single_1()\
            and self.denominator.is_displ_as_a_single_1()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Quotient can be displayed as a single -1
    # If the Quotient is negative and its numerator and
    # both are equivalent to single 1.
    #   @todo Other cases should return True as well
    #         (use the sign_of_product())
    def is_displ_as_a_single_minus_1(self):
        return self.sign == '-' \
            and self.numerator.is_displ_as_a_single_1() \
            and self.denominator.is_displ_as_a_single_1()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Quotient can be displayed as a single 0
    # If the numerator is equivalent to a single 0
    def is_displ_as_a_single_0(self):
        return self.numerator.is_displ_as_a_single_0()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object is or only contains one numeric Item
    def is_displ_as_a_single_numeric_Item(self):
        if not self.is_numeric():
            return False
        else:
            return (self.denominator.is_displ_as_a_single_1()
                    and self.numerator.is_displ_as_a_single_numeric_Item())

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single int
    def is_displ_as_a_single_int(self):
        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be considered as a neutral element
    def is_displ_as_a_single_neutral(self, elt):
        if elt == Item(0):
            return self.is_displ_as_a_single_0()
        elif elt == Item(1):
            return self.is_displ_as_a_single_1()
        else:
            raise TypeError('Got: ' + str(type(elt))
                            + ' instead of a neutral element for addition'
                            ' or multiplication, e.g. Item(1) | Item(0).')


class Division(Quotient):
    """Same as Quotient, but using ÷ sign as default."""

    def __init__(self, arg, ignore_1_denominator=False, **options):
        options.update({'use_divide_symbol': True})
        super().__init__(arg, ignore_1_denominator=False, **options)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Fraction
# @brief Quotient of two numeric Sums and/or Products
class Fraction(Quotient):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg Fraction|decimal.Decimal|(num,den)|(sign,num,den)
    #              |(sign,num,den,exponent)|
    #              zero-degree-Monomial having a Fraction as coefficient
    #   @param **options copy_other_fields_from=<Fraction>
    #                    -> can be used with (num, den) to get all the
    #                       other fields from the given Fraction (including
    #                       sign)
    #   @todo ? raise a division by zero error !
    #   @return One instance of Fraction
    def __init__(self, arg, ignore_1_denominator=False, **options):
        Exponented.__init__(self)

        # default initialization of the other fields
        self._numerator = Product([Item(1)])
        self._denominator = Product([Item(2)])
        self._status = "nothing"
        self._symbol = 'like_a_fraction'
        self._same_deno_reduction_in_progress = False
        self._ignore_1_denominator = ignore_1_denominator

        arg_sign = 'default'
        arg_nume = 'default'
        arg_deno = 'default'

        if type(arg) == tuple:
            if len(arg) >= 3 and arg[0] != RANDOMLY:
                arg_sign = arg[0]
                arg_nume = arg[1]
                arg_deno = arg[2]
            elif len(arg) == 2:
                arg_nume = arg[0]
                arg_deno = arg[1]

        # 1st CASE:
        # The argument's a tuple containing exactly one sign and 2 Exponenteds
        # OR (num,den)[, copy_other_fields_from=<Fraction>]
        if (type(arg) == tuple and len(arg) >= 2 and arg[0] != RANDOMLY
            and ((isinstance(arg_nume, Exponented) and arg_nume.is_numeric())
                 or is_number(arg_nume))
            and ((isinstance(arg_deno, Exponented) and arg_deno.is_numeric())
                 or is_number(arg_deno))):
            # __

            if is_number(arg_nume):
                self._numerator = Product([Item(arg_nume)])
            elif not isinstance(arg_nume, Product):
                self._numerator = Product(arg_nume.clone())
            else:
                self._numerator = arg_nume.clone()

            if is_number(arg_deno):
                self._denominator = Product([Item(arg_deno)])
            elif not isinstance(arg_deno, Product):
                self._denominator = Product(arg_deno.clone())
            else:
                self._denominator = arg_deno.clone()

            if (len(arg) == 2
                and 'copy_other_fields_from' in options
                and isinstance(options['copy_other_fields_from'], Fraction)):
                # __
                self._exponent = options['copy_other_fields_from']\
                    .exponent.clone()
                self._sign = options['copy_other_fields_from'].sign
                self._status = options['copy_other_fields_from'].status
                self._symbol = options['copy_other_fields_from'].symbol
                self._same_deno_reduction_in_progress = \
                    options['copy_other_fields_from']\
                    .same_deno_reduction_in_progress

            if len(arg) >= 3 and arg_sign in ['+', '-']:
                self._sign = arg[0]

            if len(arg) >= 4:
                self._exponent = arg[3].clone()

        # 2d CASE: removed (RANDOMLY unused)

        # 3d CASE:
        # The argument's a Fraction to copy
        elif isinstance(arg, Fraction):
            self._exponent = arg.exponent.clone()
            self._numerator = arg.numerator.clone()
            self._denominator = arg.denominator.clone()
            self._sign = arg.sign
            self._status = arg.status
            self._same_deno_reduction_in_progress = \
                arg.same_deno_reduction_in_progress
            self._ignore_1_denominator = arg._ignore_1_denominator

        # 4th CASE:
        elif isinstance(arg, Decimal):
            f = Number(10) ** max(1, Number(arg).fracdigits_nb())
            self._numerator = Product([Item(Number(Number(f) * Number(arg))
                                            .standardized())])
            self._denominator = Product([Item(f)])

        # 5th CASE: COMMENTED OUT SINCE IT SEEMS UNUSED: A zero-degree
        # Monomial having a Fraction as coefficient
        # elif (isinstance(arg, Monomial) and arg.is_numeric()
        #       and isinstance(arg.factor[0], Fraction)):
        #     # __
        #     self._exponent = Value(1)
        #     self._numerator = arg.factor[0].numerator.clone()
        #     self._denominator = arg.factor[0].denominator.clone()
        #     self._sign = arg.factor[0].sign
        #     self._status = arg.factor[0].status
        #     self._same_deno_reduction_in_progress = \
        #         arg.factor[0].same_deno_reduction_in_progress

        # All unforeseen cases: an exception is raised
        else:
            raise TypeError('Got: ' + str(type(arg))
                            + ' instead of (sign, numerator, denominator)')

        # Now it may be useful to de-embbed some Products or Sums...
        temp_objects = [self.numerator, self.denominator]

        for i in range(len(temp_objects)):
            if len(temp_objects[i]) == 1:
                if (isinstance(temp_objects[i].factor[0], Sum)
                    and len(temp_objects[i].factor[0]) == 1):
                    # __
                    temp_objects[i] = temp_objects[i].factor[0].term[0]

                elif (isinstance(temp_objects[i].factor[0], Product)
                      and len(temp_objects[i].factor[0]) == 1):
                    # __
                    temp_objects[i] = temp_objects[i].factor[0].factor[0]

                if not isinstance(temp_objects[i], Product):
                    temp_objects[i] = Product([temp_objects[i]])

        self._numerator = temp_objects[0]
        self._denominator = temp_objects[1]

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Fraction's status
    #   @return the Fraction's status
    def get_status(self):
        return self._status

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Fraction's status
    #   @return the Fraction's status
    def get_same_deno_reduction_in_progress(self):
        return self._same_deno_reduction_in_progress

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns True if Fraction's status is simplification_in_progress
    #   @return True if Fraction's status is simplification_in_progress
    def get_simplification_in_progress(self):
        for i in range(len(self.numerator)):
            if isinstance(self.numerator.factor[i], Item):
                if self.numerator.factor[i].is_out_striked:
                    return True

        for i in range(len(self.denominator)):
            if isinstance(self.denominator.factor[i], Item):
                if self.denominator.factor[i].is_out_striked:
                    return True

        return False

    def get_first_letter(self):
        return self._numerator.get_first_letter()

    status = property(get_status,
                      doc="Fraction's status")

    simplification_in_progress = property(get_simplification_in_progress,
                                          doc="Fraction's simplification_"
                                          "in_progress status")

    same_deno_reduction_in_progress = \
        property(get_same_deno_reduction_in_progress,
                 doc="Fraction's same_deno_reduction_in_progress field")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the Fraction's status
    def set_status(self, arg):
        if not type(arg) == str:
            raise ValueError("arg should be a str")

        else:
            self._status = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the Fraction's status
    def set_same_deno_reduction_in_progress(self, arg):
        if arg not in [True, False]:
            raise ValueError("arg should be True|False")

        else:
            self._same_deno_reduction_in_progress = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the sign of the fraction and of numerator in the case
    #   @brief of this example: +{-2}/{5} (nothing to compute just the minus
    #   @brief sign to put "down"
    #   @return True if Fraction's status is simplification_in_progress
    def set_down_numerator_s_minus_sign(self):
        if (len(self.numerator) == 1
            and self.numerator.calculate_next_step() is None
            and len(self.denominator) == 1
            and self.denominator.calculate_next_step() is None
            and self.denominator.get_sign() == '+'
            and self.numerator.get_sign() == '-'
            and self.get_sign() == '+'):
            # __
            self.set_sign(sign_of_product([self.get_sign(),
                                           self.numerator.get_sign()]))
            self.numerator.set_sign('+')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the value of a numerically evaluable object
    def evaluate(self, **options):
        if ('keep_not_decimal_nb_as_fractions' in options
            and options['keep_not_decimal_nb_as_fractions']
            and not self.is_a_decimal_number()):
            # __
            return self.completely_reduced()
        else:
            return Quotient.evaluate(self, **options)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns None|The Fraction in the next step of simplification
    #   @todo Fix the 4th case. Should be less cases... check source
    #   @todo Fix the /!\ or check if the 3d CASE is not obsolete (duplicated
    #   in the simplified method)
    def calculate_next_step(self, **options):
        log = settings.dbg_logger.getChild(
            'Fraction.calculate_next_step')
        log.debug("Entering with: " + repr(self))

        # First, let's handle the case when a Decimal Result is awaited
        # rather than a Fraction's simplification
        if 'decimal_result' in options \
           and self.numerator.calculate_next_step() is None \
           and self.denominator.calculate_next_step() is None:
            # __
            if self.sign == '+':
                result_sign = 1
            else:
                result_sign = -1
            result = Item(Value(result_sign * self.numerator.evaluate()
                                / self.denominator.evaluate())
                          .rounded(options['decimal_result']))
            log.debug("Decimal calculation has been done. Result: \n"
                      + repr(result) + " which _has_been_rounded: "
                      + str(result.contains_a_rounded_number()))
            return result

        temp_next_nume = self.numerator.calculate_next_step(**options)
        temp_next_deno = self.denominator.calculate_next_step(**options)

        # 1st CASE
        if self.simplification_in_progress:
            self_simplified = Fraction(self).simplified()
            if (isinstance(self_simplified, Item)
                or (isinstance(self_simplified, Fraction)
                    and not self_simplified.is_reducible())):
                # __
                log.debug("1st CASE-a")
                return self_simplified
            else:
                log.debug("1st CASE-b")
                aux_fraction = Fraction(self)
                aux_fraction = aux_fraction.replace_striked_out()
                aux_fraction.set_numerator(
                    aux_fraction.numerator.throw_away_the_neutrals())
                aux_fraction.set_denominator(
                    aux_fraction.denominator.throw_away_the_neutrals())
                return aux_fraction.simplification_line()

        # 2d CASE
        elif self.same_deno_reduction_in_progress:
            log.debug("2d CASE")
            new_nume = self.numerator
            new_deno = self.denominator

            if temp_next_nume is not None:
                new_nume = temp_next_nume
            if temp_next_deno is not None:
                new_deno = temp_next_deno

            resulting_fraction = Fraction((new_nume, new_deno),
                                          copy_other_fields_from=self)

            if temp_next_deno is not None or temp_next_nume is not None:
                return resulting_fraction
            else:
                return None

        # 3d CASE
        elif self.is_reducible():
            log.debug("3d CASE")
            return self.simplification_line()

        # 4th CASE
        # don't forget to put the exponent of the fraction on the numerator !!
        # obsolete ?
        elif self.denominator.is_displ_as_a_single_1():
            log.debug("4th CASE")
            if self.sign == '-':
                # /!\ this might lead to results like -(-3) instead of 3
                return Item((Product([Item(-1), self.numerator])).evaluate())
            else:
                return self.numerator

        # 5th CASE
        elif temp_next_nume is not None or temp_next_deno is not None:
            log.debug("6th CASE")
            new_nume = self.numerator
            new_deno = self.denominator

            if temp_next_nume is not None:
                new_nume = temp_next_nume
            if temp_next_deno is not None:
                new_deno = temp_next_deno

            resulting_fraction = Fraction((new_nume, new_deno),
                                          copy_other_fields_from=self)

            resulting_fraction.set_down_numerator_s_minus_sign()

            return resulting_fraction

        # 6th CASE
        elif ((len(self.numerator) == 1
               and self.numerator.factor[0].get_sign() == '-')
              or (len(self.denominator) == 1
                  and self.denominator.factor[0].get_sign() == '-')):
            # __
            self.set_sign(sign_of_product([self.get_sign(),
                                           self.numerator.get_sign(),
                                           self.denominator.get_sign()]))
            self.numerator.factor[0].set_sign('+')
            self.denominator.factor[0].set_sign('+')
            return self

        # 7th CASE
        # don't forget to check the exponent of the fraction
        # before returning None... if it's not equivalent to a single 1, it
        # should be put on both numerator & denominator
        else:
            log.debug("7th CASE")
            return None

    # --------------------------------------------------------------------------
    ##
    #   @brief Same as calculate_next_step in the case of Fractions
    def expand_and_reduce_next_step(self, **options):
        return self.calculate_next_step(**options)

    # --------------------------------------------------------------------------
    ##
    #   @brief Raw display of the Fraction (debugging method)
    #   @param options No option available so far
    #   @return A string: "F# sign ( numerator / denominator )^{ exponent }#F"
    def __repr__(self, **options):
        return "F# " + str(self.sign) + " ( " + repr(self.numerator) \
            + " / " + repr(self.denominator)\
            + " ) ^ | " + repr(self.exponent) + " | #F"

    # --------------------------------------------------------------------------
    ##
    #   @brief Makes Fractions hashable (so, usable as dictionnary keys)
    def __hash__(self):
        return hash(repr(self._numerator) + str(self.sign)
                    + self._status + self._symbol + repr(self._denominator))

    # --------------------------------------------------------------------------
    ##
    #   @brief Compares two Fractions
    #   @return True if they're equal
    def __eq__(self, obj):
        if not isinstance(obj, Fraction):
            return False

        if (self.sign == obj.sign
            and self.numerator == obj.numerator
            and self.denominator == obj.denominator
            and self.exponent == obj.exponent):
            # __
            return True
        else:
            # it is difficult to tell whether a Fraction is greater or
            # lower than another... needs same denominator reduction etc.
            return False

    def __lt__(self, obj):
        if isinstance(obj, Fraction):
            return self.evaluate() < obj.evaluate()
        elif is_number(obj):
            return self < Fraction(Decimal(obj))

    def __gt__(self, obj):
        if isinstance(obj, Fraction):
            return self.evaluate() > obj.evaluate()
        elif is_number(obj):
            return self > Fraction(Decimal(obj))

    def __le__(self, obj):
        if isinstance(obj, Fraction):
            return self.evaluate() <= obj.evaluate()
        elif is_number(obj):
            return self <= Fraction(Decimal(obj))

    def __ge__(self, obj):
        if isinstance(obj, Fraction):
            return self.evaluate() >= obj.evaluate()
        elif is_number(obj):
            return self >= Fraction(Decimal(obj))

    # --------------------------------------------------------------------------
    ##
    #   @brief Simplification line of a fraction
    # i.e. Factorization of numerator and denominator in the right smaller
    # numbers Products.
    #   @todo Add an option to __init__ to allow "inserting Products": see code
    #   @todo maybe the case of Item having a negative *value* has not been
    # managed. I mean, Items like ±(-2)
    #   @return One Fraction
    def simplification_line(self):
        log = settings.dbg_logger.getChild(
            'Fraction.simplification_line')
        if not self.is_reducible():
            return self

        elif self.numerator.evaluate() == 0:
            return Item(0)

        else:
            # the new numerator will be constructed this way:
            # first create a Product containing as many factors as the
            # original one but each factor replaced by a one ; same action
            # for numerator and denominator
            # these ones will be later replaced by the processed values (like
            # striked Items) or at the end by the original values for the
            # factors that haven't changed.
            new_numerator = Product([Item(1)
                                     for i in range(len(self.numerator))])
            new_denominator = Product([Item(1)
                                       for i in range(len(self.denominator))])

            this_numerators_factor_has_been_processed = \
                [False for i in range(len(self.numerator))]
            this_denominators_factor_has_been_processed = \
                [False for i in range(len(self.denominator))]

            # If this method is called on a fraction which already contains
            # striked out Items, then they shouldn't be taken in account, so
            # let's consider them as already processed
            # for i in xrange(len(self.numerator)):
            #    if isinstance(self.numerator.factor[i], Item) and   \
            #       self.numerator.factor[i].is_out_striked:
            #        # __
            #        this_numerators_factor_has_been_processed[i] = True

            # for j in xrange(len(self.denominator)):
            #    if isinstance(self.denominator.factor[j], Item) and   \
            #       self.denominator.factor[j].is_out_striked:
            #        # __
            #        this_denominators_factor_has_been_processed[j] = True

            # Let's first check if there are any factors already "strikable"
            # like in <10×5>/<5×9>
            # If we don't do that first, the first 10 will turn into <5×2> and
            # its 5 will be simplified with the one of the denominator ;
            # which is not false but it would be more natural to simplify the
            # two 5 before decomposing any factor
            for i in range(len(self.numerator)):
                for j in range(len(self.denominator)):
                    if (self.numerator.factor[i].raw_value
                        == self.denominator.factor[j].raw_value
                        and not
                        (this_numerators_factor_has_been_processed[i]
                         or this_denominators_factor_has_been_processed[j])):
                        # __
                        new_numerator.set_element(i,
                                                  self.numerator
                                                  .factor[i].clone())
                        new_numerator.element[i].set_is_out_striked(True)
                        log.debug("[0] Striked out: "
                                  + repr(new_numerator.factor[i]))
                        new_denominator.set_element(j,
                                                    self.denominator
                                                    .factor[j].clone())
                        new_denominator.factor[j].set_is_out_striked(True)
                        log.debug("[1] Striked out: "
                                  + repr(new_denominator.factor[j]))

                        this_numerators_factor_has_been_processed[i] = True
                        this_denominators_factor_has_been_processed[j] = True

            # Now let's check if decomposing some factors could help simplify
            # the fraction
            for i in range(len(self.numerator)):
                for j in range(len(self.denominator)):
                    if not this_denominators_factor_has_been_processed[j] \
                       and not this_numerators_factor_has_been_processed[i]:
                        # __
                        g = pupil_gcd(self.numerator.factor[i].raw_value,
                                      self.denominator.factor[j].raw_value)
                        if g != 1:
                            if g == self.numerator.factor[i].raw_value:
                                new_numerator.set_element(i,
                                                          self.numerator
                                                          .factor[i].clone())

                                new_numerator.factor[i]\
                                    .set_is_out_striked(True)

                                log.debug("[2A]Striked out: "
                                          + repr(new_numerator.factor[i]))

                                this_numerators_factor_has_been_processed[i] =\
                                    True

                                factor1 = g
                                factor2 = self.denominator.factor[j]\
                                    .raw_value / g

                                if self.denominator.factor[j].sign == '-':
                                    factor1 *= -1

                                item1 = Item(factor1)
                                item1.set_is_out_striked(True)
                                log.debug("[2B]Striked out: " + repr(item1))

                                item2 = Item(factor2)

                                new_denominator.factor[j] = \
                                    Product([item1, item2])

                                this_denominators_factor_has_been_processed[j]\
                                    = True

                            elif g == self.denominator.factor[j].raw_value:
                                new_denominator.factor[j] = self.denominator\
                                    .factor[j].clone()
                                new_denominator.factor[j].set_is_out_striked(
                                    True)
                                this_denominators_factor_has_been_processed[j]\
                                    = True
                                factor1 = g
                                factor2 = self.numerator.factor[i]\
                                    .raw_value / g
                                if self.numerator.factor[i].sign == '-':
                                    factor1 *= -1
                                item1 = Item(factor1)
                                item1.set_is_out_striked(True)
                                log.debug("[3]Striked out: " + repr(item1))
                                item2 = Item(factor2)
                                new_numerator.factor[i] = Product([item1,
                                                                   item2])
                                this_numerators_factor_has_been_processed[i] =\
                                    True
                            else:
                                factor1 = g
                                factor2 = self.numerator.factor[i]\
                                    .raw_value / g
                                if self.numerator.factor[i].sign == '-':
                                    factor1 *= -1
                                item1 = Item(factor1)
                                item1.set_is_out_striked(True)
                                log.debug("[4]Striked out: " + repr(item1))
                                item2 = Item(factor2)
                                new_numerator.factor[i] = Product([item1,
                                                                  item2])
                                this_numerators_factor_has_been_processed[i] =\
                                    True
                                factor1 = g
                                factor2 = \
                                    self.denominator.factor[j].raw_value / g
                                if self.denominator.factor[j].sign == '-':
                                    factor1 *= -1
                                item1 = Item(factor1)
                                item1.set_is_out_striked(True)
                                log.debug("[5]Striked out: " + repr(item1))
                                item2 = Item(factor2)
                                new_denominator.factor[j] = Product([item1,
                                                                     item2])
                                this_denominators_factor_has_been_processed[j]\
                                    = True
            for i in range(len(new_numerator)):
                if not this_numerators_factor_has_been_processed[i]:
                    new_numerator.factor[i] = self.numerator.factor[i]
            for j in range(len(new_denominator)):
                if not this_denominators_factor_has_been_processed[j]:
                    new_denominator.factor[j] = self.denominator.factor[j]

            # Check if there are some unstriked factors left that could've
            # been striked: (it is the case when simplifying fractions like
            # <8×3>/<5×6>: at this point, the fraction is
            # <<2×4>×3>/<5×<2×3>>) with striked 2s but not striked 3s !
            # So, first, let's "dissolve" the inserted Products
            # (e.g. if numerator "<3×8>" has been transformed into "<3×<2×4>>"
            # let's rewrite it "<3×2×4>")
            # Products imbricated in Products imbricated in Products... are not
            # managed recursively by this function. If that should be useful,
            # an auxiliary function doing that could be implemented. (or
            # maybe an option in __init__ (which is recursive), which would
            # be much better)
            final_numerator = []
            final_denominator = []
            for i in range(len(new_numerator)):
                if isinstance(new_numerator.factor[i], Item):
                    final_numerator.append(new_numerator.factor[i].clone())
                elif isinstance(new_numerator.factor[i], Product):
                    for j in range(len(new_numerator.factor[i])):
                        final_numerator.append(new_numerator.factor[i]
                                               .factor[j].clone())

            for i in range(len(new_denominator)):
                if isinstance(new_denominator.factor[i], Item):
                    final_denominator.append(new_denominator.factor[i].clone())
                elif isinstance(new_denominator.factor[i], Product):
                    for j in range(len(new_denominator.factor[i])):
                        final_denominator.append(new_denominator.factor[i]
                                                 .factor[j].clone())

            # Now let's check if some unstriked Items could be striked
            for i in range(len(final_numerator)):
                if not final_numerator[i].is_out_striked:
                    for j in range(len(final_denominator)):
                        if not final_denominator[j].is_out_striked:
                            if (final_numerator[i].raw_value
                                == final_denominator[j].raw_value):
                                # __
                                final_numerator[i].set_is_out_striked(True)
                                log.debug("[6]Striked out: "
                                          + repr(final_numerator[i]))
                                final_denominator[j].set_is_out_striked(True)
                                log.debug("[7]Striked out: "
                                          + repr(final_denominator[j]))

            # Now let's simplify eventually minus signs and display them
            # as forced "+". We'll do that only if the numerator and/or the
            # denominator have at least 2 elements. (More simple cases are
            # handled somewhere else, in a different way: we want the -2/-5
            # fraction first be visible and then the - signs just "disappear").
            # We'll convert them into plusses just two by two.
            position_of_the_last_minus_sign = None
            if self.sign == '-':
                    position_of_the_last_minus_sign = ('f', 0)
            if len(final_numerator) >= 2 or len(final_denominator) >= 2:
                log.debug("Entering minus signs simplification")
                for K in [final_numerator, final_denominator]:
                    for i in range(len(K)):
                        if K[i].get_sign() == '-':
                            if position_of_the_last_minus_sign is None:
                                if K == final_numerator:
                                    position_of_the_last_minus_sign = ('n', i)
                                else:
                                    position_of_the_last_minus_sign = ('d', i)
                            elif position_of_the_last_minus_sign[0] == 'f':
                                self.set_sign('+')
                                K[i].set_sign('+')
                                K[i].set_force_display_sign_once(True)
                                position_of_the_last_minus_sign = None
                                log.debug(" [A] 2 signs set to '+' ")
                            elif position_of_the_last_minus_sign[0] == 'n':
                                final_numerator[
                                    position_of_the_last_minus_sign[1]]\
                                    .set_sign('+')
                                final_numerator[
                                    position_of_the_last_minus_sign[1]]\
                                    .set_force_display_sign_once(True)
                                K[i].set_sign('+')
                                K[i].set_force_display_sign_once(True)
                                position_of_the_last_minus_sign = None
                                log.debug(" [B] 2 signs set to '+' ")
                            elif position_of_the_last_minus_sign[0] == 'd':
                                final_denominator[
                                    position_of_the_last_minus_sign[1]].\
                                    set_sign('+')
                                final_denominator[
                                    position_of_the_last_minus_sign[1]].\
                                    set_force_display_sign_once(True)
                                K[i].set_sign('+')
                                K[i].set_force_display_sign_once(True)
                                position_of_the_last_minus_sign = None
                                log.debug(" [C] 2 signs set to '+' ")

            answer = Fraction((self.sign,
                               Product(final_numerator),
                               Product(final_denominator)))

            for i in range(len(answer.numerator)):
                if answer.numerator[i].force_display_sign_once:
                    log.debug("Found a plus sign forced to display in nume")

            for i in range(len(answer.denominator)):
                if answer.denominator[i].force_display_sign_once:
                    log.debug("Found a plus sign forced to display in deno")

            answer.set_status("simplification_in_progress")

            return answer

    # --------------------------------------------------------------------------
    ##
    #   @brief Replace the striked out Items by Item(1)
    def replace_striked_out(self):
        log = settings.dbg_logger.getChild(
            'Fraction.replace_striked_out')
        log.debug("Entering on: " + repr(self))

        result = Fraction(self)

        # The values of all striked out factors get replaced by "1"
        # ... numerator:
        for i in range(len(result.numerator)):
            if result.numerator.factor[i].is_out_striked:
                result.numerator.factor[i].set_value_inside(Value(1))
                result.numerator.factor[i].set_is_out_striked(False)

        # ... denominator
        for j in range(len(result.denominator)):
            if result.denominator.factor[j].is_out_striked:
                result.denominator.factor[j].set_value_inside(Value(1))
                result.denominator.factor[j].set_is_out_striked(False)

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the fraction after a simplification step
    def simplified(self):
        log = settings.dbg_logger.getChild(
            'Fraction.simplified')
        log.debug("Entering, on: " + repr(self))

        aux_fraction = None

        if self.simplification_in_progress:
            aux_fraction = Fraction(self)
        else:
            aux_fraction = Fraction(self.simplification_line())

        # determination of the sign:
        final_sign = sign_of_product([Item((aux_fraction.sign, 1, 1)),
                                      aux_fraction.numerator,
                                      aux_fraction.denominator])

        aux_fraction = aux_fraction.replace_striked_out()

        final_numerator = Product([Item(int(math.fabs(aux_fraction
                                   .numerator.evaluate())))])

        final_denominator = Product([Item(int(math.fabs(aux_fraction
                                     .denominator.evaluate())))])

        # Note that this final Fraction has a
        # status = "nothing" (default)

        if final_denominator.is_displ_as_a_single_1():
            if final_sign == '-':
                return Item((Product([Item(-1), final_numerator])).evaluate())
            else:
                if len(final_numerator) == 1:
                    return final_numerator[0]
                else:
                    return final_numerator
        else:
            return Fraction((final_sign, final_numerator, final_denominator))

    def reduced_by(self, n, ignore_1_denominator=False):
        """Divide numerator and denominator by n."""
        return Fraction((self.sign,
                         Item(self.numerator.evaluate() / n),
                         Item(self.denominator.evaluate() / n)),
                        ignore_1_denominator=ignore_1_denominator)

    def minimally_reduced(self, ignore_1_denominator=False):
        """Return the simplest reduction step possible"""
        temp = math.gcd(int(self.numerator.evaluate()),
                        int(self.denominator.evaluate()))
        if temp == 1:
            return None
        # lowest prime common divisor
        lpcd = prime_factors(temp)[0]
        return Fraction((self.sign,
                         Item(self.numerator.evaluate() / lpcd),
                         Item(self.denominator.evaluate() / lpcd)),
                        ignore_1_denominator=ignore_1_denominator)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the fraction after all simplification steps
    def completely_reduced(self):
        temp = math.gcd(int(self.numerator.evaluate()),
                        int(self.denominator.evaluate()))
        if temp == 1:
            return self
        else:
            return Fraction((self.sign,
                             Item(self.numerator.evaluate() / temp),
                             Item(self.denominator.evaluate() / temp)))

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the fraction is reducible
    # So if numerator and denominator *are numeric Products* with both
    # exponent 1 both and their GCD is strictly greater than 1.
    # If any of denominator or numerator is an Item, then it is embedded by
    # this method in a Product to allow the further simplification of the
    # Fraction
    def is_reducible(self):
        if not self.is_numeric():
            return False

        if self.numerator.evaluate() == 0:
            return True

        if not isinstance(self.numerator, Product):
            if isinstance(self.numerator, Item):
                self.set_numerator(Product(self.numerator))
            else:
                return False

        if not isinstance(self.denominator, Product):
            if isinstance(self.denominator, Item):
                self.set_denominator(Product(self.denominator))
            else:
                return False

        for i in range(len(self.numerator)):
            if not (isinstance(self.numerator.factor[i], Item)
                    and is_integer(self.numerator.factor[i].raw_value)
                    and self.numerator.factor[i].exponent == Value(1)):
                return False

        for i in range(len(self.denominator)):
            if not (isinstance(self.denominator.factor[i], Item)
                    and is_integer(self.denominator.factor[i].raw_value)
                    and self.denominator.factor[i].exponent == Value(1)):
                return False

        if math.gcd(int(self.numerator.evaluate()),
                    int(self.denominator.evaluate())) > 1:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Fraction is a decimal number
    def is_a_decimal_number(self):
        deno = self.completely_reduced().denominator.evaluate()
        while not (deno % 2):
            deno /= 2
        while not (deno % 5):
            deno /= 5
        if deno == 1:
            return True
        else:
            return False


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class CommutativeOperation
# @brief Abstract mother class of Product and Sum. Gathers common methods.
class CommutativeOperation(Operation, metaclass=ABCMeta):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @warning CommutativeOperation objects are not really usable
    #   @return An "instance" of CommutativeOperation
    def __init__(self):
        Operation.__init__(self)

        # These strings are used in the (debugging) dbg_str method.
        # The __init__ of Sum and Product will initialize them at
        # desired values (so far, [] for a Sum and <> for a Product)
        # They are not treated as the other fields because they're only
        # useful for debugging
        self.str_openmark = ""
        self.str_closemark = ""

        # Two "displaying mode" fields
        self._compact_display = True
        self._info = []

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the compact_display field of a CommutativeOperation
    def get_compact_display(self):
        return self._compact_display

    # --------------------------------------------------------------------------
    ##
    #   @brief Allow the subclasses to access this field
    def get_info(self):
        return self._info

    # --------------------------------------------------------------------------
    ##
    #   @brief If the Product is literal, returns the first factor's letter
    def get_first_letter(self):
        if self.is_literal(displ_as=True):
            return self.element[0].get_first_letter()

        else:
            raise TypeError('Cannot get the first letter '
                            'of a non literal object')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the sign of the first element of the
    #          CommutativeOperation
    def get_sign(self):
        return self.element[0].sign

    info = property(get_info, doc="info field of a CommutativeOperation")

    compact_display = property(get_compact_display,
                               doc="compact_display field of a "
                                   "CommutativeOperation")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the info field of the CommutativeOperation
    def set_info(self, arg):
        if not type(arg) == list:
            raise ValueError("arg should be a list")
        if len(arg) == 0:
            self._info = arg
        else:
            for elt in arg:
                if elt not in [True, False]:
                    raise ValueError("elt should be True|False")
            self._info = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the sign of the first element of the CommutativeOperation
    def set_sign(self, arg):
        self._element[0].set_sign(arg)

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets a value to the compact_display field
    #   @param arg Must be True or False
    def set_compact_display(self, arg):
        if not isinstance(arg, bool):
            raise TypeError('Expected a bool')
        self._compact_display = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief  Returns the value (number) of an numerically evaluable
    #           CommutativeOperation
    #   @return The result as a number
    def evaluate(self, **options):
        log = settings.dbg_logger.getChild(
            'CommutativeOperation.evaluate')
        log.debug("Entered with: " + repr(self))

        if not('stop_recursion' in options and options['stop_recursion']):
            next_step = self.calculate_next_step()

            if next_step is not None:
                log.debug("Exiting, returning evaluate() "
                          "called on: " + repr(next_step))
                return next_step.evaluate()

        answer = self.neutral.raw_value

        for elt in self.element:
            log.debug("current elt is: " + repr(elt))
            if (isinstance(elt, Item) or isinstance(elt, Value)
                or isinstance(elt, Function)):
                # we don't check if the possibly Item is numeric.
                # if it's not, an error will be raised
                if not isinstance(elt, Function):
                    val = elt.raw_value
                else:
                    val = Item((elt.sign,
                                elt.fct(elt.num_val.evaluate()),
                                1)).evaluate()
                expo = 1
                sign_val = 1

                if isinstance(elt, Item):
                    expo = elt.exponent.evaluate()
                    if elt.is_negative():
                        sign_val = -1

                if expo == 0:
                    val = 1

                answer = self.operator(answer, sign_val * (val ** expo))
                log.debug("a- current answer is: " + str(answer))

            elif isinstance(elt, CommutativeOperation):
                answer = self.operator(answer, elt.evaluate())
                log.debug("b- current answer is: " + str(answer))

            elif isinstance(elt, Quotient):
                answer = self.operator(answer, elt.evaluate())
                log.debug("c- current answer is: " + str(answer))

        external_expon = self.exponent.evaluate()

        log.debug("external_expon is: " + str(external_expon))

        return (answer ** external_expon)

    # --------------------------------------------------------------------------
    ##
    #   @brief Raw display of the CommutativeOperation (debugging method)
    #   @param options: info=True let dbg_str display more info
    #   @return A string: "<info1|info2||factor0, ..., factorn>^{exponent}"
    #                 or: "[info1|info2||term0, ..., termn]^{exponent}"
    def __repr__(self, **options):
        elements_list_string = ""
        for i in range(len(self)):
            elements_list_string += repr(self.element[i])
            if i < len(self) - 1:
                elements_list_string += ' ' + self.symbol + ' '

        info = ""
        if 'info' in options and options['info']:
            info = str(self.compact_display) + " info:"\
                + str(self.info) + ":info "

        expo = ""
        if not self.exponent.is_displ_as_a_single_1():
            expo = "^|" + repr(self.exponent) + "|"

        return self.str_openmark + info + elements_list_string \
            + self.str_closemark + expo + " "

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the number of elements of the CommutativeOperation
    def __len__(self):
        return len(self.element)

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the CommutativeOperation contains exactly the given
    #               objct
    #   It can be used to detect objects embedded in this CommutativeOperation
    #   @param objct The object to search for
    #   @return True if the CommutativeOperation contains exactly the given
    #               objct
    def contains_exactly(self, objct):
        if len(self) != 1:
            return False
        elif self.element[0] == objct:
            return True
        else:
            return self.element[0].contains_exactly(objct)

    # --------------------------------------------------------------------------
    ##
    #   @brief To check if this contains a rounded number...
    #   @return True or False
    def contains_a_rounded_number(self):
        for elt in self:
            if elt.contains_a_rounded_number():
                return True

        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief Appends a given element to the current CommutativeOperation
    #   @param elt  The element to append (assumed to be a Exponented)
    def append(self, elt):
        self._element.append(elt)
        self._info.append(False)

    # --------------------------------------------------------------------------
    ##
    #   @brief Removes a given element from the current CommutativeOperation
    #   @param elt  The element to remove (assumed to be a Exponented)
    def remove(self, elt):
        i = 0

        # Let's find the position of the term
        while (i < len(self)
               and self.element[i] != elt
               and not self.element[i].contains_exactly(elt)):
            # __
            i += 1

        # Check if we really find the researched term
        if i == len(self):
            raise ValueError('CommutativeOperation.remove(elt): elt '
                             + str(elt)
                             + ' not in ' + repr(self))

        # Then pop the right one
        self._element.pop(i)
        self._info.pop(i)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns self without the equivalent-to-a-single-neutral elements
    def throw_away_the_neutrals(self):
        log = \
            settings.dbg_logger.getChild(
                'CommutativeOperation.throw_away_the_neutrals')
        collected_positions = list()

        for i in range(len(self)):
            if self.element[i].is_displ_as_a_single_neutral(self.neutral):
                log.debug(repr(self.element[i]) + "has been detected as "
                          "'single neutral' the ref. neutral being "
                          + repr(self.neutral))
                collected_positions.append(i)

        result = None

        if isinstance(self, Product):
            result = Product(self)
        elif isinstance(self, Sum):
            result = Sum(self)

        if len(collected_positions) == len(self):
            result.reset_element()
            result.element.append(Item(self.neutral))
            result.set_info([False])

        else:
            for i in range(len(collected_positions)):
                # this - i is necessary in the case of several items
                # because the real length of the element list diminishes
                # each time an item is poped.
                result._element.pop(collected_positions[i] - i)
                result._info.pop(collected_positions[i] - i)

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single neutral element
    def is_displ_as_a_single_neutral(self, neutral_elt):
        for elt in self.element:
            if not elt.is_displ_as_a_single_neutral(neutral_elt):
                return False

        return True

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the CommutativeOperation contains only one numeric Item
    def is_displ_as_a_single_numeric_Item(self):
        if not self.is_numeric() or not len(self) == 1:
            return False
        else:
            return self.element[0].is_displ_as_a_single_numeric_Item()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single int
    def is_displ_as_a_single_int(self):
        if len(self) == 1:
            return self[0].is_displ_as_a_single_int()
        else:
            return False


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Product
# @brief Has Exponented factors & an exponent. Iterable. Two display modes.
class Product(CommutativeOperation):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg None|Product|Number|Exponented|[Numbers|Exponenteds]
    #   In the case of the list, the Products having an exponant equal to 1
    #   won't be treated so that their factors are inserted in the current
    #   Product instead of inserting a factor as a Product.
    #   If it would, then the compact and non compact display properties
    #   might be lost. (For instance, multiplying two Monomials and setting
    #   the compact display field of the resulting Product to False would
    #   result in displaying all the Monomials Items which isn't always wished)
    #   If the argument isn't of the kinds listed above, an exception will be
    #   raised.
    #   Giving None or an empty list is equivalent to giving 1.
    #   The exponent of a Product is 'outside' (like 3 in (4×5x)³)
    #   @return An instance of Product
    def __init__(self, arg, compact_display=True):
        CommutativeOperation.__init__(self)
        # The self.compact_display flag is let set to True
        # If it is set to False, the display_multiply_symbol (aka info)
        # will be used to know whether the × symbol is to be displayed
        # between two factors.
        # If it is set to True, the × symbol will never be displayed unless
        # the general writing rules of mathematical expressions force the ×
        # to be displayed (for instance between two numbers)

        # The self._info is a list whose first element doesn't match anything,
        # it will always be False, whatever. The 2d element means the
        # × symbol between 1st and 2d factor etc.
        self._symbol = '×'

        self._neutral = Item(1)

        self.str_openmark = "<"
        self.str_closemark = ">"

        self._compact_display = compact_display
        # 1st CASE: None or void list []
        if arg is None or (type(arg) == list and len(arg) == 0):
            self._element.append(Item(1))

        # 2d CASE: Product
        elif isinstance(arg, Product):
            self._compact_display = arg.compact_display
            self._exponent = arg.exponent.clone()
            for i in range(len(arg.element)):
                self._element.append(arg.element[i].clone())
            for i in range(len(arg.info)):
                self._info.append(arg.info[i])

        # 3d CASE: Number
        elif is_number(arg):
            self._element.append(Item(arg))

        # 4th CASE: Exponented
        elif isinstance(arg, Exponented):
            self._element.append(arg.clone())

        # 5th CASE: [Numbers|Exponenteds]
        elif (type(arg) == list) and len(arg) >= 1:
            for i in range(len(arg)):

                if i == 0:
                    self._info.append(False)
                else:
                    self._info.append(True)

                # If 1-exponent Products are being treated as the 1-exponent
                # Sums it leads to bugs: the Monomials would "dissolve" into
                # other Products, indeed ! And more generally, what about
                # "adding" a compact Product to a non-compact one... ?
                # So, this is definitely not to do.
                if isinstance(arg[i], Exponented):
                    self._element.append(arg[i].clone())

                elif is_number(arg[i]) or isinstance(arg[i], Value):
                    self._element.append(Item(arg[i]))

                elif arg[i] is None:
                    self._element.append(Item(1))

                else:
                    raise TypeError('Got: ' + str(type(arg[i]))
                                    + ' instead of a Exponented or a number')

        # All other unforeseen cases: an exception is raised.
        else:
            raise TypeError('Got: ' + str(type(arg))
                            + ' instead of a Product|Exponented|Number|'
                            '[Exponenteds|Numbers]')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the factors' list of the Product except the given one
    def get_factors_list_except(self, objct):
        if len(self) == 1 and self.factor[0] == objct:
            return None
        else:
            if objct in self.factor:
                aux_list = list()
                objct_was_found = False
                for i in range(len(self)):
                    if self.factor[i] != objct:
                        aux_list.append(self.factor[i])
                    else:
                        if objct_was_found:
                            aux_list.append(self.factor[i])
                        else:
                            objct_was_found = True
                return aux_list
            else:
                raise ValueError("the object: " + repr(objct)
                                 + " is nowhere to find in this Product: "
                                 + repr(self))

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the first Sum/Item factor of the Product
    #   @warning Maybe not functionnal because of the 1's...
    #   For instance, if <factor1,factor2> is a Product & [term1,term2] a Sum:
    #   <<2,3>,x> would return 2
    #   <[2,3],x>² would return (2+3)²
    #   <<2x>²,4> would return 2²
    #   @todo check the intricate case of <<[<0, 1>]>, 4>
    def get_first_factor(self):
        if len(self) == 0:
            return None
        else:
            # Either it's a one-term Sum, it has to be managed recursively
            # as if this term was embedded in a Product instead of a Sum
            if (isinstance(self.factor[0], Sum)
                and len(self.factor[0]) == 1):
                # __
                answer = Product(self.factor[0].term[0]).get_first_factor()

            # Or it's a Product, we get its first factor then recursively
            elif isinstance(self.factor[0], Product):
                answer = self.factor[0].get_first_factor()

            # Or anything else, we just get the thing
            # (Anything else being a )
            else:
                answer = self.factor[0]

            answer.set_exponent(answer.exponent * self.exponent)
            return answer

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the number of - signs (negative factors) in the Product
    def get_minus_signs_nb(self):
        answer = 0
        for factor in self.element:
            answer += factor.get_minus_signs_nb()

        return answer

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the factors' list of a given kind (numeric, literal...)
    #   For instance, for the product:
    #   2x × (-4x²) × (x + 3)³ × 5 × (x²)³ × (-1)² × (2×3)²,
    #   this method would return:
    #   - in the case of simple numeric items: [2, -4, 5, (-1)², 2², 3²]
    #   - in the case of simple literal items: [x, x², x**6]
    #   - in the "others" list: [(x+3)³]
    #   This method helps to reduce a Product.
    #   It doesn't calculate anything and doesn't manage exotic cases
    #   (imbricated Products...) which are too complex to foresee. As far as
    #   I could... (later note: but I'm not sure it doesn't manage them now,
    #   I might have done that later than this comment).
    #   It will still be convenient to reorder the factors of a Monomials
    #   Product.
    #   @param given_kind: NUMERIC | LITERALS | OTHERS
    #   @return a list containing the factors
    #   @todo The - signs of the literals should be treated as -1 in the
    #   numeric list (and shouldn't remain in the literals' list)
    def get_factors_list(self, given_kind):
        log = settings.dbg_logger.getChild(
            'Product.get_factors_list')
        resulting_list = list()
        a_factor_not_equivalent_to_1_has_been_found = False
        log.debug("Entered, looking for " + given_kind
                  + "\ncurrent Product is: " + repr(self))

        for factor in self.element:
            log.debug("current factor is: " + repr(factor))

            if (isinstance(factor, Item)
                and ((factor.is_numeric() and given_kind == NUMERIC)
                     or (factor.is_literal() and given_kind == LITERALS))):
                # __
                log.debug("current factor is an Item, "
                          "is it positive? "
                          + str(factor.is_positive()) + "; "
                          "is it negative? "
                          + str(factor.is_negative()) + "; "
                          "self.compact_display is "
                          + str(self.compact_display))
                # Here the possible external exponent has to get down
                # and a possible (-1)² product has to be created here
                if factor.is_positive()                                       \
                   and not (self.compact_display
                            and factor.is_displ_as_a_single_1()):
                    # __
                    # If the Item has got a '+' sign, no worry, it can get
                    # added to the list without forgetting to put the external
                    # exponent on it.
                    # The "1" value Items are not managed here in the case of
                    # compact displayed Products
                    # (that's useless, moreover, it would make reappear all
                    # the "1" of terms such like x, x², x³ etc.)
                    # But one "1" has to be added in the case when the given
                    # product contains only "1"s (otherwise we would return
                    # an empty list)
                    log.debug("current factor is positive")
                    item_to_be_added = Item((factor.sign,
                                             factor.raw_value,
                                             factor.exponent * self.exponent))
                    item_to_be_added.set_is_out_striked(factor.is_out_striked)
                    resulting_list.append(item_to_be_added)
                    log.debug("adding: " + repr(item_to_be_added))
                    a_factor_not_equivalent_to_1_has_been_found = True

                elif factor.is_negative():
                    log.debug("current factor is negative")
                    # If the Item has got a '-' sign, it has to be embedded
                    # in a Product (of only one factor) on which the external
                    # has to be put down. For instance, (a × (-1) × b)² should
                    # return a², b² (managed in the Items section) AND also
                    # (-1)²
                    # It has to be done only if the exponent is even.
                    item_to_be_added = factor
                    if is_even(self.exponent):
                        item_to_be_added = Product([factor])
                    item_to_be_added.set_exponent(self.exponent)
                    log.debug("adding: " + repr(item_to_be_added))
                    resulting_list.append(item_to_be_added)
                    a_factor_not_equivalent_to_1_has_been_found = True

            elif isinstance(factor, Product):
                log.debug("current factor is a Product")
                # If it's a Product, the external exponent must get down on
                # it and the function is recursively called. This includes
                # managing the factor (-1)³ in this example: (a * (-1)³ * b)²
                # It will be then managed like the Product (-1)⁶ and managed
                # in the negative Items section somewhat above.
                aux_product = Product(factor)
                aux_product.set_exponent(factor.exponent * self.exponent)
                temp_list = aux_product.get_factors_list(given_kind)

                if len(temp_list) != 0:
                    resulting_list += temp_list
                    a_factor_not_equivalent_to_1_has_been_found = True

            elif isinstance(factor, Sum):
                if len(factor) == 1:
                    # Only-one-term Sum: it is copied into an only-one-factor
                    # Product (including the exponent) and the method is
                    # called recursively on it.
                    aux_list = list()
                    aux_list.append(factor.term[0])
                    aux_product = Product(aux_list)
                    aux_product.set_exponent(factor.exponent)
                    temp_list = aux_product.get_factors_list(given_kind)
                    if len(temp_list) != 0:
                        resulting_list += temp_list
                        a_factor_not_equivalent_to_1_has_been_found = True

                elif given_kind == OTHERS:
                    # Several-terms Sums get managed only if OTHERS kind of
                    # factors are wanted
                    aux_sum = Sum(factor)
                    aux_sum.set_exponent(factor.exponent * self.exponent)
                    resulting_list.append(aux_sum)
                    a_factor_not_equivalent_to_1_has_been_found = True

            elif isinstance(factor, Quotient):
                if ((factor.is_numeric() and given_kind == NUMERIC)
                    or (factor.is_literal() and given_kind == LITERALS)):
                    # __
                    resulting_list.append(factor)
                    a_factor_not_equivalent_to_1_has_been_found = True
                else:
                    if given_kind == OTHERS:
                        resulting_list.append(factor)
                        a_factor_not_equivalent_to_1_has_been_found = True

        if (given_kind == NUMERIC
            and not a_factor_not_equivalent_to_1_has_been_found
            and len(resulting_list) == 0):
            # __
            resulting_list.append(Item(1))

        log.debug("exiting ; len(resulting_list) = "
                  + str(len(resulting_list)))

        return resulting_list

    factor = property(CommutativeOperation.get_element,
                      doc="To access the factors of the Product.")

    # --------------------------------------------------------------------------
    ##
    #   @brief
    #   @param n: number of the factor to set
    #   @param arg: the object to put as n-th factor
    def set_factor(self, n, arg):
        self.set_element(n, arg)

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        global expression_begins
        if options.get('js_repr', False):
            multiply_symbol = '*'
        else:
            multiply_symbol = MARKUP['times']
        log = settings.dbg_logger.getChild('Product.into_str')
        log.debug('Entering...')

        if ('force_expression_begins' in options
            and options['force_expression_begins']):
            # __
            expression_begins = True
            options['force_expression_begins'] = False

        # This reflects the position to indicate to the function
        # requires_brackets()
        # It will be incremented everytime something is displayed.
        position = 0
        if 'force_position' in options \
           and is_integer(options['force_position']):
            # __
            position = options['force_position']
            # let's remove this option from the options
            # since it might be re-used recursively
            temp_options = dict()
            for key in options:
                if key != 'force_position':
                    temp_options[key] = options[key]
            options = temp_options

        remember = expression_begins
        # Looks like the repr(self) in log.debug changes expression_begins
        # what we don't want
        log.debug('expression_begins = ' + str(expression_begins)
                  + ' | position set to ' + str(position)
                  + '\nCurrent Product: ' + repr(self))

        expression_begins = remember

        # All Product objects are treated here
        # (including Monomials & Developables)
        # Displaying the + sign depends on the expression_begins machine's flag
        # In a product, this flag has to be reset to True for each new factor
        # after the first one.
        if self.compact_display:
            log.debug('(0) expression_begins = ' + str(expression_begins))
            log.debug('self.compact_display is True; is_equiv_single_neutral: '
                      + str(self.element[0].is_displ_as_a_single_neutral(
                          self.neutral)))
            log.debug('(1) expression_begins = ' + str(expression_begins))

            # copy = self.clone().throw_away_the_neutrals()
            # log.debug(
            #    "Current Copy without 'ones': " + str(copy))

            # Compact display section:
            # - All unnecessary and unrequired × signs won't be displayed,
            # - All factors equal to 1 won't be displayed (which means
            #   positive items having a 0 exponent and/or whose value is 1
            #   in the case of numeric items).
            # - If the first factor equals -1, only the - sign is displayed
            # - If the product only contains ones (1), 1 is displayed at
            #   the end
            # - And -1 is displayed if the product contains only one -1 and
            #   items equal to 1
            resulting_string = ''

            # This couple is a couple of objects to display.
            # It is needed to determine wether a - sign is necessary or not
            # before dislaying a new factor (the second one in the couple)
            # If the couple contains:
            # - (None, None), then nothing has been displayed yet
            #   In this case, if any new factor "factor1" gets displayed,
            #   the couple becomes (factor1, None)
            # - (factor1, None), only factor1 has been displayed yet.
            #   In this case, if any new factor "factor2" gets displayed,
            #   the couple becomes (factor1, factor2)
            # - (factor1, factor2), then these two factors have already
            #   been displayed.
            #   In this case, if any new factor "factor3" gets displayed,
            #   the couple becomes (factor2, factor3)
            couple = (None, None)

            # This flag checks if one factor at least has already been
            # displayed. If not, then a "1" will be displayed at the end.
            flag = False

            # Here was the previous localization of the initialization of the
            # local variable position...

            # This checks if an "orphan" - sign has been displayed
            orphan_minus_sign = False

            # This flag is used to add brackets inside of "compact" Products
            # like in 9×(-2a)×4b where (-2a)×4b is a "compact" Product itself
            unclosed_bracket = 0

            # Any product must contain one factor at least.
            # It is processed here.
            # Its processing is made apart from the others because it
            # requires a special processing if it is a -1
            if self.factor[0].is_displ_as_a_single_1():
                log.debug('(2) expression_begins = ' + str(expression_begins))
                # Nothing has to be done. If the product only contains
                # ones, a "1" will be displayed at the end (because flag
                # will then remain to False)
                # expression_begins = False: that can't be made here like
                # it is in the case of -1 (the case of -1 has the help of
                # the flag orphan_minus_sign). It is made later, when the
                # finally lonely 1 is displayed. If it is not a lonely 1
                # then other factors will set expression_begins to False
                pass
            elif self.factor[0].is_displ_as_a_single_minus_1():
                log.debug('[n°0] processing a \'-1\' 1st factor: '
                          + repr(self.factor[0])
                          + ' with position forced to ' + str(position))
                log.debug('[n°0] expression_begins = '
                          + str(expression_begins))
                if position >= 1:
                    log.debug('and a bracket is */opened/*')
                    resulting_string += MARKUP['opening_bracket']
                    unclosed_bracket += 1

                # Then the - sign has to be displayed
                # and position has to be incremented (because it
                # influences the next factor displaying)
                resulting_string += MARKUP['minus']
                position += 1
                orphan_minus_sign = True
                # This expression_begins set to False is required to
                # avoid the problem Sum(Product(Item(-1)), Item(x))
                # being displayed -1x instead of -1+x
                # The next factor needs to have it set True to be displayed
                # correctly... but it doesn't matter thanks to the flag
                # orphan_minus_sign which is used later to reset expressions_
                # begins to True just in time:o)
                expression_begins = False
                log.debug('[n°0] expression_begins set to False')
            else:
                # In this case, the first factor is different
                # from 1 and from -1: it will be displayed normally.
                # To avoid putting brackets around a Sum that would be
                # alone in the Product or with other factors which all
                # are equivalent to 1, we check if it's not the case
                # Note that the test position == 0 is necessary since
                # the current Product might not be the first to be displayed:
                # the current "first" factor is maybe not the first factor
                # to be displayed
                log.debug('(3) expression_begins = ' + str(expression_begins))
                if ((Product(self.get_factors_list_except(self.factor[0]))
                     .is_displ_as_a_single_1() and position == 0)
                    or not (self.factor[0].requires_brackets(position)
                            and len(self) >= 2)
                    or self.requires_inner_brackets()):
                    # __
                    log.debug('[n°1A] processing 1st factor: '
                              + repr(self.factor[0])
                              + ' with position forced to ' + str(position)
                              + ' ; NO brackets')

                    resulting_string += self.factor[0]\
                        .into_str(force_position=position, **options)

                # This case has been added to get rid of the "Monomial's
                # patch" in Product.requires_brackets()
                else:
                    expression_begins = True
                    log.debug('[n°1B] processing 1st factor: '
                              + repr(self.factor[0])
                              + ' with position NOT forced to ' + str(position)
                              + ', needs brackets ? '
                              + str(self.factor[0].requires_brackets(position))
                              + '; a bracket is */opened/*')
                    log.debug('(4) expression_begins = '
                              + str(expression_begins))

                    resulting_string += MARKUP['opening_bracket'] \
                        + self.factor[0].into_str(**options)

                    unclosed_bracket += 1

                    if len(self.factor[0]) >= 2:
                        log.debug('and */closed/*')
                        resulting_string += MARKUP['closing_bracket']
                        unclosed_bracket -= 1

                # Flag is set to True because something has been
                # displayed
                # & this factor gets into the "couple" as first member
                flag = True
                position += 1
                couple = (self.factor[0], None)
                log.debug('Finished processing the first factor; '
                          'couple is (' + repr(self.factor[0])
                          + ', None); flag is ' + str(flag)
                          + '; position is ' + str(position))
                log.debug('(5) expression_begins = ' + str(expression_begins))

            # If there are other factors:
            log.debug('(6) expression_begins = ' + str(expression_begins))
            if len(self) >= 2:
                for i in range(len(self) - 1):
                    log.debug('Processing factor #{n}, '
                              'expression_begins = {eb}'
                              .format(n=str(i + 1), eb=str(expression_begins)))
                    if self.factor[i + 1].is_displ_as_a_single_1():
                        # inside the product, the 1 factors just don't
                        # matter
                        pass
                    else:
                        if couple == (None, None):
                            # That means it's the first factor that will be
                            # displayed (apart from a possibly only - sign)
                            log.debug("more than one factor to process; "
                                      "current couple is ("
                                      + str(couple[0]) + ", "
                                      + str(couple[1]) + "); "
                                      "flag is " + str(flag)
                                      + " position is " + str(position))
                            couple = (self.factor[i + 1], None)
                            if (self.factor[i + 1].requires_brackets(position)
                                and not
                                Product(self.get_factors_list_except(
                                        self.factor[i + 1]))
                                .is_displ_as_a_single_1()):
                                # __
                                expression_begins = True
                                log.debug("[n°2A] processing factor: "
                                          + repr(self.factor[i + 1])
                                          + "with position NOT forced to "
                                          + str(position) + " ; "
                                          "a bracket is */opened/*")
                                # Not sure it has an incidence, but would the
                                # msg here above change expression_begins, it
                                # should be set back to True before calling
                                # the next .into_str() right below
                                # expression_begins = True

                                resulting_string += MARKUP['opening_bracket'] \
                                    + self.factor[i + 1].into_str(**options)

                                unclosed_bracket += 1

                                if len(self.factor[i + 1]) >= 2:
                                    log.debug("and */closed/*")
                                    resulting_string += \
                                        MARKUP['closing_bracket']
                                    unclosed_bracket -= 1

                            else:
                                # If an orphan - has been displayed, the
                                # next item shouldn't display its
                                # + sign if it is positive.
                                if orphan_minus_sign:
                                    expression_begins = True
                                    log.debug("[n°2B] (orphan - sign) "
                                              "processing factor: "
                                              + repr(self.factor[i + 1])
                                              + " with position forced to "
                                              + str(position)
                                              + "; NO brackets")

                                    resulting_string += self.factor[i + 1]\
                                        .into_str(force_position=position,
                                                  **options)
                                else:
                                    log.debug('(7) expression_begins = '
                                              + str(expression_begins))
                                    remember = expression_begins
                                    log.debug("[n°2C] (NO orphan - sign) "
                                              "processing factor: "
                                              + repr(self.factor[i + 1])
                                              + " with position forced to "
                                              + str(position)
                                              + "; NO brackets")

                                    expression_begins = remember

                                    options['force_expression_begins'] = \
                                        expression_begins

                                    resulting_string += self.factor[i + 1]\
                                        .into_str(force_position=position,
                                                  **options)

                            # Something has been displayed, so...
                            flag = True
                            position += 1

                        else:
                            if couple[1] is None:
                                # It's the second factor to be displayed.
                                # Let's update the current couple:
                                current_factor_1 = couple[0]
                                current_factor_2 = self.factor[i + 1]
                            else:
                                # At least two factors have been displayed
                                # Let's update the current couple:
                                current_factor_1 = couple[1]
                                current_factor_2 = self.factor[i + 1]

                            couple = (current_factor_1, current_factor_2)

                            # If necessary, the × sign will be displayed.
                            # The value of position - 1 will be used
                            # because couple[0]'s position matters
                            # and position matches couple[1]'s position
                            log.debug("Checking if a × should be required "
                                      "between " + repr(couple[0])
                                      + "    and    " + repr(couple[1]))
                            if (couple[0]
                                .multiply_symbol_is_required(couple[1],
                                                             position - 1)):
                                # __
                                log.debug("... yes")
                                if unclosed_bracket >= 1:
                                    if (couple[0]
                                        .multiply_symbol_is_required(couple[1],
                                                                     0)):
                                        # __
                                        log.debug("the bracket gets "
                                                  "*/closed/*")
                                        resulting_string += \
                                            MARKUP['closing_bracket']
                                        unclosed_bracket -= 1

                                        resulting_string += multiply_symbol
                                    else:
                                        pass
                                else:
                                    resulting_string += multiply_symbol

                            else:
                                log.debug("... no")

                            # Because at least one factor has already been
                            # displayed, the expression_begins flag has to
                            # be reset (wether the next factor requires
                            # brackets or not).
                            expression_begins = True

                            if couple[1].requires_brackets(position):
                                # It is useless to test if the other factors
                                # are all equivalent to 1 because since we're
                                # here, there must have been one factor that'd
                                # not equivalent to 1
                                # and not Product(self.get_factors_list_except(
                                #     couple[1])
                                #   ).is_displ_as_a_single_1():
                                log.debug("[n°3A] processing factor: "
                                          + repr(couple[1])
                                          + " with position NOT forced to "
                                          + str(position)
                                          + " ; a bracket is */opened/*")

                                resulting_string += MARKUP['opening_bracket'] \
                                    + couple[1].into_str(**options)

                                unclosed_bracket += 1

                                if len(self.factor[i + 1]) >= 2:
                                    log.debug("and */closed/*")
                                    resulting_string += \
                                        MARKUP['closing_bracket']
                                    unclosed_bracket -= 1

                            else:
                                log.debug("[n°3B] processing factor: "
                                          + repr(couple[1])
                                          + "with position forced to "
                                          + str(position) + "; NO brackets")

                                resulting_string += couple[1]\
                                    .into_str(force_position=position,
                                              **options)

                            position += 1
                            flag = True

            # All factors have been processed so far.
            # If flag is still False, nothing has been displayed (excepted
            # maybe an orphan -) and in this case, a "1" has to be
            # displayed.
            if not flag:
                # If the product only contained plus ones, no sign has been
                # displayed yet
                if not expression_begins                                      \
                   and self.factor[0].is_displ_as_a_single_1():
                    # __
                    resulting_string += MARKUP['plus'] + MARKUP['one']
                    # expression_begins = False (useless !)
                else:
                    if options.get('js_repr', False):
                        resulting_string += '1'
                    else:
                        resulting_string += MARKUP['one']
                        # If expression begins is not reset to False here,
                        # it is then possible to display something and still
                        # have it True !
                    expression_begins = False

            # Before leaving, maybe close a possibly left unclosed bracket
            if unclosed_bracket >= 1:
                for i in range(unclosed_bracket):
                    log.debug("[end of product]the bracket is */closed/*")
                    resulting_string += MARKUP['closing_bracket']

            # Displaying the product's exponent does not depends on the
            # compact or not compact displaying so this portion of code has
            # been written once for the two cases, somewhat farther, just
            # before the final return resulting_string.

            # end of the compact displaying section.

        # begining of the non compact displaying section
        else:
            # Non compact displaying:
            # All factors will be displayed,
            # All × signs will be displayed except the ones that are
            # especially specified not to be displayed in the
            # display_multiply_symbol list of the product
            # (unless they're required by conventional rules, like between
            # two numbers, for example)
            resulting_string = ""

            # First factor is displayed:
            if (self.factor[0].requires_brackets(position)
               and not len(self) == 1):
                # to avoid displaying a single Sum
                # with brackets around it
                # __
                expression_begins = True
                log.debug("[n°4A]×: processing 1st factor: "
                          + repr(self.factor[0]) + " with position "
                          "NOT forced to " + str(position)
                          + "; WITH brackets")
                f = self.factor[0].into_str(**options)
                if not (f.startswith('(') and f.endswith(')')):
                    resulting_string += MARKUP['opening_bracket']    \
                        + f + MARKUP['closing_bracket']
                else:
                    resulting_string += f
            else:
                log.debug("[n°4B]×: processing 1st factor: "
                          + repr(self.factor[0]) + " with position "
                          "forced to " + str(position) + "; NO brackets")
                resulting_string += self.factor[0]\
                    .into_str(force_position=position, **options)

            #
            position += 1

            # If there are other factors, the × symbols are displayed
            # as well as the next factors
            if len(self) >= 2:
                for i in range(len(self) - 1):
                    # /!\ The i-th is the last displayed, the (i+1)th is
                    # the current one
                    if (self.factor[i]
                        .multiply_symbol_is_required(self.factor[i + 1], i)
                        or self.info[i + 1]):
                        # __
                        resulting_string += multiply_symbol
                    else:
                        pass

                    expression_begins = True

                    if self.factor[i + 1].requires_brackets(i + 1):
                        # here it is not necessary to check if the brackets
                        # might be useless because in non compact display,
                        # if there are several factors they all will be
                        # displayed
                        log.debug("[n°5A]×: processing factor: "
                                  + repr(self.factor[i + 1])
                                  + "with position NOT forced to "
                                  + str(position) + "; WITH brackets")

                        resulting_string += MARKUP['opening_bracket'] \
                            + self.factor[i + 1].into_str(**options)\
                            + MARKUP['closing_bracket']
                    else:
                        log.debug("[n°5B]×: processing factor: "
                                  + repr(self.factor[i + 1])
                                  + " with position forced to " + str(position)
                                  + "; NO brackets")
                        resulting_string += self.factor[i + 1]\
                            .into_str(force_position=position, **options)

                    position += 1

        # Display of the possible product's exponent
        # and management of inner brackets (could be necessary because
        # of the exponent)
        if self.requires_inner_brackets():
            log.debug("[n°6] - wrapped in (inner) brackets")

            resulting_string = MARKUP['opening_bracket']\
                + resulting_string\
                + MARKUP['closing_bracket']

        if self.exponent_must_be_displayed():
            expression_begins = True
            exponent_string = self.exponent.into_str(**options)
            log.debug("[n°7] - processing the exponent")

            resulting_string += MARKUP['opening_exponent']\
                + exponent_string\
                + MARKUP['closing_exponent']
            expression_begins = False

        log.debug('returning: ' + str(resulting_string))
        return resulting_string

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the next calculated step of a numeric Product
    #   @todo This method is only very partially implemented (see source code)
    #   @todo The way the exponents are handled is still to be decided
    #   @todo the inner '-' signs (±(-2)) are not handled by this method so far
    def calculate_next_step(self, **options):
        log = settings.dbg_logger.getChild('Product.calculate_next_step')
        log.debug('Entering')
        if not self.is_numeric() or isinstance(self, Monomial):
            return self.expand_and_reduce_next_step(**options)

        # general idea: check if the exponent is to calculate_next_step itself
        # if yes, replace it by self.exponent.calculate_next_step() in the
        # newly built object
        # The above mentionned idea is yet to do!!!

        # then check if any of the factors is to be calculated_next_step itself
        # as well. if yes, rebuild the Product replacing any of these factors
        # by factor[i].calculate_next_step()  (maybe except Fractions which
        # can be simplified at a later step, which would be shorter and
        # more efficient...)
        # The step above is implemented, but the rest not yet
        # BUT don't forget to put the exponent on the
        # numes & denos to make the next steps easier (for instance, at this
        # step, (4×(3/4)²)³ should become (4×{9/16})³ (or maybe distribute
        # the Product's exponent on the factors ??)
        # if any of the preceding calculations has been done, then return a
        # newly rebuilt Product
        result = self.clone()
        new_elt_found = False
        unpacked = False
        for i, elt in enumerate(self._element):
            next_step = None
            if not isinstance(elt, Fraction):
                next_step = elt.calculate_next_step(**options)
            if next_step is not None:
                result[i] = next_step
                new_elt_found = True
            elif isinstance(elt, CommutativeOperation) and len(elt) == 1:
                result[i] = elt[0]
                unpacked = True
            else:
                result[i] = elt
        if new_elt_found:
            if len(result) == 2:
                if (result._element[0].is_displ_as_a_single_1()
                    and result._element[1]
                    .is_displ_as_a_single_numeric_Item()):
                    return Item(result._element[1].evaluate())
                elif (result._element[0].is_displ_as_a_single_minus_1()
                      and result._element[1]
                      .is_displ_as_a_single_numeric_Item()):
                    return Item(-result._element[1].evaluate())
                else:
                    return result
            return result
        elif unpacked:
            return result.calculate_next_step(**options)

        # case of Products having several factors but None of them neither
        # its exponent is to be calculated
        # that can be: 2×3 | (2×3)² | 2×{3/4} | {5/2}×{4/15} etc.
        # but shouldn't be 7³×5 because 7³ would have already been replaced
        # by its value (343)
        # what has to be done is effectively calculate the Product
        # of its factors so that there's only one remaining:

        # CASE
        # Several factors (not to be calculated anymore)
        if len(self) >= 2:
            # Possibly cases: only Items | Items & Fractions | only Fractions
            # Plus, the 0-degree-Monomials are converted into Items
            nb_items = 0
            nb_minus_1 = 0
            nb_fractions = 0

            # Let's count how many items, fractions etc. there are here
            for i in range(len(self)):
                # Is this content factorizable ?
                if isinstance(self.factor[i], Item):
                    if not (self.factor[i].is_displ_as_a_single_1()
                            and self.compact_display
                            or self.factor[i].is_displ_as_a_single_minus_1()):
                        # __
                        nb_items += 1
                    else:
                        if self.factor[i].is_displ_as_a_single_minus_1():
                            nb_minus_1 += 1

                if isinstance(self.factor[i], Monomial) \
                   and self.factor[i].is_numeric() \
                   and isinstance(self.factor[i][0], Item):
                    # __
                    if not (self.factor[i].is_displ_as_a_single_1()
                            and self.compact_display
                            or self.factor[i].is_displ_as_a_single_minus_1()):
                        # __
                        nb_items += 1
                        self.factor[i] = Item(self.factor[i][0])
                    else:
                        if self.factor[i].is_displ_as_a_single_minus_1():
                            self.factor[i] = Item(-1)
                            nb_minus_1 += 1

                if isinstance(self.factor[i], Fraction):
                    if not (self.factor[i].is_displ_as_a_single_1()
                            or self.factor[i].is_displ_as_a_single_minus_1()):
                        # __
                        nb_fractions += 1
                    else:
                        if self.factor[i].is_displ_as_a_single_minus_1():
                            nb_minus_1 += 1

            # Now let's check if...

            # 1st
            # There are only Items:
            if nb_fractions == 0 and nb_items >= 1:
                log.debug('Evaluating everything')
                return Item(self.evaluate(stop_recursion=True))
                # NOTE: this Item used to be "packed" in Product([])
                # NOTE: if something weird happens this might be the cause?
                # NOTE: ref. tests on Products test_product_auto_calculation()

            # 2d
            # There is at least one Fraction & one Item (not equivalent to a
            # single ±1)
            # THIS IS PARTIALLY IMPLEMENTED: negative Fractions and
            # exponented Fractions are not being handled at all ; the case of
            # equivalent-to-±1 Items is not being handled neither
            elif nb_fractions >= 1 and nb_items >= 1:
                nume_list = []
                deno_list = []

                for i in range(len(self)):
                    if isinstance(self[i], Item):
                        nume_list += [self[i]]
                    elif isinstance(self[i], Fraction):
                        nume_list += [self[i].numerator]
                        deno_list += [self[i].denominator]

                return Fraction((Product(nume_list), Product(deno_list)))

            # 3d
            # There are at least two Fractions (& maybe Items that are
            # equivalent to a single ±1)
            elif nb_fractions >= 2 and nb_items == 0:
                resulting_sign_list = []  # useless initializations
                resulting_nume_list = []
                resulting_deno_list = []
                possibly_items_list = []

                for i in range(len(self)):
                    if (isinstance(self.factor[i], Fraction)
                        and not (self.factor[i].is_displ_as_a_single_1()
                                 or
                                 self.factor[i]
                                 .is_displ_as_a_single_minus_1())):
                        # __
                        # don't forget possibly exponents here !
                        # (not implemented yet...)
                        # THEY SHOULD BE TREATED EITHER EARLIER (1st CASE)
                        # OR LATER...
                        resulting_sign_list.append(self.factor[i])
                        for j in range(len(self.factor[i].numerator.factor)):
                            item_to_add = Item(self.factor[i]
                                               .numerator.factor[j])
                            item_to_add.set_sign('+')
                            resulting_nume_list.append(item_to_add)

                        # resulting_nume_list +=
                        # self.factor[i].numerator.factor
                        for j in range(len(self.factor[i].denominator.factor)):
                            item_to_add = Item(self.factor[i]
                                               .denominator.factor[j])
                            item_to_add.set_sign('+')
                            resulting_deno_list.append(item_to_add)
                        # resulting_deno_list += \
                        #                     self.factor[i].denominator.factor

                    else:  # there won't be checked if there are Items here !
                        possibly_items_list.append(self.factor[i])

                resulting_sign = sign_of_product(resulting_sign_list)
                resulting_nume = Product(resulting_nume_list)
                resulting_nume.set_compact_display(False)
                resulting_deno = Product(resulting_deno_list)
                resulting_deno.set_compact_display(False)

                resulting_fraction = Fraction((resulting_sign,
                                               resulting_nume,
                                               resulting_deno))

                if len(possibly_items_list) == 0:
                    return resulting_fraction
                else:
                    return Product(possibly_items_list + [resulting_fraction])

            # 4th
            # There is one Fraction (and two subcases: with an Item equivalent
            # to a single -1 OR without such an Item)
            # Note that the cases "with Item(s) equivalent to a single 1" and
            # "with several Items equivalent to a single -1" should have been
            # handled before (2d case of this list)
            elif nb_fractions == 1 and nb_minus_1 == 1:
                # Let's get this fraction...
                the_fraction = None
                for i in range(len(self)):
                    if isinstance(self.factor[i], Fraction):
                        the_fraction = Fraction(self.factor[i])

                if the_fraction.calculate_next_step(**options) is None:
                    return None

                else:
                    return Product([Item(-1),
                                    the_fraction
                                    .calculate_next_step(**options)])

            # 5th
            # There is one Fraction (and remaining ones...)
            # (should never happen)
            elif nb_fractions == 1 and nb_minus_1 == 0 and nb_items == 0:
                # Let's get this fraction...
                the_fraction = None
                for i in range(len(self)):
                    if isinstance(self.factor[i], Fraction):
                        the_fraction = Fraction(self.factor[i])

                return the_fraction.calculate_next_step(**options)

            # 6th
            # There is nothing ?? (could that happen ?)
            # (or if there's only equivalent to ±1 objects... ?)

        # in the case of Products having only one factor (that does not have
        # to be calculated: which implies the factor's exponent is 1)
        # put the product's exponent on the factor[0]'s exponent and
        # return factor[0].calculate_next_step()
        # so that in the case of a Product where factor[0] = Item(3)
        # and exponent = 4, it will return Item(81) ;
        # and in the case of a Product where factor[0] = Item(5)
        # and exponent = 1, it will return None
        # (in this case the result is simply recursively delegated to Item
        # or Fraction etc.)

        # CASE
        # Only one remaining factor
        elif len(self) == 1:
            if isinstance(self.factor[0], Item):
                new_item = Item(self.factor[0])
                new_item.set_exponent(self.exponent * new_item.exponent)
                if is_even(new_item.exponent):
                    new_item.set_sign('+')
                return new_item.calculate_next_step(**options)

            elif isinstance(self.factor[0], Fraction):
                new_fraction = Fraction(self.factor[0])
                new_fraction.set_exponent(self.exponent
                                          * new_fraction.exponent)
                if is_even(new_fraction.exponent):
                    new_fraction.set_sign('+')
                return new_fraction.calculate_next_step(**options)

            elif isinstance(self.factor[0], Sum):
                new_sum = self.factor[0].calculate_next_step(**options)
                if new_sum is not None:
                    return Product([new_sum])
                else:
                    return None

            # add here the cases of a Sum, of a Product (do that recursively
            # although... well there shouldn't be a Product still there nor
            # a Sum) + cases of Quotient|Fraction

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the next step of reduction of the Product
    #   It won't check if it is expandable. Either it IS and the object is not
    #   just a Product but an Expandable or it isn't.
    #   @return Exponented
    def expand_and_reduce_next_step(self, **options):
        log = settings.dbg_logger.getChild(
            'Product.expand_and_reduce_next_step')
        log.debug("Entered on: " + repr(self))

        if type(self) == BinomialIdentity:
            return self.expand()

        if self.is_numeric() and not isinstance(self, Monomial):
            log.debug("Exiting and calling calculate_next_step on self")
            return self.calculate_next_step(**options)

        if isinstance(self, Monomial):
            log.debug("Exiting and returning None")
            return None

        copy = Product(self)

        a_factor_at_least_has_been_modified = False

        # check if any of the factors needs to be reduced
        for i in range(len(copy)):
            test = copy.factor[i].expand_and_reduce_next_step(**options)
            if test is not None:
                if isinstance(test, CommutativeOperation) and len(test) == 1:
                    # in order to depack useless 1-element
                    # CommutativeOperations...
                    copy.set_element(i, test[0])
                else:
                    copy.set_element(i, test)
                a_factor_at_least_has_been_modified = True

        if a_factor_at_least_has_been_modified:
            # we should now return the copy ; but to avoid special
            # problematic cases, let's check and possibly modify something
            # first (the case of copy being like <{-1}, <{9}, {x^2}>> would
            # produce a new step, later, transformed in <{-9}, {x^2}> what
            # will be displayed though the user won't see any difference in
            # compact display mode)
            if len(copy) >= 2 \
               and copy.factor[0].is_displ_as_a_single_minus_1():
                # __
                if isinstance(copy.factor[1], Product) \
                   and copy.factor[1].exponent.is_displ_as_a_single_1() \
                   and copy.factor[1].get_first_factor().is_positive():
                    # __
                    new_copy = Product(copy)
                    new_copy.reset_element()
                    new_first_factor = Product([Item(-1),
                                                copy.factor[1].
                                                get_first_factor()])
                    new_first_factor = new_first_factor.reduce_()
                    new_copy.element.append(new_first_factor)
                    for i in range(len(copy.factor[1]) - 1):
                        new_copy.element.append(copy.factor[1].factor[i + 1])
                    for i in range(len(copy.factor) - 2):
                        new_copy.element.append(copy.factor[i + 2])
                    copy = new_copy
            return copy

        # no factor of the Product needs to be reduced
        else:
            log.debug("No factor has been modified")
            if self.is_reducible():
                # self.set_compact_display(True)
                log.debug("self is reducible, returning self.reduce_")
                return self.reduce_()

            # this next test let Products like 2×1 (which are not considered
            # as reducible) be reduced at the end of the calculation
            # elif self.is_numeric() and len(self) >= 2 \
            #     and not self.compact_display:
            # __
            #   return self.throw_away_the_neutrals()
            else:
                # self.set_compact_display(True)
                log.debug("self is not reducible, returning None")
                return None

    # --------------------------------------------------------------------------
    ##
    #   @brief Compares two Products
    #   Returns 0 if all factors are the same in the same order and if the
    #   exponents are also the same
    #   /!\ a × b will be different from b × a
    #   It's not a mathematical comparison, but a "displayable"'s one.
    #   @return True if all factors are the same in the same order & the
    #           exponent
    def __eq__(self, objct):
        if not isinstance(objct, Product):
            return False

        if len(self) != len(objct):
            return False

        for i in range(len(self)):
            if self.factor[i] != objct.factor[i]:
                return False

        if self.exponent != objct.exponent:
            return False

        return True

    # --------------------------------------------------------------------------
    ##
    #   @brief Makes Products hashable (so, usable as dictionnary keys)
    def __hash__(self):
        return hash(self.symbol + str(self.sign)
                    + ''.join([repr(elt) for elt in self.element])
                    + repr(self.exponent))

    # --------------------------------------------------------------------------
    ##
    #   @brief Defines the performed CommutativeOperation as a Product
    def operator(self, arg1, arg2):
        return arg1 * arg2

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the usual writing rules require a × between two factors
    #   @param objct The other one
    #   @param position The position (integer) of self in the Product
    #   @todo   check Why in source code
    #   @return True if the writing rules require × between self & obj
    def multiply_symbol_is_required(self, objct, position):
        next_to_last = len(self) - 1
        # 1st CASE: Product × Item|Function
        if isinstance(objct, Item):
            return self.factor[next_to_last]\
                .multiply_symbol_is_required(objct, position)

        # 2d CASE: Product × Product
        if isinstance(objct, Product):
            return self.factor[next_to_last]\
                .multiply_symbol_is_required(objct.factor[0], position)

        # 3d CASE: Product × Sum
        if isinstance(objct, Sum):
            if len(objct) == 1:
                return self.multiply_symbol_is_required(objct.term[0],
                                                        position)
            else:
                # Why factor[0] and not factor[next_to_last] ?
                return self.factor[0].multiply_symbol_is_required(objct,
                                                                  position)

        # 4th CASE: Product × Quotient
        if isinstance(objct, Quotient):
            return True

    # --------------------------------------------------------------------------
    ##
    #   @brief True if (one)self requires brackets inside of a Product.
    #   For instance, a Sum with several terms or a negative Item would.
    #   @param position The position of the object in the Product
    #   @return True if the object requires brackets in a Product
    def requires_brackets(self, position):
        log = settings.dbg_logger.getChild('Product.requires_brackets')
        log.debug('Entering on: ' + repr(self))
        # If the exponent is equal or equivalent to 1
        if self.exponent.is_displ_as_a_single_1():
            # Either there's only one displayable factor and then
            # putting it in brackets depends on what it is...
            self_without_ones = self.throw_away_the_neutrals()

            if len(self_without_ones) == 1:
                log.debug('result depends on first non-neutral factor')
                return self_without_ones.factor[0].requires_brackets(position)
            # Or there are several factors and then it doesn't require
            # brackets: the exact positions of any brackets inside of a
            # Product are determined in into_str() ; for instance,
            # if you want to display 9×(-2x)×4x, where (-2x)×4x is a compact
            # Product, you need to put brackets INSIDE it (only wrapping to
            # factors, not the whole of it). No, not outside.
            else:
                log.debug('returning False')
                return False

        # If the exponent is different from one, then the brackets are
        # always useless. Take care that here we manage the "external"
        # brackets, not the inner ones. Here is told that (ab)² doesn't
        # require brackets i.e. shouldn't be displayed like that:
        # ((ab)²).
        # The inner brackets (the one around ab and meaning the squared
        # influences the entire ab product) are managed in
        # requires_inner_brackets()
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the argument requires inner brackets
    #   The reason for requiring them is having an exponent different
    #   from 1 and several terms or factors (in the case of Products & Sums)
    #   @return True if the object requires inner brackets
    def requires_inner_brackets(self):
        log = settings.dbg_logger.getChild(
            'Product.requires_inner_brackets')
        log.debug("Entering")

        if self.exponent_must_be_displayed():
            log.debug("the exponent should be displayed")

            compacted_self = Product(self)
            compacted_self = compacted_self.throw_away_the_neutrals()

            if len(compacted_self) == 1:
                log.debug("len(compacted_self) is 1")
                if (compacted_self.get_sign() == '+'
                    and
                    not compacted_self.factor[0].exponent_must_be_displayed()
                    and
                    not (compacted_self.exponent_must_be_displayed()
                         and len(compacted_self.factor[0]) >= 2)):
                    # __
                    return False
                else:
                    return True

            # this case is when there are several factors (at least two
            # factors not equivalent to a single 1)
            else:
                return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Product once put in order
    def order(self):
        num_factors = self.get_factors_list(NUMERIC)

        literal_factors = self.get_factors_list(LITERALS)
        literal_factors = sorted(literal_factors,
                                 key=lambda item: item.get_first_letter())

        other_factors = self.get_factors_list(OTHERS)

        return Product(num_factors + literal_factors + other_factors)

    # --------------------------------------------------------------------------
    ##
    #   @brief Return a reduced Product (if possible)
    #   For instance, giving this Product:
    #   2x × (-4x²) × (x + 3)³ × 5 × (x²)³ × (-1)² × (2×3)²,
    #   reduce_() would return:
    #   -1440 * x⁹ * (x + 3)³
    def reduce_(self):
        # Get each kind of factors possible (numeric, literals, others like
        # Sums of more than one term)
        log = settings.dbg_logger.getChild('Product.reduce')

        log.debug("Entered on:" + repr(self))

        # So, numeric factors:
        numeric_part = Product(self.get_factors_list(NUMERIC)).evaluate()

        log.debug("numeric part found is: " + str(numeric_part))

        # Literal factors:
        raw_literals_list = self.get_factors_list(LITERALS)
        literals_list = reduce_literal_items_product(raw_literals_list)

        # Determine the sign
        final_sign = sign_of_product([numeric_part] + raw_literals_list)

        if numeric_part >= 0:
            numeric_item = Item((final_sign, numeric_part, 1))
        else:
            numeric_item = Item((final_sign, -1 * numeric_part, 1))

        # Other factors
        others_list = self.get_factors_list(OTHERS)

        # Reassemble the different parts and return it
        if numeric_item.is_displ_as_a_single_0():
            return Product([Item(0)])
        else:
            return Product([numeric_item] + literals_list + others_list)

    # --------------------------------------------------------------------------
    ##
    #   @brief True if any of the factors is null
    def is_null(self):
        for elt in self.element:
            if elt.is_null():
                return True

        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Product contains only single 1s. For instance, 1×1×1
    def is_displ_as_a_single_1(self):

        # Why is there this difference between Sums & Products ??
        if not self.exponent.is_displ_as_a_single_1():
            return False

        if len(self) == 1:
            return self.factor[0].is_displ_as_a_single_1()

        return self.is_displ_as_a_single_neutral(Item(1))

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Product can be displayed as a single -1
    # For instance, the Product 1×1×(-1)×1
    def is_displ_as_a_single_minus_1(self):
        if not self.exponent.is_displ_as_a_single_1():
            return False

        a_factor_different_from_1_and_minus1_has_been_found = False
        equivalent_to_minus1_nb_factors = 0

        for factor in self.element:
            if factor.is_displ_as_a_single_minus_1():
                equivalent_to_minus1_nb_factors += 1
            elif not factor.is_displ_as_a_single_1():
                a_factor_different_from_1_and_minus1_has_been_found = True

        if a_factor_different_from_1_and_minus1_has_been_found:
            return False
        elif equivalent_to_minus1_nb_factors == 1:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be DISPLAYED as a single 0
    # For instance, the Product 0×0×0×0 (but NOT 0×1)
    def is_displ_as_a_single_0(self):
        answer = True

        for factor in self.element:
            answer = answer and factor.is_displ_as_a_single_0()

        return answer

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Product is reducible
    #   This is based on the result of the get_factors_list method
    #   @return True|False
    #   @todo check the comment in the code
    #   Fix the problem bound to the get_factors list not giving - signs
    #   of literals as -1 in the list of numerics.
    def is_reducible(self):
        log = settings.dbg_logger.getChild('Product.is_reducible')
        if self.is_displ_as_a_single_0() \
           or self.is_displ_as_a_single_1() \
           or self.is_displ_as_a_single_minus_1():
            # __
            log.debug("returning False - A")

            return False

        # That's a fix about the exponent of the Product itself which won't
        # get counted when creating the numerics list below... only the
        # exponents of the factors themselves will be reported in this list.
        # Note: don't change the get_factors_list() before thinking about
        # why it doesn't return the exponent of the Product × the one of
        # each factor: there may be a good reason for that.
        if not self.exponent.is_displ_as_a_single_1():
            log.debug("returning True - B")
            return True

        # Check the numeric factors: if there are several, then, the Product
        # is reducible.
        # First of all, throwing away the ones will make the
        # job easier in the case of compact displayed Product
        if self.compact_display:
            log.debug("Throw away the neutrals")
            test_product = self.throw_away_the_neutrals()
        else:
            log.debug("Work on a copy of self")
            test_product = Product(self)

        # Note: maybe manage the non-compact-display Products another way ?
        # Does it make sense at all... ?
        # YES IT DOES !!! (otherwise, the 2×1 Product and 1×7x Product are
        # found as not reducible and are displayed so even after "reduction"

        numerics = test_product.get_factors_list(NUMERIC)

        log.debug("len(numerics) == " + str(len(numerics)))

        # If there are two numeric factors left, then the Product is reducible
        # (they are both different from one if Product is compact_displayable):
        if len(numerics) >= 2:
            log.debug("returning True - C")
            return True

        # If there is only one numeric factor left, it can be either
        # - a one, which means either it's the only factor of the Product
        #   (and that the Product is therefore not reducible)
        #   or that there was no other numeric factor & that it has been
        #   added to the list by get_factors_list() so we can't say
        #   anything in this case so far, so just don't !
        # if len(numerics) == 1 and numerics[0].is_equivalent_to_a_single_1():
        #  return False

        # - or another number. If its exponent is different from 1, then
        #   it can be reduced:
        if (len(numerics) == 1
            and (not numerics[0].exponent.is_displ_as_a_single_1()
                 or numerics[0].is_displ_as_a_single_0())):
            # __
            log.debug("returning True - D")
            return True

        # finally if this factor is the only one of the Product, then
        # it is not reducible
        elif len(numerics) == 1 and len(test_product) == 1:
            log.debug("returning False - E")

            return False

        # If the remaining number is not a one and has an exponent equivalent
        # to one, and is not the only factor of the Product, then the result
        # depends on the literals. If there's no remaining number, then it
        # depends on the literals as well.

        # Let's check the literals...
        literals = self.get_factors_list(LITERALS)
        aux_lexicon = dict()

        for element in literals:
            put_term_in_lexicon(element, Item(1), aux_lexicon)

        # If the same literal has been found several times, then the Product
        # is reducible (Caution, x and x² are of course not the same literals)
        for key in aux_lexicon:
            if len(aux_lexicon[key]) >= 2:
                log.debug("returning True - F")
                return True

        # Now we almost know that the literals are reduced. In fact, the
        # get_factors_list() method doesn't return the minus 1 if they're
        # "stuck" in the sign of a literal. For instance, the factors' list of
        # a×(-b) would be [Item(1)] only. The - sign before the b will be
        # managed in the literal factors' list. So. Let's check if any - sign
        # remains there before asserting the literals are reduced.
        for i in range(len(literals)):
            # this next test is to avoid the cases of a literal in first
            # position having a '-' sign (doesn't need to be reduced then)
            # e.g. -ab ; but if the first factor is numeric then we know that
            # the first literal doesn't come first (so if it has a '-' sign,
            # then the Product has to be reduced)
            if test_product.factor[0].is_numeric() \
               or (test_product.factor[0].is_literal() and i != 0):
                # __
                if literals[i].sign == '-':
                    # __
                    log.debug("returning True - G")
                    return True

        # Now we know that the literals are reduced.

        # Let's finally check if the order is right, i.e. that the possibly
        # numeric comes first
        # It means that neither ab×3 nor a×3b are accepted as reduced !

        # First, if there were no numeric factors (and the literals reduced),
        # as we don't have a rule to reduce the OTHERS kinds of factors,
        # we can consider that the Product can't be reduced.
        if len(numerics) == 0:
            log.debug("returning False - H")
            return False
        # Second, if there is one number left, let's check if it appears
        # first in the Product
        elif len(numerics) == 1:
            if test_product.get_first_factor().is_numeric():
                log.debug("returning False - I")
                return False

            elif (numerics[0].is_displ_as_a_single_1()
                  and self.compact_display):
                # __
                log.debug("returning False - J")
                return False

            else:
                log.debug("returning True - K")
                log.debug("numerics[0] = " + repr(numerics[0]))
                return True

        # This last return should be useless
        log.debug("returning False - L")
        return False


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Sum
# @brief Has Exponented terms & an exponent. Iterable. Two display modes.
class Sum(CommutativeOperation):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg None|Sum|Number|String|Exponented|[Number|String|Exponented]
    #   In the case of the list, the Sums having an exponent equal to 1
    #   will be treated before the Exponenteds so that their terms are
    #   inserted in the current Sum instead of inserting a term as a
    #   Sum. If the exponent is greater than 1, then it will be the case.
    #   If the argument isn't of the kinds listed above, an exception will be
    #   raised.
    #   Giving None or an empty list is equivalent to giving 0
    #   @return One instance of Sum
    def __init__(self, arg):
        CommutativeOperation.__init__(self)
        # self._info is set to an empty list.
        # The flag 'compact_display' is let to True.
        # If this flag is set to True, no addition sign will be displayed.
        # If it is set to False, they all will be displayed, except the ones
        # which are mentioned not to be in the info list, aka info.
        # Example with compact_display=True: 2 - 3 + 5
        # Same with compact_display=False: (+2) + (-3) + (+5)

        self._symbol = '+'

        self._neutral = Item(0)

        # should this next flag be copied when creating a copy of a Sum ?
        self._force_inner_brackets_display = False

        self.str_openmark = "["
        self.str_closemark = "]"

        # 1st CASE: Sum
        if isinstance(arg, Sum):
            self._compact_display = arg.compact_display
            self._force_inner_brackets_display = \
                arg.force_inner_brackets_display
            self._exponent = arg.exponent.clone()
            for i in range(len(arg)):
                self._element.append(arg.term[i].clone())
                self._info.append(arg.info[i])

        # 2d CASE: Number
        elif is_number(arg) or type(arg) is str:
            self._element.append(Item(arg))
            self._info.append(False)

        # 3d CASE: Exponented
        elif isinstance(arg, Exponented):
            self._element.append(arg.clone())
            self._info.append(False)

        # 4th CASE: [Numbers|Exponenteds]
        elif (type(arg) == list) and len(arg) >= 1:
            for i in range(len(arg)):
                # The 1-exponent Sum are processed apart from all other
                # Exponenteds
                if (isinstance(arg[i], Sum)
                    and arg[i].exponent.is_displ_as_a_single_1()):
                    # __
                    for j in range(len(arg[i])):
                        self._element.append(arg[i].term[j].clone())
                        self._info.append(arg[i].info[j])

                elif isinstance(arg[i], Exponented):
                    self._element.append(arg[i].clone())
                    self._info.append(False)

                elif is_number(arg[i]) or type(arg[i]) is str:
                    self._element.append(Item(arg[i]))
                    self._info.append(False)

                else:
                    raise TypeError('Got: ' + str(type(arg[i]))
                                    + ' instead of a number|String|Exponented')

        # 5th CASE: None|[]
        elif arg is None or (type(arg) == list and len(arg) == 0):
            self._element.append(Item(0))
            self._info.append(False)

        # All other unforeseen cases: an exception is raised.
        else:
            raise TypeError('Got: ' + str(type(arg))
                            + ' instead of a Sum|Number|String|Exponented|'
                            '[Numbers|Strings|Exponenteds]')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the number of negative factors of the Sum (i.e. 0)
    def get_minus_signs_nb(self):
        return 0

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns a raw list of the numeric terms of the Sum
    def get_numeric_terms(self):
        numeric_terms_list = []

        for term in self.element:
            if isinstance(term, Sum):
                numeric_terms_list = numeric_terms_list \
                    + term.get_numeric_terms()

            elif term.is_numeric():
                numeric_terms_list.append(term)

        return numeric_terms_list

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns a raw list of the literal terms of the Sum
    def get_literal_terms(self):
        literal_terms_list = []

        for term in self.element:
            if isinstance(term, Sum):
                literal_terms_list = literal_terms_list \
                    + term.get_literal_terms()

            elif not term.is_numeric():
                literal_terms_list.append(term)

        return literal_terms_list

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a dict. of couples (literal object):(numeric coeffs sum)
    #   Two objects are in fact created: a dictionary + an index which is a
    #   list containing the objects in the order they appear. The dictionary
    #   loses this order in general and the Sums created after that would never
    #   be in the same order without this index.
    #   Numeric Items are labeled NUMERIC in the index.
    #   For ex. giving the expression 6 + 2x² + 3x - 9 + x³ - 5x as an argument
    #   should return ({NUMERIC:(6-9), x²:2, x:(3-5), x³:1},
    #                  [NUMERIC, x², x, x³]).
    #   This method is fundamental to reduce Sums correctly, it is most
    #   important that it returns an object of the kind mentionned here above.
    #   @param provided_sum The Sum to examine...
    #   @return A tuple (dic, index).
    def get_terms_lexicon(self):
        # Here's the dictionary ("lexicon") to build and return
        lexi = {}
        # Here's the index
        index = []

        # GLANCE AT THE TERMS ONE AFTER THE OTHER
        for term in self.element:
            # IF THE i-TH TERM IS AN ITEM WHICH IS...
            # ... NUMERIC:
            if isinstance(term, Item) and term.is_numeric():
                put_term_in_lexicon(NUMERIC, term, lexi)
                if NUMERIC not in index:
                    index.append(NUMERIC)

            # ... LITERAL:
            elif isinstance(term, Item) and term.is_literal():
                # First create the coefficient that will be put into the
                # coeffs Sum i.e. either +1 or -1 depending on the sign
                # of the Item
                if term.is_positive():
                    associated_coeff = Item(1)
                else:
                    associated_coeff = Item(-1)

                # Create the Item "without sign" (this version is used
                # as a key in the lexicon)
                positive_associated_item = term.clone()
                positive_associated_item.set_sign('+')

                # and put it in the lexicon:
                put_term_in_lexicon(positive_associated_item,
                                    associated_coeff,
                                    lexi)
                if positive_associated_item not in index:
                    index.append(positive_associated_item)

            # IF THE i-TH TERM IS A MONOMIAL:
            elif isinstance(term, Monomial):
                if term.get_degree() == 0 or term.is_null():
                    put_term_in_lexicon(NUMERIC, term[0], lexi)
                    if NUMERIC not in index:
                        index.append(NUMERIC)
                else:
                    put_term_in_lexicon(term[1], term[0], lexi)
                    if term[1] not in index:
                        index.append(term[1])

            # IF THE i-TH TERM IS A PRODUCT:
            elif isinstance(term, Product):
                # first reduce it to make things clearer !
                aux_product = term.reduce_()
                # get the first Item of this reduced Product, it is sure that
                # it is numeric because a Product reduction necessary creates
                # a Product (numeric Item) × (possibly something else)
                associated_coeff = aux_product.factor.pop(0)

                # either there's nothing left in the remaining factors list
                # which means the product only contained one numeric Item
                # which has to be put in the right place of the lexicon
                if len(aux_product.factor) == 0:
                    put_term_in_lexicon(NUMERIC, associated_coeff, lexi)
                    if NUMERIC not in index:
                        index.append(NUMERIC)

                # or there's another factor left in the remaining list
                # if it's literal, then it means that the Product was
                # something like -5x, and so the Item -5 has to be added
                # to the "x" key
                # (the one which has been "poped" just somewhat above)
                elif (len(aux_product.factor) == 1
                      and isinstance(aux_product.factor[0], Item)
                      and aux_product.factor[0].is_literal()):
                    # __
                    put_term_in_lexicon(aux_product.factor[0],
                                        associated_coeff,
                                        lexi)
                    if aux_product.factor[0] not in index:
                        index.append(aux_product.factor[0])

                # in all other cases (several factors Product, or the 2d
                # factor is a Sum etc.) the term is put at its place in
                # the lexicon
                else:
                    put_term_in_lexicon(aux_product, associated_coeff, lexi)
                    if aux_product not in index:
                        index.append(aux_product)

            # IF THE i-TH TERM IS A SUM:
            elif isinstance(term, Sum):
                # If the exponent is different from 1, it is managed as a
                # standard term (just check if a key already matches it
                # and add +/- 1 as associated coeff)
                # ex: the 2d term in: 2x + (x + 3)² + 5
                # notice that the case of 2x + 7(x + 3)² + 5 would be managed
                # in the "PRODUCT" section of this method
                if term.exponent != Value(1):
                    associated_coeff = Item(1)
                    put_term_in_lexicon(term, associated_coeff, lexi)

                    if term not in index:
                        index.append(term)

                else:  # Case of a Sum having a exponent equal to 1
                    # and imbricated in the initial Sum: we get its
                    # lexicon&index recursively
                    lexi_index_tuple_to_add = term.get_terms_lexicon()

                    lexi_to_add = lexi_index_tuple_to_add[0]
                    index_to_add = lexi_index_tuple_to_add[1]

                    # __e content of this lexicon is added to the one
                    # we're building now
                    additional_keys = list()
                    # this list let us collect the keys
                    # that don't exist yet in the lexicon.
                    # as the loop is on this lexicon, it is
                    # not possible to add new keys while
                    # we're reading it (otherwise we'll get a
                    # run time error)
                    for suppl_key in index_to_add:
                        # what follows here looks like the put_term_in_lexicon
                        # method but difference is that there are maybe several
                        # coefficients to add for each key
                        added_key = False

                        for key in lexi:
                            if key == suppl_key:
                                for objct in lexi_to_add[suppl_key].term:
                                    put_term_in_lexicon(key, objct, lexi)
                                    # nothing has to be added to the index
                                    # because all of these terms are already
                                    # in the lexicon

                                added_key = True

                        if not added_key:
                            additional_keys.append(suppl_key)

                    # the keys that weren't in the lexicon yet have been saved
                    # in the list additional_keys, they are added now to the
                    # lexicon
                    # /!\ POSSIBLE BUG HERE !!!!! if any of these keys is many
                    # times there ? check if using put_term_in_lexicon
                    # wouldn't be better
                    # (--> or is this situation impossible ?)
                    for suppl_key in additional_keys:
                        lexi[suppl_key] = lexi_to_add[suppl_key]
                        index.append(suppl_key)

        return (lexi, index)

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the value of the force_inner_brackets_display field
    def get_force_inner_brackets_display(self):
        return self._force_inner_brackets_display

    term = property(CommutativeOperation.get_element,
                    doc="To access the terms of the Sum.")

    force_inner_brackets_display = property(get_force_inner_brackets_display,
                                            doc="force_inner_brackets_display"
                                                " field of a Sum")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the n-th term to the given arg
    def set_term(self, n, arg):
        self.set_element(n, arg)

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets a value to the force_inner_brackets_display field
    #   @param arg Assumed to be True or False (not tested)
    def set_force_inner_brackets_display(self, arg):
        self._force_inner_brackets_display = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        global expression_begins
        log = settings.dbg_logger.getChild('Sum.into_str')

        if ('force_expression_begins' in options
            and options['force_expression_begins']):
            # __
            expression_begins = options['force_expression_begins']
            options['force_expression_begins'] = False

        # Here are processed all Sum objects (including Polynomials etc.)
        # Displaying the + sign at the begining of an expression still depends
        # on the machine's expression_begins flag.
        # In a Sum, expression_begins can be reset to True for one good reason
        # at least: if inner brackets are required because of an exponent
        # different from 1
        resulting_string = ""

        # This flag checks if one term at least has been displayed
        # If it is still False at the end of this processing, a 0 will
        # be displayed.
        flag = False

        # If
        # - the exponent differs from 1 and if (the sum contains several
        #   terms or only one which is negative)
        # OR
        # - displaying inner brackets is being forced (needed in exercises
        #   like reducing 3x + 4 - (2x + 7) + (x + 1))
        # then
        # the Sum has to be displayed between inner brackets
        log.debug("Entering: expression_begins = "
                  + str(expression_begins)
                  + "; force_inner_brackets_display = "
                  + str(self.force_inner_brackets_display))

        if ((not (self.exponent.is_displ_as_a_single_1())
             and (len(self) >= 2
                  or (len(self) == 1 and self.term[0].get_sign() == '-')))
            or self.force_inner_brackets_display):
            # __
            if not expression_begins:
                resulting_string += MARKUP['plus'] + MARKUP['opening_bracket']
            else:
                resulting_string += MARKUP['opening_bracket']

            expression_begins = True

        # Compact_display's main loop
        # which will display the terms one after the other
        if self.compact_display:
            log.debug(
                "[compact_display]: expression_begins = "
                + str(expression_begins)
                + "; force_inner_brackets_display = "
                + str(self.force_inner_brackets_display))
            for i in range(len(self)):
                # compact_display: zeros won't be displayed
                if not self.term[i].is_displ_as_a_single_0():
                    resulting_string += self.term[i].into_str(**options)
                    flag = True
                    next_term_nb = self.next_displayable_term_nb(i)
                    expression_begins = False

                    if next_term_nb is None:
                        log.debug("no next term to display.")
                    else:
                        log.debug("the next term to display is "
                                  + repr(self.term[next_term_nb]))

                    if (next_term_nb is not None
                        and (self.term[next_term_nb].requires_inner_brackets()
                             or (isinstance(self.term[next_term_nb], Product)
                                 and
                                 (self.term[next_term_nb]
                                  .factor[0].requires_brackets(0)
                                  or self.term[next_term_nb]
                                  .factor[0].is_displ_as_a_single_0())
                                 and not
                                 (len(self.term[next_term_nb]
                                      .throw_away_the_neutrals()) == 1
                                  and
                                  self.term[next_term_nb]
                                  .throw_away_the_neutrals()
                                  .factor[0].requires_brackets(0)))
                             or (isinstance(self.term[next_term_nb], Sum)
                                 and (self.term[next_term_nb].term[0]
                                      .requires_inner_brackets())))):
                        # __
                        log.debug(
                            "In into_str in Sum: adding a + for the next term "
                            "in case it can't do that on its own.")
                        # \
                        #   + "Tests results: \n" \
                        #   + "self.term[next_term_nb]." \
                        #   + "requires_inner_brackets()" + " returned " \
                        #   + str(self.term[next_term_nb].\
                        #         requires_inner_brackets()) \
                        #   + "\nself.term[next_term_nb].factor[0]" \
                        #   + ".requires_brackets(0) returned " \
                        #   + str(self.term[next_term_nb].\
                        #         factor[0].requires_brackets(0)) \
                        #   + "\nself.term[next_term_nb].factor[0]." \
                        #   + "is_displ_as_a_single_0() returned " \
                        #   + str(self.term[next_term_nb].\
                        #         factor[0].is_displ_as_a_single_0())

                        resulting_string += MARKUP['plus']
                        expression_begins = True

        # Not compact_display's main loop
        else:
            log.debug("[not compact_display]: expression_begins = "
                      + str(expression_begins)
                      + "; force_inner_brackets_display = "
                      + str(self.force_inner_brackets_display))
            for i in range(len(self)):
                if (self.info[i]
                    and not self.term[i].requires_inner_brackets()
                    and not self.term[i].is_displ_as_a_single_0()):
                    # __
                    resulting_string += MARKUP['opening_bracket'] \
                        + self.term[i].into_str(force_display_sign='ok',
                                                **options) \
                        + MARKUP['closing_bracket']
                    flag = True

                elif not self.term[i].is_displ_as_a_single_0():
                    resulting_string += self.term[i].into_str(**options)
                    flag = True

                # A "+" is finally added in the case of another term left
                # to be complete-writing displayed
                next_term_nb = self.next_displayable_term_nb(i)

                if next_term_nb is not None and self.info[next_term_nb]:
                    resulting_string += MARKUP['plus']
                    expression_begins = True

        # if nothing has been displayed, a default 0 is displayed:
        if flag is False:
            resulting_string += MARKUP['zero']

        # if the sum's exponent differs from 1 and (the sum contains
        # several terms or only one negative term),
        # then the bracket earlier opened has to be shut
        if ((not self.exponent.is_displ_as_a_single_1()
             and (len(self) >= 2
                  or (len(self) == 1 and self.term[0].get_sign() == '-')))
            or self.force_inner_brackets_display):
            # __
            resulting_string += MARKUP['closing_bracket']
        if self.exponent_must_be_displayed():
            expression_begins = True
            exponent_string = self.exponent.into_str(**options)
            resulting_string += MARKUP['opening_exponent'] \
                + exponent_string \
                + MARKUP['closing_exponent']

        log.debug("Leaving: resulting_string = " + resulting_string)
        return resulting_string

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the next calculated step of a *numeric* Sum
    #   @todo This method may be only partially implemented (see source)
    #   @todo the inner '-' signs (±(-2)) are not handled by this method so far
    def calculate_next_step(self, **options):
        log = settings.dbg_logger.getChild(
            'Sum.calculate_next_step')
        if not self.is_numeric():
            return self.expand_and_reduce_next_step(**options)

        copy = self.clone()
        log.debug("Entering with copied Sum: " + repr(copy))
        # First recursively dive into embedded sums &| products &| fractions:
        if len(copy) == 1 and (isinstance(copy.term[0], CommutativeOperation)
                               or isinstance(copy.term[0], Fraction)):
            # __
            log.debug("Exiting, recursively diving in element[0]")
            return copy.term[0].calculate_next_step(**options)

        # Also de-embed recursively all terms that are CommutativeOperations
        # containing
        # only one element AND replace these f*** 0-degree-Monomials by
        # equivalent Item/Fraction.
        a_term_has_been_depacked = False
        for i in range(len(copy)):
            if ((isinstance(copy.term[i], CommutativeOperation)
                 and len(copy.term[i]) == 1)
                or isinstance(copy.term[i], Monomial)):
                # __
                copy.set_element(i, copy.term[i].element[0])
                a_term_has_been_depacked = True

        if a_term_has_been_depacked:
            log.debug("Exiting, having depacked one element at least"
                      + "calculate_next_step is called on: " + repr(copy))
            return copy.calculate_next_step(**options)

        # Second point:
        # if any sign of numerator or denominator is negative, compute the
        # sign of the fraction in order to get a "clean" Sum and by the way,
        # all denominators will be positive
        a_minus_sign_in_a_fraction_was_found = False
        for i in range(len(copy)):
            if isinstance(copy.term[i], Fraction) \
               and (copy.term[i].numerator.get_sign() == '-'
                    or copy.term[i].denominator.get_sign() == '-'):
                # __
                # case of a denominator like -(-3) is probably not well handled
                copy.element[i]\
                    .set_sign(sign_of_product([copy.element[i].get_sign(),
                                               copy.element[i]
                                               .numerator.get_sign(),
                                               copy.element[i]
                                               .denominator.get_sign()]))
                copy.element[i].numerator.set_sign('+')
                copy.element[i].denominator.set_sign('+')
                a_minus_sign_in_a_fraction_was_found = True

        if a_minus_sign_in_a_fraction_was_found:
            log.debug("Exiting, having changed negative denominators, "
                      "the returned object is: " + repr(copy))
            return copy

        # Then, check if the case is not this special one:
        # at least two fractions having the same denominator
        # If yes, then there's something special to do (put these fractions
        # together)
        # If not, just go on...

        # First let's count how many numbers & fractions there are
        numeric_items_nb = 0
        fractions_nb = 0

        for i in range(len(copy)):
            if isinstance(copy.term[i], Fraction):
                fractions_nb += 1
            elif isinstance(copy.term[i], Item) and copy.term[i].is_numeric():
                numeric_items_nb += 1
            elif (isinstance(copy.term[i], Product)
                  and len(copy.term[i]) == 1
                  and isinstance(copy.term[i].factor[0], Item)
                  and copy.term[i].factor[0].is_numeric()):
                # __
                copy.element[i] = copy.term[i].factor[0]
                numeric_items_nb += 1

        log.debug("We found: " + str(fractions_nb) + " fractions, "
                  "and " + str(numeric_items_nb) + " numeric items.")

        # Now check if there are at least two fractions having the
        # same denominator
        fractions_have_been_added = False
        dont_touch_these = []

        if fractions_nb >= 1:
            # we will build a dictionnary containing:
            # {denominator1:[fraction1 + fraction3], denominator2:[...], ...}
            lexi = {}
            for objct in copy:
                if isinstance(objct, Fraction):
                    put_term_in_lexicon(objct.denominator, objct, lexi)

            built_lexi = "".join(["Key: " + repr(k) + " "
                                  "Value: " + repr(v) + "\n"
                                  for k, v in lexi.items()])
            log.debug("Looking for fractions having the same denominator; "
                      "built the lexicon:\n" + str(built_lexi))

            # now we check if any of these denominators is there several times
            # and if yes, we change the copy
            for denominator_key in lexi:
                if len(lexi[denominator_key]) >= 2:
                    fractions_have_been_added = True
                    common_denominator = denominator_key
                    numes_list = []
                    for fraction in lexi[denominator_key].element:
                        if fraction.sign == '+':
                            numes_list.append(fraction.numerator)
                        else:
                            new_term = Product([Item(-1)]
                                               + fraction.numerator.factor)
                            if fraction.numerator.get_sign() == '+':
                                new_term = new_term.reduce_()
                            new_term.set_compact_display(True)
                            numes_list.append(new_term)

                    new_fraction = Fraction((Sum(numes_list),
                                            common_denominator))

                    log.debug("Found " + str(len(lexi[denominator_key]))
                              + " fractions having this denominator: "
                              + repr(denominator_key)
                              + "\nnew_fraction looks like: "
                              + repr(new_fraction))

                    first_fraction_met = True
                    for i in range(len(copy)):
                        if not i >= len(copy):
                            log.debug("copy.term[" + str(i) + "] = "
                                      + repr(copy.term[i])
                                      + "\nlooked for here: "
                                      + repr(lexi[denominator_key]))
                            if isinstance(copy.term[i], Fraction) \
                               and copy.term[i] in lexi[denominator_key].term:
                                # __
                                log.debug("copy.term[" + str(i) + "] is in"
                                          " this lexicon: "
                                          + repr(lexi[denominator_key]))
                                if first_fraction_met:
                                    copy.set_element(i, new_fraction)
                                    first_fraction_met = False
                                    dont_touch_these.append(new_fraction)
                                else:
                                    copy.remove(copy.term[i])

        # if fractions_have_been_added:
        #   return copy

        # now gather numeric items in a sum.
        # if they were scattered, the sum doesn't have to be calculated
        # hereafter but if they were not scattered, then the sum may be
        # calculated (so we'll put the newly created sum in dont_touch_these
        # or not, depending on the case)
        some_terms_have_been_moved = False
        max_found_gap = 1
        last_numeric_item_position = 0

        if numeric_items_nb >= 2:
            numeric_terms_collection = []
            for i in range(len(copy)):
                if isinstance(copy.term[i], Item) \
                   and copy.term[i].is_numeric():
                    # __
                    if i - last_numeric_item_position > max_found_gap:
                        max_found_gap = i - last_numeric_item_position
                    last_numeric_item_position = i
                    numeric_terms_collection.append(copy.term[i])

            # if there are only numeric items, then they don't have to be
            # embedded in a Sum (it would result in infinitely embedding
            # sums)
            if fractions_nb >= 1:
                first_numeric_item_met = True
                for i in range(len(copy)):
                    if not i >= len(copy) \
                       and isinstance(copy.term[i], Item) \
                       and copy.term[i].is_numeric():
                        # __
                        if first_numeric_item_met:
                            copy.term[i] = Sum(numeric_terms_collection)
                            first_numeric_item_met = False
                            if max_found_gap >= 2:
                                some_terms_have_been_moved = True
                                dont_touch_these.append(copy.term[i])
                        else:
                            copy.remove(copy.term[i])

        # Now check if any of the terms has to be
        # "calculated_next_step" itself.
        # If yes, just replace these terms by the calculated ones.

        a_term_has_been_modified = False

        for i in range(len(copy)):
            if not copy.term[i] in dont_touch_these:
                temp = copy.term[i].calculate_next_step(**options)
                if temp is not None:
                    copy.term[i] = temp
                    a_term_has_been_modified = True

        # if a_term_has_been_modified:
        #   return copy

        if fractions_have_been_added \
           or a_term_has_been_modified \
           or some_terms_have_been_moved:
            # __
            log.debug('Exiting, returning ' + str(copy) + 'because\n'
                      'a term has been modified: {a}\n'
                      'fractions have been added: {f}\n'
                      'some terms have been moved: {t}'
                      .format(a=str(a_term_has_been_modified),
                              f=str(fractions_have_been_added),
                              t=str(some_terms_have_been_moved)))
            return copy

        # no term has been modified, no term has been moved,
        # no fractions have already been added,
        # so let's check in which case we are:
        # 1. There are only numbers (e.g. numeric Items)
        # 2. There are only fractions
        # 3. There are fractions mixed with numbers.
        # first if nothing has to be computed, just return None
        if len(copy) == 1:
            # if this unique term has to be calculated, then it has been
            # done above
            log.debug('Exiting, returning None')
            return None

        # 1. There are only numbers (e.g. numeric Items)
        if numeric_items_nb >= 1 and fractions_nb == 0:
            return Item(copy.evaluate(stop_recursion=True))

        # 2. There are only fractions
        if numeric_items_nb == 0 and fractions_nb >= 1:
            denos_list = []
            for i in range(len(copy)):
                denos_list.append(copy.term[i].denominator.factor[0].raw_value)

            lcm = lcm_of_the_list(denos_list)
            lcm_item = Item(lcm)

            # now check if at least two denominators are different
            # if yes, then the fractions have to be reduced to the same
            # denominator
            # if no, then the numerators can be added and the denominator
            # will be kept
            same_deno_reduction_required = False

            for i in range(len(copy)):
                if lcm_item != copy.term[i].denominator.factor[0]:
                    same_deno_reduction_required = True

            if same_deno_reduction_required:
                for i in range(len(copy)):
                    aux_item = Item(int(lcm / copy.term[i].
                                        denominator.factor[0].raw_value))
                    if aux_item.raw_value != 1:
                        copy.term[i]\
                            .set_numerator(Product([copy.term[i]
                                                    .numerator.factor[0],
                                                   aux_item]))
                        copy.term[i].numerator.set_compact_display(False)
                        copy.term[i]\
                            .set_denominator(Product([copy.term[i]
                                                      .denominator.factor[0],
                                                     aux_item]))
                        copy.term[i].denominator.set_compact_display(False)
                        copy.term[i].set_same_deno_reduction_in_progress(True)
            else:
                numes_list = []
                for i in range(len(copy)):
                    numes_list\
                        .append(Product([copy.term[i].numerator.factor[0],
                                         Item((copy.term[i].sign, 1))])
                                .reduce_().factor[0])
                copy = Sum([Fraction(('+',
                                      Sum(numes_list),
                                      lcm_item))])
            return copy

        # 3. There are fractions mixed with numbers.
        if numeric_items_nb >= 1 and fractions_nb >= 1:
            # copy = Sum(self)
            for i in range(len(copy)):
                if isinstance(copy.term[i], Item) \
                   and copy.term[i].is_numeric():
                    # __
                    copy.term[i] = copy.term[i].turn_into_fraction()
                    copy.term[i].set_same_deno_reduction_in_progress(True)

            return copy.calculate_next_step(**options)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the next step of expansion/reduction of the Sum
    #   So, either the Sum of its expanded/reduced terms,
    #   or the Sum itself reduced, or None
    #   @return Exponented
    def expand_and_reduce_next_step(self, **options):
        log = settings.dbg_logger.getChild(
            'Sum.expand_and_reduce_next_step')
        if self.is_numeric():
            return self.calculate_next_step(**options)

        log.debug("Entered, on: " + repr(self) + "; info: " + str(self.info))

        copy = Sum(self).throw_away_the_neutrals()

        # to reduce the number of required steps in the case of
        # imbricated Sums like: [x, [x, x]] what should produce [(1+1+1)x]
        # in the next step and not [x, [(1+1)x]] and then [x, [2x]] and
        # then [(1+2)x] etc. which is far too long !
        # The Monomials with degree 0 also cause problem (because they
        # require a reduction line to become the equivalent Item and again,
        # the user won't see any difference...)
        new_copy = Sum(copy)
        new_copy.reset_element()
        new_copy.set_info(list())
        an_imbricated_sum_has_been_found = False
        a_degree_0_monomial_has_been_found = False

        for i in range(len(copy)):
            if ((not isinstance(copy.term[i], Sum)
                 or (isinstance(copy.term[i], Sum)
                 and not copy.term[i].exponent.is_displ_as_a_single_1()))
                and not (isinstance(copy.term[i], Monomial)
                and copy.term[i].degree == 0)):
                # __
                new_copy.element.append(copy.term[i])
                new_copy.info.append(copy.info[i])

            elif (isinstance(copy.term[i], Monomial)
                  and copy.term[i].degree == 0):
                # __
                new_copy.element.append(copy.term[i].factor[0])
                new_copy.info.append(copy.info[i])
            else:
                an_imbricated_sum_has_been_found = True
                for j in range(len(copy.term[i])):
                    new_copy.element.append(copy.term[i].term[j])
                    new_copy.info.append(copy.term[i].info[j])

        if an_imbricated_sum_has_been_found \
           or a_degree_0_monomial_has_been_found:
            # __
            log.debug(
                "Exiting, a term has been modified, so recursive call on: "
                + repr(new_copy))

            return new_copy.expand_and_reduce_next_step(**options)

        # Now let's begin without any imbricated Sum nor 0-degree Monomials !
        # That's clean:o)
        a_term_at_least_has_been_modified = False

        # A similar protection as in intermediate_reduction_line has to
        # be made for other cases
        numeric_terms_must_be_reduced = False
        the_first_numeric_term_has_been_found = False

        if copy.numeric_terms_require_to_be_reduced():
            # __
            numeric_terms_must_be_reduced = True
            (lexi, index) = copy.get_terms_lexicon()
            numeric_value = Item(lexi[NUMERIC].evaluate())

        # this list will contain the numeric terms that should be removed
        # from the Sum after the reduction of numeric terms (e.g.
        # if 12 - 1 + 4x has to be reduced, will become 11 + 4x this
        # way: replacing 12 by 11 and removing -1)
        terms_to_remove = list()
        # the terms that have been modified in the "first round" don't have
        # to be modified anew in the "second round".
        modified_term = list()

        # first round:
        # check if any of the terms needs to be reduced
        # (excepted numeric terms)
        for i in range(len(copy)):
            test = copy.term[i].expand_and_reduce_next_step(**options)
            if test is not None:
                copy.term[i] = test
                a_term_at_least_has_been_modified = True
                modified_term.append(True)
            else:
                modified_term.append(False)

        # second round:
        # if necessary, let's reduce the numeric terms
        if numeric_terms_must_be_reduced \
           and a_term_at_least_has_been_modified:
            # __
            for i in range(len(copy)):
                if copy.term[i].is_numeric() \
                   and not modified_term[i]:
                    # __
                    if the_first_numeric_term_has_been_found:
                        terms_to_remove.append(copy.term[i])
                    else:
                        copy.term[i] = numeric_value
                        the_first_numeric_term_has_been_found = True

            for j in range(len(terms_to_remove)):
                copy.remove(terms_to_remove[j])

            # elif numeric_terms_must_be_reduced \
            #   and copy.term[i].is_numeric():
                # __
            #    if the_first_numeric_term_has_been_found:
            #        terms_to_remove.append(copy.term[i])

            #    else:
            #        copy.term[i] = numeric_value
            #        the_first_numeric_term_has_been_found = True
            #        a_term_at_least_has_been_modified = True

        # for j in xrange(len(terms_to_remove)):
        #    copy.remove(terms_to_remove[j])

        if a_term_at_least_has_been_modified:
            log.debug("Exiting, a term has been modified, so returning: "
                      + repr(copy))
            return copy

        # no term of the Sum needs to be reduced
        else:
            if copy.is_numeric() and copy.is_reducible():
                log.debug("Exiting, no term has been modified, but: "
                          + repr(copy) + "\nis numeric and reducible "
                          "so, returning a reduced copy of it.")

                return copy.reduce_()

            elif copy.is_reducible():
                log.debug("Exiting, no term has been modified, and: "
                          + repr(copy) + "\nisn't numeric but is reducible "
                          "so, returning the intermediate line generated "
                          "from it.")

                details_level = options.get('details_level', 'maximum')
                if details_level == 'maximum':
                    return copy.intermediate_reduction_line()
                else:  # 'medium' or 'none', so far, produce the same result
                    return copy.intermediate_reduction_line()\
                        .expand_and_reduce_next_step()

            else:
                log.debug("Exiting, no term has been modified, and: "
                          + repr(copy) + "\nisn't numeric nor reducible, "
                          "so, returning None.")

                return None

    # --------------------------------------------------------------------------
    ##
    #   @brief Compares two Sums
    #   Returns 0 if all terms are the same in the same order and if the
    #   exponents are also the same
    #   /!\ a + b will be different from de b + a
    #   It's not a mathematical comparison, but a "displayable"'s one.
    #   @return True if all terms are the same in the same order & the exponent
    def __eq__(self, objct):
        if not isinstance(objct, Sum):
            return False

        if len(self) != len(objct):
            return False

        for i in range(len(self)):
            if self.term[i] != objct.term[i]:
                return False

        if self.exponent != objct.exponent:
            return False

        return True

    # --------------------------------------------------------------------------
    ##
    #   @brief Defines the performed CommutativeOperation as a Sum
    def operator(self, arg1, arg2):
        return arg1 + arg2

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the position of next non-equivalent to 0 term...
    #   @param position The point where to start from to search
    #   @return The position of next non-equivalent to 0 term (or None)
    def next_displayable_term_nb(self, position):
        for i in range(len(self) - 1 - position):
            if not self.term[i + 1 + position].is_displ_as_a_single_0():
                return i + 1 + position
        return None

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the usual writing rules require a × between two factors
    #   @param objct The other one
    #   @param position The position (integer) of self in the Product
    #   @return True if the writing rules require × between self & obj
    def multiply_symbol_is_required(self, objct, position):
        # 1st CASE: Sum × Item|Function
        if isinstance(objct, Item):
            if len(self) >= 2:
                return (objct.is_numeric(displ_as=True)
                        or (objct.is_literal(displ_as=True)
                            and objct.sign == '-'))
            else:
                return self.term[0].multiply_symbol_is_required(objct,
                                                                position)
        # 2d CASE: Sum × Sum
        if isinstance(objct, Sum):
            if len(self) >= 2 and len(objct) >= 2:
                return False
            if len(self) == 1:
                return self.term[0].multiply_symbol_is_required(objct,
                                                                position)
            if len(objct) == 1:
                return self.multiply_symbol_is_required(objct.term[0],
                                                        position)
        # 3d CASE: Sum × Product
        if isinstance(objct, Product):
            if len(self) == 1:
                return self.term[0].multiply_symbol_is_required(objct,
                                                                position)
            else:
                return self.multiply_symbol_is_required(objct.factor[0],
                                                        position)
        # 4th CASE: Sum × Quotient
        if isinstance(objct, Quotient):
            return True

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the argument requires brackets in a product
    #   For instance, a Sum with several terms or a negative Item
    #   @param position The position of the object in the Product
    #   @return True if the object requires brackets in a Product
    def requires_brackets(self, position):
        log = settings.dbg_logger.getChild('Sum.requires_brackets')
        log.debug('Entering on: ' + repr(self))
        # A Sum having more than one term requires brackets
        tested_sum = None
        if self.compact_display:
            tested_sum = self.throw_away_the_neutrals()

        else:
            tested_sum = self.clone()

        if len(tested_sum) >= 2:
            # return True
            r = tested_sum.requires_inner_brackets()
            log.debug("self.requires_inner_brackets = " + str(r))
            log.debug("--> so, return  " + str(not r))
            return not tested_sum.requires_inner_brackets()
        # If the Sum has only one term, then it will depend on its
        # exponent and on its content
        else:
            # If the exponent is different from 1 (or is not equivalent
            # to 1) then the answer (True/False) will be the same than
            # the one for self.term[0] but not at the first position.
            # In other words, if the first term begins with a -, it
            # requires brackets.
            if not tested_sum.exponent.is_displ_as_a_single_1():
                return tested_sum.term[0].requires_brackets(position + 1)
            else:
                return tested_sum.term[0].requires_brackets(position)

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the argument requires inner brackets
    #   The reason for requiring them is having an exponent different
    #   from 1 and several terms or factors (in the case of Products & Sums)
    #   @return True if the object requires inner brackets
    def requires_inner_brackets(self):
        if self.exponent_must_be_displayed():
            if len(self) == 1 or self.is_displ_as_a_single_1():
                return not(self.get_sign() == '+'
                           and self.term[0].is_numeric(displ_as=True))
            # this case is when there are several terms
            else:
                return True
        return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if a gathering of numeric terms must be reduced
    #   It is True if at least two consecutive numeric Items are in the list
    #   and no other numeric term elsewhere.
    #   Examples where it's True:
    #   3x - 5 + 2 + 5x
    #   -2 + 4 + 9 - 2x + 3x²
    #   When it's False:
    #   3 - 5 + 2x + 6
    #   4 + x - 2
    #   -7 + 2×5 + 4 + 2x
    #   @return True if a gathering of numeric terms must be reduced
    def numeric_terms_require_to_be_reduced(self):
        at_least_one_numeric_term_has_been_found = False
        at_least_two_numeric_terms_have_been_found = False
        two_scattered_terms_have_been_found = False
        last_numeric_term_position = -1
        for i in range(len(self)):
            if self.term[i].is_displ_as_a_single_numeric_Item():
                if not at_least_one_numeric_term_has_been_found:
                    at_least_one_numeric_term_has_been_found = True
                    last_numeric_term_position = i
                else:
                    at_least_two_numeric_terms_have_been_found = True
                    if last_numeric_term_position == i - 1:
                        last_numeric_term_position = i
                    else:
                        two_scattered_terms_have_been_found = True

        if at_least_two_numeric_terms_have_been_found \
           and not two_scattered_terms_have_been_found:
            # __
            return True

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates the intermediate reduction line.
    #   For instance, giving the Sum 5x + 7x³ - 3x + 1,
    #   this method would return (5 - 3)x + 7x³ + 1.
    #   No intermediate expansion will be done, though.
    #   For instance, the expression a + b + (a + b)
    #   will be reduced in 2a + 2b (provided the (a+b) is given as a Sum and
    #   not, for instance, as this Product: 1×(a + b) ;
    #   but the expression a + b + 5(a + b) won't be reduced in 6a + 6b. It has
    #   to be expanded first (there's a Expandable term there !).
    #   This method is the base to process the reduction of a Sum.
    #   It is therefore important that it returns the described kind of result.
    #   @return A Products' Sum: (coefficients Sum)×(literal factor)
    def intermediate_reduction_line(self):
        # In the case of a given Sum like 5x + 4 - 7 + 3x²
        # the intermediate_reduction_line should return the reduced Sum
        # instead of... the same line.
        # So if the numeric terms are in a row (and no other numeric term
        # is anywhere else, otherwise it would be useless), we reduce them
        # This is redundant (?) with the expand_and_reduce_next_step() but is
        # necessary to prevent cases when this method is called without
        # protection
        numeric_terms_must_be_reduced = False

        if self.numeric_terms_require_to_be_reduced():
            # __
            numeric_terms_must_be_reduced = True

        # Let's begin to build the intermediate line
        (lexi, index) = self.get_terms_lexicon()

        final_sum_terms_list = list()

        for key in index:
            if key == NUMERIC:
                temp_object = lexi[key]
                if numeric_terms_must_be_reduced:
                    temp_object = Item(temp_object.evaluate())
                elif len(temp_object) == 1:
                    temp_object = temp_object.term[0]

            elif lexi[key].is_displ_as_a_single_1():
                temp_object = key

            else:
                if len(lexi[key]) == 1:
                    temp_object = Product([lexi[key].term[0], key])
                else:
                    temp_object = Product([lexi[key], key])

            final_sum_terms_list.append(temp_object)

        final_sum = Sum(final_sum_terms_list)

        if self.force_inner_brackets_display:
            final_sum.set_force_inner_brackets_display(True)

        return final_sum

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the reduced Sum
    #   For instance, giving the Sum 5x + 7x³ - 3x + 1,
    #   this method would return -2x + 7x³ + 1.
    #   No intermediate expandment will be done, though.
    #   For instance, the expression a + b + (a + b)
    #   will be reduced in 2a + 2b (provided the (a+b) is given as a Sum and
    #   not, for instance, as this Product: 1×(a + b) ;
    #   but the expression a + b + 5(a + b) won't be reduced in 6a + 6b. It has
    #   to be expanded first (there's a Expandable term there !).
    #   @todo support for Fractions (evaluation...)
    #   @return One instance of Sum (reduced) [?] or of the only remaining term
    def reduce_(self):
        log = settings.dbg_logger.getChild('Sum.reduce')
        # The main difference with the intermediate_reduction_line method
        # is that the numeric part will be evaluated
        (lexi, index) = self.get_terms_lexicon()

        log.debug("Entered on:" + repr(self))

        lexi_content = "".join([repr(k) + ": "
                                + repr(v) + "; "
                                for k, v in lexi.items()])

        log.debug("get_terms_lexicon returned this: " + lexi_content)

        final_sum_terms_list = list()

        for key in index:
            if key == NUMERIC:
                temp_object = lexi[key].evaluate()
            elif lexi[key].is_displ_as_a_single_1():
                temp_object = key
            else:
                computed_coeff = Item(lexi[key].evaluate())
                if computed_coeff.is_displ_as_a_single_0():
                    temp_object = computed_coeff
                else:
                    temp_object = Product([computed_coeff, key])
            final_sum_terms_list.append(temp_object)
        final_sum = (Sum(final_sum_terms_list)).throw_away_the_neutrals()

        if self.force_inner_brackets_display:
            final_sum.set_force_inner_brackets_display(True)

        # Here follows a patch to avoid returning a Sum containing only one
        # term.
        if len(final_sum) == 1 \
           and final_sum.term[0].exponent.is_displ_as_a_single_1():
            # __
            final_sum = final_sum.term[0]

        log.debug("Leaving, returning: " + repr(final_sum))

        return final_sum

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the result of the Sum is null
    def is_null(self):
        if self.evaluate() == 0:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Sum contains only 0s and one 1. For instance, 1+0+0
    def is_displ_as_a_single_1(self):
        # dive recursively into embedded objects
        if len(self) == 1:
            return self.term[0].is_displ_as_a_single_1()

        a_term_different_from_0_and_1_has_been_found = False
        equivalent_to_1_terms_nb = 0

        for term in self.element:
            if term.is_displ_as_a_single_1():
                equivalent_to_1_terms_nb += 1
            elif not term.is_displ_as_a_single_0():
                a_term_different_from_0_and_1_has_been_found = True

        if a_term_different_from_0_and_1_has_been_found:
            return False
        elif equivalent_to_1_terms_nb == 1:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Sum can be displayed as a single -1
    # So, if it only contains 0s and a single -1. For instance, 0+0+(-1)+0
    def is_displ_as_a_single_minus_1(self):
        a_term_different_from_0_and_minus1_has_been_found = False
        equivalent_to_minus1_terms_nb = 0

        for term in self.element:
            if term.is_displ_as_a_single_minus_1():
                equivalent_to_minus1_terms_nb += 1
            elif not term.is_displ_as_a_single_0():
                a_term_different_from_0_and_minus1_has_been_found = True

        if a_term_different_from_0_and_minus1_has_been_found:
            return False
        elif equivalent_to_minus1_terms_nb == 1:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the object can be displayed as a single 0
    #   For instance, 0 + 0 + 0 but NOT - 1 + 0 + 1 (it's a matter of display)
    def is_displ_as_a_single_0(self):
        return self.is_displ_as_a_single_neutral(Item(0))

    # --------------------------------------------------------------------------
    ##
    #   @brief True if the Sum is reducible
    #   This is based on the result of the get_term_lexicon method
    #   @return True|False
    def is_reducible(self):
        if self.is_displ_as_a_single_0() \
           or self.is_displ_as_a_single_1() \
           or self.is_displ_as_a_single_minus_1():
            # __
            return False

        lexi = self.get_terms_lexicon()[0]

        # If one of the coefficient Sums contains at least 2 terms, then
        # the Sum is reducible
        for key in lexi:
            if len(lexi[key].term) >= 2:
                return True

        return False


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Monomial
# @brief A Monomial is a Product of a numeric Exponented and a literal Item
class Monomial(Product):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg DEFAULT|Monomial|(sign, coeff, degree)|.......
    #   Possible arguments are:
    #   - DEFAULT, which is equivalent to ('+', 1, 0)
    #   - another Monomial which will be copied
    #   - (sign, coeff, degree) where coeff is a number and degree an integer
    #   - (coeff, degree) where coeff's numeric Exponented & degree an integer
    #   - (RANDOMLY, max_coeff, max_degree) where max_* are integers
    #   A Monomial will always be by default compact displayed (i.e. 2x and not
    #   2×x).
    #   If the argument isn't of the kinds listed above, an exception will be
    #   raised.
    #   @param options any option
    #   Options can be:
    #   - randomly_plus_signs_ratio: will be effective only in the case
    #     of (RANDOMLY, max_coeff, max_degree) arg. In this case, the
    #     random choice of the sign of the Monomial will respect the given
    #     ratio
    #   @return A instance of Monomial
    def __init__(self, arg, **options):
        CommutativeOperation.__init__(self)

        self._info = [False, False]

        self._neutral = Item(1)

        # 1st CASE: DEFAULT
        if arg == DEFAULT:
            factor1 = Item(1)
            factor2 = Item(('+', settings.default.MONOMIAL_LETTER, 0))
            self._element.append(factor1)
            self._element.append(factor2)

        # 2d CASE: another Monomial
        elif type(arg) == Monomial:
            self._compact_display = arg.compact_display
            self._info = [arg.info[0], arg.info[1]]
            factor1 = arg.factor[0].clone()
            factor2 = Item(arg.factor[1])
            self._element.append(factor1)
            self._element.append(factor2)
            self._exponent = arg.exponent.clone()

        # 3d CASE: tuple (sign, number, integer)
        elif (type(arg) == tuple and len(arg) == 3 and arg[0] in ['+', '-']
              and (is_number(arg[1]) and is_integer(arg[2]))):
            # __
            factor1 = Item((arg[0], arg[1]))
            factor2 = Item(('+', settings.default.MONOMIAL_LETTER, arg[2]))
            self._element.append(factor1)
            self._element.append(factor2)

        # 4th CASE: tuple (number|numeric Exponented, integer)
        elif (type(arg) == tuple and len(arg) == 2
              and (is_number(arg[0]) or (isinstance(arg[0], Exponented)
                                         and arg[0].is_numeric())
              and is_integer(arg[1]))):
            # __
            if is_number(arg[0]):
                if arg[0] >= 0:
                    factor1 = Item(('+', arg[0]))
                elif arg[0] < 0:
                    factor1 = Item(('-', -arg[0]))
            else:
                factor1 = arg[0].clone()

            factor2 = Item(('+', settings.default.MONOMIAL_LETTER, arg[1]))
            self._element.append(factor1)
            self._element.append(factor2)

        # 5th CASE: tuple (RANDOMLY, max_coeff, max_degree)
        elif (type(arg) == tuple and len(arg) == 3 and arg[0] == RANDOMLY
              and is_number(arg[1]) and is_integer(arg[2])):
            # __
            aux_ratio = 0.5
            if 'randomly_plus_signs_ratio' in options \
               and is_number(options['randomly_plus_signs_ratio']):
                # __
                aux_ratio = options['randomly_plus_signs_ratio']
            factor1 = Item((random.choices(['+', '-'],
                                           cum_weights=[aux_ratio, 1])[0],
                            random.randint(1, arg[1])))
            factor2 = Item(('+',
                            settings.default.MONOMIAL_LETTER,
                            random.randint(0, arg[2])))
            self._element.append(factor1)
            self._element.append(factor2)

        # All other unforeseen cases: an exception is raised.
        else:
            raise TypeError('Got: ' + str(type(arg))
                            + ' instead of a DEFAULT|Monomial|'
                            '(sign, coeff, degree)|'
                            '(number|numeric Exponented, integer)|'
                            '(RANDOMLY, max_coeff, max_degree)')

        # We take care to set the exponent to ZERO_POLYNOMIAL_DEGREE
        # in the case the coefficient is null:
        if self.factor[0].is_null():
            self._element[1].set_exponent(Value(ZERO_POLYNOMIAL_DEGREE))

        if (self.element[1].exponent == Value(0)
            and isinstance(self.element[0], Item)):
            # __
            # This is just to mimic the Item it could be, when the exponent
            # of x is zero:
            # Monomial 3×x^0 is like Item 3.
            self._value_inside = Value(self.factor[0].raw_value)

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the sign of the Monomial
    #   @return The sign of the Monomial
    #   This can't be done by CommutativeOperation.get_sign() apparently.
    #   Maybe check exactly why, some day
    def get_sign(self):
        if self.is_null():
            return '+'
        else:
            return self.factor[0].get_sign()

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the numeric coefficient of the Monomial
    #   @return The numeric coefficient of the Monomial
    def get_coeff(self):
        return self.factor[0]

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the value of a Monomial of degree 0
    #   @warning Raises an error if asked on non-degree-0 Monomial
    #   @return value_inside.raw_value
    def get_raw_value(self):
        return self.value_inside.raw_value

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the letter of the Monomial
    #   @return The letter of the Monomial
    def get_first_letter(self):
        return self.factor[1].raw_value

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the degree of the Monomial (i.e. exponent of factor[1])
    #   @return The degree of the Monomial
    def get_degree(self):
        return self.factor[1].exponent.evaluate()

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the Value of the Monomial, just to mimic the case when
    #          it is of degree 0
    #   @return value_inside
    def get_value_inside(self):
        return self._value_inside

    sign = property(get_sign, doc="Monomial's sign")

    coeff = property(get_coeff, doc="Monomial's coefficient")

    raw_value = property(get_raw_value, doc="0-degree-Monomial's value")

    degree = property(get_degree, doc="Monomial's degree")

    letter = property(get_first_letter, doc="Monomial's letter")

    value_inside = property(get_value_inside,
                            doc="0-degree Monomial's Value inside")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the letter of the Monomial
    def set_letter(self, letter):
        self.element[1].set_value_inside(Value(letter))

    # --------------------------------------------------------------------------
    ##
    #   @brief Set the degree of the Monomial
    def set_degree(self, arg):
        if is_natural(arg):
            self.factor[1].set_exponent(arg)
        else:
            raise TypeError('Got: ' + str(type(arg))
                            + ' instead of a natural integer')

    # --------------------------------------------------------------------------
    ##
    #   @brief Set the degree of the Monomial
    def set_coeff(self, arg):
        self._element[0] = Item(arg)

    # --------------------------------------------------------------------------
    ##
    #   @brief Raw display of the Monomial (debugging method)
    #   @param options No option available so far
    #   @return A string containing " << coeff × X ^ degree>> "
    def __repr__(self, **options):
        expo = ""
        if self.exponent != Value(1):
            expo = "^|" + repr(self.exponent) + "| "
        return " <<" + repr(self.coeff)          \
               + "× X ^" + str(self.degree) + ">> " + expo

    # --------------------------------------------------------------------------
    ##
    #   @brief True if it's the null Monomial
    def is_null(self):
        return self.degree == ZERO_POLYNOMIAL_DEGREE or self.coeff.is_null()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if Monomial's degree is 0 or ZERO_POLYNOMIAL_DEGREE
    def is_numeric(self, displ_as=False):
        return self.is_null() or self.degree == 0

    # --------------------------------------------------------------------------
    ##
    #   @brief True if Monomial's coefficient's *sign* is '+'
    #   @todo How to answer to the question if this Monomial is null ?
    def is_positive(self):
        return self.element[0].is_positive()

    # --------------------------------------------------------------------------
    ##
    #   @brief True if Monomial's coefficient's *sign* is '-'
    #   @todo How to answer to the question if this Monomial is null ?
    def is_negative(self):
        return self.element[0].is_negative()


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Polynomial
# @brief A Polynomial is a Sum of Monomials, not necessarily reduced or ordered
class Polynomial(Sum):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg DEFAULT|[Monomial|Polynomial]|Sum(...)|(RANDOMLY, ...)
    #   Possible arguments are:
    #   - DEFAULT:
    #     Will create a default Monomial embedded in a Polynomial
    #   - [Monomial|Polynomial] or Sum(Monomial|Polynomial):
    #     They'll get turned into one Polynomial
    #   - (RANDOMLY,
    #      max_coeff,
    #      max_degree,
    #      [length|tuple(RANDOMLY, max_length)]):
    #     The coefficients and degrees of the Polynomial will be created
    #     randomly. Limits are given by: CONSTANT_TERMS_MAXIMUM_RATIO
    #     and CONSTANT_TERMS_MINIMUM_NUMBER. The length can either be given
    #     or be let generated randomly.
    #   If the argument isn't of the kinds listed above, an exception will be
    #   raised.
    #   @return One instance of Polynomial
    def __init__(self, arg):
        log = settings.dbg_logger.getChild('Polynomial.init')
        # The exponent of a Polynomial should always be 1.
        # Maybe redefine the set_exponent function (inherited from Sum)
        # so that it raises an exception in the case of Polynomials.
        # To get something like (2x+3)³, it is possible to put the 2x+3
        # into a Product whose exponent would be 3.
        # (Or let it still so ? to avoid recursivity problems ?)
        # Anyway it wouldn't be good to set the exponent of a Polynomial to
        # something else than 1, it would cause problems because it is
        # everywhere assumed that the exponent is 1. That makes for example the
        # Sum of two Polynomials just a simple other Polynomial etc.
        CommutativeOperation.__init__(self)

        self._neutral = Item(0)

        self._force_inner_brackets_display = False

        if isinstance(arg, Sum):
            self._force_inner_brackets_display = \
                arg.force_inner_brackets_display

        # 1st CASE: DEFAULT
        if arg == DEFAULT:
            self._element.append(Monomial(DEFAULT))
            self._info.append(False)

        # 2d CASE: [Monomial|Polynomial] or Sum(Monomial|Polynomial)
        elif ((type(arg) == list) and len(arg) >= 1) or isinstance(arg, Sum):
            for i in range(len(arg)):
                log.debug("Copying: " + repr(arg[i]))
                if isinstance(arg[i], Monomial):
                    self._element.append(arg[i].clone())
                    self._info.append(False)
                elif isinstance(arg[i], Polynomial):
                    for j in range(len(arg[i])):
                        self._element.append(arg[i].term[j].clone())
                        self._info.append(arg[i].info[j])
                else:
                    raise TypeError('Got: ' + str(type(arg[i]))
                                    + ' instead of a Monomial|Polynomial')

        # 3d CASE: (RANDOMLY, max_coeff, max_degree, length)
        elif type(arg) == tuple and len(arg) == 4 and arg[0] == RANDOMLY:
            # Let's determine first the desired length
            length = 0

            # ...either randomly
            if type(arg[3]) == tuple and len(arg[3]) == 2                     \
               and is_integer(arg[3][1]) and arg[3][0] == RANDOMLY:
                # __
                if arg[3][1] < 1:
                    raise ValueError('Expected an integer greater or equal '
                                     'to 1, got {} instead'.format(arg[3][1]))
                else:
                    length = random.randint(1, arg[3][1])

            # ...or simply using the provided number
            elif is_integer(arg[3]) and arg[3] >= 1:
                length = arg[3]
            else:
                raise TypeError('Got: ' + str(type(arg))
                                + ' instead of (RANDOMLY, max_coeff, '
                                'max_degree, length|(RANDOMLY, max_length))')

            # Then create the Monomials randomly
            # Note that no null Monomial will be created (not interesting)
            # To avoid having twice the same degree, we will put the last
            # drawing off the list for one turn and put it in again for the
            # (over) next turn. To avoid having to many constant terms, we
            # determine their max number, and once there are enough of them,
            # the 0 degree (= constant terms) won't be put again in the drawing
            # list
            max_nb_constant_terms = max([int(CONSTANT_TERMS_MAXIMUM_RATIO
                                             * length),
                                         CONSTANT_TERMS_MINIMUM_NUMBER])

            current_nb_constant_terms = 0
            degrees_list = [i for i in range(arg[2] + 1)]

            for i in range(length):
                coeff = random.randint(1, arg[1])
                deg = random.choice(degrees_list)
                if deg == 0:
                    current_nb_constant_terms += 1
                    if current_nb_constant_terms == max_nb_constant_terms:
                        degrees_list = [i + 1 for i in range(arg[2])]

                self.append(Monomial((random.choice(['+', '-']), coeff, deg)))

            log.debug("Randomly Created Polynomial is: \n" + repr(self)
                      + "\ninfo: " + str(self.info))

        else:
            raise TypeError('Got: ' + str(type(arg))
                            + ' instead of DEFAULT | [Monomial|Polynomial] |'
                            'Sum(Monomial|Polynomial) | (RANDOMLY, max_coeff, '
                            'max_degree, [length|(RANDOMLY, max_length)])')

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the maximal degree value that can be found in thePolynomial
    #   @return The maximal degree value that can be found in the Polynomial
    def get_max_degree(self):
        d = ZERO_POLYNOMIAL_DEGREE

        for i in range(len(self)):
            if self.term[i].degree > d:
                d = self.term[i].degree

        return d

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the real Polynomial's degree
    #   @return The real Polynomial's degree
    def get_degree(self):
        # Let's glance at the degrees in reverse order
        for i in range(self.get_max_degree(), -1, -1):
            coefficients_sum = 0
            # Let's calculate the sum of coefficients for a given degree
            for j in range(len(self)):
                # We check each Monomial of i-th degree
                if self.term[j].degree == i:
                    if self.term[j].sign == '+':
                        coefficients_sum += self.term[j].coeff
                    else:
                        coefficients_sum -= self.term[j].coeff

            # If this sum isn't null, it means we found the term of highest
            # possible degree that's not null. Its degree is therefore the one
            # of the Polynomial
            if coefficients_sum != 0:
                # As the Polynomial's exponent is assumed to be 1, we don't
                # return i×exponent but just i.
                return i

        return ZERO_POLYNOMIAL_DEGREE

    degree = property(get_degree, doc='Real degree of the Polynomial')

    # --------------------------------------------------------------------------
    ##
    #   @brief Raw display of the Polynomial (debugging method)
    #   @param options No option available so far
    #   @return " [[ term0, ..., termn ]]"
    def __repr__(self, **options):
        resulting_string = " [["
        for i in range(len(self)):
            resulting_string += repr(self.term[i])
            if i < len(self) - 1:
                resulting_string += " + "
        resulting_string += "]] "
        return resulting_string


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Expandable
# @brief Mother class of all expandable objects
class Expandable(Product):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param arg (Exponented, Exponented)|(RANDOMLY, <type>)
    #   (randomly) types details:
    #   - monom0_polyn1 will create this kind of objects: 5(3x-2)
    #   - monom1_polyn1 will create this kind of objects: -5x(2-3x)
    #   - polyn1_polyn1 will create this kind of objects: (5x+1)(3x-2)
    #   - minus_polyn1_polyn1 will create -<polyn1_polyn1>
    #   - sign_exp will create ±(±ax²±bx±c) | ±(±bx±c) | ±(±ax²±c) | ±(±ax²±bx)
    #   @param options reversed|randomly_reversed=<nb>
    #   Options details:
    #   - reversed will change the sums' order. This is useless if the sums
    #     are the same kind of objects (like (2x+3)(3x-7))
    #   - randomly_reversed=0.3 will change the sums' order in a ratio of 0.3
    def __init__(self, arg, **options):
        if not ((isinstance(arg, tuple) and len(arg) == 2)
                or isinstance(arg, Expandable)):
            # __
            raise TypeError('Got: ' + str(type(arg))
                            + ' instead of a tuple of two elements')

        CommutativeOperation.__init__(self)

        max_coeff = 12

        if 'max_coeff' in options and type(options['max_coeff']) == int:
            max_coeff = options['max_coeff']

        self._info = [False, False]

        self._neutral = Item(1)

        self._symbol = '×'
        self.str_openmark = "<X:"
        self.str_closemark = ":X>"

        sum1 = None
        sum2 = None

        # 1st CASE
        # another Expandable to copy
        if isinstance(arg, Expandable):
            self._compact_display = arg.compact_display
            self.reset_element()
            for i in range(len(arg.element)):
                self._element.append(arg.element[i].clone())
            for i in range(len(arg.info)):
                self._info.append(arg.info[i])

        # 2d CASE
        # given Exponenteds
        else:
            if isinstance(arg[0], Exponented) \
               and isinstance(arg[1], Exponented):
                # __
                if not isinstance(arg[0], Sum):
                    sum1 = Sum([arg[0].clone()])
                else:
                    sum1 = arg[0].clone()
                if not isinstance(arg[1], Sum):
                    sum2 = Sum([arg[1].clone()])
                else:
                    sum2 = arg[1].clone()

        # 3d CASE
        # RANDOMLY
            elif arg[0] == RANDOMLY:
                if arg[1] == 'monom0_polyn1':
                    sum1 = Sum(Monomial((RANDOMLY, max_coeff, 0)))

                    if sum1.element[0].factor[0].raw_value == 1:
                        sum1.element[0].factor[0].set_value_inside(Value(
                            random.randint(2, max_coeff)))

                    sum2 = Polynomial((RANDOMLY, max_coeff, 1, 2))

                elif arg[1] == 'monom1_polyn1':
                    sum1 = Sum(Monomial((RANDOMLY, max_coeff, 1)))
                    sum1.element[0].set_degree(1)
                    sum2 = Polynomial((RANDOMLY, max_coeff, 1, 2))

                elif arg[1] == 'polyn1_polyn1':
                    sum1 = Polynomial((RANDOMLY, max_coeff, 1, 2))
                    sum2 = Polynomial((RANDOMLY, max_coeff, 1, 2))

                elif arg[1] == 'minus_polyn1_polyn1':
                    sum1 = Sum(Monomial(('-', 1, 0)))
                    sum2 = Sum(Expandable((RANDOMLY, 'polyn1_polyn1')))

                elif arg[1] == 'sign_exp':
                    sum1 = Sum(Monomial((random.choices(['+', '-'],
                                                        cum_weights=[0.25,
                                                                     1])[0],
                                         1, 0)))

                    if random.choice([True, False]):
                        sum2 = Sum(Polynomial((RANDOMLY, 15, 2, 3)))
                    else:
                        sum2 = Sum(Polynomial((RANDOMLY, 15, 2, 2)))

                else:
                    raise TypeError('Got: ' + str(type(arg[1]))
                                    + ' instead of a monom0_polyn1|'
                                    'monom1_polyn1|polyn1_polyn1'
                                    '|minus_polyn1_polyn1|sign_exp')

            else:
                raise TypeError('Got: ' + str(type(arg))
                                + ' instead of (Exponented, Exponented)|'
                                '(RANDOMLY, <type>)')

            if ('reversed' in options
                or ('randomly_reversed' in options
                    and is_number(options['randomly_reversed'])
                    and
                    random.random() <= options['randomly_reversed'])):
                # __
                self._element.append(sum2)
                self._element.append(sum1)
            else:
                self._element.append(sum1)
                self._element.append(sum2)

            # In the case of the Expandable +(...), force the displaying
            # of the brackets
            if len(self.factor[0]) == 1 \
               and self.factor[0].element[0].is_displ_as_a_single_1():
                # __
                self.factor[1].set_force_inner_brackets_display(True)

    # --------------------------------------------------------------------------
    ##
    #   @brief The expanded object, like 2×(x+3) would return 2×x + 2×3
    def expand(self, **options):
        # First: imbricated Sums are managed recursively
        if len(self.factor[0]) == 1 \
           and isinstance(self.factor[0].term[0], Sum):
            # __
            copy = Expandable(self)
            copy.set_element(0, copy.factor[0].term[0])
            return copy.expand()

        if len(self.factor[1]) == 1 \
           and isinstance(self.factor[1].term[0], Sum):
            # __
            copy = Expandable(self)
            copy.set_element(1, copy.factor[1].term[0])
            return copy.expand()

        # And here we go:
        terms_list = list()

        for i in range(len(self.factor[0])):
            for j in range(len(self.factor[1])):
                temp = Product([self.factor[0].term[i],
                                self.factor[1].term[j]])
                temp.set_compact_display(False)
                terms_list.append(temp)

        if (len(self.factor[0]) == 1
            and (self.factor[0].term[0].is_displ_as_a_single_minus_1()
                 or self.factor[0].term[0].is_displ_as_a_single_1())):
            # __
            for i in range(len(terms_list)):
                terms_list[i] = terms_list[i].reduce_()

        details_level = options.get('details_level', 'maximum')

        if details_level == 'maximum':
            return Sum(terms_list)
        else:  # 'medium' or 'none' produce the same result, so far
            return Sum(terms_list).expand_and_reduce_next_step(**options)

    # --------------------------------------------------------------------------
    ##
    #   @brief The expanded & reduced object, like 2×(x+3) would return 2x + 6
    #   Take care that the resulting Sum might not be reduced itself.
    #   For instance, (3 + x)(2x - 5) would return 6x - 15 + 2x² - 5x
    #   The rest of the calculation has to be done with the Sum's reduction
    #   method
    #   @obsolete ?
    def expand_and_reduce_(self):
        expanded_objct = self.expand()

        terms_list = list()

        for term in expanded_objct:
            terms_list.append(term.reduce_())

        return Sum(terms_list)

    def calculate_next_step(self, **options):
        if not self.is_numeric():
            return self.expand_and_reduce_next_step(**options)
        numeric_product = Product(1)
        numeric_product._compact_display = self.compact_display
        numeric_product.reset_element()
        for i in range(len(self.element)):
            numeric_product._element.append(self.element[i].clone())
        for i in range(len(self.info)):
            numeric_product._info.append(self.info[i])
        return numeric_product.calculate_next_step(**options)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the expanded object as a Sum
    def expand_and_reduce_next_step(self, **options):
        if self.is_numeric():
            return self.calculate_next_step(**options)
        copy = Expandable(self)

        a_factor_at_least_has_been_modified = False

        # to expand the ± signs first in the case of a Sum as second factor
        if (len(self.factor[0]) == 1
            and (self.factor[0].term[0].is_displ_as_a_single_1()
                 or self.factor[0].term[0].is_displ_as_a_single_minus_1())):
                # __
                if (isinstance(self.factor[1], Sum)
                    and len(self.factor[1]) > 1
                    and self.factor[1].exponent.is_displ_as_a_single_1()):
                    # __
                    return self.expand(**options)

        # check if any of the factors needs to be reduced
        for i in range(len(copy)):
            test = copy.factor[i].expand_and_reduce_next_step(**options)
            if test is not None:
                copy.set_element(i, test)
                a_factor_at_least_has_been_modified = True

        if a_factor_at_least_has_been_modified:
            return copy

        # no factor of the Expandable needs to be reduced
        else:
            return self.expand(**options)

    # --------------------------------------------------------------------------
    ##
    #   @brief True
    #   @return True
    def is_expandable(self):
        return True


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class BinomialIdentity
# @brief These objects are expanded using: (a+b)² = a² + 2ab + b², (a-b)² =
# a² -2ab + b² and (a+b)(a-b) = a² - b²
# This object is a Product of two Sums but won't be displayed as is in the
# case of (a+b)² and (a-b)².
# For instance, (3x-2)(3x-2) will be displayed (3x-2)².
class BinomialIdentity(Expandable):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param arg (Exponented, Exponented)|(RANDOMLY, <type>)
    #   Types details:
    #   - sum_square: matches (a+b)²
    #   - difference_square: matches (a-b)²
    #   - squares_difference: matches (a+b)(a-b) (name comes from a²-b²)
    #   - any: matches any of (a+b)², (a-b)², (-a+b)², (-a-b)², (a+b)(a-b)...
    #   - numeric_*: matches a numeric one...
    #   @param options squares_difference
    #   Options details:
    #   - in the case of arg being (Exponented, Exponented),
    #     squares_difference let produce a (a+b)(a-b) from the given
    #     Exponenteds instead of a default (a+b)²
    #   @todo fix the square_difference option (see source code)
    def __init__(self, arg, **options):
        if not (type(arg) == tuple and len(arg) == 2) \
           and not isinstance(arg, BinomialIdentity):
            # __
            raise TypeError('Got: ' + str(type(arg))
                            + ' instead of a  tuple of two elements or a '
                            'BinomialIdentity')

        # The exponent (like 3 in ((3-x)(4+5x))³)
        CommutativeOperation.__init__(self)

        self._info = [False, False]

        self._neutral = Item(1)

        self._symbol = '×'
        self.str_openmark = "<B: "
        self.str_closemark = ":B>"

        # This property is to set to help the into_str and expand functions
        # It has to be either 'sum_square' which refers to (a+b)² objects,
        # or 'difference_square', which refers to (a-b)² objects,
        # or 'squares_difference' which refers to (a+b)(a-b) objects
        self._kind = ""

        # 1st CASE
        # Another BinomialIdentity to copy
        if isinstance(arg, BinomialIdentity):
            for i in range(len(arg.element)):
                self._element.append(arg.element[i].clone())
            self._compact_display = arg.compact_display
            for i in range(len(arg.info)):
                self._info.append(arg.info[i])
            self._exponent = arg.exponent.clone()
            self._kind = arg.kind
            self._a = arg.a.clone()
            self._b = arg.b.clone()

        # 2d CASE
        # given Exponented
        elif isinstance(arg[0], Exponented) and isinstance(arg[1], Exponented):
            a = arg[0].clone()
            b = arg[1].clone()

            self._a = a
            self._b = b

            self._element.append(Sum([a, b]))

            if b.get_sign() == '+':
                self._kind = 'sum_square'
            else:
                self._kind = 'difference_square'

            if 'squares_difference' in options:
                # fix it: b will be reduced every time ! it is not
                # the desired effect !!
                b = Product([Item(-1), b]).reduce_()
                self._kind = 'squares_difference'

            self._element.append(Sum([a, b]))

        # 3d CASE
        # RANDOMLY
        elif arg[0] == RANDOMLY:

            if arg[1] in ['numeric_sum_square',
                          'numeric_difference_square',
                          'numeric_squares_difference']:
                # __
                a_list = [20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400,
                          500, 600, 700, 800, 1000]

                b_list = [1, 2, 3]

                a_choice = random.choice(a_list)

                if a_choice >= 200:
                    b_list = [1, 2]

                a = Monomial(('+',
                              a_choice,
                              0))

                b_choice = random.choice(b_list)

                b = Monomial(('+',
                              b_choice,
                              0))

            else:
                degrees_list = [0, 1]
                coeff_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                random.shuffle(degrees_list)
                random.shuffle(coeff_list)
                a = Monomial(('+', coeff_list.pop(), degrees_list.pop()))
                b = Monomial(('+', coeff_list.pop(), degrees_list.pop()))

            self._a = a
            self._b = b

            if arg[1] in ['sum_square', 'numeric_sum_square']:
                self._element.append(Sum([a, b]))
                self._element.append(Sum([a, b]))
                self._kind = 'sum_square'

            elif arg[1] in ['difference_square', 'numeric_difference_square']:
                b.set_sign('-')
                self._element.append(Sum([a, b]))
                self._element.append(Sum([a, b]))
                self._kind = 'difference_square'

            elif arg[1] in ['squares_difference',
                            'numeric_squares_difference']:
                # __
                sums_list = list()
                sums_list.append(Sum([a, b]))
                minus_b = Monomial(b)
                minus_b.set_sign('-')
                sums_list.append(Sum([a, minus_b]))
                random.shuffle(sums_list)
                self._element.append(sums_list.pop())
                self._element.append(sums_list.pop())
                self._kind = 'squares_difference'

            elif arg[1] == 'any':
                if random.choice([True, False]):
                    # doesn't make sense to have (-3 - 4x)² as a BI,
                    # it's uselessly complicated for the pupils
                    a.set_sign('+')
                    b.set_sign(random.choice(['+', '-']))
                    self._a = a
                    self._b = b
                    self._element.append(Sum([a, b]))
                    self._element.append(Sum([a, b]))
                    if b.get_sign() == '+':
                        self._kind = 'sum_square'
                    else:
                        self._kind = 'difference_square'

                else:
                    # doesn't make sense to have (-3 - 4x)² as a BI,
                    # it's uselessly complicated for the pupils
                    a.set_sign('+')
                    b.set_sign(random.choice(['+', '-']))
                    self._a = a
                    self._b = b
                    self._element.append(Sum([a, b]))
                    minus_b = Monomial(b)
                    minus_b.set_sign(sign_of_product(['-', b.sign]))
                    self._element.append(Sum([a, minus_b]))
                    self._kind = 'squares_difference'

            else:
                raise TypeError('Got: ' + str(arg[1])
                                + ' instead of sum_square|difference_square|'
                                'squares_difference|'
                                'numeric_{sum_square|difference_square|'
                                'squares_difference}|any')
        else:
            raise TypeError('Got: ' + str(type(arg)) + ' instead of '
                            '(Exponented, Exponented)|(RANDOMLY, <type>)')

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the 'a' term of the BinomialIdentity
    #   @return the content of the 'a' term
    def get_a(self):
        return self._a

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the 'b' term of the BinomialIdentity
    #   @return the content of the 'b' term
    def get_b(self):
        return self._b

    # --------------------------------------------------------------------------
    ##
    #   @brief Gets the kind of BinomialIdentity it is
    #   @return 'sum_square'|'difference_square'|'squares_difference'
    def get_kind(self):
        return self._kind

    a = property(get_a,
                 doc="Gets the 'a' term of the BinomialIdentity")

    b = property(get_b,
                 doc="Gets the 'b' term of the BinomialIdentity")

    kind = property(get_kind,
                    doc="kind of BinomialIdentity it, "
                        "e.g. 'sum_square'|'difference_square'|"
                        "'squares_difference'")

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        global expression_begins

        if self.kind == 'squares_difference':
            return Product(self.factor).into_str(**options)

        else:
            squared_sum = Sum([self.a, self.b])
            squared_sum.set_exponent(2)
            return squared_sum.into_str(**options)

    # --------------------------------------------------------------------------
    ##
    #   @brief The expanded object, like (2x+3)² would return (2x)²+2×2x×3+3²
    def expand(self):

        log = settings.dbg_logger.getChild(
            'BinomialIdentity.expand')
        log.debug("Entering, self.kind = " + str(self.kind))

        if self.kind == 'sum_square':
            square_a = Product(self.a)
            square_a.set_exponent(2)
            double_product = Product([2, self.a, self.b])
            square_b = Product(self.b)
            square_b.set_exponent(2)
            return Sum([square_a,
                        double_product,
                        square_b])

        elif self.kind == 'difference_square':
            square_a = Product(self.a)
            square_a.set_exponent(2)
            b = self.b
            b.set_sign('+')
            double_product = Product([-2, self.a, b])
            square_b = Product(b)
            square_b.set_exponent(2)
            return Sum([square_a,
                        double_product,
                        square_b])

        elif self.kind == 'squares_difference':
            square_a = Product(self.a)
            square_a.set_exponent(2)
            b = self.b
            b.set_sign('+')
            square_b = Product(b)
            square_b.set_exponent(2)
            square_b = Product([Item(-1), square_b])
            return Sum([square_a,
                        square_b])

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the next step of reduction of the BinomialIdentity
    #   @return Exponented
    def expand_and_reduce_next_step(self, **options):
        return self.expand()
