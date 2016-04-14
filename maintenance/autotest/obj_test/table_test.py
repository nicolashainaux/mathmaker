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

#from lib.common.settings import default

from core import *
from core.base_calculus import *
from core.calculus import *

from maintenance.autotest import common

#try:
#   locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
#except:
#    locale.setlocale(locale.LC_ALL, '')

check = common.check

def action():
    if common.verbose:
        os.write(common.output, bytes("--- TABLES\n", 'utf-8'))

    # Don't forget to uncomment the convenient lines above if a test
    # requires to use the locale module.

    t1 = Table([[Item((2)), Item((5)),  Item((6)),  Item((7)) ],
                [Item((4)), Item((10)), Item((12)), Item((14))]
               ]
              )

    check(str(len(t1)),
         ["4"])

    check(str(t1.is_numeric()),
         ["True"])

    check(t1.into_str(),
         [  "\\begin{tabular}{|c|c|c|c|}" \
          + "\hline " \
          + "2&5&6&7\\\\" \
          + "\\hline " \
          + "4&10&12&14\\\\" \
          + "\\hline " \
          + "\end{tabular}" ])

    check(t1.into_str(as_a_quotients_equality='yes'),
         ["\\frac{2}{4}=\\frac{5}{10}=\\frac{6}{12}=\\frac{7}{14}" ])

    check(t1.cross_product((0,1), 0),
         ["\\frac{5\\times 4}{10}"])

    check(t1.cross_product((0,1), 1),
         ["\\frac{2\\times 10}{4}"])

    check(t1.cross_product((0,1), 2),
         ["\\frac{5\\times 4}{2}"])

    check(t1.cross_product((0,1), 3),
         ["\\frac{2\\times 10}{5}"])
