# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
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

import os
import sys
#import locale

#from lib.common import default

from core import *
from core.calculus import *
from core.base_calculus import *

from maintenance.autotest import common

try:
   locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
except:
    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, "--- CROSS PRODUCT EQUATIONS\n")


    e1 = CrossProductEquation((Item("AB"),    Item(3),
                               Item(4),       Item(8)))

    check(e1,
         [  "\\frac{\\text{AB}}{4}=\\frac{3}{8}"])

    check(e1.auto_resolution(dont_display_equations_name=True),
         [  "\[\\frac{\\text{AB}}{4}=\\frac{3}{8}\]" \
         +  "\[\\text{AB}=\\frac{3\\times 4}{8}\]"
         +  "\[\\text{AB}=\\frac{3\\times \\bcancel{4}}{\\bcancel{4}\\times 2}\]"
         +  "\[\\text{AB}=\\frac{3}{2}\]"
         ])

    check(e1.auto_resolution(dont_display_equations_name=True,
                             skip_fraction_simplification=True,
                             decimal_result=2),
         [  "\[\\frac{\\text{AB}}{4}=\\frac{3}{8}\]" \
         +  "\[\\text{AB}=\\frac{3\\times 4}{8}\]"
         +  "\[\\text{AB}=" + locale.str(1.5) + "\]"
         ])

    check(e1.auto_resolution(dont_display_equations_name=True,
                             skip_fraction_simplification=True),
         [  "\[\\frac{\\text{AB}}{4}=\\frac{3}{8}\]" \
         +  "\[\\text{AB}=\\frac{3\\times 4}{8}\]"
         +  "\[\\text{AB}=\\frac{3}{2}\]"
         ])

    e2 = CrossProductEquation((Item(6),   Item(1.4),
                               Item(1.5), Item("AB")
                             ))

    check(e2.auto_resolution(dont_display_equations_name=True,
                             skip_fraction_simplification=True,
                             decimal_result=2),
         [  "\[\\frac{6}{" + locale.str(1.5) + "}=\\frac{" \
         + locale.str(1.4) + "}{\\text{AB}}\]" \
         +  "\[\\text{AB}=\\frac{" + locale.str(1.4) + "\\times " \
         + locale.str(1.5) + "}{6}\]"
         +  "\[\\text{AB}=" + locale.str(0.35) + "\]"
         ])





