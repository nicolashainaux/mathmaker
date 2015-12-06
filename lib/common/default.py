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

import os, sys, locale

from lib.common.cfg import CONFIG

LANGUAGE = CONFIG["LOCALES"]["LANGUAGE"]
ENCODING = CONFIG["LOCALES"]["ENCODING"]

try:
    locale.setlocale(locale.LC_ALL, LANGUAGE + '.' + ENCODING)
except:
    locale.setlocale(locale.LC_ALL, '')

#DECIMAL_POINT = str(locale.localeconv()['decimal_point'])

MC_MM_FILE = os.path.abspath(os.path.dirname(sys.argv[0])) \
           + "/sheet/mental_calculation_default.xml"

NUMBER_OF_QUESTIONS = 6

MONOMIAL_LETTER = 'x'
MAX_MONOMIAL_COEFF = 20

EQUATION_NAME = 'E'
