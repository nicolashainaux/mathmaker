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

import random

from mathmakerlib.calculus import Number
from mathmakerlib.geometry import Point, AngleMark, Polygon, Triangle
from mathmakerlib.geometry import IsoscelesTriangle, EquilateralTriangle
from mathmakerlib.geometry import Quadrilateral, Rectangle, Rhombus, Square

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

    def _polygon(self, shapes_source, shape_variants, shape_builder, labels,
                 masks=None, marks=None, length_unit=None, name=None,
                 shape_variant_nb=None, label_vertices=None, thickness=None):
        if shape_variant_nb is None:
            shape_variant_nb = next(shapes_source)[0]
        build_data = shape_variants[shape_variant_nb]
        build_data.update({'name': name, 'label_vertices': label_vertices,
                           'thickness': thickness})
        baseline = build_data.pop('baseline', None)
        boundingbox = build_data.pop('boundingbox', None)
        if masks is None:
            masks = build_data.pop('masks', None)
        elif 'masks' in build_data:
            del build_data['masks']
        args = build_data.pop('args', [])
        right_angle_radius = build_data.pop('right_angle_radius', None)
        polygon = shape_builder(*args, **build_data)
        polygon.setup_labels([Number(lbl, unit=length_unit)
                              for lbl in labels], masks=masks)
        polygon.baseline = baseline
        polygon.boundingbox = boundingbox
        polygon.setup_marks(marks)
        if right_angle_radius is not None:
            for a in polygon.angles:
                if isinstance(a.mark, AngleMark) and a.mark_right:
                    a.mark.radius = right_angle_radius
        return polygon

    def _quadrilateral_1_1_1_1(self, variant=None, labels=None, name=None,
                               label_vertices=None, thickness=None,
                               length_unit=None, shape_variant_nb=None):
        quadrilateral_shape1 = [Point(0, 0), Point('0.6', '-0.3'),
                                Point('1.6', '0.2'), Point('0.4', 1)]
        quadrilateral_shape2 = [Point(0, 0), Point(1, '-0.2'),
                                Point('1.2', '0.9'), Point('-0.2', '0.8')]
        shape_variants = {
            1: {'args': quadrilateral_shape1, 'rotation_angle': 0,
                'baseline': '4pt',
                # 'boundingbox': None,
                # 'use_mark': next(shared.ls_marks_source)[0]
                },
            2: {'args': quadrilateral_shape1, 'rotation_angle': 90,
                'baseline': '4pt'
                },
            3: {'args': quadrilateral_shape1, 'rotation_angle': -90,
                'baseline': '4pt'
                },
            4: {'args': quadrilateral_shape1, 'rotation_angle': 180,
                'baseline': '4pt'
                },
            5: {'args': quadrilateral_shape2, 'rotation_angle': 0,
                'baseline': '9pt'
                },
            6: {'args': quadrilateral_shape2, 'rotation_angle': 180,
                'baseline': '9pt'
                }
        }
        return self._polygon(
            shared.quadrilateral_1_1_1_1_shapes_source,
            shape_variants,
            Quadrilateral,
            labels=[lbl[1] for lbl in labels],
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
        )

    def _quadrilateral_2_1_1(self, variant=None, labels=None, name=None,
                             label_vertices=None, thickness=None,
                             length_unit=None, shape_variant_nb=None):
        quadrilateralv0_shape1 = [Point(0, 0), Point('1.2', '0.7'),
                                  Point('2.4', 0), Point('0.8', '-0.4')]
        quadrilateralv0_shape2 = [Point('1.2', '-0.6'), Point(0, 0),
                                  Point('1.2', '0.5'), Point('2.4', '0.2')]
        quadrilateralv1_shape1 = [Point(0, 0), Point('0.8', '0.6'),
                                  Point('1.8', '0.6'), Point('1.2', '-0.2')]
        quadrilateralv1_shape2 = [Point('0.2', '-0.4'), Point(0, '0.6'),
                                  Point('1.2', '0.6'), Point('2.2', '0.4')]
        mark = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': quadrilateralv0_shape1, 'rotation_angle': 0,
                    'baseline': '-1pt'},
                2: {'args': quadrilateralv0_shape1, 'rotation_angle': 180,
                    'baseline': '-1pt'},
                3: {'args': quadrilateralv0_shape2, 'rotation_angle': 0,
                    'baseline': '-3pt'},
                4: {'args': quadrilateralv0_shape2, 'rotation_angle': 180,
                    'baseline': '-3pt'}
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': quadrilateralv1_shape1, 'rotation_angle': 0,
                    'baseline': '4pt'},
                2: {'args': quadrilateralv1_shape1, 'rotation_angle': 180,
                    'baseline': '5pt'},
                3: {'args': quadrilateralv1_shape2, 'rotation_angle': 0,
                    'baseline': '3pt'},
                4: {'args': quadrilateralv1_shape2, 'rotation_angle': 180,
                    'baseline': '8pt'},
            }
        singles = []
        doubled = []
        for lbl in labels:
            if lbl[0] == 1:
                singles.append(lbl[1])
            else:
                doubled.append(lbl[1])
                doubled.append(lbl[1])
        random.shuffle(singles)
        if variant == 0:
            lbls = [doubled.pop(), doubled.pop(), singles.pop(), singles.pop()]
            masks = [None, ' ', None, None]
            marks = [mark, mark, None, None]
        elif variant == 1:
            lbls = [doubled.pop(), singles.pop(), doubled.pop(), singles.pop()]
            masks = [None, None, ' ', None]
            marks = [mark, None, mark, None]
        return self._polygon(
            shared.quadrilateral_2_1_1_shapes_source,
            shape_variants,
            Quadrilateral,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks
        )

    def _quadrilateral_2_2(self, variant=None, labels=None, name=None,
                           label_vertices=None, thickness=None,
                           length_unit=None, shape_variant_nb=None):
        shape_builder = Quadrilateral
        kite_shape1 = [Point(0, 0), Point('1.2', '0.2'),
                       Point('2.4', 0), Point('1.2', '-0.8')]
        kite_shape2 = [Point('0.7', '-0.5'), Point(0, 0),
                       Point('0.7', '0.5'), Point('2.4', 0)]
        parallelogram_shape1 = [Point(0, 0), Point('0.6', '0.8'),
                                Point('2.6', '0.8'), Point(2, 0)]
        parallelogram_shape2 = [Point(0, 0), Point('-0.6', '0.8'),
                                Point('1.4', '0.8'), Point(2, 0)]
        parallelogram_shape3 = [Point(0, 0), Point('0.2', '0.65'),
                                Point('2.1', '0.8'), Point('1.9', '0.15')]
        parallelogram_shape4 = [Point(0, '0.8'), Point('1.9', '0.65'),
                                Point('2.1', 0), Point('0.2', '0.15')]
        mark1 = next(shared.ls_marks_source)[0]
        mark2 = next(shared.ls_marks_source)[0]
        lbls = masks = marks = None
        masks_disposition = next(shared.alternate_2masks_source)[0]
        if variant == 0:  # kites
            shape_variants = {
                1: {'args': kite_shape1, 'rotation_angle': 0,
                    'baseline': '-9pt'},
                2: {'args': kite_shape1, 'rotation_angle': 180,
                    'baseline': '-5pt'},
                3: {'args': kite_shape2, 'rotation_angle': 0,
                    'baseline': '-4pt',
                    'boundingbox': (0, '-0.5', '2.4', '0.7')},
                4: {'args': kite_shape2, 'rotation_angle': 180,
                    'baseline': '0pt',
                    'boundingbox': (0, '-0.7', '2.4', '0.5')}
            }
            lbls = [labels[0][1], labels[0][1], labels[1][1], labels[1][1]]
            masks = {'left': [None, ' ', None, ' '],
                     'right': [None, ' ', ' ', None]}[masks_disposition]
            marks = [mark1, mark1, mark2, mark2]
        elif variant == 1:  # parallelograms
            shape_variants = {
                1: {'args': parallelogram_shape1, 'rotation_angle': 0,
                    'baseline': {'left': '12pt',
                                 'right': '3pt'}[masks_disposition]},
                2: {'args': parallelogram_shape2, 'rotation_angle': 0,
                    'baseline': {'left': '10pt',
                                 'right': '5pt'}[masks_disposition]},
                3: {'args': parallelogram_shape3, 'rotation_angle': 0,
                    'baseline': {'left': '12pt',
                                 'right': '4pt'}[masks_disposition]},
                4: {'args': parallelogram_shape4, 'rotation_angle': 0,
                    'baseline': {'left': '12pt',
                                 'right': '4pt'}[masks_disposition]},
            }
            shortest = min(labels[0][1], labels[1][1])
            longest = max(labels[0][1], labels[1][1])
            lbls = [shortest, longest, shortest, longest]
            marks = [mark1, mark2, mark1, mark2]
        elif variant == 2:  # rectangles
            shape_builder = Rectangle
            shape_variants = {
                1: {'width': Number('0.5'), 'length': Number('2.6'),
                    'rotation_angle': 0, 'right_angle_radius': Number('0.15'),
                    'baseline': {'left': '8pt',
                                 'right': '1pt'}[masks_disposition]},
                2: {'width': Number('0.7'), 'length': 2,
                    'rotation_angle': 0, 'right_angle_radius': Number('0.15'),
                    'baseline': {'left': '8pt',
                                 'right': '1pt'}[masks_disposition]},
                3: {'width': Number('0.6'), 'length': Number('2.4'),
                    'rotation_angle': 0, 'right_angle_radius': Number('0.15'),
                    'baseline': {'left': '9pt',
                                 'right': '2pt'}[masks_disposition]},
                4: {'width': Number('0.8'), 'length': Number('1.6'),
                    'rotation_angle': 0, 'right_angle_radius': Number('0.15'),
                    'baseline': {'left': '8pt',
                                 'right': '1pt'}[masks_disposition],
                    'boundingbox': (0, '-0.2', '1.6', 1)},
            }
            shortest = min(labels[0][1], labels[1][1])
            longest = max(labels[0][1], labels[1][1])
            lbls = [longest, shortest, longest, shortest]
        if variant in [1, 2]:
            # common masking for rectangles and parallelogram
            masks = {'left': [None, None, ' ', ' '],
                     'right': [' ', ' ', None, None]}[masks_disposition]
        return self._polygon(
            shared.quadrilateral_2_2_shapes_source,
            shape_variants,
            shape_builder,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks
        )

    def _quadrilateral_3_1(self, variant=None, labels=None, name=None,
                           label_vertices=None, thickness=None,
                           length_unit=None, shape_variant_nb=None):
        shape1 = [Point(0, 0), Point('0.46', '0.8'),
                  Point('1.38', '0.8'), Point('1.84', 0)]
        shape2 = [Point('0.02', '0.5'), Point('0.9', '0.7'),
                  Point('0.9', '-0.2'), Point('0.02', 0)]
        mark = next(shared.ls_marks_source)[0]
        masks_disposition = next(shared.alternate_3masks_source)[0]
        shape_variants = {
            1: {'args': shape1, 'rotation_angle': 0,
                'baseline':
                {1: '5pt', 2: '8pt', 3: '6pt'}[masks_disposition]},
            2: {'args': shape1, 'rotation_angle': 180,
                'baseline':
                {1: '10pt', 2: '8pt', 3: '11pt'}[masks_disposition]},
            3: {'args': shape2, 'rotation_angle': 0,
                'baseline':
                {1: '10pt', 2: '5pt', 3: '-1pt'}[masks_disposition],
                'boundingbox': (0, '-0.3', '0.9', '0.9')},
            4: {'args': shape2, 'rotation_angle': 180,
                'baseline':
                {1: '-1pt', 2: '5pt', 3: '10pt'}[masks_disposition],
                'boundingbox': (0, '-0.3', '0.9', '0.9')},
        }
        lbls = [labels[1][1], labels[1][1], labels[1][1], labels[0][1]]
        masks = {1: [None, ' ', ' ', None],
                 2: [' ', None, ' ', None],
                 3: [' ', ' ', None, None]}[masks_disposition]
        marks = [mark, mark, mark, None]
        return self._polygon(
            shared.quadrilateral_3_1_shapes_source,
            shape_variants,
            Quadrilateral,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks
        )

    def _quadrilateral_4(self, variant=None, labels=None, name=None,
                         label_vertices=None, thickness=None,
                         length_unit=None, shape_variant_nb=None):
        mark = next(shared.ls_marks_source)[0]
        masks_disposition = next(shared.alternate_4masks_source)[0]
        if variant == 0:  # rhombuses
            shape_builder = Rhombus
            shape_variants = {
                1: {'side_length': Number('1.2'), 'build_angle': 45,
                    'rotation_angle': 0,
                    'use_mark': mark,
                    # 1: above right, 2: bottom right,
                    # 3: bottom left, 4: above left
                    'baseline':
                    {1: '0pt', 2: '-6pt', 3: '-6pt', 4: '0pt'}
                    [masks_disposition],
                    'boundingbox': (0, '-0.65', '2.3', '0.65')},
            }
        elif variant == 1:  # squares
            shape_builder = Square
            shape_variants = {
                1: {'side_length': 1,
                    'rotation_angle': 0,
                    'use_mark': mark,
                    'right_angle_radius': Number('0.15'),
                    # 1: above, 2: right, 3: below, 4: left
                    'baseline':
                    {1: '16pt', 2: '12pt', 3: '7pt', 4: '12pt'}
                    [masks_disposition]},
            }
        lbls = [labels[0][1]]
        masks = {1: [None, ' ', ' ', ' '],
                 2: [' ', None, ' ', ' '],
                 3: [' ', ' ', None, ' '],
                 4: [' ', ' ', ' ', None]}[masks_disposition]
        return self._polygon(
            shared.quadrilateral_4_shapes_source,
            shape_variants,
            shape_builder,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks
        )

    def _pentagon_1_1_1_1_1(self, variant=None, labels=None, name=None,
                            label_vertices=None, thickness=None,
                            length_unit=None, shape_variant_nb=None):
        pentagon_shape1 = [Point('0.6', 0), Point(0, '0.4'),
                           Point('1.2', '0.8'), Point('2.4', '0.4'),
                           Point('1.8', 0)]
        shape_variants = {
            1: {'args': pentagon_shape1, 'rotation_angle': 0,
                'baseline': '8pt',
                # 'boundingbox': None,
                # 'use_mark': next(shared.ls_marks_source)[0]
                },
            2: {'args': pentagon_shape1, 'rotation_angle': 180,
                'baseline': '6pt',
                # 'boundingbox': None,
                # 'use_mark': next(shared.ls_marks_source)[0]
                },
        }
        return self._polygon(
            shared.pentagon_1_1_1_1_1_shapes_source,
            shape_variants,
            Polygon,
            labels=[lbl[1] for lbl in labels],
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
        )

    def _pentagon_2_1_1_1(self, variant=None, labels=None, name=None,
                          label_vertices=None, thickness=None,
                          length_unit=None, shape_variant_nb=None):
        pentagonv0_shape1 = [Point('1.05', '-0.2'), Point('0.3', '-0.1'),
                             Point(0, '0.6'), Point('1.4', '0.6'),
                             Point('2.4', '0.1')]
        pentagonv1_shape1 = [Point('0.2', 0), Point(0, '0.57'),
                             Point('1.2', '0.8'), Point('1.95', '0.4'),
                             Point('1.5', 0)]
        mark = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': pentagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '3pt'},
                2: {'args': pentagonv0_shape1, 'rotation_angle': 180,
                    'baseline': '3pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': pentagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '9pt'},
                2: {'args': pentagonv1_shape1, 'rotation_angle': 180,
                    'baseline': '6pt'},
            }
        singles = []
        doubled = []
        for lbl in labels:
            if lbl[0] == 1:
                singles.append(lbl[1])
            else:
                doubled.append(lbl[1])
                doubled.append(lbl[1])
        random.shuffle(singles)
        if variant == 0:
            lbls = [doubled.pop(), doubled.pop(), singles.pop(), singles.pop(),
                    singles.pop()]
            masks = [None, ' ', None, None, None]
            marks = [mark, mark, None, None, None]
        elif variant == 1:
            lbls = [doubled.pop(), singles.pop(), singles.pop(), doubled.pop(),
                    singles.pop()]
            masks = [None, None, None, ' ', None]
            marks = [mark, None, None, mark, None]
        return self._polygon(
            shared.pentagon_2_1_1_1_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb
        )

    def _pentagon_2_2_1(self, variant=None, labels=None, name=None,
                        label_vertices=None, thickness=None,
                        length_unit=None, shape_variant_nb=None):
        pentagonv0_shape1 = [Point(1, 0), Point('0.08', '0.4'),
                             Point('0.77', '0.8'), Point('1.57', '0.7'),
                             Point(2, '0.1')]
        pentagonv1_shape1 = [Point('0.5', 0), Point(0, '0.33'),
                             Point('0.88', '0.8'), Point('1.86', '0.59'),
                             Point('1.73', 0)]
        pentagonv2_shape1 = [Point('0.71', '-0.1'), Point(0, '0.46'),
                             Point('0.76', '0.7'), Point('1.64', '0.5'),
                             Point('1.5', 0)]
        mark1 = next(shared.ls_marks_source)[0]
        mark2 = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': pentagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '8pt'},
                2: {'args': pentagonv0_shape1, 'rotation_angle': 180,
                    'baseline': '8pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': pentagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '7pt'},
                2: {'args': pentagonv1_shape1, 'rotation_angle': 180,
                    'baseline': '7pt'},
            }
        elif variant == 2:
            shape_variants = {
                1: {'args': pentagonv2_shape1, 'rotation_angle': 0,
                    'baseline': '6pt'},
                2: {'args': pentagonv2_shape1, 'rotation_angle': 180,
                    'baseline': '6pt'},
            }
        singles = []
        doubled1 = []
        doubled2 = []
        for lbl in labels:
            if lbl[0] == 1:
                singles.append(lbl[1])
            else:
                if not doubled1:
                    doubled1.append(lbl[1])
                    doubled1.append(lbl[1])
                else:
                    doubled2.append(lbl[1])
                    doubled2.append(lbl[1])
        random.shuffle(singles)
        if variant == 0:
            lbls = [doubled1.pop(), doubled1.pop(),
                    doubled2.pop(), doubled2.pop(),
                    singles.pop()]
            masks = [None, ' ', None, ' ', None]
            marks = [mark1, mark1, mark2, mark2, None]
        elif variant == 1:
            lbls = [doubled1.pop(), doubled2.pop(),
                    doubled2.pop(), doubled1.pop(),
                    singles.pop()]
            masks = [None, None, ' ', ' ', None]
            marks = [mark1, mark2, mark2, mark1, None]
        elif variant == 2:
            lbls = [doubled1.pop(), doubled2.pop(),
                    doubled1.pop(), doubled2.pop(),
                    singles.pop()]
            masks = [None, None, ' ', ' ', None]
            marks = [mark1, mark2, mark1, mark2, None]
        return self._polygon(
            shared.pentagon_2_2_1_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb
        )

    def _pentagon_3_1_1(self, variant=None, labels=None, name=None,
                        label_vertices=None, thickness=None,
                        length_unit=None, shape_variant_nb=None):
        pentagonv0_shape1 = [Point(0, '0.3'), Point('0.62', '0.8'),
                             Point('1.42', '0.8'), Point('1.81', '0.1'),
                             Point('0.7', 0)]
        pentagonv1_shape1 = [Point('0.3', '0.6'), Point('1.28', '0.8'),
                             Point('2.26', '0.6'), Point('1.4', 0),
                             Point('0.4', 0)]
        mark = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': pentagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '8pt'},
                2: {'args': pentagonv0_shape1, 'rotation_angle': 180,
                    'baseline': '9pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': pentagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '9pt'},
                2: {'args': pentagonv1_shape1, 'rotation_angle': 180,
                    'baseline': '7pt'},
            }
        singles = []
        tripled = []
        for lbl in labels:
            if lbl[0] == 1:
                singles.append(lbl[1])
            else:
                tripled.append(lbl[1])
                tripled.append(lbl[1])
                tripled.append(lbl[1])
        random.shuffle(singles)
        if variant == 0:
            lbls = [tripled.pop(), tripled.pop(), tripled.pop(), singles.pop(),
                    singles.pop()]
            masks = [None, ' ', ' ', None, None]
            marks = [mark, mark, mark, None, None]
        elif variant == 1:
            lbls = [tripled.pop(), tripled.pop(), singles.pop(), tripled.pop(),
                    singles.pop()]
            masks = [None, ' ', None, ' ', None]
            marks = [mark, mark, None, mark, None]
        return self._polygon(
            shared.pentagon_3_1_1_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb
        )

    def _pentagon_3_2(self, variant=None, labels=None, name=None,
                      label_vertices=None, thickness=None,
                      length_unit=None, shape_variant_nb=None):
        pentagonv0_shape1 = [Point(0, 0), Point('0.33', '0.73'),
                             Point('1.12', '0.8'), Point('1.86', '0.5'),
                             Point(1, 0)]
        pentagonv1_shape1 = [Point(0, 0), Point('0.33', '0.73'),
                             Point('1.12', '0.8'), Point('1.86', '0.5'),
                             Point(1, 0)]
        mark1 = next(shared.ls_marks_source)[0]
        mark2 = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': pentagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '6pt'},
                2: {'args': pentagonv0_shape1, 'rotation_angle': 180,
                    'baseline': '12pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': pentagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
                2: {'args': pentagonv1_shape1, 'rotation_angle': 180,
                    'baseline': '4pt'},
            }
        doubled = []
        tripled = []
        for lbl in labels:
            if lbl[0] == 2:
                doubled.append(lbl[1])
                doubled.append(lbl[1])
            else:
                tripled.append(lbl[1])
                tripled.append(lbl[1])
                tripled.append(lbl[1])
        if variant == 0:
            lbls = [tripled.pop(), tripled.pop(), tripled.pop(), doubled.pop(),
                    doubled.pop()]
            masks = [None, ' ', ' ', None, ' ']
            marks = [mark1, mark1, mark1, mark2, mark2]
        elif variant == 1:
            lbls = [tripled.pop(), tripled.pop(), doubled.pop(), tripled.pop(),
                    doubled.pop()]
            masks = [None, ' ', None, ' ', ' ']
            marks = [mark1, mark1, mark2, mark1, mark2]
        return self._polygon(
            shared.pentagon_3_2_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb
        )

    def _pentagon_4_1(self, variant=None, labels=None, name=None,
                      label_vertices=None, thickness=None,
                      length_unit=None, shape_variant_nb=None):
        pentagonv0_shape1 = [Point('0.21', '0.73'), Point('1.11', '0.8'),
                             Point('1.78', '0.2'), Point('0.9', 0),
                             Point(0, 0)]
        mark = next(shared.ls_marks_source)[0]
        shape_variants = {
            1: {'args': pentagonv0_shape1, 'rotation_angle': 0,
                'baseline': '13pt'},
            2: {'args': pentagonv0_shape1, 'rotation_angle': 180,
                'baseline': '1pt'},
        }
        singles = []
        quadrupled = []
        for lbl in labels:
            if lbl[0] == 4:
                quadrupled.append(lbl[1])
                quadrupled.append(lbl[1])
                quadrupled.append(lbl[1])
                quadrupled.append(lbl[1])
            else:
                singles.append(lbl[1])
        lbls = [quadrupled.pop(), quadrupled.pop(), quadrupled.pop(),
                quadrupled.pop(), singles.pop()]
        masks = [None, ' ', ' ', ' ', None]
        marks = [mark, mark, mark, mark, None]
        return self._polygon(
            shared.pentagon_4_1_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb
        )

    def _pentagon_5(self, variant=None, labels=None, name=None,
                    label_vertices=None, thickness=None,
                    length_unit=None, shape_variant_nb=None):
        pentagonv0_shape1 = [Point('-0.22', '0.67'), Point('0.35', '1.08'),
                             Point('0.92', '0.67'), Point('0.7', 0),
                             Point(0, 0)]
        mark = next(shared.ls_marks_source)[0]
        shape_variants = {
            1: {'args': pentagonv0_shape1, 'rotation_angle': 0,
                'baseline': '16pt'},
            2: {'args': pentagonv0_shape1, 'rotation_angle': 180,
                'baseline': '4pt'},
        }
        masks = [None, ' ', ' ', ' ', ' ']
        marks = [mark, mark, mark, mark, mark]
        return self._polygon(
            shared.pentagon_5_shapes_source,
            shape_variants,
            Polygon,
            labels=[labels[0][1] for _ in range(5)],
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb
        )
