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
import math
#import locale

#from lib.common import default

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
        os.write(common.output,
                 bytes("--- TABLES : uncomplete but proportional\n", 'utf-8')
                )

    #t1 = Table_UP([[Item((2)),   Item(("AB")),   Item((6)) ],
    #               [Item((3.4)), Item((8.5)), Item(("MN")) ]
    #              ]
    #             )

    AB = Item("AB")
    MN = Item("MN")
    CD = Item("CD")
    EF = Item("EF")
    GH = Item("GH")

    t1 = Table_UP(1.7,
                  [Item(2), Item(5), Item(6)],
                  [None, (AB, None), (None, MN)]
                 )

    check(t1,
         [  "\\begin{tabular}{|c|c|c|}" \
          + "\hline " \
          + "2&\\text{AB}&6\\\\" \
          + "\\hline " \
          + locale.str(3.4) + "&" + locale.str(8.5) + "&\\text{MN}\\\\" \
          + "\\hline " \
          + "\end{tabular}" ])

    #t2 = Table_UP([[Item((2)),   Item(("AB")),   Item(("EF")),    Item((4)) ],
    #               [Item((2.5)), Item(("CD")),   Item((3.75)),  Item(("GH")) ]
    #              ]
    #             )

    t2 = Table_UP(1.25,
                  [Item(2), None, Item(3), Item(4)
                  ],
                  [None,
                   (AB, CD),
                   (EF, None),
                   (None, GH)
                  ]
                 )

    check(t2,
         [  "\\begin{tabular}{|c|c|c|c|}" \
          + "\hline " \
          + "2&\\text{AB}&\\text{EF}&4\\\\" \
          + "\\hline " \
          + "" + locale.str(2.5) + "&\\text{CD}&" \
          + locale.str(3.75) + "&\\text{GH}\\\\" \
          + "\\hline " \
          + "\end{tabular}" ])

    check(str(t1.crossproducts_info[AB]),
         ["(1, 0)"])

    check(str(t1.crossproducts_info[MN]),
         ["(2, 0)"])

    check(str(t2.crossproducts_info[EF]),
         ["(2, 0)"])

    check(str(t2.crossproducts_info[GH]),
         ["(3, 0)"])

    check(t1.into_crossproduct_equation(AB),
         ["\\frac{2}{" + locale.str(3.4) + "}=\\frac{\\text{AB}}{" \
         + locale.str(8.5) + "}"])

    check(t1.into_crossproduct_equation(MN),
         ["\\frac{2}{" + locale.str(3.4) + "}=\\frac{" \
         + locale.str(6) + "}{\\text{MN}}"])

    check(t2.into_crossproduct_equation(GH),
         ["\\frac{2}{" + locale.str(2.5) + "}=\\frac{" \
         + locale.str(4) + "}{\\text{GH}}"])

    t3 = Table_UP(0.8,
                  [Item(3), Item(4), Item(9)],
                  [(AB, None), (None, None), (None, MN)]
                 )

    check(t3,
         [  "\\begin{tabular}{|c|c|c|}" \
          + "\hline " \
          + "\\text{AB}&4&9\\\\" \
          + "\\hline " \
          + "" + locale.str(2.4) + "&" + locale.str(3.2) + "&\\text{MN}\\\\" \
          + "\\hline " \
          + "\end{tabular}" ])

    check(t3.into_crossproduct_equation(AB),
         ["\\frac{\\text{AB}}{" + locale.str(2.4) + "}=\\frac{" \
         + locale.str(4) + "}{" + locale.str(3.2) + "}"])

    check(t3.into_crossproduct_equation(MN),
         ["\\frac{" + locale.str(4) + "}{" + locale.str(3.2) + "}=\\frac{" \
         + locale.str(9) + "}{\\text{MN}}"])




