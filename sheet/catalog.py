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

from lib.common.software import ROOT_PATH
from . import exercise

D = ROOT_PATH + "sheet/frameworks/"

XML_SHEETS = { 'mental_calculation_default' : D +\
                                              "mental_calculation/default.xml",
               'tables2_9' : D + "mental_calculation/tables2_9.xml",
               'divisions' : D + "mental_calculation/divisions.xml",
               'multi_hole_tables2_9' : D + \
                                "mental_calculation/multi_hole_tables2_9.xml",
               'multi_hole_any_nb' : D + \
                                "mental_calculation/multi_hole_any_nb.xml",
               'multi_decimal' : D + \
                                "mental_calculation/multi_decimal.xml",
               'multi_reversed' : D + \
                                "mental_calculation/multi_reversed.xml"}

CATALOG = { 'mental_calculation' : exercise.X_MentalCalculation,
            #'generic' : exercise.X_Generic
          }
