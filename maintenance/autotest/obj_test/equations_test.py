# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

from lib.common.settings import default
from lib.common import latex

from core import *
from core.base_calculus import *
from core.calculus import *

from maintenance.autotest import common

try:
    locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
except:
    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- EQUATIONS\n", 'utf-8'))

    eq_basic1 = Equation((Polynomial([Monomial(('+', 1, 1)),
                                      Monomial(('+', 7, 0))
                                     ]),
                          Item(3)
                          ),
                         number=1)

    eq_basic2 = Equation((Polynomial([Monomial(('-', 8, 0)),
                                      Monomial(('+', 1, 1))
                                     ]),

                          Item(-2)
                          ),
                          number=1)

    eq_basic_r1 = Equation((Item(-5),
                            Polynomial([Monomial(('+', 1, 1)),
                                        Monomial(('+', 3, 0))
                                       ]),
                            ),
                            number=1)

    eq_basic_r2 = Equation((Item(-6),
                            Monomial(('+', 5, 1))
                            ),
                            number=1)


    eq_basic3 = Equation((Monomial(('+', 8, 1)),
                          Item(1)
                          ),
                          number=1)


    eq_basic4 = Equation((Monomial(('+', 12, 1)),
                          Item(8)
                          ),
                          number=1)

    eq_standard1 = Equation((Polynomial([Monomial(('+', 2, 1)),
                                         Monomial(('+',  3, 0))
                                        ]),
                             Item(8)
                             ),
                             number=1)

    # 19+3x=2x
    eq_standard2 = Equation((Polynomial([Monomial(('+', 19, 0)),
                                         Monomial(('+',  3, 1))
                                        ]),
                             Monomial(('+', 2, 1))
                             ),
                             number=1)

    eq_difficult1 = Equation((Polynomial([Monomial(('+', 4, 1)),
                                          Monomial(('+', 2, 0))
                                         ]),
                              Polynomial([Monomial(('-', 3, 0)),
                                          Monomial(('+', 2, 1))
                                         ])
                             ),
                             number=1)

    eq_difficult2 = Equation((Polynomial([Monomial(('-', 2, 1)),
                                          Monomial(('+', 5, 0))
                                         ]),
                              Polynomial([Monomial(('+', 3, 1)),
                                          Monomial(('-', 4, 0))
                                         ])
                             ),
                             number=1)

    eq_difficult3 = Equation((Polynomial([Monomial(('+', 5, 0)),
                                          Monomial(('+', 4, 1))
                                         ]),
                              Polynomial([Monomial(('-', 20, 1)),
                                          Monomial(('+', 3, 0))
                                         ])
                             ),
                             number=1)
    # 5-x=5x
    eq_difficult4 = Equation((Polynomial([Monomial(('+', 5, 0)),
                                          Monomial(('-', 1, 1))
                                         ]),
                              Polynomial([Monomial(('+', 5, 1))
                                          ])
                             ),
                             number=1)

    eq_leading_to_0 = Equation((Polynomial([Monomial(('+', 2, 1)),
                                            Monomial(('+', 1, 0))
                                           ]),
                                Item(1)
                                ),
                                number=1)

    eq_leading_to_0_bis = Equation((Polynomial([Monomial(('+', 1, 1)),
                                                Monomial(('+', 5, 0))
                                               ]),
                                    Polynomial([Monomial(('+', 1, 1)),
                                                Monomial(('+', 2, 0))
                                              ])
                                 ),
                                 number=1)

    eq_leading_to_0_ter = Equation((Sum([Monomial(('+', 3, 0)),
                                         Monomial(('+', 10, 1))]),
                                    Monomial(('+', 10, 1))
                                  ))

    eq_impossible = Equation((Item(1), Item(2)), number=1)

    # 9x+9(-4-x)=8
    eq_impossible_2 = Equation((Sum([Monomial(('+', 9, 1)),
                                     Expandable((Monomial(('+', 9, 0)),
                                                 Sum([Monomial(('-',
                                                                4,
                                                                0)),
                                                      Monomial(('-',
                                                                1,
                                                                1))
                                                     ])
                                                ))
                                     ]),
                                 Item(8)
                                ),
                                number=1
                               )

    eq_infinity_of_solutions = Equation((Item(2), Item(2)), number=1)



    # -(-11x-10)=(-15+12x)-1
    eq_with_expd_1 = Equation((Expandable((Item(-1),
                                           Sum([Monomial((-11, 1)),
                                                Item(-10)
                                               ])
                                          )),
                               Sum([Expandable((Item(1),
                                                Sum([Item(-15),
                                                     Monomial((12, 1))
                                                    ])
                                              )),
                                    Item(-1)
                                   ])
                              ),
                              number=1)

    # -8+9-1 = 10(-2-12x)
    eq_with_expd_2 = Equation((Sum([Monomial(('-', 8, 0)),
                                    Monomial(('+', 9, 0)),
                                    Monomial(('-', 1, 0))
                                   ]),
                               Expandable((Item(10),
                                           Sum([Item(-2),
                                                Monomial((-12, 1))
                                               ])
                                          ))
                               ),
                        number=1)

    # -x-2x+7=(7x+5)
    eq_with_expd_3 = Equation((Sum([Monomial(('-', 1, 1)),
                                    Monomial(('-', 2, 1)),
                                    Monomial(('+', 7, 0))
                                   ]),
                               Expandable((Item(1),
                                           Sum([Monomial(('+', 7, 1)),
                                                Monomial(('+', 5, 0))
                                               ])
                                          ))
                               ),
                        number=1)

    # 5x=(2-5x)-2
    eq_with_expd_4 = Equation((Sum([Monomial(('+', 5, 1))
                                   ]),
                               Sum([
                                    Expandable((Item(1),
                                           Sum([Monomial(('+', 2, 0)),
                                                Monomial(('-', 5, 1))
                                               ])
                                              )),
                                    Monomial(('-', 2, 0))
                                   ])
                               ),
                        number=1)


    # - 1 - 4x = -9
    eq_buggy = Equation((Sum([Monomial(('-', 1, 0)), Monomial(('-', 4, 1))]),
                         Monomial(('-', 9, 0))
                         ))


    # 3(-9+6x)-8=9
    eq_with_expd_5 = Equation((Sum([Expandable((Item(3),
                                           Sum([Monomial(('-', 9, 0)),
                                                Monomial(('+', 6, 1))
                                               ])
                                              )),
                                    Item(-8)
                                   ]),
                              (Sum([Item(9)
                                   ])
                               )),
                        number=1)

    # 5=(x-2)+7
    eq_with_expd_6 = Equation((Item(5),
                               Sum([Expandable((Item(1),
                                                Sum([Monomial(('+', 1, 1)),
                                                     Monomial(('-', 2, 0))])
                                                )),
                                    Item(7)
                                   ])
                               ),
                               number=1)

    # x = 4² + 5²
    eq_with_exponents_1 = Equation((Monomial(('+', 1, 1)),
                                    Sum([Item(('+', 4, 2)),
                                         Item(('+', 5, 2))])
                                    ),
                                    number=1
                                  )

    # 5² = 4² + x
    eq_with_exponents_2 = Equation((Item(('+', 5, 2)),
                                    Sum([Item(('+', 4, 2)),
                                         Monomial(('+', 1, 1))])
                                    ),
                                    number=1
                                  )

    # 2x = 1 (to test with option decimal_result=1)
    eq_with_decimal_result_01 = Equation((Monomial(('+', 2, 1)),
                                          Item(1)
                                          ),
                                         number=1
                                         )

    # 3x = 1 (to test with option decimal_result=2)
    eq_with_decimal_result_02 = Equation((Monomial(('+', 3, 1)),
                                          Item(1)
                                          ),
                                         number=1
                                         )

    # 8x = 6 (to test with option decimal_result=2)
    eq_with_decimal_result_03 = Equation((Monomial(('+', 8, 1)),
                                          Item(6)
                                          ),
                                         number=1
                                         )

    # x = 4² + 5² (to test *with* the option decimal_result=2)
    eq_with_decimal_result_04 = eq_with_exponents_1

    # x = 1/4 + 1/8 (to test with/without option decimal_result=2)
    eq_with_decimal_result_05 = Equation((Monomial(('+', 1, 1)),
                                          Sum([Fraction((Item(1), Item(4))),
                                               Fraction((Item(1), Item(8)))
                                              ])
                                          ),
                                         number=1
                                         )

    # AB = 3² + 4² (to test with/without option decimal_result=0 / 1)
    eq_with_different_variable_letter = Equation((Item("AB"),
                                                  Sum([Item(('+', 3, 2)),
                                                       Item(('+', 4, 2))])
                                                  ),
                                                  number=1,
                                                  variable_letter_name="AB")

    # x = sqrt{5}
    eq_with_sqrt5 = Equation((Monomial(('+', 1, 1)),
                              SquareRoot(Item(5))))

    # x = sqrt{16}
    eq_with_sqrt16 = Equation((Monomial(('+', 1, 1)),
                               SquareRoot(Item(16))))

    # x² = 16
    eq_with_xsquare_equal_to_16 = Equation((Monomial(('+', 1, 2)),
                                            (Item(16))
                                            ))

    # x² = 5
    eq_with_xsquare_equal_to_5 = Equation((Monomial(('+', 1, 2)),
                                           (Item(5))
                                          ))

    # 73² = 48² + AB²
    pythagorean_1 = Equation((Item(('+', 73, 2)),
                              Sum([Item(('+', 48, 2)),
                                   Item(('+', "AB", 2))])
                             ),
                             number=1,
                             variable_letter_name="AB")

    # EF² = 60² + 91²
    pythagorean_2 = Equation((Item(('+', "EF", 2)),
                              Sum([Item(('+', 60, 2)),
                                   Item(('+', 91, 2))])
                             ),
                             number=1,
                             variable_letter_name="AB")

    # 2/3 x = 4/5
    with_fractions = Equation((Monomial((Fraction((Item(2), Item(3))), 1)),
                               Fraction((Item(4), Item(5)))
                               ))

    # 1/4 x + 1/7 = - 3/14
    with_fractions2 = Equation((Sum([Monomial((Fraction((Item(1), Item(4))),
                                               1
                                               )),
                                     Fraction((Item(1), Item(7)))
                                     ]),
                                 Fraction(('-', Item(3), Item(14)))
                                ))

    # 2 x - 1/5 = 4/5
    with_fractions3 = Equation((Sum([Monomial((Fraction((Item(2), Item(1))\
                                                        ).simplified(),
                                               1
                                               )),
                                     Fraction((Item(1), Item(5)))
                                     ]),
                                 Fraction(('-', Item(4), Item(5)))
                                ))



# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------


    # 01
    check(eq_basic1.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[x+7=3\]" \
          + "\[x=3-7\]" \
          + "\[x=-4\]" ])

    # 02
    check(eq_basic2.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[-8+x=-2\]" \
          + "\[x=-2+8\]" \
          + "\[x=6\]" ])

    # 03
    check(eq_basic_r1.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[-5=x+3\]" \
          + "\[x=-5-3\]" \
          + "\[x=-8\]" ])

    # 04
    check(eq_basic_r2.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[-6=5x\]" \
          + "\[x=-\\frac{6}{5}\]"])


    check(eq_basic3.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[8x=1\]" \
          + "\[x=\\frac{1}{8}\]"])

    # 06
    check(eq_basic4.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[12x=8\]" \
          + "\[x=\\frac{8}{12}\]" \
          + "\[x=\\frac{\\bcancel{4}\\times 2}{\\bcancel{4}\\times 3}\]" \
          + "\[x=\\frac{2}{3}\]" ])


    check(eq_standard1.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[2x+3=8\]" \
          + "\[2x=8-3\]" \
          + "\[2x=5\]" \
          + "\[x=\\frac{5}{2}\]"])

    # 08
    check(eq_standard2.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[19+3x=2x\]" \
          + "\[3x-2x=-19\]" \
          + "\[(3-2)x=-19\]" \
          + "\[x=-19\]"])

    check(eq_difficult1.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[4x+2=-3+2x\]" \
          + "\[4x-2x=-3-2\]" \
          + "\[(4-2)x=-5\]" \
          + "\[2x=-5\]" \
          + "\[x=-\\frac{5}{2}\]"])

    # 10
    check(eq_leading_to_0.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[2x+1=1\]" \
          + "\[2x=1-1\]" \
          + "\[2x=0\]" \
          + "\[x=0\]" ])


    check(eq_impossible.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[1=2\]" \
          + "This equation has no solution.\\newline "])


    # 12
    check(eq_impossible_2.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[9x+9(-4-x)=8\]" \
          + "\[9x+9\\times (-4)+9\\times (-x)=8\]" \
          + "\[9x-36-9x=8\]" \
          + "\[(9-9)x-36=8\]" \
          + "\[0x-36=8\]" \
          + "\[-36=8\]" \
          + "This equation has no solution.\\newline "])

    check(eq_leading_to_0_bis.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[x+5=x+2\]" \
          + "\[x-x=2-5\]" \
          + "\[(1-1)x=-3\]" \
          + "\[0x=-3\]" \
          + "\[0=-3\]" \
          + "This equation has no solution.\\newline "])


    # 14
    check(eq_leading_to_0_ter.auto_resolution(),
         [  "$(E): $" \
          + "\[3+10x=10x\]" \
          + "\[10x-10x=-3\]" \
          + "\[(10-10)x=-3\]" \
          + "\[0x=-3\]" \
          + "\[0=-3\]" \
          + "This equation has no solution.\\newline "])


    # 15
    eq_infinity_of_solutions
    check(eq_infinity_of_solutions,
         ["2=2"])

    eq_infinity_of_solutions_letter = eq_infinity_of_solutions.variable_letter

    # 16
    eq_infinity_of_solutions = eq_infinity_of_solutions.solve_next_step()
    check(eq_infinity_of_solutions,
         [_("Any value of") + " " \
          + eq_infinity_of_solutions_letter \
          + " " + _("is solution of the equation.")])

    # 17
    check(eq_difficult2.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[-2x+5=3x-4\]" \
          + "\[-2x-3x=-4-5\]" \
          + "\[(-2-3)x=-9\]" \
          + "\[-5x=-9\]" \
          + "\[x=\\frac{-9}{-5}\]" \
          + "\[x=\\frac{9}{5}\]"])

    check(eq_difficult3.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[5+4x=-20x+3\]" \
          + "\[4x+20x=3-5\]" \
          + "\[(4+20)x=-2\]" \
          + "\[24x=-2\]" \
          + "\[x=-\\frac{2}{24}\]" \
          + "\[x=-\\frac{\\bcancel{2}}{\\bcancel{2}\\times 12}\]" \
          + "\[x=-\\frac{1}{12}\]"])

    # 19
    check(eq_difficult4.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[5-x=5x\]" \
          + "\[-x-5x=-5\]" \
          + "\[(-1-5)x=-5\]" \
          + "\[-6x=-5\]" \
          + "\[x=\\frac{-5}{-6}\]"\
          + "\[x=\\frac{5}{6}\]"])


    check(eq_with_expd_1.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[-(-11x-10)=(-15+12x)-1\]" \
          + "\[11x+10=-15+12x-1\]" \
          + "\[11x+10=-15-1+12x\]" \
          + "\[11x+10=-16+12x\]" \
          + "\[11x-12x=-16-10\]" \
          + "\[(11-12)x=-26\]" \
          + "\[-x=-26\]" \
          + "\[x=26\]" ])

    # 21
    check(eq_with_expd_2.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[-8+9-1=10(-2-12x)\]" \
          + "\[0=10\\times (-2)+10\\times (-12x)\]" \
          + "\[0=-20-120x\]" \
          + "\[120x=-20\]" \
          + "\[x=-\\frac{20}{120}\]" \
          + "\[x=-\\frac{\\bcancel{10}\\times 2}{\\bcancel{10}\\times 12}\]" \
          + "\[x=-\\frac{\\bcancel{2}}{\\bcancel{2}\\times 6}\]" \
          + "\[x=-\\frac{1}{6}\]"])

    check(eq_with_expd_3.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[-x-2x+7=(7x+5)\]" \
          + "\[(-1-2)x+7=7x+5\]" \
          + "\[-3x+7=7x+5\]" \
          + "\[-3x-7x=5-7\]" \
          + "\[(-3-7)x=-2\]" \
          + "\[-10x=-2\]" \
          + "\[x=\\frac{-2}{-10}\]" \
          + "\[x=\\frac{+\\bcancel{2}}{+\\bcancel{2}\\times 5}\]" \
          + "\[x=\\frac{1}{5}\]" ])

    # 23
    check(eq_with_expd_4.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[5x=(2-5x)-2\]" \
          + "\[5x=2-5x-2\]" \
          + "\[5x=2-2-5x\]" \
          + "\[5x=-5x\]" \
          + "\[5x+5x=0\]" \
          + "\[(5+5)x=0\]" \
          + "\[10x=0\]" \
          + "\[x=0\]" ])

    # 24
    check(eq_buggy.auto_resolution(),
         [  "$(E): $" \
          + "\[-1-4x=-9\]" \
          + "\[-4x=-9+1\]" \
          + "\[-4x=-8\]" \
          + "\[x=\\frac{-8}{-4}\]" \
          + "\[x=\\frac{+\\bcancel{4}\\times 2}{+\\bcancel{4}}\]" \
          + "\[x=2\]"])


    check(eq_with_expd_5.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[3(-9+6x)-8=9\]" \
          + "\[3\\times (-9)+3\\times 6x-8=9\]" \
          + "\[-27+18x-8=9\]" \
          + "\[-27-8+18x=9\]" \
          + "\[-35+18x=9\]" \
          + "\[18x=9+35\]" \
          + "\[18x=44\]" \
          + "\[x=\\frac{44}{18}\]"  \
          + "\[x=\\frac{\\bcancel{2}\\times 22}{\\bcancel{2}\\times 9}\]"  \
          + "\[x=\\frac{22}{9}\]" ])

    # 26
    check(eq_with_exponents_1.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[x=4^{2}+5^{2}\]" \
          + "\[x=16+25\]" \
          + "\[x=41\]" ])


    check(eq_with_exponents_2.auto_resolution(dont_display_equations_name=True),
         [  "\[5^{2}=4^{2}+x\]" \
          + "\[25=16+x\]" \
          + "\[x=25-16\]" \
          + "\[x=9\]" ])

    # 28
    check(eq_with_expd_6.auto_resolution(),
         [  "$(E_{1}): $" \
          + "\[5=(x-2)+7\]" \
          + "\[5=x-2+7\]" \
          + "\[5=x+5\]" \
          + "\[x=5-5\]" \
          + "\[x=0\]"])


    check(eq_with_decimal_result_01.auto_resolution(decimal_result=1),
         [  "$(E_{1}): $" \
          + "\[2x=1\]" \
          + "\[x=\\frac{1}{2}\]" \
          + "\[x=" + locale.str(0.5) + "\]"])


    # 30
    check(eq_with_decimal_result_02.auto_resolution(decimal_result=2),
         [  "$(E_{1}): $" \
          + "\[3x=1\]" \
          + "\[x=\\frac{1}{3}\]" \
          + "\[x\\simeq" + locale.str(0.33) + "\]"])

    check(eq_with_decimal_result_03.auto_resolution(decimal_result=2),
         [  "$(E_{1}): $" \
          + "\[8x=6\]" \
          + "\[x=\\frac{6}{8}\]" \
          + "\[x=" + locale.str(0.75) + "\]"])


    check(eq_with_decimal_result_04.auto_resolution(decimal_result=2),
         [  "$(E_{1}): $" \
          + "\[x=4^{2}+5^{2}\]" \
          + "\[x=16+25\]" \
          + "\[x=41\]" ])

    # 33
    check(eq_with_decimal_result_05.auto_resolution(decimal_result=2),
         [  "$(E_{1}): $" \
          + "\[x=\\frac{1}{4}+\\frac{1}{8}\]" \
          + "\[x=\\frac{1\\times 2}{4\\times 2}+\\frac{1}{8}\]" \
          + "\[x=\\frac{2}{8}+\\frac{1}{8}\]" \
          + "\[x=\\frac{2+1}{8}\]" \
          + "\[x=\\frac{3}{8}\]" \
          + "\[x\\simeq" + locale.str(0.38) + "\]"])

    check(eq_with_different_variable_letter.auto_resolution(
                                              dont_display_equations_name=True,
                                              decimal_result=0),
         [  "\[\\text{AB}=3^{2}+4^{2}\]" \
          + "\[\\text{AB}=9+16\]" \
          + "\[\\text{AB}=25\]" ])

    # 35
    check(eq_with_different_variable_letter.auto_resolution(
                                              dont_display_equations_name=True,
                                              decimal_result=1),
         [  "\[\\text{AB}=3^{2}+4^{2}\]" \
          + "\[\\text{AB}=9+16\]" \
          + "\[\\text{AB}=25\]" ])


    check(eq_with_sqrt5.auto_resolution(dont_display_equations_name=True,
                                        decimal_result=2),
         [  "\[x=\\sqrt{5}\]" \
          + "\[x\\simeq" + locale.str(2.24) + "\]" ])


    check(eq_with_sqrt16.auto_resolution(dont_display_equations_name=True,
                                         decimal_result=2),
         [  "\[x=\\sqrt{16}\]" \
          + "\[x=4\]" ])

    # 38
    check(eq_with_xsquare_equal_to_16.auto_resolution(
                                              dont_display_equations_name=True),
         [  "\[x^{2}=16\]" \
          + "\[x=\\sqrt{16} or x=-\\sqrt{16}\]" \
          + "\[x=4 or x=-4\]" ])

    check(eq_with_xsquare_equal_to_16.auto_resolution(
                                        dont_display_equations_name=True,
                                        decimal_result=2),
         [  "\[x^{2}=16\]" \
          + "\[x=\\sqrt{16} or x=-\\sqrt{16}\]" \
          + "\[x=4 or x=-4\]" ])

    check(eq_with_xsquare_equal_to_5.auto_resolution(
                                        dont_display_equations_name=True),
         [  "\[x^{2}=5\]" \
          + "\[x=\\sqrt{5} or x=-\\sqrt{5}\]"])

    # 41
    check(eq_with_xsquare_equal_to_5.auto_resolution(
                                        dont_display_equations_name=True,
                                        decimal_result=2),
         [  "\[x^{2}=5\]" \
          + "\[x=\\sqrt{5} or x=-\\sqrt{5}\]" \
          + "\[x\\simeq" + locale.str(2.24) \
          + " or " \
          + "x\\simeq-" + locale.str(2.24)+ "\]" ])

    check(eq_with_xsquare_equal_to_5.auto_resolution(
                                        dont_display_equations_name=True,
                                        decimal_result=2,
                                        pythagorean_mode='yes'),
         [  "\[x^{2}=5\]" \
          + "\[x=\\sqrt{5}\\text{ because x is positive.}\]" \
          + "\[x\\simeq" + locale.str(2.24) + "\]" ])

    # 43
    check(pythagorean_1.auto_resolution(dont_display_equations_name=True,
                                        decimal_result=2,
                                        pythagorean_mode='yes'),
         [  "\[73^{2}=48^{2}+\\text{AB}^{2}\]" \
          + "\[5329=2304+\\text{AB}^{2}\]" \
          + "\[\\text{AB}^{2}=5329-2304\]" \
          + "\[\\text{AB}^{2}=3025\]" \
          + "\[\\text{AB}=\\sqrt{3025}" \
          + "\\text{ because \\text{AB} is positive.}\]" \
          + "\[\\text{AB}=55\]" ])

    # 44
    check(pythagorean_2.auto_resolution(dont_display_equations_name=True,
                                        pythagorean_mode='yes',
                                        unit='cm'),
         [  "\[\\text{EF}^{2}=60^{2}+91^{2}\]" \
          + "\[\\text{EF}^{2}=3600+8281\]" \
          + "\[\\text{EF}^{2}=11881\]"
          + "\[\\text{EF}=\\sqrt{11881}" \
          + "\\text{ because \\text{EF} is positive.}\]" \
          + "\[\\text{EF}=109\\text{ cm}\]" ])

    #45
    check(with_fractions.auto_resolution(dont_display_equations_name=True),
         [  "\[\\frac{2}{3}x=\\frac{4}{5}\]" \
          + "\[x=\\frac{4}{5}\div \\frac{2}{3}\]" \
          + "\[x=\\frac{4}{5}\\times \\frac{3}{2}\]" \
          + "\[x=\\frac{4\\times 3}{5\\times 2}\]" \
          + "\[x=\\frac{\\bcancel{2}\\times 2\\times 3}" \
          + "{5\\times \\bcancel{2}}\]"\
          + "\[x=\\frac{6}{5}\]"])


    check(with_fractions2.auto_resolution(dont_display_equations_name=True),
         [  "\[\\frac{1}{4}x+\\frac{1}{7}=-\\frac{3}{14}\]" \
          + "\[\\frac{1}{4}x=-\\frac{3}{14}-\\frac{1}{7}\]" \
          + "\[\\frac{1}{4}x=-\\frac{3}{14}-\\frac{1\\times 2}{7\\times 2}\]"\
          + "\[\\frac{1}{4}x=-\\frac{3}{14}-\\frac{2}{14}\]"\
          + "\[\\frac{1}{4}x=\\frac{-3-2}{14}\]"\
          + "\[\\frac{1}{4}x=-\\frac{5}{14}\]" \
          + "\[x=-\\frac{5}{14}\div \\frac{1}{4}\]"\
          + "\[x=-\\frac{5}{14}\\times \\frac{4}{1}\]"\
          + "\[x=-\\frac{5\\times 4}{14\\times 1}\]"\
          + "\[x=-\\frac{5\\times \\bcancel{2}\\times 2}"\
          + "{\\bcancel{2}\\times 7}\]"\
          + "\[x=-\\frac{10}{7}\]"])

    check(with_fractions3.auto_resolution(dont_display_equations_name=True),
         [  "\[2x+\\frac{1}{5}=-\\frac{4}{5}\]" \
          + "\[2x=-\\frac{4}{5}-\\frac{1}{5}\]" \
          + "\[2x=\\frac{-4-1}{5}\]" \
          + "\[2x=-\\frac{5}{5}\]" \
          + "\[2x=-\\frac{\\bcancel{5}}{\\bcancel{5}}\]" \
          + "\[2x=-1\]" \
          + "\[x=-\\frac{1}{2}\]"])


