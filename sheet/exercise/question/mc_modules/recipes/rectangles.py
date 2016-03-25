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

        if not hasattr(self, 'unit_length'):
            units.sub_object.__init__(self, **options)

        rectangle_name = next(shared.four_letters_words_source)

        w = Value(min([self.nb1, self.nb2]), unit=self.unit_length)
        l = Value(max([self.nb1, self.nb2]), unit=self.unit_length)

        self.rectangle = Rectangle([Point([rectangle_name[3], (0,0)]),
                                    3,
                                    1.5,
                                    rectangle_name[2],
                                    rectangle_name[1],
                                    rectangle_name[0]],
                                    read_name_clockwise=True)

        self.rectangle.set_lengths([l, w])

        self.rectangle.setup_labels([False, False, True, True])
