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

from core import *
from core.base_calculus import *
from core.base_geometry import *

from maintenance.autotest import common

#try:
#   locale.setlocale(locale.LC_ALL, config.LANGUAGE + '.' + config.ENCODING)
#except:
#    locale.setlocale(locale.LC_ALL, '')

check = common.check


def action():
    if common.verbose:
        os.write(common.output, bytes("--- NAME\n", 'utf-8'))

    # Don't forget to uncomment the convenient lines above if a test
    # requires to use the locale module.

    # after you replaced the NAME right above,
    # define your OBJECTS here
    # for instance: monom_6 = Monomial(('+', 6, 0))



    # then use the CHECK function (it's like an assert)
    # check(monom_6_ones_away,
    #       ["6"])



