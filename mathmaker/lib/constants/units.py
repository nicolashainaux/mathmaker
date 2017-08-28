# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

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

LENGTH_UNITS = ['km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm', 'µm', 'nm', 'pm']
CAPACITY_UNITS = ['kL', 'hL', 'daL', 'L', 'dL', 'cL', 'mL', 'µL', 'nL', 'pL']
MASS_UNITS = ['kg', 'hg', 'dag', 'g', 'dg', 'cg', 'mg', 'µg', 'ng', 'pg']
COMMON_LENGTH_UNITS = LENGTH_UNITS[:-3]
COMMON_CAPACITY_UNITS = CAPACITY_UNITS[1:-3]
COMMON_MASS_UNITS = MASS_UNITS[:-3]
ANGLE_UNITS = ['\\textdegree']
CURRENCY_UNITS = ['€', '\officialeuro',
                  '$', '\\textdollar',
                  '£', '\\textsterling']
CURRENCIES_DICT = {'euro': '\officialeuro',
                   'dollar': '\\textdollar',
                   'sterling': '\\textsterling'}
AVAILABLE_UNITS = LENGTH_UNITS + CAPACITY_UNITS + MASS_UNITS + ANGLE_UNITS\
    + CURRENCY_UNITS
UNIT_KINDS = {'length': COMMON_LENGTH_UNITS,
              'mass': COMMON_MASS_UNITS,
              'capacity': COMMON_CAPACITY_UNITS,
              'currency': CURRENCY_UNITS}
VALUE_AND_UNIT_SEPARATOR = {'km': "~", 'hm': "~", 'dam': "~", 'm': "~",
                            'dm': "~", 'cm': "~", 'mm': "~", 'µm': "~",
                            'nm': "~", 'pm': "~",
                            'kL': "~", 'hL': "~", 'daL': "~", 'L': "~",
                            'dL': "~", 'cL': "~", 'mL': "~", 'µL': "~",
                            'nL': "~", 'pL': "~",
                            'kg': "~", 'hg': "~", 'dag': "~", 'g': "~",
                            'dg': "~", 'cg': "~", 'mg': "~", 'µg': "~",
                            'ng': "~", 'pg': "~",
                            '\\textdegree': "",
                            '\officialeuro': "~",
                            '\\textdollar': "~",
                            '\\textsterling': "~"}
