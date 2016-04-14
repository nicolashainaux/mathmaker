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

from lib.common import settings
from . import exercise

D = settings.rootdir + "sheet/frameworks/"
DM = D + "mental_calculation/"
L11_1 = "lev11_1/"
L11_2 = "lev11_2/"

XML_SCHEMA_PATH = D + "sheet.xsd"

XML_SHEETS = { 'tables2_9': DM + L11_1 + "tables2_9.xml",
               'divisions': DM + L11_1 + "divisions.xml",
               'multi_hole_tables2_9': DM + L11_1 + "multi_hole_tables2_9.xml",
               'multi_hole_any_nb': DM + L11_1 + "multi_hole_any_nb.xml",
               'multi_11_15_25': DM + L11_1 + "multi_11_15_25.xml",
               'multi_decimal': DM + L11_1 + "multi_decimal.xml",
               'multi_reversed': DM + L11_1 + "multi_reversed.xml",
               'ranks': DM + L11_1 + "ranks.xml",
               'mini_problems': DM + L11_1 + "mini_problems.xml",
               'test_11_1': DM + L11_1 + "test_11_1.xml",
               'operations_vocabulary': DM + L11_2 \
                                         + "operations_vocabulary.xml",
               'multi_divi_10_100_1000': DM + L11_2 \
                                          + "multi_divi_10_100_1000.xml",
               'rectangles': DM + L11_2 + "rectangles.xml",
               'test_11_2': DM + L11_2 + "test_11_2.xml"
               }

CATALOG = { 'mental_calculation': exercise.X_MentalCalculation,
            #'generic': exercise.X_Generic
          }
