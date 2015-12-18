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
    r1 = Rectangle([Point(["A", (0.5, 0.5)]), 4, 3, "B", "C", "D"
                    ])

    r1.side[2].label = Value(4, unit='cm')
    r1.side[3].label = Value(3, unit='cm')

    check(r1.into_euk(),
          ["box -0.1, -0.1, 3.8, 4.6"\
          +"A = point(0.5, 0.5)"\
          +"B = point(3, 1)"\
          +"C = point(3.2, 4)"\
          +"D = point(0.8, 3)"\
          +"draw"\
          +"(A.B.C.D)"\
          +"  $\\rotatebox{11}{4~cm}$ A 11 - 12.7 deg 4.1"\
          +"  $\\rotatebox{86}{3~cm}$ B 86 - 8.9 deg 4.9"\
          +"  $\\rotatebox{23}{2~cm}$ C 203 - 12.2 deg 4.2"\
          +"  $\\rotatebox{83}{6,5~cm}$ D 263 - 12.9 deg 4.1"\
          +"  $\\rotatebox{47.3}{64\\textdegree}$ A 47.3 deg 2.7"\
          +"  $\\rotatebox{-41.3}{128\\textdegree}$ B 138.7 deg 2.7"\
          +"  $\\rotatebox{54.3}{32\\textdegree}$ C 234.3 deg 2.7"\
          +"  $\\rotatebox{322.7}{256\\textdegree}$ D 322.7 deg 2.7"\
          +"end"\
          +"label"\
          +"  B, A, D simple"\
          +"  C, B, A simple"\
          +"  D, C, B simple"\
          +"  A, D, C simple"\
          +"  A 227.3 deg"\
          +"  B 318.7 deg"\
          +"  C 54.3 deg"\
          +"  D 142.7 deg"\
          +"end"])
