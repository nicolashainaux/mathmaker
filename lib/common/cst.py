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

YES = ['yes', 'Yes', 'YES', 'ok', 'Ok', 'OK', True]

DEFAULT = "default"
RANDOMLY = "randomly"
NUMERIC = "numeric"
LITERALS = "literals"
OTHERS = "others"

UNIT = "1"
TENTH = "1.0"
HUNDREDTH = "1.00"
THOUSANDTH = "1.000"
TEN_THOUSANDTH = "1.0000"

PRECISION = [UNIT, TENTH, HUNDREDTH, THOUSANDTH, TEN_THOUSANDTH]
PRECISION_REVERSED = { UNIT : 0,
                       TENTH : 1,
                       HUNDREDTH : 2,
                       THOUSANDTH : 3,
                       TEN_THOUSANDTH : 4
                     }

PRECISION_WORDS = { UNIT : "unit",
                    TENTH : "tenth",
                    HUNDREDTH : "hundredth",
                    THOUSANDTH : "thousandth",
                    TEN_THOUSANDTH : "ten thousandth"
                  }

LENGTH_UNITS = ['km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm', 'µm', 'nm', 'pm']
ANGLE_UNITS = ['\\textdegree']
AVAILABLE_UNITS = LENGTH_UNITS + ANGLE_UNITS
VALUE_AND_UNIT_SEPARATOR = {'km':" ",
                            'hm':" ",
                            'dam':" ",
                            'm':" ",
                            'dm':" ",
                            'cm':" ",
                            'mm':" ",
                            'µm':" ",
                            'nm':" ",
                            'pm':" ",
                            '\\textdegree':""
                            }

TEXT_SCALES = ['tiny', 'scriptsize', 'footnotesize', 'small', 'normal',
               'large', 'Large', 'LARGE', 'huge', 'HUGE']

TEXT_RANKS = {'tiny':0, 'scriptsize':1, 'footnotesize':2, 'small':3,
              'normal':4, 'large':5, 'Large':6, 'LARGE':7, 'huge':8, 'HUGE':9}





