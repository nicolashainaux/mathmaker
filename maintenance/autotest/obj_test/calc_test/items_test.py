# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

import os
import sys
import locale

from lib.common import default

from core import *
from core.base_calculus import *

from maintenance.autotest import common

try:
    locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
except:
    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- ITEMS\n", 'utf-8'))

    item_1 = Item(1)
    item_minus_1 = Item(-1)
    item_minus_minus_1 = Item(('-', -1))
    item_a = Item('a')
    item_b = Item('b')
    item_minus_a = Item('-a')
    item_minus_minus_a = Item(('-', '-a'))
    item_minus_1_expon_item_minus_minus_1 = Item(('+',
                                                  -1,
                                                  item_minus_minus_1))
    item_minus_1_inside_expon_item_2 = Item(('+', -1, Item(2)))

    item_minus_1_expon_item_2 = Item(('-', 1, Item(2)))

    item_3_exponent_sum_minus_2_plus_6 = Item(('+', 3, Sum([-2, 6])))

    item_minus_3_inside_exponent_sum_minus_2_plus_5 = Item(('+',
                                                            -3,
                                                             Sum([-2, 5])
                                                           ))

    item_minus_5_inside_exponent_0 = Item(('+', -5, 0))

    item_2_power_minus_2_inside_power_4 = Item(('+', 2, Item(('+', -2, 4)) ))

    item_2_power_sum_minus_2_inside_power_4 = Item(('+',
                                                    2,
                                                    Sum([Item(('+', -2, 4))])
                                                   ))

    item_minus_2_inside_exponent_sum_1_and_0 = Item(('+', -2, Sum([1, 0]) ))

    item_minus_2_inside_exponent_sum_of_product_of_sum_1_and_0 = \
                                               Item(('+',
                                                     -2,
                                                     Sum([ Product([Sum([1, 0])
                                                                   ])
                                                         ])
                                                     ))

    item_minus_2_inside_exponent_sum_of_product_of_sum_1_and_1 = \
                                               Item(('+', -2,
                                                          Sum([
                                                          Product([Sum([1, 1])
                                                                  ])
                                                              ])
                                                     ))

    item_minus_2_inside_exponent_sum_of_sum_of_sum_1_and_1 = \
                                               Item(('+',
                                                     -2,
                                                      Sum([Sum([Sum([1, 1]) ])
                                                         ])
                                                    ))

    item_minus_2_inside_exponent_sum_of_sum_of_product_2_by_2 = \
                                               Item(('+',
                                                     -2,
                                                     Sum([Sum([Product([2, 2])
                                                               ])
                                                         ])
                                                    ))

    item_minus_2_inside_exponent_sum_of_product_of_sum_of_2 = \
                                               Item(('+', -2, Sum([Product([
                                                                       Sum([2])
                                                                          ])
                                                                  ])
                                                    ))

    item_6 = Item(6)

    item_to_round = Item(6.548)

    item_with_unit = Item(19.5)
    item_with_unit.set_unit('cm')


    #1
    check(item_1,
         ["1"])

    check(item_minus_1,
         ["-1"])

    check(item_minus_minus_1,
         ["-(-1)"])

    check(item_minus_minus_1.evaluate(),
         ["1"])

    #5
    check(item_a,
         ["a"])

    check(item_minus_a,
         ["-a"])

    check(item_minus_minus_a,
         ["-(-a)"])

    check(item_minus_1_expon_item_minus_minus_1,
         ["-1^{-(-1)}"])

    check(item_minus_1_expon_item_minus_minus_1.evaluate(),
         ["-1"])

    #10
    check(item_minus_1_inside_expon_item_2.is_numeric(),
         ["True"])

    check(item_minus_1_inside_expon_item_2.raw_value < 0,
         ["True"])

    check(item_minus_1_inside_expon_item_2.requires_inner_brackets(),
         ["True"])

    check(item_minus_1_inside_expon_item_2,
         ["(-1)^{2}"])

    check(item_minus_1_inside_expon_item_2.evaluate(),
         ["1"])

    #15
    check(item_minus_1_expon_item_2,
         ["-1^{2}"])

    check(item_minus_1_expon_item_2.evaluate(),
         ["-1"])

    check(item_3_exponent_sum_minus_2_plus_6,
         ["3^{-2+6}"])

    check(item_3_exponent_sum_minus_2_plus_6.evaluate(),
         ["81"])

    check(item_minus_3_inside_exponent_sum_minus_2_plus_5,
         ["(-3)^{-2+5}"])

    #20
    check(item_minus_3_inside_exponent_sum_minus_2_plus_5.evaluate(),
         ["-27"])

    check(item_minus_5_inside_exponent_0,
         ["1"])

    for i in range(len(common.machines)):
        test = common.machines[i].type_string(\
                                       item_minus_5_inside_exponent_0,
                                       force_display_exponent_0='OK')
        check(test, ["(-5)^{0}"])

    check(item_2_power_minus_2_inside_power_4,
         ["2^{(-2)^{4}}"])

    check(item_2_power_sum_minus_2_inside_power_4,
         ["2^{(-2)^{4}}"])

    #25 (will be shifted when adding a new machine kind)
    check(item_minus_2_inside_exponent_sum_1_and_0,
         ["-2"])

    check(item_minus_2_inside_exponent_sum_of_product_of_sum_1_and_0,
         ["-2"])

    check(item_minus_2_inside_exponent_sum_of_product_of_sum_1_and_1,
         ["(-2)^{1+1}"])

    item_minus_2_inside_exponent_sum_of_product_of_sum_1_and_1.exponent.term[
                                                  0].set_compact_display(False)
    check(item_minus_2_inside_exponent_sum_of_product_of_sum_1_and_1,
         ["(-2)^{1+1}"])


    check(item_minus_2_inside_exponent_sum_of_sum_of_sum_1_and_1,
         ["(-2)^{1+1}"])

    #30 (will be shifted when adding a new machine kind)
    check(item_minus_2_inside_exponent_sum_of_sum_of_product_2_by_2,
         ["(-2)^{2\\times 2}"])

    check(item_minus_2_inside_exponent_sum_of_product_of_sum_of_2,
         ["(-2)^{2}"])

    check(item_6.is_displ_as_a_single_1(),
         ["False"])

    check(item_to_round.digits_number(),
          ["3"])

    check(item_to_round.round(0),
          ["7"])

    #35
    check(item_to_round.round(1),
          [locale.str(6.5)])

    check(item_to_round.round(2),
          [locale.str(6.55)])

    check(item_to_round.round(3),
          [locale.str(6.548)])

    check(item_to_round.needs_to_get_rounded(0),
          ["True"])

    check(item_to_round.needs_to_get_rounded(1),
          ["True"])

    #40
    check(item_to_round.needs_to_get_rounded(2),
          ["True"])

    check(item_to_round.needs_to_get_rounded(3),
          ["False"])

    check(item_to_round.needs_to_get_rounded(4),
          ["False"])

    it = Item(2)
    couple = (it, None)

    check(str(it == None),
         ["False"])

    check(str((it, None) == (None, None)),
         ["False"])

    #45
    it0 = Item(0)
    check(str(it0 == Item(0)),
         ["True"])

    #46
    check(item_a.__lt__(item_b),
         ["True"])

    for i in range(len(common.machines)):
        test = common.machines[i].type_string(item_with_unit,
                                              display_unit='yes')
        check(test, ["19,5 cm"])
