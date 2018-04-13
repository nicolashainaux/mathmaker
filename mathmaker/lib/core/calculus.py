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
from math import gcd
from string import ascii_uppercase as alphabet
from abc import ABCMeta, abstractmethod

from mathmakerlib import required
from mathmakerlib.calculus import is_integer, is_number

from mathmaker import settings
from mathmaker.lib import shared
from mathmaker.lib.tools.maths import sign_of_product
from mathmaker.lib.constants import RANDOMLY
from mathmaker.lib.core.utils import gather_literals
from mathmaker.lib.core.base import Printable
from mathmaker.lib.core.root_calculus import (Exponented, Value, Calculable,
                                              Substitutable)
from mathmaker.lib.core.base_calculus import (Monomial, Sum, Item, Polynomial,
                                              Fraction, Expandable, Product,
                                              Quotient, Function, SquareRoot,
                                              AngleItem, CommutativeOperation)
from mathmaker.lib.constants.latex import MARKUP


MAX_VALUE = 20

# The following tables come from the fractions' calculations sheets...
# which is a shame: this code must be factorized
FRACTIONS_SUMS_TABLE = [([1, 2], 15),
                        ([1, 3], 15),
                        ([1, 4], 15),
                        ([1, 5], 15),
                        ([1, 6], 15),
                        ([1, 7], 15),
                        ([2, 3], 17),
                        ([2, 5], 10),
                        ([2, 7], 7),
                        ([3, 4], 9),
                        ([3, 5], 7),
                        ([3, 7], 5),
                        ([4, 5], 5),
                        ([4, 7], 3),
                        ([5, 6], 4),
                        ([5, 7], 4),
                        ([6, 7], 3)]

FRACTIONS_SUMS_SCALE_TABLE = [0.02,  # (1, 2)
                              0.02,
                              0.02,
                              0.01,
                              0.005,
                              0.005,  # (1, 7)
                              0.21,  # (2, 3)
                              0.14,  # (2, 5)
                              0.02,  # (2, 7)
                              0.21,  # (3, 4)
                              0.14,  # (3, 5)
                              0.01,  # (3, 7)
                              0.16,  # (4, 5)
                              0.01,  # (4, 7)
                              0.01,  # (5, 6)
                              0.005,  # (5, 7)
                              0.005]  # (6, 7)

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @package core.calculus


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class ComposedCalculable
# @brief Abstract mother class of objects composed of Calculable=Calculable=...
class ComposedCalculable(Printable, metaclass=ABCMeta):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @warning Must be redefined
    @abstractmethod
    def __init__(self):
        pass


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Expression
# @brief These are object of the kind: Name = Exponented
class Expression(ComposedCalculable):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param integer_or_letter A string or an integer
    #   @param objct The Exponented that will be at the right hand side
    #   @return One instance of Expression
    def __init__(self, integer_or_letter, objct):
        # just check if the given arguments are right
        if not (type(integer_or_letter) is str
                or (is_number(integer_or_letter)
                    and is_integer(integer_or_letter))):
            # __
            raise TypeError('Got: ' + str(type(integer_or_letter))
                            + ' instead of a str or integer number')

        if not (isinstance(objct, Exponented) or objct is None):
            raise TypeError('Got: ' + str(type(integer_or_letter))
                            + ' instead of Exponented|None')

        self._name = integer_or_letter
        self._right_hand_side = objct.clone()

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the right hand side of the Expression e.g.
    #           the Expression in itself
    def get_right_hand_side(self):
        return self._right_hand_side

    right_hand_side = property(get_right_hand_side,
                               doc="Right hand side of the object")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the right hand side of the Expression
    def set_right_hand_side(self, arg):
        if not (isinstance(arg, Exponented)):
            raise TypeError('Got: ' + str(type(arg)) + ' instead of '
                            'Exponented')

        self._right_hand_side = arg.clone()

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        global expression_begins
        required.package['amsmath'] = True
        # Expression objects displaying
        if is_number(self.name) and is_integer(self.name):
            i = self.name
            if i < len(alphabet):
                final_name = MARKUP['open_text_in_maths'] \
                    + alphabet[i] \
                    + MARKUP['close_text_in_maths']
            else:
                nb_letters = len(alphabet)
                final_name = MARKUP['open_text_in_maths'] \
                    + alphabet[i - nb_letters * int(i / nb_letters)] \
                    + MARKUP['close_text_in_maths'] \
                    + MARKUP['opening_subscript'] \
                    + MARKUP['open_text_in_maths'] \
                    + str(int(i / nb_letters)) \
                    + MARKUP['close_text_in_maths'] \
                    + MARKUP['closing_subscript']

        elif type(self.name) is str:
            final_name = MARKUP['open_text_in_maths'] \
                + self.name \
                + MARKUP['close_text_in_maths']

        expression_begins = True

        options.update({'force_expression_begins': True})

        return final_name \
            + MARKUP['equal'] \
            + self.right_hand_side.into_str(**options)

    # --------------------------------------------------------------------------
    ##
    #   @brief Create a string of the expression's exp. & red. in the given ML
    #   @param options Any options
    #   @return The formated string of the expression's resolution
    def auto_expansion_and_reduction(self, **options):
        global expression_begins
        aux_expr = self.right_hand_side
        result = ""

        # Complete expansion & reduction of any expression:o)
        while aux_expr is not None:
            result += MARKUP['opening_math_style2'] \
                + Expression(self.name,
                             aux_expr).into_str() \
                + MARKUP['closing_math_style2'] \
                + MARKUP['newline'] + "\n"
            aux_expr = aux_expr.expand_and_reduce_next_step(**options)

        return result


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Equality
# @brief These are object of the kind: Exponented = Exponented [= ...]
class Equality(ComposedCalculable, Substitutable):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param objcts is a [Exponented] of 2 elements at least
    #   @option equal_signs Contains a list of equal/not equal signs. Must be
    #   @option             as long as len(objcts) - 1. The signs are "=" or
    #                       "neq"
    #   @return One instance of Equality
    def __init__(self, objcts, subst_dict=None, **options):
        # just check if the given arguments are right
        if not (isinstance(objcts, list)):
            raise TypeError('Got: ' + str(type(objcts)) + ' instead of '
                            'a list (of two Exponenteds at least)')
        if not len(objcts) >= 2:
            raise TypeError('Got: ' + str(type(objcts)) + ' instead of '
                            'a list of TWO Exponenteds AT LEAST')

        for i in range(len(objcts)):
            if not isinstance(objcts[i], Exponented):
                raise TypeError('Got: ' + str(type(objcts[i])) + ' instead of '
                                'an Exponented')

        if 'equal_signs' in options:
            if not type(options['equal_signs']) == list:
                raise TypeError('Got: ' + str(type(options['equal_signs']))
                                + ' instead of a list')
            if not len(options['equal_signs']) == len(objcts) - 1:
                raise TypeError('Got a list of: '
                                + str(len(options['equal_signs']))
                                + ' elements instead of '
                                + str(len(objcts) - 1))

            for i in range(len(options['equal_signs'])):
                if not (options['equal_signs'][i] == '='
                        or options['equal_signs'][i] == 'neq'):
                    # __
                    raise TypeError(options['equal_signs'][i]
                                    + ' should be \'=\' or \'neq\'')

        self._elements = []
        self._equal_signs = []

        for i in range(len(objcts)):
            self._elements.append(objcts[i].clone())

            if 'equal_signs' in options:

                if i < len(options['equal_signs']):
                    sign_to_add = None

                    if options['equal_signs'][i] == '=':
                        sign_to_add = 'equal'
                    else:
                        sign_to_add = 'not_equal'

                    self._equal_signs.append(sign_to_add)

            else:
                self._equal_signs.append('equal')

        Substitutable.__init__(self, subst_dict=subst_dict)

    @property
    def content(self):
        """The content to be substituted (list containing literal objects)."""
        return self._elements

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the elements of the Equality
    def get_elements(self):
        return self._elements

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the equal signs series of the Equality
    def get_equal_signs(self):
        return self._equal_signs

    elements = property(get_elements, doc="Elements of the object")

    equal_signs = property(get_equal_signs, doc="Equal signs of the object")

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        global expression_begins
        # Equality objects displaying

        expression_begins = True

        result = ''

        if ('force_expression_markers' in options
            and options['force_expression_markers']):
            # __
            result += MARKUP['opening_math_style2']

        options.update({'force_expression_begins': True})

        result += self.elements[0].into_str(**options)

        for i in range(len(self.elements) - 1):
            options.update({'force_expression_begins': True})
            result += MARKUP[self.equal_signs[i]] \
                + self.elements[i + 1].into_str(**options)

        if ('force_expression_markers' in options
            and options['force_expression_markers']):
            # __
            result += MARKUP['closing_math_style2']

        return result

    def __getitem__(self, i):
        """Make Equality indexable."""
        return self._elements[i]

    def __setitem__(self, i, data):
        """Make Equality indexable."""
        if not isinstance(data, Exponented):
            raise TypeError('data should be a Exponented')
        self._elements[i] = data.clone()

    def __len__(self):
        """Return the number of elements of the Equality."""
        return len(self._elements)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Equation
