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
from mathmakerlib.geometry import Point, AngleMark, Triangle
from mathmakerlib.geometry import IsoscelesTriangle, EquilateralTriangle

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
        lbls = [Number(labels[0][1], unit=length_unit),
                Number(labels[1][1], unit=length_unit),
                Number(labels[2][1], unit=length_unit)]
        if variant == 1:
            lbls[0], lbls[2] = lbls[2], lbls[0]
        polygon.setup_labels(labels=lbls)
        if variant == 1:  # right triangle shapes
            polygon.angles[1].mark = AngleMark(thickness=thickness)
            polygon.angles[1].mark_right = True
        polygon.baseline = p[3]
        return polygon

    def _triangle_2_1(self, variant=None, labels=None, name=None,
                      label_vertices=None, thickness=None, length_unit=None,
                      shape_variant_nb=None):
        shape_variants = {1: [Number('2.8'), Number('1.52'), 0, '4pt'],
                          2: [Number('2.8'), Number('1.52'), 180, '2pt'],
                          3: [Number('0.8'), Number('2.4'), 90, '15pt'],
                          4: [Number('0.8'), Number('2.4'), -90, '23pt'],
                          5: [Number('0.8'), Number('2.4'), Number('-99.6'),
                              '25pt'],
                          6: [Number('0.8'), Number('2.4'), Number('-80.4'),
                              '18pt'],
                          7: [Number('0.8'), Number('2.4'), Number('99.6'),
                              '18pt'],
                          8: [Number('0.8'), Number('2.4'), Number('80.4'),
                              '15pt'],
                          }
        if shape_variant_nb is None:
            shape_variant_nb = \
                next(shared.isosceles_triangle_shapes_source)[0]
        build_data = shape_variants[shape_variant_nb]
        polygon = IsoscelesTriangle(
            base_length=build_data[0], equal_legs_length=build_data[1],
            rotation_angle=build_data[2],
            use_mark=next(shared.ls_marks_source)[0],
            name=name, label_vertices=label_vertices, thickness=thickness)
        baselbl, eqlbl = labels[0][1], labels[1][1]
        if labels[0][0] == 2:
            baselbl, eqlbl = eqlbl, baselbl
        polygon.setup_labels([Number(baselbl, unit=length_unit),
                              Number(eqlbl, unit=length_unit)])
        polygon.baseline = build_data[3]
        return polygon

    def _triangle_3(self, variant=None, labels=None, name=None,
                    label_vertices=None, thickness=None, length_unit=None,
                    shape_variant_nb=None):
        shape_variants = {1: [Number('1.1'), 0, '12pt', None],
                          2: [Number('1.1'), 60, '0pt', None],
                          3: [Number('1.1'), Number('29.9'), '6pt', None],
                          4: [Number('1.1'), 90, '0pt',
                              ('-0.2', '-0.24', '0.97', '0.97')],
                          }
        if shape_variant_nb is None:
            shape_variant_nb = \
                next(shared.equilateral_triangle_shapes_source)[0]
        build_data = shape_variants[shape_variant_nb]
        polygon = EquilateralTriangle(
            side_length=build_data[0],
            rotation_angle=build_data[1],
            use_mark=next(shared.ls_marks_source)[0],
            name=name, label_vertices=label_vertices, thickness=thickness)
        sidelbl = labels[0][1]
        polygon.setup_labels([Number(sidelbl, unit=length_unit)])
        polygon.baseline = build_data[2]
        polygon.boundingbox = build_data[3]
        return polygon
