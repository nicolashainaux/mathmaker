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

#from settings import config

from lib.core import *
from lib.core.base_calculus import *
from lib.core.base_geometry import *
from lib.core.geometry import *

from maintenance.autotest import common

#try:
#   locale.setlocale(locale.LC_ALL, config.LANGUAGE + '.' + config.ENCODING)
#except:
#    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- [GEO] RECTANGLE \n", 'utf-8'))

    # Don't forget to uncomment the convenient lines above if a test
    # requires to use the locale module.

    # 1
    r1 = Rectangle([Point(["A", (0.5, 0.5)]), 4, 3, "B", "C", "D"
                    ])

    r1.side[2].label = Value(4, unit='cm')
    r1.side[3].label = Value(3, unit='cm')

    check(r1.into_euk(),
          ["box -0.1, -0.1, 5.1, 4.1"\
          +"A = point(0.5, 0.5)"\
          +"B = point(4.5, 0.5)"\
          +"C = point(4.5, 3.5)"\
          +"D = point(0.5, 3.5)"\
          +"draw"\
          +"  (A.B.C.D)"\
          +"  $\\rotatebox{0}{4~cm}$ C 180 - 7.5 deg 6.4"\
          +"  $\\rotatebox{90}{3~cm}$ D 270 - 9 deg 4.9"\
          +"end"\
          +"label"\
          +"  B, A, D right"\
          +"  C, B, A right"\
          +"  D, C, B right"\
          +"  A, D, C right"\
          +"  A 225 deg"\
          +"  B 315 deg"\
          +"  C 45 deg"\
          +"  D 135 deg"\
          +"end"])
