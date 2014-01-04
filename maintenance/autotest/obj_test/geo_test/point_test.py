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
from core.base_calculus import *
from core.base_geometry import *

from maintenance.autotest import common

#try:
#   locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
#except:
#    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, "--- [GEO] POINT \n")

    # Don't forget to uncomment the convenient lines above if a test
    # requires to use the locale module.

    # after you replaced the NAME right above,
    # define your OBJECTS here
    point_A = Point(["A", (0, 0)])





    # 1
    check(str(point_A.x),
         ["0"])



