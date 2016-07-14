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

import math
import random
from mathmaker.lib import error
from mathmaker.lib.maths_lib import gcd

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
#   @brief Collection of functions that return randomly results


# --------------------------------------------------------------------------
##
#   @brief Return a random integer
#   @param min_value The lowest possible value of the result
#   @param max_value The highest possible value of the result
#   @param **options It is possible to use a weighted table
#   The weighted table is a probability distribution: the sum of its values
#   must be 1 and the number of values must match the number of possible
#   results. Here's an example: [0.2, 0.4, 0.3, 0.1].
#   @return An integer comprised between min_value & max_value
def integer(min_value, max_value, **options):
    if not ('weighted_table' in options
            and len(options['weighted_table']) == max_value - min_value + 1):
        # __
        return int(math.ceil(random.random() * (max_value - min_value + 1)
                             + min_value)
                   - 1)

    else:
        # The probability scale will be calculated there from the weighted
        # table's date. For instance, [0.2, 0.4, 0.3, 0.1]
        #                       gives [0.2, 0.6, 0.9, 1.0] as a result
        proba_scale = list()
        current_sum = 0
        for i in range(len(options['weighted_table'])):
            current_sum += options['weighted_table'][i]
            proba_scale.append(current_sum)

        random_number = random.random()
        last_step = 0

        for i in range(len(proba_scale)):
            if random_number >= last_step and random_number < proba_scale[i]:
                return min_value + i
            else:
                last_step = random_number

        return max_value


# --------------------------------------------------------------------------
##
#   @brief Returns a '+' or a '-'
#   @param options plus_signs_ratio=0.3 sets the + signs ratio (default 0.5)
#   @return A random sign ('+' or '-')
def sign(**options):
    plus_signs_ratio = 0.5

    if 'plus_signs_ratio' in options                                          \
       and options['plus_signs_ratio'] >= 0                                   \
       and options['plus_signs_ratio'] <= 1:
        # __
        plus_signs_ratio = options['plus_signs_ratio']

    if (random.random() < plus_signs_ratio):
        return '+'
    else:
        return '-'


# --------------------------------------------------------------------------
##
#   @brief Pops an element from the provided list
#   @param provided_list The list where to pop an element from
#   @return The randomly chosen element
def pop(provided_list, **options):
    if not ('weighted_table' in options
            and len(options['weighted_table']) == len(provided_list)):
        # __
        random_rank = integer(0, len(provided_list) - 1)

        return provided_list.pop(random_rank)

    else:
        i = integer(0, len(provided_list) - 1, **options)
        return provided_list.pop(i)


# --------------------------------------------------------------------------
##
#   @brief Returns a randomly decimal number between 0 and 1
#   @return A randomly decimal number between 0 and 1
def decimal_0_1():
    return random.random()


# --------------------------------------------------------------------------
##
#   @brief Returns True|False with probability distribution 0,5 - 0,5
#   @return True|False with probability distribution 0,5 - 0,5
def heads_or_tails():
    if random.random() > 0.5:
        return True
    else:
        return False


# --------------------------------------------------------------------------
##
#   @brief Returns a randomly integer which is coprime to the given argument
#   @param n The given number
#   @param range As a list, numbers where to pop one what will be coprime to n.
#   @return A randomly integer which is coprime to the given argument
def coprime_to(n, range):
    collected_numbers = []

    for number in range:
        if gcd(n, number) == 1:
            collected_numbers.append(number)

    if len(collected_numbers) == 0:
        raise error.ImpossibleAction("find a number coprime to n "
                                     "in the given range.")

    else:
        return pop(collected_numbers)


# --------------------------------------------------------------------------
##
#   @brief Returns a randomly integer which is coprime to the given argument
#          but possibly not to the second.
#   @param n The given number, what the result should be coprime to
#   @param p The given number, what the result should not be coprime to
#   @param range As a list, numbers where to look for.
#   @return A randomly integer which is coprime to the given argument
#          but possibly not to the second.
def coprime_to_the_first(n, p, range):
    collected_numbers_coprime_to_n = []
    collected_numbers_not_coprime_to_p = []
    collected_numbers = []

    for number in range:
        if gcd(n, number) == 1:
            collected_numbers_coprime_to_n.append(number)

    for number in range:
        if gcd(p, number) > 1:
            collected_numbers_not_coprime_to_p.append(number)

    for number in collected_numbers_coprime_to_n:
        if number in collected_numbers_not_coprime_to_p:
            collected_numbers.append(number)

    if len(collected_numbers) >= 1:
        return pop(collected_numbers)

    else:
        if len(collected_numbers_coprime_to_n) == 0:
            raise error.ImpossibleAction("find a number coprime to n "
                                         "in the given range.")

        else:
            return pop(collected_numbers_coprime_to_n)


# --------------------------------------------------------------------------
##
#   @brief Returns a randomly integer which is not coprime to the given arg.
#   @warning    If the given argument is a prime number, it'll be difficult
#               to find an integer which is not coprime to it, especillay if
#               the range is low.
#   @param n The given number, what the result must be coprime to
#   @param range As a list, numbers where to look for.
#   @return A randomly integer which is not coprime to the given argument.
def not_coprime_to(n, range, **options):
    collected_numbers = []
    check = False
    avoid = 0

    if 'excepted' in options:
        check = True
        avoid = options['excepted']

    for number in range:
        if gcd(n, number) != 1:
            if not (check and number == avoid):
                collected_numbers.append(number)

    if len(collected_numbers) == 0:
        raise error.ImpossibleAction("find a number not coprime to n "
                                     + "in the given range.")

    else:
        return pop(collected_numbers)


# --------------------------------------------------------------------------
##
#   @brief When given a list of objects, returns a randomly mixed list of the
#   @brief same objects. Must not return in the same order than given one.
#   @param objects_list
#   @return a list
def mix(objects_list):
    result = []

    order_changed = False

    for i in range(len(objects_list) - 2):
        j = integer(0, len(objects_list) - 1)

        if i != j and order_changed is False:
            order_changed = True

        next_to_add = objects_list[j].clone()
        objects_list.pop(j)

        result.append(next_to_add)

    if order_changed:
        next_to_add = pop(objects_list).clone()
        result.append(next_to_add)
        next_to_add = pop(objects_list).clone()
        result.append(next_to_add)

    else:
        next_to_add = objects_list[1].clone()
        result.append(next_to_add)
        next_to_add = objects_list[0].clone()
        result.append(next_to_add)

    return result
