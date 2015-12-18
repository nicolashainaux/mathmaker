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

#from lib.common import default

from core import *
from core.base_calculus import *
from core.base_geometry import *
from core.geometry import *

from maintenance.autotest import common

#try:
#   locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
#except:
#    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- [GEO] POLYGON \n", 'utf-8'))

    # Don't forget to uncomment the convenient lines above if a test
    # requires to use the locale module.

    # 1
    p1 = Polygon([Point(["A", (0.5, 0.5)]),
                  Point(["B", (3, 1)]),
                  Point(["C", (3.2, 4)]),
                  Point(["D", (0.8, 3)])
                  ])

    p1.side[0].label = Value(4, unit='cm')
    p1.side[1].label = Value(3, unit='cm')
    p1.side[2].label = Value(2, unit='cm')
    p1.side[3].label = Value(6.5, unit='cm')
    """p1.side[0].label = Value(4, unit='cm')
    p1.side[1].label = Value(5, unit='cm')
    p1.side[2].label = Value(4.84, unit='cm')
    p1.angle[0].label = Value('?')
    p1.angle[1].label = Value(64, unit='\\textdegree')
    p1.angle[2].label = Value(35, unit='\\textdegree')
    p1.angle[0].mark = 'simple'
    p1.angle[1].mark = 'double'
    p1.angle[2].mark = 'dotted'"""


    check(p1.into_euk(),
          ["box -1.33, -0.48, 4.71, 4.6"\
           "Z = point(4.11, 0.38)"\
           "E = point(2.42, 4)"\
           "P = point(-0.73, 0.12)"\
           "draw"\
           "  (Z.E.P)"\
           "  $\\rotatebox{-65}{4~cm}$ Z 115 - 7.5 deg 6.4"\
           "  $\\rotatebox{51}{5~cm}$ E 231 - 6.5 deg 8"\
           "  $\\rotatebox{3}{4,84~cm}$ Z 183 + 6.7 deg 7.8"\
           "  $\\rotatebox{-31}{?}$ Z 149 deg 2.7"\
           "  $\\rotatebox{83}{64\\textdegree}$ E 263 deg 2.7"\
           "  $\\rotatebox{387}{35\\textdegree}$ P 387 deg 2.7"\
           "end"\
           "label"\
           "  E, Z, P simple"\
           "  P, E, Z double"\
           "  Z, P, E dotted"\
           "  Z 115 + 200 deg"\
           "  E 115 - 45 deg"\
           "  P 115 + 65 deg"\
           "end"])
