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

import decimal

from core import *
from core.base_calculus import *

from maintenance.autotest import common

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- PRODUCTS\n", 'utf-8'))

    item_1 = Item(1)
    item_minus_1 = Item(-1)
    item_a = Item('a')
    item_b = Item('b')

    product_minus_a = Product([Item("-a")])
    product_minus_a_bis = Product([Item(('+', "-a", 1))])
    product_1_times_1 = Product([item_1, item_1])
    product_1_times_1_times_a = Product([item_1, item_1, item_a])
    product_2_times_minus_2 = Product([Item(2), Item(-2)])
    product_minus_2_times_2 = Product([Item(-2), Item(2)])

    product_8_times_minus_6 = Product([Monomial((8, 0)), Monomial((-6, 0))])

    product_2_times_a_times_b = Product([Item(2), item_a, item_b])
    product_1_times_minus_1 = Product([item_1, item_minus_1])
    product_1_times_minus_b_times_1_times_4 = Product([item_1,
                                                       Item('-b'),
                                                       item_1,
                                                       Item(4)])
    product_minus_1_times_minus_4 = Product([Item(-1), Item(-4)])

    product_minus_1_times_4 = Product([Item(-1), Item(4)])

    product_minus_1_times_1_times_1_times_1 = Product([Item(-1),
                                                       Item(1),
                                                       Item(1),
                                                       Item(1)])

    product_a_times_minus_b = Product([Item('a'), (Item('-b'))])
    product_a_times_minus_b.set_compact_display(False)

    product_a_times_ebd_minus_b = Product([Item('a'),
                                           Item(('+', "-b", 1))
                                          ])

    product_a_times_ebd_minus_b.set_compact_display(False)

    product_2_times_1 = Product([Item(2), (Item(1))])
    product_2_times_1.set_compact_display(False)

    product_1_times_7x = Product([Item(1), (Monomial((7, 1)))])
    product_1_times_7x.set_compact_display(False)

    product_minus_1_squared = Product(Item(-1))
    product_minus_1_squared.set_exponent(2)

    product_minus_3_times_minus_5_exponent_squared_minus_1 = \
                                                      Product([Item(-3),
                                                               Item(-5)])

    product_minus_3_times_minus_5_exponent_squared_minus_1.set_exponent(
                                                                  Item(('+',
                                                                        -1,
                                                                        2
                                                                       ))
                                                                        )

    product_4_times_product_minus_2_times_7 = Product([Item(4),
                                                       Product([Item(-2),
                                                                Item(7)])
                                                      ])

    product_4_times_product_minus_2_times_7_BIS = Product([Item(4),
                                                           Product([Item(-2),
                                                                    Item(7)
                                                                    ])
                                                          ])

    squared_product_minus_2_times_7 = Product([Item(-2), Item(7)])
    squared_product_minus_2_times_7.set_exponent(2)

    product_4_times_squared_product_minus_2_times_7 = Product([Item(4),
                                            squared_product_minus_2_times_7])

    sum_4_plus_2 = Sum([Item(4), Item(2)])
    product_7_times_sum_4_plus_2 = Product([Item(7), sum_4_plus_2])
    product_minus_1_times_sum_4_plus_2 = Product([Item(-1), sum_4_plus_2])

    product_sum_1_plus_2 = Product([Sum([1, 2])])

    product_1_by_sum_3_plus_4 = Product([1, Sum([3, 4])])

    product_sum_3_plus_4_by_1 = Product([Sum([3, 4]), 1])

    product_rubbish = Product([Item(('+', 1, 1)),
                                    Item(('+', "x", 1))])

    product_monom0_times_monom0 = Product([Monomial((7,0)),
                                           (Monomial((8,0))) ])
    product_monom0_times_monom0.set_compact_display(False)

    product_sum_3_plus_4_times_monom_minus8x = Product([Sum([Item(3),
                                                             Item(4)]),
                                                        Monomial((-8, 1))])

    product_4x_times_minus3x = Product([Monomial((4, 1)),
                                        Monomial((-3, 1))])

    product_nc_monomials_4_times_minus3 = Product([Monomial((4, 0)),
                                                   Monomial((-3, 0))])

    product_nc_monomials_4_times_minus3.set_compact_display(False)

    square_product_monom_6 = Product(Monomial(('+', 6, 0)))
    square_product_monom_6.set_exponent(2)

    square_product_square_item_6 = Product(Item(('+', 6, 2)))
    square_product_square_item_6.set_exponent(2)

    square_product_monom_x = Product(Monomial(('+', 1, 1)))
    square_product_monom_x.set_exponent(2)

    square_product_square_item_x = Product(Item(('+', 'x', 2)))
    square_product_square_item_x.set_exponent(2)

    product_minus1_fraction_2over3_fraction_3over4 = Product([Item(-1),
                                                              Fraction(('+',
                                                                        2,
                                                                        3)),
                                                              Fraction(('+',
                                                                        3,
                                                                        4))
                                                             ])

    product_fraction_6over2_times_fraction_8overminus5 = \
                                         Product([Fraction(('+', 6, 2)),
                                                  Fraction(('+', 8, -5))])

    product_fraction_minus3overminus2_times_fraction_minus1over5 = \
                                         Product([Fraction(('+', -3, -2)),
                                                  Fraction(('+', -1, 5))])

    product_3timesminusx = Product([Item(3), Item(('-', "x"))])

    product_0timesx = Product([Item(0), Item("x")])

    product_1square = Product(Item(1))
    product_1square.set_exponent(2)

    product_monom_minus1_times_minus7x = Product([Item(-1),
                                                  Product([
                                                           Monomial(('-', 7, 1))
                                                          ])
                                                ])
    product_monom_minus1_times_minus7x.set_compact_display(False)

    temp = Product([Item(('-', "a")),
                    Item(('+', "b"))
                  ])
    product_7_times_product_minusa_minusb = Product([Item(7),
                                                     temp
                                                    ])

    temp.set_compact_display(False)
    product_7_times_product_minusa_minusb_BIS \
                                          = Product([Item(7),
                                                     temp
                                                    ])

    temp = Product([Item(-2),
                    Item(7),
                    Item('a'),
                    Item('b')
                  ])
    product_9_times_minus2_times_7ab = Product([ Item(9),
                                                 Product([Item(-2),
                                                          Item(7),
                                                          Item('a'),
                                                          Item('b')
                                                          ])
                                                ])

    temp.set_compact_display(False)
    product_9_times_minus2_times_7ab_BIS = Product([ Item(9),
                                                     temp
                                                    ])


    temp = Product([Item(-2),
                    Item('a'),
                    Item(4),
                    Item('b')
                  ])
    product_9_times_minus2a_times_4b = Product([ Item(9),
                                                 temp
                                                ])

    temp.set_compact_display(False)
    product_9_times_minus2a_times_4b_BIS = Product([ Item(9),
                                                     temp
                                                    ])

    product_sum_minus1_plus_4_times_x = Product([
                                                 Sum([Item(-1),
                                                      Item(3)
                                                     ]),
                                                 Item('x')
                                                ])

    product_9_times_Monomial_minusx = Product([Item(9),
                                               Monomial(('-', 1, 1))
                                               ])

    product_10_times_minusminus4 = Product([Item(10),
                                            Product([Item(-1), Item(-4)])
                                           ])

    product_15_times_Monomial_3x = Product([Item(15),
                                            Sum([Item(0),
                                                 Monomial(('+', 3, 1))
                                               ])
                                          ])

    product_15_times_Monomial_3x_BIS = Product([Item(15), Sum([Item(0),
                                                       Monomial(('+', 3, 1))
                                                     ])
                                              ])

    product_15_times_Monomial_3x_TER = Product([Product([Item(15)]),
                                                Sum([Item(0),
                                                     Monomial(('+', 3, 1))
                                                   ])
                                              ])


    product_sum_2_3x_times_sum_minus4_6x = Product([Sum([Item(2),
                                                         Monomial(('+', 3, 1))
                                                         ]),
                                                    Sum([Item(-4),
                                                         Monomial(('+', 6, 1))
                                                         ])
                                                    ])

    product_item_minus0_times_item_x = Product([Item(('-', 0, 1)),
                                                Item(('+', 'x', 1))
                                              ])




    #1
    check(product_minus_a,
         ["-a"])

    check(product_minus_a.is_reducible(),
         ["False"])

    check(product_minus_a_bis.is_reducible(),
         ["False"])

    check(product_1_times_1,
         ["1"])

    #5
    check(product_1_times_1.is_reducible(),
         ["False"])

    product_1_times_1.set_compact_display(False)
    check(product_1_times_1,
         ["1\\times 1"])

    check(product_1_times_1_times_a,
         ["a"])


    check(product_1_times_1_times_a.is_reducible(),
         ["False"])

    check(product_2_times_minus_2,
         ["2\\times (-2)"])

    #10
    check(product_minus_2_times_2,
         ["-2\\times 2"])

    check(product_8_times_minus_6,
         ["8\\times (-6)"])

    check(product_2_times_a_times_b,
         ["2ab"])

    check(product_2_times_a_times_b.is_reducible(),
         ["False"])

    check(product_1_times_minus_1,
         ["-1"])

    product_1_times_minus_1.set_compact_display(False)

    #15
    check(product_1_times_minus_1,
         ["1\\times (-1)"])

    check(product_1_times_minus_b_times_1_times_4,
         ["-b\\times 4"])

    check(product_1_times_minus_b_times_1_times_4.is_reducible(),
         ["True"])

    product_1_times_minus_b_times_1_times_4.set_compact_display(False)
    check(product_1_times_minus_b_times_1_times_4,
         ["1\\times (-b)\\times 1\\times 4"])

    check(product_minus_1_times_minus_4,
         ["-(-4)"])

    #20
    check(product_minus_1_times_4,
         ["-4"])

    check(product_minus_1_times_minus_4.is_reducible(),
         ["True"])

    check(product_minus_1_times_minus_4.evaluate(),
         ["4"])

    check(product_minus_1_times_1_times_1_times_1,
         ["-1"])

    check(product_minus_1_times_1_times_1_times_1.is_reducible(),
         ["False"])

    #25
    check(product_a_times_minus_b,
         ["a\\times (-b)"])

    check(product_a_times_minus_b.is_reducible(),
         ["True"])

    check(product_a_times_ebd_minus_b,
         ["a\\times (-b)"])

    check(product_a_times_ebd_minus_b.is_reducible(),
         ["True"])

    check(product_2_times_1.is_reducible(),
         ["True"])

    #30
    check(product_1_times_7x.is_reducible(),
         ["True"])


    check(product_minus_1_squared,
         ["(-1)^{2}"])

    check(product_minus_1_squared.is_displ_as_a_single_1(),
         ["False"])

    check(product_minus_1_squared.is_displ_as_a_single_minus_1(),
         ["False"])

    check(product_minus_1_squared.is_reducible(),
         ["True"])

    #35
    check(product_minus_3_times_minus_5_exponent_squared_minus_1,
         ["(-3\\times (-5))^{(-1)^{2}}"])

    check(product_minus_3_times_minus_5_exponent_squared_minus_1.evaluate(),
         ["15"])

    check(product_4_times_product_minus_2_times_7,
         ["4\\times (-2)\\times 7"])

    check(product_4_times_product_minus_2_times_7_BIS,
         ["4\\times (-2)\\times 7"])

    check(product_4_times_product_minus_2_times_7.evaluate(),
         ["-56"])

    #40
    check(product_4_times_squared_product_minus_2_times_7,
         ["4\\times (-2\\times 7)^{2}"])

    check(product_4_times_squared_product_minus_2_times_7.is_reducible(),
         ["True"])

    check(product_4_times_squared_product_minus_2_times_7.evaluate(),
         ["784"])

    check(product_7_times_sum_4_plus_2,
         ["7(4+2)"])

    product_7_times_sum_4_plus_2.set_compact_display(False)
    check(product_7_times_sum_4_plus_2,
         ["7\\times (4+2)"])

    #45
    check(product_7_times_sum_4_plus_2.evaluate(),
         ["42"])

    check(product_minus_1_times_sum_4_plus_2,
         ["-(4+2)"])

    check(product_minus_1_times_sum_4_plus_2.evaluate(),
         ["-6"])

    check(product_sum_1_plus_2,
         ["1+2"])

    check(product_1_by_sum_3_plus_4,
         ["3+4"])

    #50
    check(product_sum_3_plus_4_by_1,
         ["3+4"])

    check(product_sum_3_plus_4_by_1.is_reducible(),
         ["False"])

    check(product_rubbish,
         ["x"])

    check(product_rubbish.is_reducible(),
         ["False"])

    check(product_monom0_times_monom0,
         ["7\\times 8"])

    #55
    check(product_sum_3_plus_4_times_monom_minus8x,
         ["(3+4)\\times (-8x)"])

    check(product_4x_times_minus3x,
         ["4x\\times (-3x)"])

    check(product_nc_monomials_4_times_minus3,
         ["4\\times (-3)"])

    check(square_product_monom_6,
         ["6^{2}"])

    check(square_product_square_item_6,
         ["(6^{2})^{2}"])

    #60
    check(square_product_monom_x,
         ["x^{2}"])

    check(square_product_square_item_x,
         ["(x^{2})^{2}"])

    check(product_minus1_fraction_2over3_fraction_3over4,
         ["-\\frac{2}{3}\\times \\frac{3}{4}"])

    check(product_fraction_6over2_times_fraction_8overminus5,
         ["\\frac{6}{2}\\times \\frac{8}{-5}"])

    check( \
    product_fraction_minus3overminus2_times_fraction_minus1over5
                                                    .calculate_next_step(),
         ["-\\frac{3\\times 1}{2\\times 5}"])

    #65
    check(product_3timesminusx,
         ["3\\times (-x)"])

    check(product_3timesminusx.is_reducible(),
         ["True"])

    check(product_0timesx,
         ["0x"])

    check(product_0timesx.is_reducible(),
         ["True"])

    check(product_1square.is_displ_as_a_single_1(),
         ["False"])

    #70
    check(product_1square.is_reducible(),
         ["True"])


    check(product_monom_minus1_times_minus7x,
         ["-1\\times (-7x)"])

    check(product_7_times_product_minusa_minusb,
         ["7\\times (-ab)"])

    check(product_7_times_product_minusa_minusb_BIS,
         ["7\\times (-a)\\times b"])

    check(product_9_times_minus2_times_7ab,
         ["9\\times (-2)\\times 7ab"])

    #75
    check(product_9_times_minus2_times_7ab_BIS,
         ["9\\times (-2)\\times 7\\times a\\times b"])

    check(product_9_times_minus2a_times_4b,
         ["9\\times (-2a)\\times 4b"])

    check(product_9_times_minus2a_times_4b_BIS,
         ["9\\times (-2)\\times a\\times 4\\times b"])

    check(product_sum_minus1_plus_4_times_x,
         ["(-1+3)x"])

    check(product_9_times_Monomial_minusx,
         ["9\\times (-x)"])

    #80
    check(product_10_times_minusminus4,
         ["10\\times (-(-4))"])

    check(product_15_times_Monomial_3x,
         ["15\\times 3x"])

    check(product_15_times_Monomial_3x_BIS,
         ["15\\times 3x"])

    check(product_15_times_Monomial_3x_TER,
         ["15\\times 3x"])

    check(product_sum_2_3x_times_sum_minus4_6x.is_reducible(),
         ["False"])

    #check(product_item_minus0_times_item_x.is_displ_as_a_single_0(),
    #     ["True"])

    p = Product([Monomial(('-', 10, 1))])
    p.set_exponent(2)

    check(p,
         ["(-10x)^{2}"])

    check(p.calculate_next_step(),
         ["100x^{2}"])

    fraction_and_item = Product([Fraction((Item(5), Item(7))),
                                 Item(8)
                                ])

    check(fraction_and_item.calculate_next_step(),
         ["\\frac{5\\times 8}{7}"])

    fraction_and_item = Product([Item(8),
                                 Fraction((Item(5), Item(7)))
                                ])

    check(fraction_and_item.calculate_next_step(),
         ["\\frac{8\\times 5}{7}"])

    fractions_and_items = Product([Fraction((Item(3), Item(5))),
                                   Item(8),
                                   Fraction((Item(7), Item(11))),
                                   Item(4),
                                   Fraction((Item(13), Item(17)))
                                  ])

    check(fractions_and_items.calculate_next_step(),
         ["\\frac{3\\times 8\\times 7\\times 4\\times 13}"\
          + "{5\\times 11\\times 17}"])



    if common.verbose:
        os.write(common.output, "\n--- PRODUCTS - evaluate\n")

    a = Item(2.5)
    b = Item(3.5)

    check(isinstance(a.evaluate(), decimal.Decimal),
         ["True"])

    c = Product([a, b]).evaluate()

    check(isinstance(c, decimal.Decimal),
         ["True"])

    check(c,
         ["8.75"])

    d = Fraction((Item(3), Item(8)))

    check(d.evaluate(),
         ["0.375"])

    e = Fraction((Item(3), Item(7)))

    check(e.evaluate(),
         ["0.4285714285714285714285714286"])

    check(e.evaluate(keep_not_decimal_nb_as_fractions=True),
         ["\\frac{3}{7}"])

    f = Product([Fraction((Item(3), Item(7))),
                 Fraction((Item(7), Item(4)))])

    check(f.evaluate(),
         ["0.75"])

    check(f.evaluate(keep_not_decimal_nb_as_fractions=True),
         ["0.75"])

    g = Product([Item(6),
                 Fraction((Item(5), Item(3)))])

    check(g.evaluate(),
         ["10"])
