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
from mathmakerlib.geometry import Point, AngleDecoration, Polygon, Triangle
from mathmakerlib.geometry import IsoscelesTriangle, EquilateralTriangle
from mathmakerlib.geometry import RightTriangle
from mathmakerlib.geometry import Quadrilateral, Rectangle, Rhombus, Square

from mathmaker.lib import shared
from mathmaker.lib.tools.generators import Generator


class ShapeGenerator(Generator):

    def generate(self, codename=None, variant=None, labels=None, name=None,
                 **kwargs):
        """
        :param codename: a str describing the type of polygon and the sides
        lengths, grouped by equal sides batches, like triangle_1_1_1,
        pentagon_3_2 etc.
        :type codename: str
        :param variant: the variant number
        :type variant: int
        :param labels: the labels to set, in the form of a list of couples
        (nb_of_sides, length). This list will be checked at start.
        :type labels: list (of couples)
        :param name: the name of the Polygon
        :type name: str (or None, then it will be set automatically)
        :param label_vertices: whether or not label the Polygon's vertices
        :type label_vertices: bool
        :param thickness: the thickness of the Polygon's sides
        :type thickness: any correct thickness value (None, or see tikz
        possible values)
        :param length_unit: the length unit of the sides labels
        :type length_unit: None or correct str unit name, or a
        mathmakerlib.calculus.Unit instance
        """
        label_vertices = kwargs.get('label_vertices', None)
        if not isinstance(label_vertices, bool):
            raise TypeError('keyword argument label_vertices must be set to '
                            'True or False')
        thickness = kwargs.get('thickness', None)
        length_unit = kwargs.get('length_unit', None)
        wlines_nb = kwargs.get('wlines_nb', 0)
        self.check_args(codename_prefix=codename.split('_')[0] + '_',
                        distcode='_'.join(codename.split('_')[1:]),
                        variant=variant, labels=labels, name=name)
        return getattr(self,
                       '_' + codename)(variant=variant, labels=labels,
                                       name=name,
                                       label_vertices=label_vertices,
                                       thickness=thickness,
                                       length_unit=length_unit,
                                       wlines_nb=wlines_nb)

    def _polygon(self, shapes_source, shape_variants, shape_builder, labels,
                 masks=None, marks=None, length_unit=None, name=None,
                 shape_variant_nb=None, label_vertices=None, thickness=None,
                 rt_extra_info=None, wlines_nb=0):
        if shape_variant_nb is None:
            shape_variant_nb = next(shapes_source)[0]
        if rt_extra_info is not None and shape_variant_nb in rt_extra_info:
            labels[0], labels[1] = labels[1], labels[0]
        build_data = shape_variants[shape_variant_nb]
        build_data.update({'name': name, 'label_vertices': label_vertices,
                           'thickness': thickness,
                           'sloped_sides_labels': False})
        baseline = build_data.pop('baseline', None)
        if isinstance(baseline, dict):
            baseline = baseline[wlines_nb]
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
                if isinstance(a.decoration, AngleDecoration) and a.mark_right:
                    u = None
                    if a.decoration.radius is not None:
                        u = a.decoration.radius.unit
                    a.decoration.radius = Number(right_angle_radius, unit=u)
        return polygon

    def _triangle_1_1_1(self, variant=None, labels=None, name=None,
                        label_vertices=None, thickness=None, length_unit=None,
                        shape_variant_nb=None, wlines_nb=0):
        if variant not in [0, 1]:
            raise ValueError('variant must be 0 or 1 (not \'{}\')'
                             .format(variant))
        if variant == 0:  # scalene triangle shapes
            shape_variants = {1: {'args': [Point(0, 0), Point(2, 0),
                                           Point(Number('0.582'),
                                                 Number('0.924'))],
                                  'baseline': '6pt'},
                              2: {'args': [Point(0, 0), Point(2, 0),
                                           Point(Number('1.418'),
                                                 Number('0.924'))],
                                  'baseline': '6pt'},
                              3: {'args': [Point(2, Number('0.924')),
                                           Point(0, Number('0.924')),
                                           Point(Number('1.418'), 0)],
                                  'baseline': '13pt'},
                              4: {'args': [Point(2, Number('0.924')),
                                           Point(0, Number('0.924')),
                                           Point(Number('0.582'), 0)],
                                  'baseline': '13pt'}
                              }
            shapes_source = shared.scalene_triangle_shapes_source
            shape_builder = Triangle
        elif variant == 1:  # right triangle shapes
            shape_variants = {1: {'start_vertex': Point(0, 0),
                                  'leg0_length': 2, 'leg1_length': 1,
                                  'baseline': {0: '8pt', 1: '8pt', 2: '6pt'}},
                              2: {'start_vertex': Point(2, 0),
                                  'leg0_length': 1, 'leg1_length': 2,
                                  'rotation_angle': 90,
                                  'baseline': {0: '17pt', 1: '17pt',
                                               2: '23pt'}},
                              3: {'start_vertex': Point(2, 1),
                                  'leg0_length': 2, 'leg1_length': 1,
                                  'rotation_angle': 180,
                                  'baseline': {0: '17pt', 1: '36pt',
                                               2: '40pt'}},
                              4: {'start_vertex': Point(0, 1),
                                  'leg0_length': 1, 'leg1_length': 2,
                                  'rotation_angle': -90,
                                  'baseline': {0: '8pt', 1: '42pt',
                                               2: '48pt'}},
                              5: {'start_vertex': Point('2.236', 0),
                                  'leg0_length': 2, 'leg1_length': 1,
                                  'rotation_angle': Number('153.4'),
                                  'baseline': {0: '8pt', 1: '6pt', 2: '10pt'}},
                              6: {'start_vertex': Point('2.236', 0),
                                  'leg0_length': 1, 'leg1_length': 2,
                                  'rotation_angle': Number('116.6'),
                                  'baseline': {0: '8pt', 1: '14pt',
                                               2: '17pt'}},
                              7: {'start_vertex': Point(0, '0.981'),
                                  'leg0_length': 1, 'leg1_length': 2,
                                  'rotation_angle': Number('-63.4'),
                                  'baseline': {0: '17pt', 1: '44pt',
                                               2: '52pt'}},
                              8: {'start_vertex': Point(0, '0.981'),
                                  'leg0_length': 2, 'leg1_length': 1,
                                  'rotation_angle': Number('-26.6'),
                                  'baseline': {0: '17pt', 1: '36pt',
                                               2: '44pt'}}
                              }
            shapes_source = shared.right_triangle_shapes_source
            shape_builder = RightTriangle
        lbls = [labels[i][1] for i in range(len(labels))]
        rt_extra_info = None
        if variant == 1:
            lbls = sorted(lbls)
            rt_extra_info = [1, 3, 5, 8]
        return self._polygon(
            shapes_source,
            shape_variants,
            shape_builder,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            shape_variant_nb=shape_variant_nb,
            rt_extra_info=rt_extra_info,
            wlines_nb=wlines_nb
        )

    def _triangle_2_1(self, variant=None, labels=None, name=None,
                      label_vertices=None, thickness=None, length_unit=None,
                      shape_variant_nb=None, wlines_nb=0):
        mark = next(shared.ls_marks_source)[0]
        shape_variants = {1: {'base_length': Number('2.8'),
                              'equal_legs_length': Number('1.52'),
                              'rotation_angle': 0, 'use_mark': mark,
                              'baseline': '4pt'},
                          2: {'base_length': Number('2.8'),
                              'equal_legs_length': Number('1.52'),
                              'rotation_angle': 180, 'use_mark': mark,
                              'baseline': '2pt'},
                          3: {'base_length': Number('0.8'),
                              'equal_legs_length': Number('2.4'),
                              'rotation_angle': 90, 'use_mark': mark,
                              'baseline': '15pt'},
                          4: {'base_length': Number('0.8'),
                              'equal_legs_length': Number('2.4'),
                              'rotation_angle': -90, 'use_mark': mark,
                              'baseline': '23pt'},
                          5: {'base_length': Number('0.8'),
                              'equal_legs_length': Number('2.4'),
                              'rotation_angle': Number('-99.6'),
                              'use_mark': mark,
                              'baseline': '25pt'},
                          6: {'base_length': Number('0.8'),
                              'equal_legs_length': Number('2.4'),
                              'rotation_angle': Number('-80.4'),
                              'use_mark': mark,
                              'baseline': '18pt'},
                          7: {'base_length': Number('0.8'),
                              'equal_legs_length': Number('2.4'),
                              'rotation_angle': Number('99.6'),
                              'use_mark': mark,
                              'baseline': '18pt'},
                          8: {'base_length': Number('0.8'),
                              'equal_legs_length': Number('2.4'),
                              'rotation_angle': Number('80.4'),
                              'use_mark': mark,
                              'baseline': '15pt'}
                          }
        baselbl, eqlbl = labels[0][1], labels[1][1]
        if labels[0][0] == 2:
            baselbl, eqlbl = eqlbl, baselbl
        return self._polygon(
            shared.triangle_2_1_shapes_source,
            shape_variants,
            IsoscelesTriangle,
            labels=[baselbl, eqlbl],
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _triangle_3(self, variant=None, labels=None, name=None,
                    label_vertices=None, thickness=None, length_unit=None,
                    shape_variant_nb=None, wlines_nb=0):
        mark = next(shared.ls_marks_source)[0]
        shape_variants = {1: {'side_length': Number('1.1'),
                              'rotation_angle': 0,
                              'use_mark': mark,
                              'baseline': '12pt'},
                          2: {'side_length': Number('1.1'),
                              'rotation_angle': 60,
                              'use_mark': mark,
                              'baseline': '0pt'},
                          3: {'side_length': Number('1.1'),
                              'rotation_angle': Number('29.9'),
                              'use_mark': mark,
                              'baseline': '6pt'},
                          4: {'side_length': Number('1.1'),
                              'rotation_angle': 90,
                              'use_mark': mark,
                              'baseline': '0pt',
                              'boundingbox': ('-0.2', '-0.24', '0.97', '0.97')}
                          }
        return self._polygon(
            shared.triangle_3_shapes_source,
            shape_variants,
            EquilateralTriangle,
            labels=[labels[0][1]],
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _quadrilateral_1_1_1_1(self, variant=None, labels=None, name=None,
                               label_vertices=None, thickness=None,
                               length_unit=None, shape_variant_nb=None,
                               wlines_nb=0):
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
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _quadrilateral_2_1_1(self, variant=None, labels=None, name=None,
                             label_vertices=None, thickness=None,
                             length_unit=None, shape_variant_nb=None,
                             wlines_nb=0):
        if variant not in [0, 1]:
            raise ValueError('variant must be 0 or 1 (not \'{}\')'
                             .format(variant))
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
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _quadrilateral_2_2(self, variant=None, labels=None, name=None,
                           label_vertices=None, thickness=None,
                           length_unit=None, shape_variant_nb=None,
                           wlines_nb=0):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be 0, 1 or 2 (not \'{}\')'
                             .format(variant))
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
                    'baseline': {'left': '-3pt',
                                 'right': '1pt'}[masks_disposition]},
                2: {'width': Number('0.7'), 'length': 2,
                    'rotation_angle': 0, 'right_angle_radius': Number('0.15'),
                    'baseline': {'left': '-3pt',
                                 'right': '1pt'}[masks_disposition]},
                3: {'width': Number('0.6'), 'length': Number('2.4'),
                    'rotation_angle': 0, 'right_angle_radius': Number('0.15'),
                    'baseline': {'left': '-3pt',
                                 'right': '2pt'}[masks_disposition]},
                4: {'width': Number('0.8'), 'length': Number('1.6'),
                    'rotation_angle': 0, 'right_angle_radius': Number('0.15'),
                    'baseline': {'left': '-3pt',
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
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _quadrilateral_3_1(self, variant=None, labels=None, name=None,
                           label_vertices=None, thickness=None,
                           length_unit=None, shape_variant_nb=None,
                           wlines_nb=0):
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
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _quadrilateral_4(self, variant=None, labels=None, name=None,
                         label_vertices=None, thickness=None,
                         length_unit=None, shape_variant_nb=None,
                         wlines_nb=0):
        if variant not in [0, 1]:
            raise ValueError('variant must be 0 or 1 (not \'{}\')'
                             .format(variant))
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
            masks=masks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _pentagon_1_1_1_1_1(self, variant=None, labels=None, name=None,
                            label_vertices=None, thickness=None,
                            length_unit=None, shape_variant_nb=None,
                            wlines_nb=0):
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
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _pentagon_2_1_1_1(self, variant=None, labels=None, name=None,
                          label_vertices=None, thickness=None,
                          length_unit=None, shape_variant_nb=None,
                          wlines_nb=0):
        if variant not in [0, 1]:
            raise ValueError('variant must be 0 or 1 (not \'{}\')'
                             .format(variant))
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
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _pentagon_2_2_1(self, variant=None, labels=None, name=None,
                        label_vertices=None, thickness=None,
                        length_unit=None, shape_variant_nb=None,
                        wlines_nb=0):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be 0, 1 or 2 (not \'{}\')'
                             .format(variant))
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
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _pentagon_3_1_1(self, variant=None, labels=None, name=None,
                        label_vertices=None, thickness=None,
                        length_unit=None, shape_variant_nb=None,
                        wlines_nb=0):
        if variant not in [0, 1]:
            raise ValueError('variant must be 0 or 1 (not \'{}\')'
                             .format(variant))
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
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _pentagon_3_2(self, variant=None, labels=None, name=None,
                      label_vertices=None, thickness=None,
                      length_unit=None, shape_variant_nb=None,
                      wlines_nb=0):
        if variant not in [0, 1]:
            raise ValueError('variant must be 0 or 1 (not \'{}\')'
                             .format(variant))
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
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _pentagon_4_1(self, variant=None, labels=None, name=None,
                      label_vertices=None, thickness=None,
                      length_unit=None, shape_variant_nb=None,
                      wlines_nb=0):
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
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _pentagon_5(self, variant=None, labels=None, name=None,
                    label_vertices=None, thickness=None,
                    length_unit=None, shape_variant_nb=None,
                    wlines_nb=0):
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
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_1_1_1_1_1_1(self, variant=None, labels=None, name=None,
                             label_vertices=None, thickness=None,
                             length_unit=None, shape_variant_nb=None,
                             wlines_nb=0):
        hexagon_shape1 = [Point(0, '0.4'), Point('0.7', '0.8'),
                          Point('1.7', '0.8'), Point('2.8', '0.5'),
                          Point(2, 0), Point('0.8', 0)]
        shape_variants = {
            1: {'args': hexagon_shape1, 'rotation_angle': 0,
                'baseline': '9pt',
                # 'boundingbox': None,
                # 'use_mark': next(shared.ls_marks_source)[0]
                },
            2: {'args': hexagon_shape1, 'rotation_angle': 180,
                'baseline': '9pt',
                # 'boundingbox': None,
                # 'use_mark': next(shared.ls_marks_source)[0]
                },
        }
        return self._polygon(
            shared.hexagon_1_1_1_1_1_1_shapes_source,
            shape_variants,
            Polygon,
            labels=[lbl[1] for lbl in labels],
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_2_1_1_1_1(self, variant=None, labels=None, name=None,
                           label_vertices=None, thickness=None,
                           length_unit=None, shape_variant_nb=None,
                           wlines_nb=0):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be 0, 1 or 2 (not \'{}\')'
                             .format(variant))
        hexagonv0_shape1 = [Point('0.17', '0.47'), Point('0.9', '0.8'),
                            Point('1.7', '0.8'), Point('2.8', '0.4'),
                            Point(2, 0), Point('0.7', 0)]
        hexagonv1_shape1 = [Point(0, '0.3'), Point('0.87', '0.8'),
                            Point('1.7', '0.8'), Point('2.68', '0.6'),
                            Point('2.2', '0.1'), Point(1, 0)]
        hexagonv2_shape1 = [Point(0, '0.7'), Point('0.83', '0.9'),
                            Point('2.2', '0.8'), Point('2.44', '0.15'),
                            Point('1.6', 0), Point('0.2', 0)]
        hexagonv2_shape2 = [Point('0.93', 0), Point('0.1', '0.2'),
                            Point('0.3', '0.9'), Point('1.3', '1'),
                            Point('2.14', '0.9'), Point('1.9', '0.1')]
        mark = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': hexagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '9pt'},
                2: {'args': hexagonv0_shape1, 'rotation_angle': 180,
                    'baseline': '9.5pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': hexagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '9pt'},
                2: {'args': hexagonv1_shape1, 'rotation_angle': 180,
                    'baseline': '10pt'},
            }
        elif variant == 2:
            shape_variants = {
                1: {'args': hexagonv2_shape1, 'rotation_angle': 0,
                    'baseline': '10pt'},
                2: {'args': hexagonv2_shape2, 'rotation_angle': 0,
                    'baseline': '10pt'},
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
                    singles.pop(), singles.pop()]
            masks = [None, ' ', None, None, None, None]
            marks = [mark, mark, None, None, None, None]
        elif variant == 1:
            lbls = [doubled.pop(), singles.pop(), doubled.pop(), singles.pop(),
                    singles.pop(), singles.pop()]
            masks = [None, None, ' ', None, None, None]
            marks = [mark, None, mark, None, None, None]
        elif variant == 2:
            lbls = [doubled.pop(), singles.pop(), singles.pop(), doubled.pop(),
                    singles.pop(), singles.pop()]
            masks = [None, None, None, ' ', None, None]
            marks = [mark, None, None, mark, None, None]
        return self._polygon(
            shared.hexagon_2_1_1_1_1_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_2_2_1_1(self, variant=None, labels=None, name=None,
                         label_vertices=None, thickness=None,
                         length_unit=None, shape_variant_nb=None,
                         wlines_nb=0):
        if variant not in [0, 1, 2, 3, 4, 5, 6, 7]:
            raise ValueError('variant must be 0, 1, 2, 3, 4, 5, 6, or 7 '
                             '(not \'{}\')'.format(variant))
        hexagonv0_shape1 = [Point('1.6', 0), Point('0.7', 0),
                            Point(0, '0.56'), Point('0.9', 1),
                            Point('1.9', 1), Point('2.8', '0.5')]
        hexagonv1_shape1 = [Point(0, '0.4'), Point('0.53', 1),
                            Point('1.63', '1.1'), Point('2.4', '0.9'),
                            Point('1.76', 0), Point('0.8', 0)]
        hexagonv2_shape1 = [Point('0.4', 0), Point(0, '0.81'),
                            Point('1.03', '1.1'), Point('2.14', '0.9'),
                            Point('2.7', '0.2'), Point('1.5', '0.2')]
        hexagonv3_shape1 = [Point(0, '0.6'), Point('0.69', '1.1'),
                            Point('1.69', '1.1'), Point('2.32', '0.54'),
                            Point('1.64', 0), Point('0.64', 0)]
        hexagonv4_shape1 = [Point('2.7', '0.8'), Point('2.41', 0),
                            Point('1.41', 0), Point('0.45', '0.27'),
                            Point('0.9', '1.1'), Point('1.75', '1.1')]
        hexagonv5_shape1 = [Point('0.39', '0.22'), Point(0, '0.8'),
                            Point('0.63', '1.1'), Point('1.88', '0.86'),
                            Point('2.44', '0.15'), Point('1.55', 0), ]
        hexagonv6_shape1 = [Point('0.22', '0.8'), Point('1.2', 1),
                            Point('1.99', '0.9'), Point('2.2', '0.1'),
                            Point('1.2', 0), Point('0.41', '0.1'), ]
        hexagonv7_shape1 = [Point('0.34', '0.9'), Point('1.11', '1.1'),
                            Point('2.09', '0.9'), Point('1.6', '0.09'),
                            Point('0.6', 0), Point('-0.18', '0.19'), ]
        mark1 = next(shared.ls_marks_source)[0]
        mark2 = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': hexagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '11pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': hexagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 2:
            shape_variants = {
                1: {'args': hexagonv2_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 3:
            shape_variants = {
                1: {'args': hexagonv3_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 4:
            shape_variants = {
                1: {'args': hexagonv4_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 5:
            shape_variants = {
                1: {'args': hexagonv5_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 6:
            shape_variants = {
                1: {'args': hexagonv6_shape1, 'rotation_angle': 0,
                    'baseline': '15pt'},
            }
        elif variant == 7:
            shape_variants = {
                1: {'args': hexagonv7_shape1, 'rotation_angle': 0,
                    'baseline': '17pt'},
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
                    singles.pop(), singles.pop()]
            masks = [None, ' ', None, ' ', None, None]
            marks = [mark1, mark1, mark2, mark2, None, None]
        elif variant == 1:
            lbls = [doubled1.pop(), doubled2.pop(),
                    doubled1.pop(), doubled2.pop(),
                    singles.pop(), singles.pop()]
            masks = [None, None, ' ', ' ', None, None]
            marks = [mark1, mark2, mark1, mark2, None, None]
        elif variant == 2:
            lbls = [doubled1.pop(), doubled2.pop(),
                    doubled2.pop(), doubled1.pop(),
                    singles.pop(), singles.pop()]
            masks = [None, None, ' ', ' ', None, None]
            marks = [mark1, mark2, mark2, mark1, None, None]
        elif variant == 3:
            lbls = [doubled1.pop(), doubled2.pop(),
                    doubled1.pop(), singles.pop(),
                    doubled2.pop(), singles.pop()]
            masks = [None, None, ' ', None, ' ', None]
            marks = [mark1, mark2, mark1, None, mark2, None]
        elif variant == 4:
            lbls = [doubled1.pop(), doubled2.pop(),
                    doubled2.pop(), singles.pop(),
                    doubled1.pop(), singles.pop()]
            masks = [None, None, ' ', None, ' ', None]
            marks = [mark1, mark2, mark2, None, mark1, None]
        elif variant == 5:
            lbls = [doubled1.pop(), doubled1.pop(),
                    singles.pop(), doubled2.pop(),
                    doubled2.pop(), singles.pop()]
            masks = [None, ' ', None, None, ' ', None]
            marks = [mark1, mark1, None, mark2, mark2, None]
        elif variant == 6:
            lbls = [doubled1.pop(), doubled2.pop(),
                    singles.pop(), doubled1.pop(),
                    doubled2.pop(), singles.pop()]
            masks = [None, None, None, ' ', ' ', None]
            marks = [mark1, mark2, None, mark1, mark2, None]
        elif variant == 7:
            lbls = [doubled1.pop(), doubled2.pop(),
                    singles.pop(), doubled2.pop(),
                    doubled1.pop(), singles.pop()]
            masks = [None, None, None, ' ', ' ', None]
            marks = [mark1, mark2, None, mark2, mark1, None]
        return self._polygon(
            shared.hexagon_2_2_1_1_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_2_2_2(self, variant=None, labels=None, name=None,
                       label_vertices=None, thickness=None,
                       length_unit=None, shape_variant_nb=None,
                       wlines_nb=0):
        if variant not in [0, 1, 2, 3]:
            raise ValueError('variant must be 0, 1, 2 or 3 '
                             '(not \'{}\')'.format(variant))
        hexagonv0_shape1 = [Point(0, '0.9'), Point('0.77', '1.1'),
                            Point('1.57', 1), Point('2.26', '0.42'),
                            Point('1.46', 0), Point('0.46', '0.01')]
        hexagonv1_shape1 = [Point(0, '0.5'), Point('0.92', '1.1'),
                            Point('1.72', '1.1'), Point('2.55', '0.63'),
                            Point('1.61', '0.05'), Point('0.66', '0.05')]
        hexagonv2_shape1 = [Point(0, '0.56'), Point('0.66', '1.02'),
                            Point('1.61', '1.07'), Point('2.4', '0.96'),
                            Point('1.87', 0), Point('0.77', 0)]
        hexagonv3_shape1 = [Point(0, '0.15'), Point(0, '.95'),
                            Point('0.94', '1.05'), Point('2.04', '0.95'),
                            Point('2.03', '0.15'), Point('1.09', 0)]
        mark1 = next(shared.ls_marks_source)[0]
        mark2 = next(shared.ls_marks_source)[0]
        mark3 = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': hexagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': hexagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '18pt'},
            }
        elif variant == 2:
            shape_variants = {
                1: {'args': hexagonv2_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 3:
            shape_variants = {
                1: {'args': hexagonv3_shape1, 'rotation_angle': 0,
                    'baseline': '18pt'},
            }
        doubled1 = []
        doubled2 = []
        doubled3 = []
        for lbl in labels:
            if not doubled1:
                doubled1.append(lbl[1])
                doubled1.append(lbl[1])
            elif not doubled2:
                doubled2.append(lbl[1])
                doubled2.append(lbl[1])
            elif not doubled3:
                doubled3.append(lbl[1])
                doubled3.append(lbl[1])
        if variant == 0:
            lbls = [doubled1.pop(), doubled1.pop(),
                    doubled2.pop(), doubled2.pop(),
                    doubled3.pop(), doubled3.pop()]
            masks = [None, ' ', None, ' ', None, ' ']
            marks = [mark1, mark1, mark2, mark2, mark3, mark3]
        elif variant == 1:
            lbls = [doubled1.pop(), doubled2.pop(),
                    doubled3.pop(), doubled1.pop(),
                    doubled3.pop(), doubled2.pop()]
            masks = [None, None, None, ' ', ' ', ' ']
            marks = [mark1, mark2, mark3, mark1, mark3, mark2]
        elif variant == 2:
            lbls = [doubled1.pop(), doubled2.pop(),
                    doubled1.pop(), doubled3.pop(),
                    doubled3.pop(), doubled2.pop()]
            masks = [None, ' ', ' ', None, ' ', None]
            marks = [mark1, mark2, mark1, mark3, mark3, mark2]
        elif variant == 3:
            lbls = [doubled1.pop(), doubled2.pop(),
                    doubled3.pop(), doubled1.pop(),
                    doubled2.pop(), doubled3.pop()]
            masks = [None, None, None, ' ', ' ', ' ']
            marks = [mark1, mark2, mark3, mark1, mark2, mark3]
        return self._polygon(
            shared.hexagon_2_2_2_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_3_1_1_1(self, variant=None, labels=None, name=None,
                         label_vertices=None, thickness=None,
                         length_unit=None, shape_variant_nb=None,
                         wlines_nb=0):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be 0, 1 or 2 (not \'{}\')'
                             .format(variant))
        hexagonv0_shape1 = [Point('0.9', '1.1'), Point('1.9', '1.1'),
                            Point('2.7', '0.5'), Point('1.84', 0),
                            Point('0.39', '0.2'), Point(0, '0.9')]
        hexagonv1_shape1 = [Point(0, '0.9'), Point('0.98', '1.1'),
                            Point('1.97', 1), Point('2.38', '0.2'),
                            Point('1.4', 0), Point('0.4', '0.1')]
        hexagonv2_shape1 = [Point('0.7', '1.1'), Point('1.8', '1.1'),
                            Point('2.62', '0.6'), Point('1.7', 0),
                            Point('0.85', 0), Point(0, '0.7')]
        mark = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': hexagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': hexagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 2:
            shape_variants = {
                1: {'args': hexagonv2_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
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
                    singles.pop(), singles.pop()]
            masks = [' ', None, ' ', None, None, None]
            marks = [mark, mark, mark, None, None, None]
        elif variant == 1:
            lbls = [tripled.pop(), tripled.pop(), singles.pop(), tripled.pop(),
                    singles.pop(), singles.pop()]
            masks = [None, ' ', None, ' ', None, None]
            marks = [mark, mark, None, mark, None, None]
        elif variant == 2:
            lbls = [tripled.pop(), singles.pop(), tripled.pop(), singles.pop(),
                    tripled.pop(), singles.pop()]
            masks = [None, None, ' ', None, ' ', None]
            marks = [mark, None, mark, None, mark, None]
        return self._polygon(
            shared.hexagon_3_1_1_1_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_3_2_1(self, variant=None, labels=None, name=None,
                       label_vertices=None, thickness=None,
                       length_unit=None, shape_variant_nb=None,
                       wlines_nb=0):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be 0, 1 or 2 (not \'{}\')'
                             .format(variant))
        hexagonv0_shape1 = [Point('0.9', '1.1'), Point('1.75', '1.1'),
                            Point('2.4', '0.56'), Point('1.76', 0),
                            Point('0.76', 0), Point('0.04', '0.7')]
        hexagonv1_shape1 = [Point('0.8', 0), Point('0.01', '0.3'),
                            Point('0.61', '1.1'), Point('1.61', '1.1'),
                            Point('2.36', '0.72'), Point('1.91', 0)]
        hexagonv2_shape1 = [Point('2.6', '0.6'), Point(2, 0),
                            Point('1.15', 0), Point('0.27', '0.49'),
                            Point('0.86', '1.1'), Point('1.86', '1.1')]
        mark1 = next(shared.ls_marks_source)[0]
        mark2 = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': hexagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': hexagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '10pt'},
            }
        elif variant == 2:
            shape_variants = {
                1: {'args': hexagonv2_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        singles = []
        doubled = []
        tripled = []
        for lbl in labels:
            if lbl[0] == 1:
                singles.append(lbl[1])
            elif lbl[0] == 2:
                doubled.append(lbl[1])
                doubled.append(lbl[1])
            else:
                tripled.append(lbl[1])
                tripled.append(lbl[1])
                tripled.append(lbl[1])
        if variant == 0:
            lbls = [tripled.pop(), tripled.pop(), tripled.pop(), doubled.pop(),
                    doubled.pop(), singles.pop()]
            masks = [' ', None, ' ', ' ', None, None]
            marks = [mark1, mark1, mark1, mark2, mark2, None]
        elif variant == 1:
            lbls = [tripled.pop(), doubled.pop(), doubled.pop(), tripled.pop(),
                    tripled.pop(), singles.pop()]
            masks = [' ', None, ' ', ' ', None, None]
            marks = [mark1, mark2, mark2, mark1, mark1, None]
        elif variant == 2:
            lbls = [tripled.pop(), tripled.pop(), doubled.pop(), tripled.pop(),
                    doubled.pop(), singles.pop()]
            masks = [None, ' ', None, ' ', ' ', None]
            marks = [mark1, mark1, mark2, mark1, mark2, None]
        return self._polygon(
            shared.hexagon_3_2_1_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_3_3(self, variant=None, labels=None, name=None,
                     label_vertices=None, thickness=None,
                     length_unit=None, shape_variant_nb=None,
                     wlines_nb=0):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be 0, 1 or 2 (not \'{}\')'
                             .format(variant))
        hexagonv0_shape1 = [Point(0, '0.57'), Point('0.72', '1.02'),
                            Point('1.57', '1.02'), Point('2.29', '0.57'),
                            Point('1.59', 0), Point('0.69', 0)]
        hexagonv1_shape1 = [Point(0, '0.49'), Point('0.66', '1.02'),
                            Point('1.51', '1.02'), Point('2.29', '0.57'),
                            Point('1.65', 0), Point('0.75', 0)]
        hexagonv2_shape1 = [Point(0, '0.4'), Point('0.55', '1.04'),
                            Point('1.45', '1.04'), Point('2.23', '0.7'),
                            Point('1.66', 0), Point('0.81', 0)]
        mark1 = next(shared.ls_marks_source)[0]
        mark2 = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': hexagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '12pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': hexagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '15pt'},
            }
        elif variant == 2:
            shape_variants = {
                1: {'args': hexagonv2_shape1, 'rotation_angle': 0,
                    'baseline': '17pt'},
            }
        tripled1 = []
        tripled2 = []
        for lbl in labels:
            if not tripled1:
                tripled1.append(lbl[1])
                tripled1.append(lbl[1])
                tripled1.append(lbl[1])
            elif not tripled2:
                tripled2.append(lbl[1])
                tripled2.append(lbl[1])
                tripled2.append(lbl[1])
        if variant == 0:
            lbls = [tripled1.pop(), tripled1.pop(), tripled1.pop(),
                    tripled2.pop(), tripled2.pop(), tripled2.pop()]
            masks = [None, ' ', ' ', None, ' ', ' ']
            marks = [mark1, mark1, mark1, mark2, mark2, mark2]
        elif variant == 1:
            lbls = [tripled1.pop(), tripled1.pop(), tripled2.pop(),
                    tripled1.pop(), tripled2.pop(), tripled2.pop()]
            masks = [None, ' ', None, ' ', ' ', ' ']
            marks = [mark1, mark1, mark2, mark1, mark2, mark2]
        elif variant == 2:
            lbls = [tripled1.pop(), tripled2.pop(), tripled1.pop(),
                    tripled2.pop(), tripled1.pop(), tripled2.pop()]
            masks = [None, None, ' ', ' ', ' ', ' ']
            marks = [mark1, mark2, mark1, mark2, mark1, mark2]
        return self._polygon(
            shared.hexagon_3_3_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_4_1_1(self, variant=None, labels=None, name=None,
                       label_vertices=None, thickness=None,
                       length_unit=None, shape_variant_nb=None,
                       wlines_nb=0):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be 0, 1 or 2 (not \'{}\')'
                             .format(variant))
        hexagonv0_shape1 = [Point(1, '1.1'), Point('1.84', '0.99'),
                            Point('1.84', '0.14'), Point(1, 0),
                            Point('0.15', '0.07'), Point('-0.2', '0.9')]
        hexagonv1_shape1 = [Point(1, 0), Point('0.16', '0.15'),
                            Point('-0.2', '0.92'), Point('0.63', '1.1'),
                            Point('2.3', 1), Point('2.01', '0.2')]
        hexagonv2_shape1 = [Point(1, 0), Point('0.16', '0.1'),
                            Point('0.11', '0.95'), Point('1.1', '1.1'),
                            Point('1.94', '0.96'), Point('2.24', '0.17')]
        mark = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': hexagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '17pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': hexagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 2:
            shape_variants = {
                1: {'args': hexagonv2_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        singles = []
        quadrupled = []
        for lbl in labels:
            if lbl[0] == 1:
                singles.append(lbl[1])
            else:
                quadrupled.append(lbl[1])
                quadrupled.append(lbl[1])
                quadrupled.append(lbl[1])
                quadrupled.append(lbl[1])
        random.shuffle(singles)
        if variant == 0:
            lbls = [quadrupled.pop(), quadrupled.pop(), quadrupled.pop(),
                    quadrupled.pop(), singles.pop(), singles.pop()]
            masks = [None, ' ', ' ', ' ', None, None]
            marks = [mark, mark, mark, mark, None, None]
        elif variant == 1:
            lbls = [quadrupled.pop(), quadrupled.pop(), quadrupled.pop(),
                    singles.pop(), quadrupled.pop(), singles.pop()]
            masks = [' ', None, ' ', None, ' ', None]
            marks = [mark, mark, mark, None, mark, None]
        elif variant == 2:
            lbls = [quadrupled.pop(), quadrupled.pop(), singles.pop(),
                    quadrupled.pop(), quadrupled.pop(), singles.pop()]
            masks = [' ', ' ', None, ' ', None, None]
            marks = [mark, mark, None, mark, mark, None]
        return self._polygon(
            shared.hexagon_4_1_1_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_4_2(self, variant=None, labels=None, name=None,
                     label_vertices=None, thickness=None,
                     length_unit=None, shape_variant_nb=None,
                     wlines_nb=0):
        if variant not in [0, 1, 2]:
            raise ValueError('variant must be 0, 1 or 2 (not \'{}\')'
                             .format(variant))
        hexagonv0_shape1 = [Point('1.2', 0), Point('0.36', '0.09'),
                            Point('0.01', '0.87'), Point('0.83', '1.1'),
                            Point('1.67', '0.97'), Point('2.19', '0.12')]
        hexagonv1_shape1 = [Point(0, '0.85'), Point('0.81', '1.1'),
                            Point('1.66', '1.02'), Point('2.32', '0.48'),
                            Point('1.44', 0), Point('0.59', '0.04')]
        hexagonv2_shape1 = [Point(0, '0.46'), Point('0.61', '1.06'),
                            Point('1.46', '1.06'), Point('2.35', '0.6'),
                            Point('1.74', 0), Point('0.89', 0)]
        mark1 = next(shared.ls_marks_source)[0]
        mark2 = next(shared.ls_marks_source)[0]
        if variant == 0:
            shape_variants = {
                1: {'args': hexagonv0_shape1, 'rotation_angle': 0,
                    'baseline': '11.5pt'},
            }
        elif variant == 1:
            shape_variants = {
                1: {'args': hexagonv1_shape1, 'rotation_angle': 0,
                    'baseline': '13pt'},
            }
        elif variant == 2:
            shape_variants = {
                1: {'args': hexagonv2_shape1, 'rotation_angle': 0,
                    'baseline': '17pt'},
            }
        doubled = []
        quadrupled = []
        for lbl in labels:
            if lbl[0] == 2:
                doubled.append(lbl[1])
                doubled.append(lbl[1])
            else:
                quadrupled.append(lbl[1])
                quadrupled.append(lbl[1])
                quadrupled.append(lbl[1])
                quadrupled.append(lbl[1])
        if variant == 0:
            lbls = [quadrupled.pop(), quadrupled.pop(), quadrupled.pop(),
                    quadrupled.pop(), doubled.pop(), doubled.pop()]
            masks = [' ', None, ' ', ' ', None, ' ']
            marks = [mark1, mark1, mark1, mark1, mark2, mark2]
        elif variant == 1:
            lbls = [quadrupled.pop(), quadrupled.pop(), quadrupled.pop(),
                    doubled.pop(), quadrupled.pop(), doubled.pop()]
            masks = [None, ' ', ' ', None, ' ', ' ']
            marks = [mark1, mark1, mark1, mark2, mark1, mark2]
        elif variant == 2:
            lbls = [quadrupled.pop(), quadrupled.pop(), doubled.pop(),
                    quadrupled.pop(), quadrupled.pop(), doubled.pop()]
            masks = [None, ' ', None, ' ', ' ', ' ']
            marks = [mark1, mark1, mark2, mark1, mark1, mark2]
        return self._polygon(
            shared.hexagon_4_2_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_5_1(self, variant=None, labels=None, name=None,
                     label_vertices=None, thickness=None,
                     length_unit=None, shape_variant_nb=None,
                     wlines_nb=0):
        hexagon_shape1 = [Point(0, '0.8'), Point('0.8', '1.1'),
                          Point('1.65', '1.1'), Point('2.38', '0.68'),
                          Point('1.88', 0), Point('1.03', 0)]
        mark = next(shared.ls_marks_source)[0]
        shape_variants = {
            1: {'args': hexagon_shape1, 'rotation_angle': 0,
                'baseline': '10pt'},
            2: {'args': hexagon_shape1, 'rotation_angle': 180,
                'baseline': '19.5pt'},
        }
        singles = []
        quintupled = []
        for lbl in labels:
            if lbl[0] == 1:
                singles.append(lbl[1])
            else:
                quintupled.append(lbl[1])
                quintupled.append(lbl[1])
                quintupled.append(lbl[1])
                quintupled.append(lbl[1])
                quintupled.append(lbl[1])
        lbls = [quintupled.pop(), quintupled.pop(), quintupled.pop(),
                quintupled.pop(), quintupled.pop(), singles.pop()]
        masks = [' ', ' ', ' ', None, ' ', None]
        marks = [mark, mark, mark, mark, mark, None]
        return self._polygon(
            shared.hexagon_5_1_shapes_source,
            shape_variants,
            Polygon,
            labels=lbls,
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )

    def _hexagon_6(self, variant=None, labels=None, name=None,
                   label_vertices=None, thickness=None,
                   length_unit=None, shape_variant_nb=None,
                   wlines_nb=0):
        shape_variant_nb = 2
        hexagon_shape1 = [Point('0.48', '0.55'), Point('0.8', '1.1'),
                          Point('1.43', '1.1'), Point('1.75', '0.55'),
                          Point('1.43', 0), Point('0.8', 0)]
        mark = next(shared.ls_marks_source)[0]
        shape_variants = {
            1: {'args': hexagon_shape1, 'rotation_angle': 0,
                'baseline': '16pt'},
            2: {'args': hexagon_shape1, 'rotation_angle': 15,
                'baseline': '13pt'},
        }
        masks = [None, ' ', ' ', ' ', ' ', ' ']
        marks = [mark, mark, mark, mark, mark, mark]
        return self._polygon(
            shared.hexagon_6_shapes_source,
            shape_variants,
            Polygon,
            labels=[labels[0][1] for _ in range(6)],
            name=name, label_vertices=label_vertices, thickness=thickness,
            length_unit=length_unit,
            masks=masks, marks=marks,
            shape_variant_nb=shape_variant_nb,
            wlines_nb=wlines_nb
        )
