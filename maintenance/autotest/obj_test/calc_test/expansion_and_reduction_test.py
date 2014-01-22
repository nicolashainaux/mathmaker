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

from lib.common import latex

from core import *
from core.base_calculus import *
from core.calculus import *

from maintenance.autotest import common

check = common.check


def action():
    if common.verbose:
        os.write(common.output, "--- --- EXPANSION & REDUCTION\n")

    expd_2_times_sum_of_1_and_5x = Expandable((Item(2),
                                               Sum([Item(1),
                                                    Monomial((5, 1))
                                                   ])
                                              ))

    expd_1_minus_11x_times_11_plus_7x = Expandable((Sum([Item(1),
                                                         Monomial((-11, 1))
                                                        ]),
                                                    Sum([Item(11),
                                                         Monomial((7, 1))
                                                        ])
                                                   ))

    expd_3x_minus_sum_xplus3_times_sum_6minus2x = \
    Sum([Monomial((3, 1)),
         Expandable((Item(-1),
                     Expandable((Sum([Item('x'), Item(3)]),
                                 Sum([Item(6), Monomial((2, 1))]) \
                                ))
                     ))
        ])

    expd_minus1_times_sum_3x_minus_2 = Expandable((Item(-1),
                                                   Sum([Monomial((3, 1)),
                                                        Item(-2)
                                                       ])
                                                  ))
    red_1 = Sum([Product([Item(-3), Item(10)]),
                 Product([Monomial(('-', 10, 1)), Monomial(('-', 9, 1))]),
                 Product([Monomial(('+', 7, 1)), Monomial(('+', 8, 1))]),
                 Product([Item(8), Item(10)])
                 ])

    red_2 = Product([Sum([Item(146)]), Item(('+', "x", 2))])

    # -2×(-6) - 1 + 3 × (-x) - 8x × (-3)
    red_3 = Sum([Product([Item(-2), Item(-6)]),
                 Item(-1),
                 Product([Item(3), Item(('-', "x", 1))]),
                 Product([Monomial(('-', 8, 1)), Item(-3)])
                ])

    # 5x + 7x × 8x + 5x × (-1) + 7×8
    red_4 = Sum([Monomial(('+', 5, 1)),
                 Product([Monomial(('+', 7, 1)), Monomial(('+', 8, 1))]),
                 Product([Monomial(('+', 5, 1)), Item(-1)]),
                 Product([Item(7), Item(8)])
                ])

    # -30 + 80 + x²
    red_5 = Sum([Item(-30), Item(80), Monomial(('+', 1, 2))])

    # 4x + (-15x + 8 - 5x)
    red_6 = Sum([Monomial(('+', 4, 1)),
                 Expandable((Monomial(('+', 1, 0)),
                             Polynomial([Monomial(('-', 15, 1)),
                                         Monomial(('+', 8, 0)),
                                         Monomial(('-', 5, 1))
                                        ])
                            ))
                ])

    # (3+3x)(3-3x)
    red_7 = BinomialIdentity((Item(3),
                             Monomial(('+', 3, 1))
                             ),
                            squares_difference='OK')

    # (1 - 10x)(1 + 10x)
    red_8 = BinomialIdentity((Item(1),
                             Monomial(('+', 10, 1))
                             ),
                            squares_difference='OK')

    # -2 -x + 8x² + x
    red_9 = Sum([Item(-2),
                 Monomial(('-', 1, 1)),
                 Monomial(('+', 8, 2)),
                 Monomial(('+', 1, 1))
                ])

    # -15 + (10 + 14x - 10x²)
    red_10 = Sum([Monomial((-15, 0)),
                  Expandable((Item(1),
                              Sum([Item(10),
                                   Monomial((14, 1)),
                                   Monomial(('-', 10, 2))
                                  ])
                             ))
                 ])

    # -(2x+9)(-3x-7)+4(-3x+9)+13
    red_11 = Sum([Expandable((Monomial(('-', 1, 0)),
                              Expandable((Sum([Monomial((2, 1)),
                                               Monomial((9, 0))
                                              ]),
                                          Sum([Monomial((-3, 1)),
                                               Monomial((-7, 0))
                                              ])
                                         ))
                            )),
                  Expandable((Monomial((4, 0)),
                              Sum([Monomial((-3, 1)),
                                   Monomial((9, 0))
                                  ])
                            )),
                  Monomial((13, 0))
                 ])


    dev_1 = Sum([Expandable((Monomial(('+', 7, 0)),
                             Sum([Monomial(('-', 6, 1)),
                                  Monomial((6, 0))
                                 ])
                            )),
                 BinomialIdentity((Monomial(('-', 10, 1)),
                                   Monomial(('-', 3, 0))
                                  ),
                                  difference_square='OK'
                                 )
                ])






    expr_1 = Expression("A", expd_2_times_sum_of_1_and_5x)
    check(expr_1.auto_expansion_and_reduction(),
         [  "$A=2(1+5x)$\\newline $A=2\\times 1+2\\times 5x$\\newline " \
          + "$A=2+10x$\\newline "])

    expr_2 = Expression("B", expd_1_minus_11x_times_11_plus_7x)
    check(expr_2.auto_expansion_and_reduction(),
         [ "$B=(1-11x)(11+7x)$\\newline $B=1\\times 11+1\\times 7x-11x\\times"\
          + " 11-11x\\times 7x$\\newline $B=11+7x-121x-77x^{2}$\\newline " \
          + "$B=11+(7-121)x-77x^{2}$\\newline $B=11-114x-77x^{2}$\\newline "])

    expr_3 = Expression("C", expd_3x_minus_sum_xplus3_times_sum_6minus2x)
    check(expr_3.auto_expansion_and_reduction(),
         [  "$C=3x-(x+3)(6+2x)$\\newline " \
          + "$C=3x-(x\\times 6+x\\times 2x+3\\times 6+3\\times 2x)$\\newline "\
          + "$C=3x-(6x+2x^{2}+18+6x)$\\newline " \
          + "$C=3x-6x-2x^{2}-18-6x$\\newline " \
          + "$C=(3-6-6)x-2x^{2}-18$\\newline " \
          + "$C=-9x-2x^{2}-18$\\newline "])

    expr_4 = Expression("D", expd_minus1_times_sum_3x_minus_2)
    check(expr_4.auto_expansion_and_reduction(),
         [  "$D=-(3x-2)$\\newline " \
          + "$D=-3x+2$\\newline "])

    expr_5 = Expression("E", red_1)
    check(expr_5.auto_expansion_and_reduction(),
         [  "$E=-3\\times 10-10x\\times (-9x)+7x\\times 8x+8\\times 10" \
          + "$\\newline $E=-30+90x^{2}+56x^{2}+80$\\newline " \
          + "$E=-30+80+(90+56)x^{2}$\\newline $E=50+146x^{2}$\\newline "])

    check(red_2.expand_and_reduce_next_step(),
         ["None"])

    expr_6 = Expression("F", red_3)
    check(expr_6.auto_expansion_and_reduction(),
         [  "$F=-2\\times (-6)-1+3\\times (-x)-8x\\times (-3)$\\newline " \
          + "$F=12-1-3x+24x$\\newline " \
          + "$F=11+(-3+24)x$\\newline " \
          + "$F=11+21x$\\newline "])


    # 5x + 7x × 8x + 5x × (-1) + 7×8
    expr_7 = Expression("G", red_4)
    check(expr_7.auto_expansion_and_reduction(),
         [  "$G=5x+7x\\times 8x+5x\\times (-1)+7\\times 8$\\newline " \
          + "$G=5x+56x^{2}-5x+56$\\newline " \
          + "$G=(5-5)x+56x^{2}+56$\\newline " \
          + "$G=0x+56x^{2}+56$\\newline " \
          + "$G=56x^{2}+56$\\newline "])


    expr_8 = Expression("H", red_5)
    check(expr_8.auto_expansion_and_reduction(),
         [  "$H=-30+80+x^{2}$\\newline " \
          + "$H=50+x^{2}$\\newline "])

    expr_9 = Expression("I", red_6)
    check(expr_9.auto_expansion_and_reduction(),
         [  "$I=4x+(-15x+8-5x)$\\newline " \
          + "$I=4x-15x+8-5x$\\newline " \
          + "$I=(4-15-5)x+8$\\newline " \
          + "$I=-16x+8$\\newline "])

    expr_10 = Expression("J", red_7)
    check(expr_10.auto_expansion_and_reduction(),
         [  "$J=(3+3x)(3-3x)$\\newline " \
          + "$J=3^{2}-(3x)^{2}$\\newline " \
          + "$J=9-9x^{2}$\\newline "])

    expr_11 = Expression("K", red_8)
    check(expr_11.auto_expansion_and_reduction(),
         [  "$K=(1+10x)(1-10x)$\\newline " \
          + "$K=1^{2}-(10x)^{2}$\\newline " \
          + "$K=1-100x^{2}$\\newline "])

    expr_12 = Expression("L", red_9)
    check(expr_12.auto_expansion_and_reduction(),
         [  "$L=-2-x+8x^{2}+x$\\newline " \
          + "$L=-2+(-1+1)x+8x^{2}$\\newline " \
          + "$L=-2+0x+8x^{2}$\\newline " \
          + "$L=-2+8x^{2}$\\newline "])

    expr_13 = Expression("M", red_10)
    check(expr_13.auto_expansion_and_reduction(),
         [  "$M=-15+(10+14x-10x^{2})$\\newline " \
          + "$M=-15+10+14x-10x^{2}$\\newline " \
          + "$M=-5+14x-10x^{2}$\\newline "])

    # -(2x+9)(-3x-7)+4(-3x+9)+13
    expr_14 = Expression("N", red_11)
    check(expr_14.auto_expansion_and_reduction(),
         [  "$N=-(2x+9)(-3x-7)+4(-3x+9)+13$\\newline " \
          + "$N=-(2x\\times (-3x)+2x\\times (-7)+9\\times (-3x)" \
                + "+9\\times (-7))+4\\times (-3x)+4\\times 9+13$\\newline " \
          + "$N=-(-6x^{2}-14x-27x-63)-12x+36+13$\\newline " \
          + "$N=6x^{2}+14x+27x+63-12x+49$\\newline " \
          + "$N=6x^{2}+(14+27-12)x+63+49$\\newline " \
          + "$N=6x^{2}+29x+112$\\newline "])

    # 7(-6x + 6) + (-10x - 3)²
    expr_15 = Expression("P", dev_1)
    check(expr_15.auto_expansion_and_reduction(),
         [  "$P=7(-6x+6)+(-10x-3)^{2}$\\newline " \
          + "$P=7\\times (-6x)+7\\times 6+(-10x)^{2}-2\\times (-10x)\\times 3"\
                + "+3^{2}$\\newline "\
          + "$P=-42x+42+100x^{2}+60x+9$\\newline "\
          + "$P=(-42+60)x+42+9+100x^{2}$\\newline "\
          + "$P=18x+51+100x^{2}$\\newline "
         ])




