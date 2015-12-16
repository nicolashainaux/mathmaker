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
#import locale

#from utils import default

from core import *
from core.base_calculus import *
from core.base_geometry import *
from core.geometry import *

from lib.common import pythagorean

from maintenance.autotest import common

#try:
#   locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
#except:
#    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- [GEO] RIGHT TRIANGLE \n", 'utf-8'))

    # Don't forget to uncomment the convenient lines above if a test
    # requires to use the locale module.

    # 1
    t1 = RightTriangle((("A", "B", "C"),
                        {'leg0' : 4, 'leg1' : 3}
                       ),
                       rotate_around_isobarycenter='no'
                      )
    t1.leg[0].set_label(Value(4, unit='cm'))
    t1.leg[1].set_label(Value(3, unit='cm'))
    t1.hypotenuse.set_label(Value(5, unit='cm'))

    check(t1.into_euk(),
          ["box -0.6, -0.6, 4.6, 3.6"\
           "A = point(0, 0)"\
           "B = point(4, 0)"\
           "C = point(4, 3)"\
           "draw  (A.B.C)"\
           "  $\\rotatebox{0}{4~cm}$ A 0 - 7.5 deg 6.4"\
           "  $\\rotatebox{-90}{3~cm}$ B 90 - 9 deg 4.9"\
           "  $\\rotatebox{37}{5~cm}$ A 37 + 6.5 deg 8"\
           "end"\
           "label"\
           "  C, B, A right"\
           "  A 0 + 200 deg"\
           "  B 0 - 45 deg"\
           "  C 0 + 65 deg"\
           "end"])

    # 2
    t2 = RightTriangle((("Y", "E", "P"),
                        {'leg0' : 4, 'leg1' : 3}
                       ),
                       rotate_around_isobarycenter=30
                      )
    t2.leg[0].set_label(Value(4, unit='cm'))
    t2.leg[1].set_label(Value(3, unit='cm'))
    t2.hypotenuse.set_label(Value(5, unit='cm'))

    check(t2.into_euk(),
          ["box 0.26, -1.8, 4.92, 4.0"\
          "Y = point(0.86, -1.2)"\
          "E = point(4.32, 0.8)"\
          "P = point(2.82, 3.4)"\
          "draw"\
          "  (Y.E.P)"\
          "  $\\rotatebox{30}{4~cm}$ Y 30 - 7.5 deg 6.4"\
          "  $\\rotatebox{-60}{3~cm}$ E 120 - 8.9 deg 4.9"\
          "  $\\rotatebox{67}{5~cm}$ Y 67 + 6.5 deg 8.1"\
          "end"\
          "label"\
          "  P, E, Y right"\
          "  Y 30 + 200 deg"\
          "  E 30 - 45 deg"\
          "  P 30 + 65 deg"\
          "end"])

    # 3
    t3 = RightTriangle((("Z", "A", "K"),
                        {'leg0' : 3, 'leg1' : 4}
                       ),
                       rotate_around_isobarycenter=75
                      )
    t3.leg[0].set_label(Value(3.2, unit='cm'))
    t3.leg[1].set_label(Value(4.5, unit='cm'))
    t3.hypotenuse.set_label(Value(""))

    check(t3.into_euk(),
          ["box -0.92, -1.54, 4.15, 3.59"\
          "Z = point(2.77, -0.94)"\
          "A = point(3.55, 1.95)"\
          "K = point(-0.32, 2.99)"\
          "draw"\
          "  (Z.A.K)"\
          "  $\\rotatebox{75}{3,2~cm}$ Z 75 - 9.1 deg 4.8"\
          "  $\\rotatebox{-15}{4,5~cm}$ A 165 - 7.5 deg 6.5"\
          "end"\
          "label"\
          "  K, A, Z right"\
          "  Z 75 + 200 deg"\
          "  A 75 - 45 deg"\
          "  K 75 + 65 deg"\
          "end"])

    # 4
    t4 = RightTriangle((("L", "O", "P"),
                        {'leg0' : 2, 'leg1' : 7}
                       ),
                       rotate_around_isobarycenter=140
                      )

    t4.leg[0].set_label(Value(1.5, unit='cm'))
    t4.leg[1].set_label(Value(""))
    t4.hypotenuse.set_label(Value(7, unit='cm'))
    t4.angle[0].set_mark("back")
    t4.angle[2].set_mark("dotted")
    t4.angle[0].set_label(Value(30, unit="\\textdegree"))

    check(t4.into_euk(),
          ["box -2.78, -1.41, 4.45, 5.15"\
          +"L = point(3.85, 3.26)"\
          +"O = point(2.32, 4.55)"\
          +"P = point(-2.18, -0.81)"\
          +"draw"\
          +"  (L.O.P)"\
          +"  $\\rotatebox{-40}{1,5~cm}$ L 140 - 17 deg 3.3"\
          +"  $\\rotatebox{34}{7~cm}$ L 214 + 5.1 deg 11.7"\
          +"  $\\rotatebox{-2.9}{30\\textdegree}$ L 177.1 deg 2.7"\
          +"end"\
          +"label"\
          +"  O, L, P back"\
          +"  P, O, L right"\
          +"  L, P, O dotted"\
          +"  L 140 + 200 deg"\
          +"  O 140 - 45 deg"\
          +"  P 140 + 65 deg"\
          +"end"])

    # 5
    check(t4.pythagorean_substequality().into_str(),
          ["\\text{OP}^{2}=\\text{PL}^{2}-\\text{LO}^{2}"])

    # 6
    check(t4.pythagorean_substequality().substitute().into_str(),
          ["\\text{OP}^{2}=7^{2}-" + locale.str(1.5) + "^{2}"])

    # 7
    eq_t4 = Equation(t4.pythagorean_substequality().substitute())
    check(eq_t4.auto_resolution(dont_display_equations_name=True,
                                decimal_result=HUNDREDTH,
                                pythagorean_mode='yes',
                                unit='cm'),
         [  "\[\\text{OP}^{2}=7^{2}-" + locale.str(1.5) + "^{2}\]" \
          + "\[\\text{OP}^{2}=49-" + locale.str(2.25) + "\]" \
          + "\[\\text{OP}^{2}=" + locale.str(46.75) + "\]" \
          + "\[\\text{OP}=\\sqrt{" + locale.str(46.75) \
          + "}\\text{ because \\text{OP} is positive.}\]"\
          + "\[\\text{OP}\\simeq" + locale.str(6.84) + "\\text{ cm}\]"])

    # 8
    # A small test about the research of matching legs... in pythagorean
    legs_matching_65_as_hyp=pythagorean.get_legs_matching_given_hypotenuse(65)
    check(str(legs_matching_65_as_hyp),
         [  "[16, 63, 25, 60, 33, 56, 39, 52]"])

    # 9
    legs_matching_36_as_a_side=pythagorean.get_legs_matching_given_leg(36)
    check(str(legs_matching_36_as_a_side),
         [  "[15, 27, 48, 77, 105, 160]"])

    # 10
    t5 = RightTriangle((("P", "A", "X"),
                        {'leg0' : 1, 'leg1' : 8}
                       ),
                       rotate_around_isobarycenter=0
                      )

    t5.leg[0].set_label(Value(1, unit='cm'))
    t5.leg[1].set_label(Value(8, unit='cm'))
    t5.hypotenuse.set_label(Value("?"))
    t5.angle[0].set_mark("simple")
    t5.angle[2].set_mark("double")
    t5.angle[0].set_label(Value(64, unit="\\textdegree"))
    t5.angle[2].set_label(Value(80, unit="\\textdegree"))

    check(t5.into_euk(),
          ["box -0.6, -0.6, 1.6, 8.6"\
          +"P = point(0, 0)"\
          +"A = point(1, 0)"\
          +"X = point(1, 8)"\
          +"draw"\
          +"  (P.A.X)"\
          +"  $\\rotatebox{0}{1~cm}$ P 0 - 25 deg 1.6"\
          +"  $\\rotatebox{-90}{8~cm}$ A 90 - 4.7 deg 12.8"\
          +"  $\\rotatebox{83}{?}$ P 83 + 4.7 deg 12.9"\
          +"  $\\rotatebox{41.4}{64\\textdegree}$ P 41.4 deg 2.7"\
          +"  $\\rotatebox{86.4}{80\\textdegree}$ X 266.4 deg 7.92"\
          +"end"\
          +"label"\
          +"  A, P, X simple"\
          +"  X, A, P right"\
          +"  P, X, A double"\
          +"  P 0 + 200 deg"\
          +"  A 0 - 45 deg"\
          +"  X 0 + 65 deg"\
          +"end"])
