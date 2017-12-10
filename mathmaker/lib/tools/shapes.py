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

from mathmakerlib.calculus import Number
from mathmakerlib.geometry import Point, Triangle


class ShapeGenerator(object):

    def generate(self, codename=None, labels=None,
                 name=None, label_vertices=None, thickness=None,
                 length_unit=None):
        if type(codename) is not str:
            raise TypeError('codename must be a str')
        try:
            return getattr(self,
                           '_generate_'
                           + codename)(labels=labels,
                                       name=name,
                                       label_vertices=label_vertices,
                                       thickness=thickness,
                                       length_unit=length_unit)
        except AttributeError:
            raise ValueError('Cannot generate \'{}\''.format(codename))

    def _generate_triangle_1_1_1(self, labels=None, name=None,
                                 label_vertices=None,
                                 thickness=None, length_unit=None):
        polygon = Triangle(Point(0, 0), Point(2, 0),
                           Point(Number('0.582'), Number('0.924')),
                           name=name, label_vertices=label_vertices,
                           thickness=thickness)
        polygon.setup_labels(
            labels=[Number(labels[0][1], unit=length_unit),
                    Number(labels[1][1], unit=length_unit),
                    Number(labels[2][1], unit=length_unit)])
        return polygon