# @brief One degree one variable. Sum=Sum. Name, number, left/right hand side.
class Equation(ComposedCalculable):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg Equation|(Exponented, Exponented)|(RANDOMLY, ...)|Equality
    #   @return One instance of Equation
    def __init__(self, arg, **options):
        self._name = settings.default.EQUATION_NAME
        self._number = ''
        self._left_hand_side = None
        self._right_hand_side = None
        self._variable_letter = settings.default.MONOMIAL_LETTER

        # First determine name and number of the equation
        if 'name' in options and type(options['name']) is str:
            self._name = options['name']

        if 'number' in options and is_integer(options['number']):
            self._number = options['number']

        # Then the letter
        if 'variable_letter_name' in options \
           and type(options['variable_letter_name']) is str:
            # __
            self._variable_letter = options['variable_letter_name'][0]

        # Then determine its left & right hand sides

        if isinstance(arg, Equality):
            if not len(arg) == 2:
                raise RuntimeError('Impossible to turn into an Equation an '
                                   'Equality having not exactly 2 members')
            literals_list = list(set(gather_literals(arg[0])
                                     + gather_literals(arg[1])))
            if not len(literals_list) == 1:
                raise RuntimeError('create an Equation from an Equality '
                                   'containing more than ONE unknown literal. '
                                   'This one contains '
                                   + str(len(literals_list))
                                   + ' literals which are '
                                   + str([repr(elt) for elt in literals_list]))

            if (not isinstance(literals_list[0], Value)
                and not literals_list[0].is_literal()):
                # __
                raise ValueError('Expected a literal Value, instead of '
                                 + repr(literals_list[0]))

            self.__init__((arg[0], arg[1]),
                          variable_letter_name=literals_list[0]
                          .get_first_letter(),
                          **options)

        # Different cases of tuples
        elif type(arg) == tuple and len(arg) == 2:

            # 1st CASE
            # Given objects
            if (isinstance(arg[0], Exponented)
                and isinstance(arg[1], Exponented)):
                # __
                if isinstance(arg[0], Sum):
                    # TO FIX ?
                    # this could be secured by checking the given Sum
                    # is not containing only one term which would be also
                    # a Sum
                    self._left_hand_side = arg[0]
                else:
                    self._left_hand_side = Sum(arg[0])

                if isinstance(arg[1], Sum):
                    # TO FIX ?
                    # this could be secured by checking the given Sum
                    # is not containing only one term which would be also
                    # a Sum
                    self._right_hand_side = arg[1]
                else:
                    self._right_hand_side = Sum(arg[1])

            # 2d CASE
            # RANDOMLY !
            elif arg[0] == RANDOMLY:
                if arg[1] == 'basic_addition':
                    self._left_hand_side = Polynomial([
                        Monomial(('+', 1, 1)),
                        Monomial((random.choice(['+', '-']),
                                  random.randint(1, MAX_VALUE),
                                  0))])

                    self._right_hand_side = Sum(
                        Item((random.choice(['+', '-']),
                              random.randint(1, MAX_VALUE))))

                    self._left_hand_side.term[0]\
                        .set_letter(self.variable_letter)

                elif arg[1] == 'basic_addition_r':
                    self._right_hand_side = Polynomial([
                        Monomial(('+', 1, 1)),
                        Monomial((random.choice(['+', '-']),
                                  random.randint(1, MAX_VALUE),
                                  0))])

                    self._left_hand_side = Sum(
                        Item((random.choice(['+', '-']),
                              random.randint(1, MAX_VALUE))))

                    self._right_hand_side.term[0]\
                        .set_letter(self.variable_letter)

                elif arg[1] == 'any_basic_addition':
                    m1 = Monomial((random.choices(['+', '-'],
                                                  cum_weights=[0.8, 1])[0],
                                   1, 1))
                    m1.set_letter(self.variable_letter)
                    m2 = Monomial((random.choice(['+', '-']),
                                   random.randint(1, MAX_VALUE),
                                   0))

                    m3 = Monomial((random.choice(['+', '-']),
                                   random.randint(1, MAX_VALUE),
                                   0))

                    if random.choice([True, False]):
                        cst_list = [m2, m3]
                    else:
                        cst_list = [m3, m2]

                    drawn_to_be_with_x = cst_list.pop()

                    if random.choice([True, False]):
                        polyn_list = [m1, drawn_to_be_with_x]
                    else:
                        polyn_list = [drawn_to_be_with_x, m1]

                    polyn = Polynomial([polyn_list.pop(),
                                        polyn_list.pop()])

                    if random.choice([True, False]):
                        sides = [polyn, Sum(cst_list.pop())]
                    else:
                        sides = [Sum(cst_list.pop()), polyn]

                    self._left_hand_side = sides.pop()
                    self._right_hand_side = sides.pop()

                elif arg[1] == 'basic_multiplication':
                    self._left_hand_side = Sum(
                        Monomial((random.choices(['+', '-'],
                                                 cum_weights=[0.75, 1])[0],
                                  random.randint(2, MAX_VALUE),
                                  1)))

                    self._right_hand_side = Sum(
                        Item((random.choices(['+', '-'],
                                             cum_weights=[0.75, 1])[0],
                              random.randint(1, MAX_VALUE),
                              1)))

                    self._left_hand_side.term[0]\
                        .set_letter(self.variable_letter)

                elif arg[1] == 'basic_multiplication_r':
                    self._right_hand_side = Sum(
                        Monomial((random.choices(['+', '-'],
                                                 cum_weights=[0.75, 1])[0],
                                  random.randint(2, MAX_VALUE),
                                  1)))

                    self._left_hand_side = Sum(
                        Item((random.choices(['+', '-'],
                                             cum_weights=[0.75, 1])[0],
                              random.randint(1, MAX_VALUE),
                              1)))

                    self._right_hand_side.term[0]\
                        .set_letter(self.variable_letter)

                elif arg[1] == 'any_basic_multiplication':
                    m1 = Monomial((random.choices(['+', '-'],
                                                  cum_weights=[0.75, 1])[0],
                                   random.randint(2, MAX_VALUE),
                                   1))
                    m1.set_letter(self.variable_letter)

                    m2 = Item((random.choices(['+', '-'],
                                              cum_weights=[0.75, 1])[0],
                               random.randint(1, MAX_VALUE),
                               1))

                    if random.choice([True, False]):
                        items_list = [Sum(m1), Sum(m2)]
                    else:
                        items_list = [Sum(m2), Sum(m1)]

                    self._left_hand_side = items_list.pop()
                    self._right_hand_side = items_list.pop()

                elif arg[1] == 'any_basic':  # code duplication... done quickly
                    if random.choice([True, False]):
                        m1 = Monomial((random.choices(['+', '-'],
                                                      cum_weights=[0.75,
                                                                   1])[0],
                                       random.randint(2, MAX_VALUE),
                                       1))
                        m1.set_letter(self.variable_letter)

                        m2 = Item((random.choices(['+', '-'],
                                                  cum_weights=[0.75, 1])[0],
                                   random.randint(1, MAX_VALUE),
                                   1))
                        if random.choice([True, False]):
                            items_list = [Sum(m1), Sum(m2)]
                        else:
                            items_list = [Sum(m2), Sum(m1)]
                        self._left_hand_side = items_list.pop()
                        self._right_hand_side = items_list.pop()
                    else:
                        cst_list = list()
                        m1 = Monomial((random.choices(['+', '-'],
                                                      cum_weights=[0.8, 1])[0],
                                       1,
                                       1))
                        m1.set_letter(self.variable_letter)
                        m2 = Monomial((random.choice(['+', '-']),
                                       random.randint(1, MAX_VALUE),
                                       0))
                        m3 = Monomial((random.choice(['+', '-']),
                                       random.randint(1, MAX_VALUE),
                                       0))

                        if random.choice([True, False]):
                            cst_list = [m2, m3]
                        else:
                            cst_list = [m3, m2]

                        drawn_to_be_with_x = cst_list.pop()

                        if random.choice([True, False]):
                            polyn_list = [m1, drawn_to_be_with_x]
                        else:
                            polyn_list = [drawn_to_be_with_x, m1]

                        polyn = Polynomial([polyn_list.pop(),
                                            polyn_list.pop()])

                        if random.choice([True, False]):
                            sides = [polyn, Sum(cst_list.pop())]
                        else:
                            sides = [Sum(cst_list.pop()), polyn]

                        self._left_hand_side = sides.pop()
                        self._right_hand_side = sides.pop()

                elif (arg[1] in ['classic', 'classic_r', 'classic_x_twice',
                      'any_classic']):
                    # __
                    # Let's build
                    # classic: ax + b = d | b + ax = d
                    # classic_r: d = ax + b | d = b + ax
                    # classic_x_twice: ax + b = cx + d | ax + b = cx |
                    #                   cx = ax + b | b + ax = cx + d etc.
                    ax = Monomial((random.choices(['+', '-'],
                                                  cum_weights=[0.65, 1])[0],
                                   random.randint(1, MAX_VALUE),
                                   1))
                    ax.set_letter(self.variable_letter)

                    b = Monomial((random.choice(['+', '-']),
                                  random.randint(1, MAX_VALUE),
                                  0))
                    cx = Monomial((random.choices(['+', '-'],
                                                  cum_weights=[0.65, 1])[0],
                                   random.randint(1, MAX_VALUE),
                                   1))
                    cx.set_letter(self.variable_letter)

                    d = Monomial((random.choice(['+', '-']),
                                  random.randint(1, MAX_VALUE),
                                  0))

                    if random.choice([True, False]):
                        polyn1 = Polynomial([ax, b])
                    else:
                        polyn1 = Polynomial([b, ax])

                    if arg[1] == 'classic' or arg[1] == 'classic_r':
                        polyn2 = Polynomial([d])
                    elif arg[1] == 'classic_x_twice':
                        if random.random() > 0.3:
                            if random.choice([True, False]):
                                polyn2 = Polynomial([cx, d])
                            else:
                                polyn2 = Polynomial([d, cx])
                        else:
                            polyn2 = Polynomial([cx])

                    elif arg[1] == 'any_classic':
                        random_nb = random.random()
                        if random_nb < 0.4:
                            if random.choice([True, False]):
                                polyn2 = Polynomial([cx, d])
                            else:
                                polyn2 = Polynomial([d, cx])
                        elif random_nb < 0.7:
                            polyn2 = Polynomial([d])
                        else:
                            polyn2 = Polynomial([cx])

                    if arg[1] == 'classic':
                        self._left_hand_side = polyn1
                        self._right_hand_side = polyn2
                    elif arg[1] == 'classic_r':
                        self._left_hand_side = polyn2
                        self._right_hand_side = polyn1
                    elif arg[1] in ['classic_x_twice', 'any_classic']:
                        if random.choice([True, False]):
                            box = [polyn1, polyn2]
                        else:
                            box = [polyn2, polyn1]
                        self._left_hand_side = box.pop()
                        self._right_hand_side = box.pop()

                elif arg[1] == 'classic_with_fractions':
                    # the following code is copied from Calculation.py
                    # -> must be factorized
                    randomly_position = \
                        random.choices([n for n in range(17)],
                                       weights=FRACTIONS_SUMS_SCALE_TABLE)[0]

                    chosen_seed_and_generator = FRACTIONS_SUMS_TABLE[
                        randomly_position]

                    seed = random.randint(2, chosen_seed_and_generator[1])

                    # The following test is only intended to avoid having
                    # "high" results too often. We just check if the common
                    # denominator will be higher than 75 (arbitrary)
                    # and if yes, we redetermine
                    # it once. We don't do it twice since we don't want to
                    # totally
                    # forbid high denominators.
                    if seed * chosen_seed_and_generator[0][0] \
                            * chosen_seed_and_generator[0][1] >= 75:
                        # __
                        seed = random.randint(2, chosen_seed_and_generator[1])

                    lil_box = [0, 1]
                    gen1 = chosen_seed_and_generator[0][lil_box.pop()]
                    gen2 = chosen_seed_and_generator[0][lil_box.pop()]

                    den1 = Item(gen1 * seed)
                    den2 = Item(gen2 * seed)

                    temp1 = random.randint(1, 20)
                    temp2 = random.randint(1, 20)

                    num1 = Item(temp1 // gcd(temp1, gen1 * seed))
                    num2 = Item(temp2 // gcd(temp2, gen2 * seed))

                    f1 = Fraction((random.choices(['+', '-'],
                                                  cum_weights=[0.7, 1])[0],
                                  num1,
                                  den1))
                    f2 = Fraction((random.choices(['+', '-'],
                                                  cum_weights=[0.7, 1])[0],
                                  num2,
                                  den2))

                    # END OF COPIED CODE --------------------------------------

                    box = list()
                    ax = Monomial((Fraction((
                        random.choices(['+', '-'], cum_weights=[0.7, 1])[0],
                        Item(random.randint(1, 10)),
                        Item(random.randint(2, 10))))
                        .simplified(), 1))
                    ax.set_letter(self.variable_letter)

                    b = Monomial((f1.simplified(), 0))
                    d = Monomial((f2.simplified(), 0))

                    if random.choice([True, False]):
                        box = [ax, b]
                    else:
                        box = [b, ax]
                    self._left_hand_side = Polynomial(box)
                    self._right_hand_side = Sum([d])

                elif arg[1] in ['any_simple_expandable',
                                'any_double_expandable']:
                    # __
                    # SIMPLE:
                    # a monom0_polyn1 or a ±(...) on one side
                    # + one Monomial with the monom0_polyn1
                    # and one or two Monomials on the other side
                    # DOUBLE:
                    # The same plus another expandable.

                    # Creation of the expandables, to begin with...
                    if random.random() <= 0.8:
                        aux_expd_1 = Expandable((RANDOMLY,
                                                 'monom0_polyn1'),
                                                max_coeff=9)
                        expd_kind = 'monom0_polyn1'

                    else:
                        sign = random.choice(['+', '-'])
                        aux_expd_1 = Expandable((
                            Monomial((sign, 1, 0)),
                            Polynomial((RANDOMLY, 9, 1, 2))))
                        if sign == '+':
                            expd_kind = '+(...)'
                        else:
                            expd_kind = 'monom0_polyn1'

                    # Now we fill the boxes to draw from
                    box_1 = []
                    box_2 = []

                    additional_Monomial = Monomial((RANDOMLY, 9, 1))
                    additional_Monomial2 = Monomial((RANDOMLY, 9, 1))

                    if additional_Monomial.degree == 0:
                        additional_Monomial2.set_degree(1)

                    box_1.append(aux_expd_1)

                    if expd_kind == '+(...)' or random.random() <= 0.5:
                        box_1.append(additional_Monomial)

                    box_2.append(Monomial((RANDOMLY, 9, 1)))

                    if random.random() <= 0.25:
                        # __
                        box_2.append(additional_Monomial2)

                    if arg[1] == 'any_double_expandable':
                        if random.random() <= 0.8:
                            aux_expd_2 = Expandable((RANDOMLY,
                                                     'monom0_polyn1'),
                                                    max_coeff=9)

                        else:
                            sign = random.choice(['+', '-'])
                            aux_expd_2 = Expandable((
                                Monomial((sign, 1, 0)),
                                Polynomial((RANDOMLY, 9, 1, 2))))

                        if random.random() <= 0.5:
                            box_1.append(aux_expd_2)
                        else:
                            box_2.append(aux_expd_2)

                    boxes = [box_1, box_2]
                    if random.choice([True, False]):
                        box_left, box_right = boxes
                    else:
                        box_right, box_left = boxes

                    random.shuffle(box_left)
                    random.shuffle(box_right)

                    self._left_hand_side = Sum(box_left)
                    self._right_hand_side = Sum(box_right)

            # All other unforeseen cases: an exception is raised.
            else:
                raise TypeError('Got: ' + str(type(arg))
                                + ' instead of (Exponented, Exponented)|'
                                '(RANDOMLY, <option>)')

        # Another Equation to copy
        elif isinstance(arg, Equation):
            self._name = arg._name
            self._number = arg.number
            self._left_hand_side = arg.left_hand_side.clone()
            self._right_hand_side = arg.right_hand_side.clone()
            self._variable_letter = arg.variable_letter

        else:
            raise TypeError('Got: ' + str(type(arg))
                            + ' instead of Equation|tuple')

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the name of the object
    @property
    def name(self):
        if self.number == '':
            return MARKUP['opening_bracket'] \
                + MARKUP['open_text_in_maths'] \
                + self._name \
                + MARKUP['close_text_in_maths'] \
                + MARKUP['closing_bracket'] \
                + MARKUP['colon'] \
                + MARKUP['space']
        else:
            return MARKUP['opening_bracket'] \
                + MARKUP['open_text_in_maths'] \
                + self._name \
                + MARKUP['close_text_in_maths'] \
                + MARKUP['opening_subscript'] \
                + MARKUP['open_text_in_maths'] \
                + str(self.number) \
                + MARKUP['close_text_in_maths'] \
                + MARKUP['closing_subscript'] \
                + MARKUP['closing_bracket'] \
                + MARKUP['colon'] \
                + MARKUP['space']

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the number of the Equality
    def get_number(self):
        return self._number

    # --------------------------------------------------------------------------
    ##
    #   @brief Getter for left hand side
    def get_left_hand_side(self):
        return self._left_hand_side

    # --------------------------------------------------------------------------
    ##
    #   @brief Getter for right hand side
    def get_right_hand_side(self):
        return self._right_hand_side

    # --------------------------------------------------------------------------
    ##
    #   @brief Getter for the variable letter
    def get_variable_letter(self):
        return self._variable_letter

    number = property(get_number, doc="Number of the Equation")

    left_hand_side = property(get_left_hand_side,
                              doc="Left hand side of the Equation")

    right_hand_side = property(get_right_hand_side,
                               doc="Right hand side of the Equation")

    variable_letter = property(get_variable_letter,
                               doc="Variable letter of the Equation")

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the number of the Equation
    def set_number(self, arg):
        if not type(arg) == int:
            raise ValueError('arg should be an int')

        self._number = str(arg)

    # --------------------------------------------------------------------------
    ##
    #   @brief Setter for hand sides
    #   @return Nothing, just sets the given argument to the left hand side,
    #           turned into a Sum if necessary
    def set_hand_side(self, left_or_right, arg):
        if not (left_or_right == 'left' or left_or_right == 'right'):
            raise ValueError('left_or_right should be \'left\' or \'right\'')
        if isinstance(arg, Exponented):
            if isinstance(arg, CommutativeOperation) and len(arg) == 1:
                arg = arg.element[0]
            if not isinstance(arg, Sum):
                arg = Sum(arg)
            if left_or_right == "left":
                self._left_hand_side = arg
            else:
                self._right_hand_side = arg

        else:
            raise TypeError('arg should have been an Exponented, instead, got '
                            + str(type(arg)))

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    def into_str(self, **options):
        global expression_begins
        # Equation objects displaying
        beginning = ''

        if 'display_name' in options:
            beginning = self.name

        left = self.left_hand_side.printed

        right = self.right_hand_side.printed

        egal_sign = MARKUP['equal']

        if self.left_hand_side.contains_a_rounded_number() \
           or self.right_hand_side.contains_a_rounded_number():
            # __
            egal_sign = MARKUP['simeq']

        return beginning + left + egal_sign + right

    # --------------------------------------------------------------------------
    ##
    #   @brief Raw display of the Equation (debugging method)
    #   @return A string containing "type: sign coeff × X ^ degree"
    def __repr__(self):
        return "\nEquation: " + str(self.name) \
               + " " + str(self.number) \
               + "\n Left hand side: " + repr(self.left_hand_side) \
               + "\n Right hand side: " + repr(self.right_hand_side) \
               + "\n Variable: " + str(self.variable_letter)

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the equation's resolution in the given ML
    #   @param options Any options
    #   @return The formated string of the equation's resolution
    def auto_resolution(self, **options):
        global expression_begins

        # Complete resolution of the equation:o)
        result = ""

        if 'dont_display_equations_name' not in options:
            result = MARKUP['opening_math_style2'] \
                + self.name \
                + MARKUP['closing_math_style2']

        # result += MARKUP['newline']

        uline1 = ""
        uline2 = ""
        if 'underline_result' in options and options['underline_result']:
            uline1 = MARKUP['open_underline']
            uline2 = MARKUP['close_underline']
            required.package['ulem'] = True

        eq_aux = None
        if (isinstance(self, Equation)
            and not isinstance(self, CrossProductEquation)):
            # __
            eq_aux = Equation(self)
        elif isinstance(self, CrossProductEquation):
            eq_aux = CrossProductEquation(self)

        eq_aux1 = None
        eq_aux2 = None
        equation_did_split_in_two = False
        go_on = True

        step_nb = 0

        while go_on:
            step_nb += 1
            if not equation_did_split_in_two:

                next_eq_aux = eq_aux.solve_next_step(**options)
                if not('skip_first_step' in options and step_nb == 1):
                    if next_eq_aux is None and 'unit' in options:
                        result += MARKUP['opening_math_style1'] \
                            + uline1 \
                            + eq_aux.into_str() \
                            + MARKUP['open_text_in_maths'] \
                            + " " + str(options['unit']) \
                            + MARKUP['close_text_in_maths'] \
                            + uline2 \
                            + MARKUP['closing_math_style1']
                    else:
                        result += MARKUP['opening_math_style1'] \
                            + eq_aux.into_str() \
                            + MARKUP['closing_math_style1']

                if (next_eq_aux is None or type(next_eq_aux) == str
                    or isinstance(next_eq_aux, tuple)):
                    # __
                    eq_aux = next_eq_aux
                else:
                    eq_aux = Equation(next_eq_aux)

                if isinstance(eq_aux, tuple):
                    (eq_aux1, eq_aux2) = eq_aux
                    equation_did_split_in_two = True

                elif isinstance(eq_aux, str) or eq_aux is None:
                    go_on = False

            else:
                if isinstance(eq_aux1, Equation):
                    next_eq_aux1 = eq_aux1.solve_next_step(**options)

                if isinstance(eq_aux2, Equation):
                    next_eq_aux2 = eq_aux2.solve_next_step(**options)

                if eq_aux1 is not None or eq_aux2 is not None:
                    result += MARKUP['opening_math_style1']

                if isinstance(eq_aux1, Equation):
                    if next_eq_aux1 is None:
                        result += uline1

                    result += eq_aux1.into_str()

                    if next_eq_aux1 is None and 'unit' in options:
                        result += MARKUP['open_text_in_maths'] \
                            + " " + str(options['unit']) \
                            + MARKUP['close_text_in_maths']

                    if next_eq_aux1 is None:
                        result += uline2

                    if isinstance(eq_aux2, Equation):
                        result += " " + _("or") + " "

                elif eq_aux1 is not None:
                    result += eq_aux1

                if isinstance(eq_aux2, Equation):

                    if next_eq_aux2 is None:
                        result += uline1

                    result += eq_aux2.into_str()

                    if next_eq_aux2 is None and 'unit' in options:
                        result += MARKUP['open_text_in_maths'] \
                            + " " + str(options['unit']) \
                            + MARKUP['close_text_in_maths']

                    if next_eq_aux2 is None:
                        result += uline2

                elif eq_aux2 is not None:
                    result += eq_aux2
                    eq_aux2 = None

                if not isinstance(eq_aux1, Equation) \
                   and not isinstance(eq_aux2, Equation):
                    # __
                    go_on = False

                if eq_aux1 is not None or eq_aux2 is not None:
                    result += MARKUP['closing_math_style1']

                if isinstance(eq_aux1, Equation):
                    eq_aux1 = eq_aux1.solve_next_step(**options)

                if isinstance(eq_aux2, Equation):
                    eq_aux2 = eq_aux2.solve_next_step(**options)

        if (not equation_did_split_in_two):
            if eq_aux is None:
                pass
            else:
                result += eq_aux + MARKUP['newline']
        else:
            if eq_aux1 is None and eq_aux2 is None:
                pass
            else:
                if eq_aux1 is None:
                    result += eq_aux2 + MARKUP['newline']
                else:
                    result += eq_aux1 + MARKUP['newline']

        # if 'get_solution' in options and options['get_solution']:

        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates the next Equation object in the resolution
    #   @todo Expandables (which have to get checked first, btw) !
    #   @todo check the case -x = -7 where the - belongs to the Item's value
    #   @return An Equation
    def solve_next_step(self, **options):
        log = settings.dbg_logger.getChild('Equation.solve_next_step')
        new_eq = Equation(self)
        log.debug("Entering, with Equation: " + repr(new_eq))

        # CASE 0: preparing the Equation: getting recursively rid of
        #          imbricated Sums
        if isinstance(new_eq.left_hand_side.term[0], Sum) \
           and len(new_eq.left_hand_side) == 1:
            # __
            log.debug("CASE-0s-left")
            new_eq.set_hand_side("left", new_eq.left_hand_side.term[0])
            return new_eq.solve_next_step(**options)

        elif (isinstance(new_eq.right_hand_side.term[0], Sum)
              and len(new_eq.right_hand_side) == 1):
            # __
            log.debug("CASE-0s-right")
            new_eq.set_hand_side("right", new_eq.right_hand_side.term[0])
            return new_eq.solve_next_step(**options)

        if isinstance(new_eq.left_hand_side.term[0], Product) \
           and len(new_eq.left_hand_side) == 1 \
           and len(new_eq.left_hand_side.term[0]) == 1:
            # __
            log.debug("CASE-0p-left")
            new_eq.set_hand_side("left",
                                 Sum(new_eq.left_hand_side.term[0].factor[0]))
            return new_eq.solve_next_step(**options)

        elif (isinstance(new_eq.right_hand_side.term[0], Product)
              and len(new_eq.right_hand_side) == 1
              and len(new_eq.right_hand_side.term[0]) == 1):
            # __
            log.debug("CASE-0p-right")
            new_eq.set_hand_side("right",
                                 Sum(new_eq.right_hand_side.term[0].factor[0]))
            return new_eq.solve_next_step(**options)

        reduced_options = {
            'details_level': options.get('details_level', 'maximum')
        }
        next_left_X = new_eq.left_hand_side.expand_and_reduce_next_step(
            **reduced_options
        )
        next_right_X = new_eq.right_hand_side.expand_and_reduce_next_step(
            **reduced_options
        )
        # next_left_C = new_eq.left_hand_side.calculate_next_step()
        # next_right_C = new_eq.right_hand_side.calculate_next_step()

        if not (isinstance(next_left_X, Calculable)
                or isinstance(next_left_X, ComposedCalculable)):
            # __
            next_left_X_str = str(next_left_X)
        else:
            next_left_X_str = repr(next_left_X)
        log.debug("'decimal_result' is in options? "
                  + str('decimal_result' in options) + "; "
                  "len(new_eq.left_hand_side): "
                  + str(len(new_eq.left_hand_side))
                  + "\nnext_left_X is: " + next_left_X_str
                  + "\nnext_right_X is: " + repr(next_right_X)
                  + "\nnew_eq.left_hand_side.term[0].is_literal()? "
                  + str(new_eq.left_hand_side.term[0].is_literal()) + "; "
                  "len(new_eq.right_hand_side): "
                  + str(len(new_eq.right_hand_side))
                  + "\nisinstance(new_eq.right_hand_side.term[0], "
                  "Fraction)? "
                  + str(isinstance(new_eq.right_hand_side.term[0],
                                   Fraction)))

        at_left_one_literal_not_expandable_element = \
            (len(new_eq.left_hand_side) == 1
             and next_left_X is None
             and not new_eq.left_hand_side.term[0].is_numeric()
             and len(new_eq.right_hand_side) == 1)

        if (at_left_one_literal_not_expandable_element
            and isinstance(new_eq.left_hand_side.term[0], Function)
            and new_eq.right_hand_side.is_numeric()):
            log.debug("A Function to invert")
            item_class = Item
            if isinstance(new_eq.left_hand_side.term[0].var, AngleItem):
                item_class = AngleItem
            new_eq.set_hand_side('right',
                                 item_class(new_eq.left_hand_side
                                            .term[0].inv_fct(
                                                new_eq.right_hand_side.term[0]
                                                .evaluate(**options)))
                                 .rounded(options['decimal_result']))
            new_eq.set_hand_side('left',
                                 new_eq.left_hand_side.term[0].var)

        elif (at_left_one_literal_not_expandable_element
              and isinstance(new_eq.right_hand_side.term[0], Fraction)
              and new_eq.right_hand_side.term[0].is_reducible()
              and 'skip_fraction_simplification' in options):
            # __
            log.debug('At left, one literal not reducible element; '
                      'at right, one reducible Fraction, but Fraction '
                      'simplification must be skipped.')
            if 'decimal_result' in options:
                log.debug('And decimal result is required')
                new_eq.set_hand_side("right",
                                     Item(new_eq
                                          .right_hand_side.term[0]
                                          .evaluate(**options)))
            else:
                log.debug('But no decimal result is required')
                new_eq.set_hand_side("right",
                                     new_eq.right_hand_side.term[0]
                                     .completely_reduced())
        elif (at_left_one_literal_not_expandable_element
              and 'decimal_result' in options
              and (isinstance(new_eq.right_hand_side.term[0], Quotient)
                   or isinstance(new_eq.right_hand_side.term[0], Function)
                   or isinstance(new_eq.right_hand_side.term[0], SquareRoot))):
            # __
            log.debug('At left, one literal not reducible element; '
                      'at right, one Quotient|Function|SquareRoot and '
                      'decimal result is required.')
            options.update({'force_evaluation': True})
            new_eq.set_hand_side("right",
                                 new_eq.right_hand_side.
                                 expand_and_reduce_next_step(**options))

        # 1st CASE
        # Expand & reduce each side of the Equation, whenever possible
        elif (next_left_X is not None) or (next_right_X is not None):
            # __
            log.debug("1st CASE")
            if next_left_X is not None:
                # __
                new_eq.set_hand_side("left", next_left_X)

            if next_right_X is not None:
                # __
                new_eq.set_hand_side("right", next_right_X)
                at_left_one_literal_not_expandable_element = \
                    (len(new_eq.left_hand_side) == 1
                     and next_left_X is None
                     and not new_eq.left_hand_side.term[0].is_numeric()
                     and len(new_eq.right_hand_side) == 1)
                if (at_left_one_literal_not_expandable_element
                    and 'decimal_result' in options
                    and isinstance(new_eq.right_hand_side.term[0], Item)
                    and new_eq.right_hand_side.term[0]
                    .needs_to_get_rounded(options['decimal_result'])):
                    # __
                    new_eq.set_hand_side("right",
                                         new_eq.right_hand_side.term[0]
                                         .rounded(options['decimal_result']))

        # 2d CASE
        # Irreducible SUMS, like 3 + x = 5 or x - 2 = 3x + 7
        # It seems useless to test if one side is reducible, if it was,
        # then it would have been treated in the first case.
        # After that case is treated, every literal term will be moved
        # to the left, and every numeric term moved to the right.
        elif (len(new_eq.left_hand_side) >= 2
              or len(new_eq.right_hand_side) >= 2
              or (len(new_eq.right_hand_side) == 1
                  and not new_eq.right_hand_side.term[0].is_numeric())):
            # __
            log.debug("2d CASE")
            # All the literal objects will be moved to the left,
            # all numeric will be moved to the right
            log.debug("Current Equation: " + repr(self))

            left_collected_terms = new_eq.left_hand_side.get_numeric_terms()
            right_collected_terms = new_eq.right_hand_side.get_literal_terms()

            log.debug("left content: " + repr(self.left_hand_side)
                      + "\nright content: "
                      + repr(self.right_hand_side))

            log.debug("\nleft collected terms: "
                      + "".join([repr(t) for t in left_collected_terms]))

            log.debug("\nright collected terms: "
                      + "".join([repr(t) for t in right_collected_terms]))

            # Special case of equations like 5 = x - 9
            # which should become x = 5 + 9 at the next line, instead of
            # -x = -5 - 9 (not suited for Pythagorean Equations)
            if new_eq.left_hand_side.is_numeric() \
               and not new_eq.right_hand_side.is_numeric() \
               and len(new_eq.right_hand_side) == 2 \
               and len(right_collected_terms) == 1:
                # __
                log.debug("Entered in the Special Case [part of 2d Case]")
                log.debug("isinstance(right_collected_terms[0], Product)? "
                          + str(isinstance(right_collected_terms[0], Product))
                          + "\nlen(right_collected_terms[0]) == 2? "
                          + str(len(right_collected_terms[0]) == 2)
                          + "\nlen(right_collected_terms[0]) == 1? "
                          + str(len(right_collected_terms[0]) == 1)
                          + "\nisinstance(right_collected_terms[0], Item)? "
                          + str(isinstance(right_collected_terms[0], Item)))

                if ((isinstance(right_collected_terms[0], Product)
                     and len(right_collected_terms[0]) == 2
                     and right_collected_terms[0][0].is_positive())
                    or (isinstance(right_collected_terms[0], Product)
                        and len(right_collected_terms[0]) == 1)
                    or (isinstance(right_collected_terms[0], Item)
                        and right_collected_terms[0].is_positive())):
                    # __
                    log.debug("Special Case [part 2]")

                    return Equation((new_eq.right_hand_side,
                                     new_eq.left_hand_side))\
                        .solve_next_step(**options)

            # Special Case 2:
            # of Equations like 9 = 3x which should become x = 9/3
            # and not -3x = -9
            if new_eq.left_hand_side.is_numeric() \
               and not new_eq.right_hand_side.is_numeric() \
               and len(new_eq.right_hand_side) == 1 \
               and isinstance(right_collected_terms[0], Product):
                # __
                log.debug("Special Case [part 3]")

                return Equation((new_eq.right_hand_side,
                                 new_eq.left_hand_side)) \
                    .solve_next_step(**options)

            for term in left_collected_terms:
                # log.debug("(left)term: " + str(term))
                new_eq.left_hand_side.remove(term)
                term.set_sign(sign_of_product(['-', term.sign]))
                new_eq.set_hand_side("right",
                                     Sum([new_eq.right_hand_side, term]))
                log.debug("Now, right_hand_side looks like: "
                          + repr(new_eq.right_hand_side))

            for term in right_collected_terms:
                # log.debug("(right)term: " + str(term))
                new_eq.right_hand_side.remove(term)
                # term.set_sign(sign_of_product(['-', term.sign]))
                term = Product([term, Item(-1)]).reduce_()
                new_eq.set_hand_side("left", Sum([new_eq.left_hand_side,
                                                  term]))

            new_eq.left_hand_side.reduce_()
            new_eq.right_hand_side.reduce_()
            # log.debug("after reduction, "
            #                       + "right_hand_side looks like: "
            #                       + str(new_eq.right_hand_side))

        # 3rd CASE
        # Weird cases like 0 = 1 or 2 = 2
        elif (new_eq.left_hand_side.term[0].is_numeric()
              and (new_eq.right_hand_side.term[0].is_numeric())):
            # __
            log.debug("3rd CASE")
            if new_eq.left_hand_side.term[0].raw_value == \
                new_eq.right_hand_side.term[0].raw_value \
               and new_eq.left_hand_side.get_sign() == \
                    new_eq.right_hand_side.get_sign():
                # __
                return _('Any value of {variable_name} is '
                         'solution of the equation.')\
                    .format(variable_name=new_eq.variable_letter)

            else:
                return _('This equation has no solution.')

        # 4th CASE
        # Irreducible PRODUCTS ax = b or -x = b or x = b,
        # where a and b are Exponenteds.
        # The Product in the left side can't be numeric, or it would
        # have been already treated before
        elif isinstance(new_eq.left_hand_side.term[0], Product):
            # __
            log.debug("4th CASE")

            # Let's replace the possibly remaining Monomial of degree 0
            # at the right by an equivalent Item or Fraction
            if isinstance(new_eq.right_hand_side.term[0], Monomial):
                if isinstance(new_eq.right_hand_side.term[0].factor[0],
                              Item):
                    # __
                    new_eq.right_hand_side\
                        .set_term(0,
                                  Item(new_eq.right_hand_side.term[0]))
                elif isinstance(new_eq.right_hand_side.term[0].factor[0],
                                Fraction):
                    # __
                    new_eq.right_hand_side\
                        .set_term(0,
                                  Fraction(new_eq.right_hand_side.term[0]))

            # Let's get the numeric Exponented to remove from the left:
            coefficient = new_eq.left_hand_side.term[0].factor[0]

            if coefficient.is_displ_as_a_single_1():
                new_eq.set_hand_side("left",
                                     Item(new_eq.left_hand_side.term[0]
                                          .factor[1]))
                return new_eq.solve_next_step(**options)

            elif coefficient.is_displ_as_a_single_minus_1():
                new_eq.left_hand_side.term[0].set_opposite_sign()
                new_eq.right_hand_side.term[0].set_opposite_sign()

            elif (isinstance(coefficient, Item)
                  and isinstance(new_eq.right_hand_side.term[0], Item)):
                # __
                new_eq.left_hand_side.term[0].set_factor(0, Item(1))
                new_eq.set_hand_side("right",
                                     Fraction(('+',
                                               new_eq.right_hand_side.term[0],
                                               Item(coefficient))))
                new_eq.right_hand_side.term[0]\
                    .set_down_numerator_s_minus_sign()

            else:
                new_eq.left_hand_side.term[0].set_factor(0, Item(1))
                new_eq.right_hand_side\
                    .set_term(0,
                              Quotient(('+',
                                        new_eq
                                        .right_hand_side
                                        .term[0],
                                        coefficient),
                                       use_divide_symbol=True))

        # 5th CASE
        # Literal Items -x = b (or -x² = b) or x = b, or x² = b
        # where a and b are (reduced/simplified) Exponenteds.
        # The Item at the left can't be numeric, the case should have
        # been treated before
        elif (isinstance(new_eq.left_hand_side.term[0], Item)
              and new_eq.left_hand_side.term[0].is_literal()):
            # __
            log.debug("5th CASE")
            if new_eq.left_hand_side.term[0].get_sign() == '-':
                new_eq.left_hand_side.term[0].set_opposite_sign()
                new_eq.right_hand_side.term[0].set_opposite_sign()
                log.debug("Swapped signs")
            else:
                # CASES x² = b
                if new_eq.left_hand_side.term[0].exponent == Value(2):

                    if new_eq.right_hand_side.term[0].is_negative():
                        return _("This equation has no solution.")

                    elif new_eq.left_hand_side.is_displ_as_a_single_0():
                        new_eq.left_hand_side.term[0].set_exponent(Value(1))

                    else:
                        temp_sqrt1 = SquareRoot(new_eq.
                                                right_hand_side.term[0])
                        temp_sqrt2 = SquareRoot(temp_sqrt1)
                        temp_sqrt2.set_sign('-')
                        temp_item = Item(new_eq.left_hand_side.term[0])
                        temp_item.set_exponent(Value(1))
                        new_eq1 = Equation((temp_item,
                                            temp_sqrt1))
                        new_eq2 = Equation((temp_item,
                                            temp_sqrt2))

                        if ('pythagorean_mode' in options
                            and options['pythagorean_mode']):
                            # __
                            new_eq2 = MARKUP['open_text_in_maths'] + ' '\
                                + _('because {L} is positive.')\
                                .format(L=temp_item.printed)\
                                + MARKUP['close_text_in_maths']

                        return (new_eq1, new_eq2)

                # Now the exponent must be equivalent to a single 1
                # or the algorithm just doesn't know how to solve further.
                else:
                    log.debug("Returning None")
                    return None

        # log.debug(
        #                   "Before having thrown away the neutrals: "
        #                   + str(new_eq))

        # throwing away the possibly zeros left..
        new_eq.set_hand_side("left",
                             new_eq.left_hand_side.throw_away_the_neutrals())
        new_eq.set_hand_side("right",
                             new_eq.right_hand_side.throw_away_the_neutrals())

        # log.debug(
        #                   "After having thrown away the neutrals,"
        #                    right_hand_side looks like: "
        #                    + str(new_eq.right_hand_side))

        log.debug("Leaving, with Equation: " + repr(new_eq))
        return new_eq


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class CrossProductEquation
# @brief All objects that are displayable as Cross Product Equations
class CrossProductEquation(Equation):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg    CrossProductEquation|(Quotient, Quotient)|
    #                                               (num1, num2, deno1, deno2)
    #   @param arg      numx and denox are expected as Calculables
    def __init__(self, arg):
        if not (type(arg) == tuple or isinstance(arg, CrossProductEquation)):
            raise ValueError('Got ' + str(type(arg))
                             + 'instead of a tuple|CrossProductEquation')
        elif type(arg) == tuple and not (len(arg) == 2 or len(arg) == 4):
            raise ValueError('Got a tuple of length ' + str(len(arg))
                             + 'instead of a tuple of length 2 or 4')

        if isinstance(arg, CrossProductEquation):
            self._name = arg.name
            self._number = arg.number
            self._left_hand_side = arg.left_hand_side.clone()
            self._right_hand_side = arg.right_hand_side.clone()
            self._variable_letter = arg.variable_letter
            self._variable_position = arg.variable_position
            self._variable_obj = arg.variable_obj.clone()

        else:
            self._name = settings.default.EQUATION_NAME
            self._number = ''

            if len(arg) == 2:
                if not(isinstance(arg[0], Quotient)
                       and isinstance(arg[1], Quotient)):
                    # __
                    raise ValueError('Got a a tuple of ' + str(type(arg[0]))
                                     + ' and of ' + str(type(arg[1])
                                     + ' instead of a tuple of two Quotients'))
                else:
                    self._left_hand_side = arg[0].clone()
                    self._right_hand_side = arg[1].clone()

            elif len(arg) == 4:
                if not(isinstance(arg[0], Calculable)
                       and isinstance(arg[1], Calculable)
                       and isinstance(arg[2], Calculable)
                       and isinstance(arg[3], Calculable)):
                    # __
                    raise ValueError('Got a tuple of ' + str(type(arg[0]))
                                     + ', ' + str(type(arg[1]))
                                     + ', ' + str(type(arg[2]))
                                     + 'and ' + str(type(arg[3]))
                                     + 'instead of a tuple of four '
                                     'Calculables')
                else:
                    self._left_hand_side = Quotient(('+', arg[0], arg[2]),
                                                    ignore_1_denominator=True)
                    self._right_hand_side = Quotient(('+', arg[1], arg[3]),
                                                     ignore_1_denominator=True)

            # Let's find the variable
            # In the same time, we'll determine its position and the var obj
            stop = 0
            literal_position = 0
            literals = 0
            variable_letter = ""
            variable_obj = None
            # Don't change the order of elt below, it is inspired by this...
            #                 0: x a     1: a x     2: a b    3: a b
            #                    b c        b c        c x       x c
            for elt in [self.left_hand_side.numerator,
                        self.right_hand_side.numerator,
                        self.right_hand_side.denominator,
                        self.left_hand_side.denominator]:
                if elt.is_literal():
                    literals += 1
                    variable_letter += elt.into_str()
                    variable_obj = elt.clone()
                    stop = 1
                if not stop:
                    literal_position += 1

            if not literals == 1:
                raise ValueError('Got ' + str(literals) + 'literal objects'
                                 'instead of exactly one literal object '
                                 'among 4')

            self._variable_letter = variable_letter

            self._variable_position = literal_position

            self._variable_obj = variable_obj

    # --------------------------------------------------------------------------
    ##
    #   @brief Getter for the variable obj
    def get_variable_obj(self):
        return self._variable_obj

    # --------------------------------------------------------------------------
    ##
    #   @brief Getter for the variable position
    def get_variable_position(self):
        return self._variable_position

    variable_obj = property(get_variable_obj,
                            doc="Variable object of the Equation")
    variable_position = property(get_variable_position,
                                 doc="Variable position in the Equation")

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates the next Equation object in the resolution
    #   @return An Equation
    def solve_next_step(self, **options):
        temp_table = Table([[self.left_hand_side.numerator,
                             self.right_hand_side.numerator],
                            [self.left_hand_side.denominator,
                             self.right_hand_side.denominator]])

        r1d = options.get('remove_1_deno', True)
        new_eq = Equation((self.variable_obj,
                           temp_table.cross_product((0, 1),
                                                    self.variable_position,
                                                    remove_1_deno=r1d)))
        if (self.left_hand_side.numerator.is_literal()
            and self.left_hand_side.denominator.is_displ_as_a_single_1()):
            new_eq = new_eq.solve_next_step(**options)
        return new_eq


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Table
# @brief All objects that are displayable as Tables
class Table(Printable, Substitutable):

    class SubstitutableList(list, Substitutable):
        """A list that can call substitute() on its elements."""
        def __init__(self, *args, subst_dict=None):
            list.__init__(self, *args)
            Substitutable.__init__(self, subst_dict=subst_dict)

        @property
        def content(self):
            """
            The content to be substituted (list containing literal objects).
            """
            return self

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param arg [[Calculable], [Calculable]]   (the Calculables' lists must
    #                                              have the same length)
    def __init__(self, arg, displ_as_qe=False, ignore_1_denos=None,
                 subst_dict=None):
        if not type(arg) == list:
            raise TypeError('arg must be a list (of two lists)')

        if not len(arg) == 2:
            raise ValueError('Got a list of ' + str(len(arg)) + 'elements'
                             'instead of a list of 2 elements')

        if not type(arg[0]) == list:
            raise ValueError('Got ' + str(type(arg[0]))
                             + 'instead of a list')

        if not type(arg[1]) == list:
            raise ValueError('Got ' + str(type(arg[1]))
                             + 'instead of a list')

        if not len(arg[0]) == len(arg[1]):
            raise ValueError('Got two lists of different lengths: '
                             + str(len(arg[0])) + ' and ' + str(len(arg[1]))
                             + 'instead of two lists of the same length')

        for j in range(2):
            for i in range(len(arg[j])):
                if not isinstance(arg[j][i], Calculable):
                    raise ValueError('Got: arg[' + str(j) + ']['
                                     + str(i) + '] being a: '
                                     + str(type(arg[j][i]))
                                     + ' instead of a Calculable')

        if not isinstance(displ_as_qe, bool):
            raise TypeError('displ_as_qe should be a boolean')

        if ignore_1_denos is not None and not isinstance(ignore_1_denos, bool):
            raise TypeError('if set, ignore_1_denos should be a boolean')

        self._nb_of_cols = len(arg[0])
        self._data = [Table.SubstitutableList(arg[0], subst_dict=None),
                      Table.SubstitutableList(arg[1], subst_dict=None)]
        self._displ_as_qe = displ_as_qe
        self._ignore_1_denos = displ_as_qe
        if ignore_1_denos is not None:
            self._ignore_1_denos = ignore_1_denos
        Substitutable.__init__(self, subst_dict=subst_dict)

    @property
    def displ_as_qe(self):
        return self._displ_as_qe

    @property
    def ignore_1_denos(self):
        return self._ignore_1_denos

    @property
    def content(self):
        return self._data

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Table's content as a list of two lists so it
    #           can be addressed
    def get_cell(self):
        return self._data
    # --------------------------------------------------------------------------
    cell = property(get_cell,
                    doc="t.cell is the complete Table t.cell[i][j] is a cell")

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates a string of the given object in the given ML
    #   @param options Any options
    #   @return The formated string
    #   @todo Separate this from the LaTeX format (seems difficult to do)
    def into_str(self, as_a_quotients_equality=None, ignore_1_denos=None,
                 **options):
        if as_a_quotients_equality is None:
            as_a_quotients_equality = self._displ_as_qe
        elif not isinstance(as_a_quotients_equality, bool):
            raise TypeError('as_a_quotients_equality should be a boolean.')
        if ignore_1_denos is None:
            ignore_1_denos = self._ignore_1_denos
        elif not isinstance(ignore_1_denos, bool):
            raise TypeError('ignore_1_denos should be a boolean.')
        result = ""
        if as_a_quotients_equality:
            for i in range(len(self)):
                options['ignore_1_denominator'] = ignore_1_denos
                result += Quotient(('+',
                                    self.cell[0][i],
                                    self.cell[1][i]
                                    ), **options).printed
                if i < len(self) - 1:
                    result += MARKUP['equal']

        else:  # there, the table will be displayed normally, as a table
            content = []
            for i in range(2):
                for j in range(len(self)):
                    content += [self.cell[i][j].printed]
            result = shared.machine\
                .create_table((2, len(self)),
                              content,
                              col_fmt=['c' for i in range(len(self))],
                              borders='all')
        return result

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the number of columns of the Table
    def __len__(self):
        return self._nb_of_cols

    # --------------------------------------------------------------------------
    ##
    #   @brief Produces the cross product of a cell among 4 given
    #   @param cols: (nb of col 1, nb of col 2)
    #   @param x_position: position of the unknown variable to compute
    #                       it will be 0, 1, 2 or 3
    #                       0: x a     1: a x     2: a b    3: a b
    #                          b c        b c        c x       x c
    #   @param options Any options
    #   @return A Quotient or possibly a Fraction
    def cross_product(self, col, x_position, remove_1_deno=True, **options):
        if col[0] >= len(self) or col[1] >= len(self):
            raise ValueError(str(col[0]) + ' or ' + str(col[1])
                             + 'should be < ' + str(len(self)))
        if x_position not in [0, 1, 2, 3]:
            raise ValueError(str(x_position) + 'should be in [0, 1, 2, 3]')
        num = None
        if x_position == 0 or x_position == 2:
            num = Product([self.cell[0][col[1]],
                           self.cell[1][col[0]]]).throw_away_the_neutrals()
        elif x_position == 1 or x_position == 3:
            num = Product([self.cell[0][col[0]],
                           self.cell[1][col[1]]]).throw_away_the_neutrals()
        deno = None
        if x_position == 0:
            deno = self.cell[1][col[1]]
            if deno.is_displ_as_a_single_1() and remove_1_deno:
                return num
            if (self.cell[0][col[1]].is_displ_as_a_single_int()
                and self.cell[1][col[0]].is_displ_as_a_single_int()
                and self.cell[1][col[1]].is_displ_as_a_single_int()):
                # __
                return Fraction((num, deno))
            else:
                return Quotient(('+', num, deno))

        elif x_position == 1:
            deno = self.cell[1][col[0]]
            if deno.is_displ_as_a_single_1() and remove_1_deno:
                return num
            if (self.cell[0][col[0]].is_displ_as_a_single_int()
                and self.cell[1][col[1]].is_displ_as_a_single_int()
                and self.cell[1][col[0]].is_displ_as_a_single_int()):
                # __
                return Fraction((num, deno))
            else:
                return Quotient(('+', num, deno))

        elif x_position == 2:
            deno = self.cell[0][col[0]]
            if deno.is_displ_as_a_single_1() and remove_1_deno:
                return num
            if (self.cell[0][col[1]].is_displ_as_a_single_int()
                and self.cell[1][col[0]].is_displ_as_a_single_int()
                and self.cell[0][col[0]].is_displ_as_a_single_int()):
                # __
                return Fraction((num, deno))
            else:
                return Quotient(('+', num, deno))

        elif x_position == 3:
            deno = self.cell[0][col[1]]
            if deno.is_displ_as_a_single_1() and remove_1_deno:
                return num
            if (self.cell[0][col[0]].is_displ_as_a_single_int()
                and self.cell[1][col[1]].is_displ_as_a_single_int()
                and self.cell[0][col[1]].is_displ_as_a_single_int()):
                # __
                return Fraction((num, deno))
            else:
                return Quotient(('+', num, deno))

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns True if the Table is entirely numeric
    def is_numeric(self, displ_as=False):
        for i in range(2):
            for j in range(len(self)):
                if not self.cell[i][j].is_numeric(displ_as=displ_as):
                    return False

        return True

    def into_crossproduct_equation(self,
                                   col0=0,
                                   col1=1) -> CrossProductEquation:
        """
        Create a CrossProductEquation from two columns.

        Ensure there is only one literal among the four cells before using it.

        :param col0: the number of the first column to use
        :param col1: the number of the second column to use
        """
        return CrossProductEquation((self.cell[0][col0],
                                     self.cell[0][col1],
                                     self.cell[1][col0],
                                     self.cell[1][col1]))

    def auto_resolution(self, col0=0, col1=1, subst_dict=None, **options):
        result = MARKUP['opening_math_style1'] + self.printed\
            + MARKUP['closing_math_style1']
        self.substitute(subst_dict=subst_dict)
        return result + self.into_crossproduct_equation(col0=col0, col1=col1)\
            .auto_resolution(**options)


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Table_UP
# @brief All objects that are displayable as proportional Tables but uncomplete
class Table_UP(Table):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor
    #   @param coeff        nb|numericCalculable
    #   @param first_line   [nb|numericCalculable]
    #   @param info         [None|(None|literalCalculable,
    #                              None|literalCalculable)]
    #   info and first_line should have the same length
    #   info should contain at least one None|(None, None) element
    #   (means the column is completely numeric)
    def __init__(self, coeff, first_line, info, displ_as_qe=False):
        log = settings.dbg_logger.getChild('Table_UP.init')

        if (not is_number(coeff)
            and not (isinstance(coeff, Calculable) and coeff.is_numeric())):
            # __
            raise ValueError('Got:' + str(type(coeff))
                             + ' instead of a number or a numeric Calculable')

        if not type(first_line) == list:
            raise ValueError('Got:' + str(type(first_line))
                             + ' instead of a list ')

        if not type(info) == list:
            raise ValueError('Got:' + str(type(info))
                             + ' instead of a list ')

        if not len(info) == len(first_line):
            raise ValueError('Got: two lists of lengths ' + str(len(info))
                             + ' and ' + str(len(first_line))
                             + ' instead of two lists of the same length.')

        for elt in first_line:
            if (elt is not None and not is_number(elt)
                and not (isinstance(elt, Calculable) and elt.is_numeric())):
                # __
                raise ValueError('Got:' + str(type(elt)) + ' ' + repr(elt)
                                 + 'instead of None | nb | numericCalculable')

        complete_cols = []
        literals_positions = {}
        col_nb = 0

        for i in range(len(first_line)):
            if first_line[i] is None and (info[i] is None
                                          or info[i] == (None, None)):
                # __
                raise ValueError('Got first_line[i] and info[i] being'
                                 ' both equal to None though only one of '
                                 'them can be None in the same time')
            elt = info[i]
            log.debug('elt: ' + str(elt))

            if not (elt is None or type(elt) == tuple):
                raise ValueError('Got:' + str(type(elt))
                                 + ' instead of either None or a tuple ')

            if elt is None or elt == (None, None):
                complete_cols += [col_nb]

            if type(elt) == tuple:
                if not len(elt) == 2:
                    raise ValueError('Got: a tuple of length ' + str(len(elt))
                                     + 'instead of a tuple of length 2')

                if not ((isinstance(elt[0], Calculable)
                         and elt[0].is_literal())
                        or elt[0] is None):
                    # __
                    raise ValueError('Got:' + str(elt[0])
                                     + ' instead of None|literalCalculable')

                if not ((isinstance(elt[1], Calculable)
                         and elt[1].is_literal())
                        or elt[1] is None):
                    # __
                    raise ValueError('Got:' + str(type(elt[1]))
                                     + ' instead of None|literalCalculable')

                if elt[0] in literals_positions:
                    raise ValueError('Got:' + elt[0].into_str()
                                     + ' being already in the Table,'
                                     + ' but it should be there only once.')
                else:
                    if (isinstance(elt[0], Calculable)
                        and not isinstance(elt[1], Calculable)):
                        # __
                        literals_positions[elt[0]] = col_nb

                if elt[1] in literals_positions:
                    raise ValueError('Got:' + elt[1].into_str()
                                     + ' being already in the Table.'
                                     + ' but it should be there only once')
                else:
                    if (isinstance(elt[1], Calculable)
                        and not isinstance(elt[0], Calculable)):
                        # __:
                        literals_positions[elt[1]] = col_nb
            col_nb += 1

        if len(complete_cols) == 0:
            raise ValueError('Got:' + "no complete column found",
                                      "there should be at least one complete")

        # Now everything is clean, let's set the fields
        self._coeff = coeff

        second_line = []

        for i in range(len(first_line)):
            if first_line[i] is None:
                second_line += [None]
            else:
                second_line += [Item(Product([coeff,
                                              first_line[i]]).evaluate())]

        data = [[], []]

        for i in range(len(first_line)):
            if info[i] is None:
                data[0] += [first_line[i]]
                data[1] += [second_line[i]]

            elif first_line[i] is None:
                data[0] += [info[i][0]]
                data[1] += [info[i][1]]

            else:
                if info[i][0] is None:
                    data[0] += [first_line[i]]
                    if info[i][1] is None:
                        data[1] += [second_line[i]]
                    else:
                        data[1] += [info[i][1]]
                else:
                    data[0] += [info[i][0]]
                    if info[i][1] is None:
                        data[1] += [second_line[i]]
                    else:
                        data[1] += [info[i][1]]

        # for i in xrange(len(data[0])):
        #    if data[0][i] is None:
        #        d0 = "None"
        #    else:
        #        d0 =  repr(data[0][i])

        #    if data[1][i] is None:
        #        d1 = "None"
        #    else:
        #        d1 =  repr(data[1][i])

        #    print "data[0][" + str(i) + "] = " + d0 + "\n"
        #    print "data[1][" + str(i) + "] = " + d1 + "\n"

        Table.__init__(self, data, displ_as_qe=displ_as_qe)

        for elt in literals_positions:
            col_ref = literals_positions[elt]
            distance = len(data[0])
            final_col = None

            for i in range(len(complete_cols)):
                if abs(complete_cols[i] - col_ref) <= distance:
                    final_col = complete_cols[i]
                    distance = abs(complete_cols[i] - col_ref)

            literals_positions[elt] = (col_ref, final_col)

        self._crossproducts_info = literals_positions

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Table's coefficient
    def get_coeff(self):
        return self._coeff

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the info about Cross Products
    def get_crossproducts_info(self):
        return self._crossproducts_info

    coeff = property(get_coeff,
                     doc="the coefficient of the Table_UP")

    crossproducts_info = property(get_crossproducts_info,
                                  doc="infos about the cross products")
    # for instance, {'EF': (2,0), "GH": (3,0)} means Item 'EF' can
    # be calculated by a CrossProduct using columns 2 and 0, etc.

    # --------------------------------------------------------------------------
    ##
    #   @argument   arg is expected to be an object that exists in the cp info
    #   @brief Returns the CrossProductEquation matching the given arg
    def into_crossproduct_equation(self, arg):
        if arg not in self.crossproducts_info:
            raise ValueError('Got: ' + str(arg)
                             + ' instead of an object expected to exist'
                             'in self.crossproducts_info')

        col0 = self.crossproducts_info[arg][0]
        col1 = self.crossproducts_info[arg][1]

        col_temp = col1

        if col0 > col1:
            col1 = col0
            col0 = col_temp

        return CrossProductEquation((self.cell[0][col0],
                                     self.cell[0][col1],
                                     self.cell[1][col0],
                                     self.cell[1][col1]))


class QuotientsEquality(Table):
    """A shortcut to create Tables as quotients equalities."""

    def __init__(self, arg, displ_as_qe=True, ignore_1_denos=True,
                 subst_dict=None):
        """Initialization of the Table as a Quotients equality."""
        Table.__init__(self, arg, displ_as_qe=displ_as_qe,
                       ignore_1_denos=ignore_1_denos,
                       subst_dict=subst_dict)
