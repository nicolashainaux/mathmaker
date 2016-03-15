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

import copy

from core.base_calculus import Item
from core.root_calculus import Value
from core.base_geometry import Point
from core.geometry import Rectangle
from lib.common import shared

from . import nb_variants, units

class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        nb_variants.sub_object.__init__(self, numbers_to_use, **options)
        units.sub_object.__init__(self, numbers_to_use, **options)

        nb_list = [self.nb1, self.nb2]

        self.context = options['context'] if 'context' in options else "default"

        self.w = min(nb_list)
        self.l = max(nb_list)

        self.w_val = Value(self.w, unit=self.unit_length)
        self.w_str = Item(self.w, unit=self.unit_length)
        self.w_str = self.w_str.into_str(force_expression_begins=True,
                                         display_unit=True)

        self.l_val = Value(self.l, unit=self.unit_length)
        self.l_str = Item(self.l, unit=self.unit_length)
        self.l_str = self.l_str.into_str(force_expression_begins=True,
                                         display_unit=True)

        self.rectangle = None
        if self.context == "sketch":
            rectangle_name = next(shared.four_letters_word_generator)
            self.rectangle = Rectangle([Point([rectangle_name[3], (0,0)]),
                                        3,
                                        1.5,
                                        rectangle_name[2],
                                        rectangle_name[1],
                                        rectangle_name[0]],
                                        read_name_clockwise=True)

            self.rectangle.side[2].label = self.l_val
            self.rectangle.side[3].label = self.w_val
