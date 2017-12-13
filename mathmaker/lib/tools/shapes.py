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
from mathmakerlib.geometry import Point, Triangle, AngleMark

from mathmaker.lib import shared


class ShapeGenerator(object):

    def generate(self, codename=None, variant=None, labels=None,
                 name=None, label_vertices=None, thickness=None,
                 length_unit=None):
        if type(codename) is not str:
            raise TypeError('codename must be a str')
        try:
            return getattr(self,
                           '_' + codename)(variant=variant, labels=labels,
                                           name=name,
                                           label_vertices=label_vertices,
                                           thickness=thickness,
                                           length_unit=length_unit)
        except AttributeError:
            raise ValueError('Cannot generate \'{}\''.format(codename))

    def _triangle_1_1_1(self, variant=None, labels=None, name=None,
                        label_vertices=None, thickness=None, length_unit=None,
                        shape_variant_nb=None):
        if variant == 0:  # scalene triangle shapes
            shape_variants = {1: [(0, 0),
                                  (2, 0),
                                  (Number('0.582'), Number('0.924')),
                                  '6pt'],
                              2: [(0, 0),
                                  (2, 0),
                                  (Number('1.418'), Number('0.924')),
                                  '6pt'],
                              3: [(2, Number('0.924')),
                                  (0, Number('0.924')),
                                  (Number('1.418'), 0),
                                  '13pt'],
                              4: [(2, Number('0.924')),
                                  (0, Number('0.924')),
                                  (Number('0.582'), 0),
                                  '13pt']
                              }
            if shape_variant_nb is None:
                shape_variant_nb = \
                    next(shared.scalene_triangle_shapes_source)[0]
        elif variant == 1:  # right triangle shapes
            shape_variants = {1: [(0, 0), (2, 0), (2, 1), '8pt'],
                              2: [(2, 0), (2, 1), (0, 1), '17pt'],
                              3: [(2, 1), (0, 1), (0, 0), '17pt'],
                              4: [(0, 1), (0, 0), (2, 0), '8pt'],
                              5: [('2.236', 0), ('0.582', '0.981'), (0, 0),
                                  '8pt'],
                              6: [('2.1', 0), ('1.418', '0.981'), (0, 0),
                                  '8pt'],
                              7: [(0, '0.981'), ('0.582', 0),
                                  ('2.236', '0.981'),
                                  '17pt'],
                              8: [(0, '0.981'), ('1.418', 0),
                                  ('2.1', '0.981'),
                                  '17pt']
                              }
            if shape_variant_nb is None:
                shape_variant_nb = \
                    next(shared.right_triangle_shapes_source)[0]
        p = shape_variants[shape_variant_nb]
        polygon = Triangle(Point(*p[0]), Point(*p[1]), Point(*p[2]),
                           name=name, label_vertices=label_vertices,
                           thickness=thickness)
        polygon.setup_labels(
            labels=[Number(labels[2][1], unit=length_unit),
                    Number(labels[1][1], unit=length_unit),
                    Number(labels[0][1], unit=length_unit)])
        if variant == 1:  # right triangle shapes
            polygon.angles[1].mark = AngleMark(thickness=thickness)
            polygon.angles[1].mark_right = True
        polygon.baseline = p[3]
        return polygon
