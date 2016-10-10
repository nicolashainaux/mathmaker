# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @package core.geometry
# @brief Mathematical geometrical objects.

import math
import copy
from decimal import Decimal, ROUND_HALF_UP

from mathmaker.lib import randomly
from mathmaker.lib import is_, error
from mathmaker.lib.maths_lib import (deg_to_rad, barycenter,
                                     POLYGONS_NATURES, round)
from .root_calculus import Evaluable, Value, Unit
from .base_calculus import Item, Product, Sum
from .calculus import Equality, SubstitutableEquality, Table, Table_UP
from .base import Drawable
from .base_geometry import Point, Segment, Angle, Vector


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Polygon
# @brief
class Polygon(Drawable):
    # --------------------------------------------------------------------------
    ##
    #   @brief Polygon's constructor.
    #   @param arg: Polygon |
    #                [Point, Point...] |
    #                [str, str...] <-- not implemented yet
    #            NB: the str will be the vertices' names
    #   @param options
    #   Options details:
    #   - rotate_around_gravity_center = 'no'|'any'|nb
    #                        (nb being the angle,
    #               defaulting to 'any' if sketch or 'no' if not a sketch)
    def __init__(self, arg, **options):
        self._vertex = []
        self._side = []
        self._angle = []
        self._rotation_angle = 0
        self._read_name_clockwise = False

        if 'read_name_clockwise' in options and options['read_name_clockwise']:
            self._read_name_clockwise = True

        if 'rotate_around_isobarycenter' in options:
            if options['rotate_around_isobarycenter'] == 'randomly':
                self._rotation_angle = randomly.integer(0, 35) * 10
            elif is_.a_number(options['rotate_around_isobarycenter']):
                self._rotation_angle = options['rotate_around_isobarycenter']

        if isinstance(arg, Polygon):
            self._vertex = [v.clone() for v in arg.vertex]
            self._side = [s.clone() for s in arg.side]
            self._angle = [a.clone() for a in arg.angle]
            self._rotation_angle = arg.rotation_angle

        elif type(arg) == list:
            if len(arg) <= 2:
                raise error.WrongArgument("A list of length " + str(len(arg)),
                                          "a list of length >= 3")
            if all([type(elt) == str for elt in arg]):
                raise NotImplementedError(
                    'Using a list of str is not implemented yet')
            elif all([isinstance(elt, Point) for elt in arg]):
                start_vertices = [p.clone() for p in arg]

                if self._rotation_angle != 0:
                    G = barycenter(start_vertices, "G")

                    self._vertex = [
                        Point(v.rotate(
                            G, self._rotation_angle, keep_name=True))
                        for v in start_vertices]
                else:
                    self._vertex = [v.clone() for v in start_vertices]

                self._side = []
                self._angle = []
                shifted_vertices = copy.deepcopy(self._vertex)
                shifted_vertices += [shifted_vertices.pop(0)]
                for (p0, p1) in zip(self._vertex, shifted_vertices):
                    self._side += [Segment((p0, p1))]
                left_shifted_vertices = copy.deepcopy(self._vertex)
                left_shifted_vertices = \
                    [left_shifted_vertices.pop(-1)] + left_shifted_vertices
                for (p0, p1, p2) in zip(left_shifted_vertices,
                                        self._vertex,
                                        shifted_vertices):
                    self._angle += [Angle((p0, p1, p2))]
            else:
                raise error.WrongArgument("A list of Points or str "
                                          + str(len(arg)),
                                          "a list containing something else")

        else:
            raise error.WrongArgument(str(type(arg)),
                                      "Polygon|[Point]|[str]")

        self._name = ''.join([v.name for v in self._vertex])

        if len(self._side) in POLYGONS_NATURES:
            self._nature = POLYGONS_NATURES[len(self._side)]
        else:
            self._nature = \
                "Polygon_of_{n}_sides".format(n=str(len(self._side)))

        self._random_id = \
            ''.join([str(randomly.integer(0, 9)) for i in range(8)])

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the vertices (as a list of Points)
    @property
    def vertex(self):
        return self._vertex

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the sides (as a list of Segments)
    @property
    def side(self):
        return self._side

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the three angles (as a list of Angles)
    @property
    def angle(self):
        return self._angle

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the angle of rotation around the isobarycenter
    @property
    def rotation_angle(self):
        return self._rotation_angle

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Polygon's name
    @property
    def name(self):
        if self._read_name_clockwise:
            return self._name[::-1]
        else:
            return self._name

    # --------------------------------------------------------------------------
    ##
    #   @brief Rename the Polygon
    def rename(self, n):
        if not type(n) == str:
            raise TypeError("The 'n' argument should be a string")
        if not len(n) == len(self.vertex):
            raise ValueError("The given name should have the same length as "
                             "the number of vertices of the Polygon ("
                             + str(len(self.vertex)) + "). "
                             "Instead it has a length of " + str(len(n)))

        if not self._read_name_clockwise:
            n = n[::-1]
        for i, v in enumerate(self._vertex):
            v.name = n[i]
        self._name = ''.join([v.name for v in self._vertex])

        shifted_vertices = copy.deepcopy(self._vertex)
        shifted_vertices += [shifted_vertices.pop(0)]
        for i, (p0, p1) in enumerate(zip(self._vertex, shifted_vertices)):
            self._side[i].points[0].name = p0.name
            self._side[i].points[1].name = p1.name

        left_shifted_vertices = copy.deepcopy(self._vertex)
        left_shifted_vertices = \
            [left_shifted_vertices.pop(-1)] + left_shifted_vertices
        for i, (p0, p1, p2) in enumerate(zip(left_shifted_vertices,
                                             self._vertex,
                                             shifted_vertices)):
            self._angle[i].points[0].name = p0.name
            self._angle[i].points[1].name = p1.name
            self._angle[i].points[2].name = p2.name

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Polygon's nature
    @property
    def nature(self):
        return self._nature

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Polygon's filename
    @property
    def filename(self):
        return _(self.nature) + "_" + self.name + "-" + self._random_id

    # --------------------------------------------------------------------------
    ##
    #   @brief  Returns the Polygon's perimeter (based on the fake lengths)
    #   @todo   This assumes the fake lengths all have the same Unit...
    @property
    def perimeter(self):
        if not self.lengths_have_been_set:
            raise error.ImpossibleAction("calculate the perimeter while "
                                         + "ignoring the lengths of several "
                                         + "sides (fake lengths have not been"
                                         + " set yet).")
        else:
            return Value(sum([s.length.raw_value for s in self.side]),
                         unit=self.side[0].length.unit)

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the lengths that will be used in an exercise
    #          (not the real ones)
    #   @param lengths_list A list of Values, being as long as len(self.side)
    def set_lengths(self, lengths_list):
        if len(lengths_list) != len(self.side):
            raise error.WrongArgument("A list of length "
                                      + str(len(lengths_list)),
                                      "A list of length the number of sides ("
                                      + str(len(self.side)) + ")")

        for s in self.side:
            s.length = lengths_list[self.side.index(s)]

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns True if all fake lengths of the sides have been set.
    @property
    def lengths_have_been_set(self):
        return all(s.length_has_been_set for s in self.side)

    def setup_labels(self, flags_list, segments_list=None):
        """
        Tells what to display along each segment of the list.

        If no segments' list is provided, it defaults to the Polygon's sides'
        list. It is expected that both the flags' and segments' lists have the
        same length.
        Meaning of the flags' list:
        - a '?' will be displayed for each Segment flagged as None or '?'
        - its length will be displayed if it's flagged as anything else
          evaluating to True
        - nothing will be displayed it it's flagged as anything else evaluating
          to False

        :param flags_list: the list of the flags
        :type flags_list: list
        :param segments_list: the list of the Segments to flag
        :type segments_list: list (of Segments)
        """
        if segments_list is None:
            segments_list = self.side
        if len(flags_list) != len(segments_list):
            raise ValueError("The number of flags ({}) should be equal "
                             "to the number of segments ({})."
                             .format(str(len(flags_list)),
                                     str(len(segments_list))))

        for (s, f) in zip(segments_list, flags_list):
            s.setup_label(f)

    # --------------------------------------------------------------------------
    ##
    #   @brief Works out the dimensions of the box
    #   @param options Any options
    #   @return (x1, y1, x2, y2)
    def work_out_euk_box(self, vertices=None):
        if vertices is None:
            vertices = self.vertex
        x_list = [v.x for v in vertices]
        y_list = [v.y for v in vertices]

        return (min(x_list) - Decimal("0.6"), min(y_list) - Decimal("0.6"),
                max(x_list) + Decimal("0.6"), max(y_list) + Decimal("0.6"))

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates the euk string to put in the file
    #   @param options Any options
    #   @return The string to put in the picture file
    def into_euk(self, **options):
        box_values = self.work_out_euk_box()
        result = "box {val0}, {val1}, {val2}, {val3}\n"\
                 .format(val0=str(box_values[0]),
                         val1=str(box_values[1]),
                         val2=str(box_values[2]),
                         val3=str(box_values[3]))

        result += "\n"

        for v in self.vertex:
            result += "{name} = point({x}, {y})\n".format(name=v.name,
                                                          x=v.x,
                                                          y=v.y)

        result += "\ndraw\n  "

        result += "("
        result += '.'.join([v.name for v in self.vertex])
        result += ")\n"

        # Let's add the sides' labels, if any
        for s in self.side:
            result += s.label_into_euk()

        for a in self.angle:
            if a.label != Value(""):
                scale_factor = Decimal('2.7')
                if Decimal(str(a.measure)) < Decimal('28.5'):
                    scale_factor = round(
                        Decimal('38.1') * pow(Decimal(str(a.measure)),
                                              Decimal('-0.8')),
                        Decimal('0.01'),
                        rounding=ROUND_HALF_UP)

                label_display_angle = \
                    Vector((a.points[1], a.points[0]))\
                    .bisector_vector(Vector((a.points[1], a.points[2])))\
                    .slope

                label_position_angle = label_display_angle

                rotate_box_angle = Decimal(label_position_angle)

                if (rotate_box_angle >= 90 and rotate_box_angle <= 270):
                    rotate_box_angle -= Decimal("180")
                elif (rotate_box_angle <= -90 and rotate_box_angle >= -270):
                    rotate_box_angle += Decimal("180")

                result += "  $\\rotatebox{"
                result += str(rotate_box_angle)
                result += "}{\sffamily "
                result += a.label.into_str(display_unit=True,
                                           graphic_display=True)
                result += "}$ "
                result += a.vertex.name + " "
                result += str(label_position_angle) + " deg "
                result += str(scale_factor)
                result += "\n"

        names_angles_list = [Vector((a.points[0], a.points[1]))
                             .bisector_vector(Vector((a.points[2],
                                                      a.points[1])))
                             .slope for a in self.angle]

        for (i, v) in enumerate(self.vertex):
            result += '  "{n}" {n} {a} deg, font("sffamily")\n'\
                      .format(n=v.name, a=str(names_angles_list[i]))

        result += "end\n"

        # To avoid empty label...end sections (what make euktoeps raise a
        # syntax error), we first check whether there's anything to put in it.
        all_marks = "".join([a.mark + s.mark
                             for a, s in zip(self.angle, self.side)])
        if all_marks != "":
            result += "\nlabel\n"
            for a in self.angle:
                if a.mark != "":
                    result += "  {p0}, {v}, {p2} {m}\n"\
                              .format(p0=a.points[2].name,
                                      v=a.vertex.name,
                                      p2=a.points[0].name,
                                      m=a.mark)
            for s in self.side:
                if s.mark != "":
                    result += "  {p1}.{p2} {m}\n"\
                              .format(p1=s.points[0].name,
                                      p2=s.points[1].name,
                                      m=s.mark)
            result += "end"

        return result


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Rectangle
# @brief
class Rectangle(Polygon):
    # --------------------------------------------------------------------------
    ##
    #   @brief Rectangle's constructor.
    #   @param arg: Rectangle |
    #                [Point, length, height, str1, str2, str3]
    #            NB: the str will be the vertices' names
    #   @param options
    #   Options details:
    #   - rotate_around_gravity_center = 'no'|'any'|nb
    #                        (nb being the angle,
    #               defaulting to 'any' if sketch or 'no' if not a sketch)
    def __init__(self, arg, **options):
        if isinstance(arg, Rectangle):
            Polygon.__init__(self, (tuple(arg.points)))
        elif isinstance(arg, list):
            if (isinstance(arg[0], Point)
                and is_.a_number(arg[1])
                and is_.a_number(arg[2])
                and all(isinstance(arg[i], str) for i in [3, 4, 5])):
                # __
                length = arg[1]
                height = arg[2]
                Polygon.__init__(self,
                                 [arg[0],
                                  Point([arg[3],
                                         (Decimal(str(arg[0].x_exact))
                                          + Decimal(str(length)),
                                          arg[0].y_exact)]),
                                  Point([arg[4],
                                         (Decimal(str(arg[0].x_exact))
                                          + Decimal(str(length)),
                                          Decimal(str(arg[0].y_exact))
                                          + Decimal(str(height)))]),
                                  Point([arg[5],
                                         (arg[0].x_exact,
                                          Decimal(str(arg[0].y_exact))
                                          + Decimal(str(height)))])
                                  ])

            else:
                raise error.WrongArgument(
                    "One of the elements is not of the expected type",
                    "[Point, nb1, nb2, str1, str2, str3]")

        else:
            raise error.WrongArgument(
                str(type(arg)),
                "Rectangle|[Point, length, height, str1, str2, str3]")

        for a in self._angle:
            a.mark = 'right'

        self._nature = 'Rectangle'

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Rectangle's width
    @property
    def width(self):
        if not self.lengths_have_been_set:
            raise error.ImpossibleAction("Return the width of a Rectangle "
                                         + "before is has been set.")

        return self.side[1].length

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Rectangle's length
    @property
    def length(self):
        if not self.lengths_have_been_set:
            raise error.ImpossibleAction("Return the length of a Rectangle "
                                         + "before is has been set.")

        return self.side[0].length

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Rectangle's area
    #   @todo  This method assumes width and length both have the same Unit
    @property
    def area(self):
        if self.width.get_unit() != "":
            return Value(Product([Item(self.width),
                                  Item(self.length)]).evaluate(),
                         unit=Unit(self.width.get_unit().name, exponent=2))
        else:
            return Value(Product([Item(self.width),
                                  Item(self.length)]).evaluate())

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the length and width of the Rectangle
    #   @param lengths_list A list of 2 Values
    def set_lengths(self, lengths_list):
        if len(lengths_list) != 2:
            raise error.WrongArgument("A list of length "
                                      + str(len(lengths_list)),
                                      "A list of length 2.")

        super(Rectangle, self).set_lengths([lengths_list[0], lengths_list[1],
                                            lengths_list[0], lengths_list[1]])


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Square
# @brief
class Square(Polygon):
    # --------------------------------------------------------------------------
    ##
    #   @brief Rectangle's constructor.
    #   @param arg: Rectangle |
    #                [Point, length, str1, str2, str3]
    #            NB: the str will be the vertices' names
    #   @param options
    #   Options details:
    #   - rotate_around_gravity_center = 'no'|'any'|nb
    #                        (nb being the angle,
    #               defaulting to 'any' if sketch or 'no' if not a sketch)
    def __init__(self, arg, **options):
        if isinstance(arg, Square):
            Polygon.__init__((self, tuple(arg.points)))
        elif isinstance(arg, list):
            if (isinstance(arg[0], Point)
                and is_.a_number(arg[1])
                and all(isinstance(arg[i], str) for i in [2, 3, 4])):
                # __
                Rectangle.__init__(self, [arg[0], arg[1], arg[1], arg[2],
                                   arg[3], arg[4]], **options)
        else:
            raise ValueError("Expected argument is:"
                             "Square, or [Point, length, str1, str2, str3]")

        for a in self._angle:
            a.mark = 'right'

        self._nature = 'Square'

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Square's side's length
    @property
    def side_length(self):
        if not self.lengths_have_been_set:
            raise error.ImpossibleAction("Return the side's length of a "
                                         "Square before is has been set.")
        return self.side[0].length

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the Square's area
    @property
    def area(self):
        if self.side_length.get_unit() != "":
            return Value(Product([Item(self.side_length),
                                  Item(self.side_length)]).evaluate(),
                         unit=Unit(self.side_length.get_unit().name,
                                   exponent=2))
        else:
            return Value(Product([Item(self.side_length),
                                  Item(self.side_length)]).evaluate())

    # --------------------------------------------------------------------------
    ##
    #   @brief  Sets the side's length the Square. Defined to match the same
    #           method of Rectangle.
    #   @param  lengths_list A list of 1 Value
    #   @todo   Maybe log a warning instead of raising a ValueError?
    def set_lengths(self, lengths_list):
        if not type(lengths_list) == list:
            raise ValueError("Expected a list, got a "
                             + str(type(lengths_list)) + " instead.")
        if not len(lengths_list) == 1:
            raise ValueError("A list of length " + str(len(lengths_list)) + " "
                             "was given, whereas a list of length 1 "
                             "was expected.")
        Polygon.set_lengths(self, [lengths_list[0], lengths_list[0],
                                   lengths_list[0], lengths_list[0]])

    # --------------------------------------------------------------------------
    ##
    #   @brief  Sets marks on the Square's sides.
    #   @param  arg The mark to be used.
    def set_marks(self, arg):
        for s in self.side:
            s.mark = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the length of the Square's side
    #   @param  side_length:    a Value
    def set_side_length(self, side_length):
        self.set_lengths([side_length])


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Triangle
# @brief
class Triangle(Polygon):
    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param arg: Triangle |
    #                ((str, str, str), 'sketch'
    #        OR:                       {'side0':nb0, 'angle1':nb1, 'side1':nb2}
    #        OR: (not implemented yet) {'side0':nb0, 'side1':nb1, 'side2':nb2}
    #        OR: (not implemented yet) etc.
    #                )
    #            NB: the three str will be the vertices' names
    #            NB: 'sketch' will just choose (reasonnably) random values
    #   @param options
    #   Options details:
    #   - rotate_around_isobarycenter = 'no'|'any'|nb
    #                        (nb being the angle,
    #               defaulting to 'any' if sketch or 'no' if not a sketch)
    #   FOLLOWING STUFF CAN BE REPLACED BY SETTERS
    #   - label_side0, label_side1, label_side2,
    #   - mark_side0, mark_side1, mark_side2,
    #   - label_angle0, label_angle1, label_angle2,
    #   - mark_angle0, mark_angle1, mark_angle2,
    #   @warning Might raise...
    def __init__(self, arg, **options):
        if not (isinstance(arg, Triangle) or type(arg) == tuple):
            raise error.WrongArgument(' Triangle|tuple ',
                                      str(type(arg)))

        self._vertex = []
        self._side = []
        self._angle = []
        self._name = ""
        self._rotation_angle = 0

        if type(arg) == tuple:
            if not len(arg) == 2:
                raise error.WrongArgument(' tuple of length 2 ',
                                          ' tuple of length '
                                          + str(len(arg)))

            vertices_names = arg[0]
            construction_data = arg[1]

            if not type(vertices_names) == tuple:
                raise error.WrongArgument(' a tuple ', str(vertices_names))

            if (not type(vertices_names[0]) == str
                and type(vertices_names[1]) == str
                and type(vertices_names[2]) == str):
                # __
                raise error.WrongArgument(' three strings ',
                                          ' one of them at least is not '
                                          'a string')

            if not (construction_data == 'sketch'
                    or (type(construction_data) == dict
                        and 'side0' in construction_data
                        and is_.a_number(construction_data['side0'])
                        and (('side1' in construction_data
                              and is_.a_number(construction_data['side1']))
                             or
                             (('angle1' in construction_data
                               and is_.a_number(
                                   construction_data['angle1'])))))):
                # __
                raise error.WrongArgument(
                    " 'sketch' | "
                    + "{'side0':nb0, 'angle1':nb1, 'side1':nb2} | ",
                    str(construction_data))

            start_vertex = [None, None, None]

            rotate_around_isobarycenter = \
                options.get('rotate_around_isobarycenter', 'no')
            if construction_data == 'sketch':
                rotate_around_isobarycenter = 'randomly'
                side0_length = Decimal(str(randomly.integer(35, 55))) / 10
                side1_length = Decimal(str(randomly.integer(35, 55))) / 10
                angle1 = randomly.integer(20, 70)
            else:
                side0_length = construction_data['side0']
                side1_length = construction_data['side1']
                angle1 = construction_data['angle1']

            if rotate_around_isobarycenter == 'randomly':
                self._rotation_angle = randomly.integer(0, 35) * 10
            elif is_.a_number(rotate_around_isobarycenter):
                self._rotation_angle = rotate_around_isobarycenter

            start_vertex[0] = Point([vertices_names[0], (0, 0)])
            start_vertex[1] = Point([vertices_names[1], (side0_length, 0)])
            cos1 = math.cos(deg_to_rad(angle1))
            sin1 = math.sin(deg_to_rad(angle1))
            x2 = side0_length - side1_length * Decimal(str(cos1))
            y2 = side1_length * Decimal(str(sin1))
            start_vertex[2] = Point([vertices_names[2], (x2, y2)])

            Polygon.__init__(self, start_vertex, **options)

        elif isinstance(arg, Triangle):
            Polygon.__init__(self, arg, **options)

        else:
            raise error.WrongArgument(str(type(arg)),
                                      "Triangle|((str, str, str),"
                                      " {'side0': nb0, 'angle1': nb1, "
                                      "'side1': nb2})")


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class RightTriangle
# @brief
class RightTriangle(Triangle):
    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param arg: RightTriangle |
    #                ((str, str, str), 'sketch'
    #        OR:                      {'leg0': nb0, 'leg1': nb1}
    #        OR: (not implemented yet){'leg0': nb0, 'angle0': nb1}
    #                )
    #            NB: the three str will be the vertices' names
    #                 The second name will be the right corner
    #                 so, hypotenuse will be vertices_names[0] & [2]
    #            NB: 'sketch' will just choose (reasonnably) random values
    #   @param options
    #   Options details:
    #   - rotate_around_isobarycenter = 'no'|'any'|nb
    #                        (nb being the angle,
    #               defaulting to 'any' if sketch or 'no' if not a sketch)
    #   FOLLOWING ONES HAVE BEEN REPLACED BY MATCHING SETTERS
    #   - label_leg0, label_leg1, label_hypotenuse,
    #   - dont_label_right_angle, label_angle0, label_angle2
    #   @warning Might raise...
    def __init__(self, arg, **options):
        if not (isinstance(arg, RightTriangle) or type(arg) == tuple):
            raise error.WrongArgument(' RightTriangle|tuple ',
                                      str(type(arg)))

        self._vertex = [None, None, None]
        self._rotation_angle = 0
        self._side = [None, None, None]
        self._name = ""

        if type(arg) == tuple:
            if not len(arg) == 2:
                raise error.WrongArgument(' tuple of length 2 ',
                                          ' tuple of length '
                                          + str(len(arg)))
            vertices_names = arg[0]
            construction_data = arg[1]

            if not type(vertices_names) == tuple:
                raise error.WrongArgument(' a tuple ', str(vertices_names))

            if (not type(vertices_names[0]) == str
                and type(vertices_names[1]) == str
                and type(vertices_names[2]) == str):
                # __
                raise error.WrongArgument(' three strings ',
                                          ' one of them at least is '
                                          'not a string')

            rotation = 0

            if ('rotate_around_isobarycenter' in options
                and options['rotate_around_isobarycenter'] == 'randomly'):
                # __
                rotation = randomly.integer(0, 35) * 10

            elif ('rotate_around_isobarycenter' in options
                  and is_.a_number(options['rotate_around_isobarycenter'])):
                # __
                rotation = options['rotate_around_isobarycenter']

            leg0_length = 0
            leg1_length = 0

            if construction_data == 'sketch':
                leg0_length = Decimal(str(randomly.integer(35, 55))) / 10
                leg1_length = \
                    Decimal(str(randomly.integer(7, 17))) \
                    / Decimal("20") * leg0_length

            elif (type(construction_data) == dict
                  and 'leg0' in construction_data
                  and is_.a_number(construction_data['leg0'])
                  and 'leg1' in construction_data
                  and is_.a_number(construction_data['leg1'])):
                # __
                leg0_length = construction_data['leg0']
                leg1_length = construction_data['leg1']

            else:
                raise error.WrongArgument(" 'sketch' | "
                                          + "{'leg0': nb0, 'leg1': nb1}",
                                          str(construction_data))

            Triangle.__init__(self,
                              ((vertices_names[0],
                                vertices_names[1],
                                vertices_names[2]
                                ),
                               {'side0': leg0_length,
                                'angle1': 90,
                                'side1': leg1_length}),
                              rotate_around_isobarycenter=rotation)

        elif isinstance(arg, RightTriangle):
            Polygon.__init__(self, arg, **options)

        self.right_angle.mark = "right"

        self._nature = 'RightTriangle'

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns legs (as a list of two Segments)
    @property
    def leg(self):
        return [self._side[0], self._side[1]]

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns hypotenuse (as a Segment)
    @property
    def hypotenuse(self):
        return self._side[2]

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the right angle (as an Angle)
    @property
    def right_angle(self):
        return self.angle[1]

    # --------------------------------------------------------------------------
    ##
    #   @brief Creates the correct pythagorean equality hyp²=leg0²+leg1²
    #   @return an Equality but not usable to calculate (see substequality)
    def pythagorean_equality(self, **options):

        objcts = [Item(('+', self.hypotenuse.length_name, 2)),
                  Sum([Item(('+', self.leg[0].length_name, 2)),
                       Item(('+', self.leg[1].length_name, 2))])]

        return Equality(objcts, **options)

# --------------------------------------------------------------------------
    ##
    #   @brief Creates the correct (substitutable) pythagorean equality
    #   @brief Uses the labels to determine the result...
    #   @return a SubstitutableEquality
    def pythagorean_substequality(self, **options):
        # First, check the number of numeric data
        # and find the unknown side
        n_numeric_data = 0
        unknown_side = ""
        if self.leg[0].label.is_numeric():
            n_numeric_data += 1
        elif self.leg[0].label.raw_value == "":
            unknown_side = 'leg0'
        if self.leg[1].label.is_numeric():
            n_numeric_data += 1
        elif self.leg[1].label.raw_value == "":
            unknown_side = 'leg1'
        if self.hypotenuse.label.is_numeric():
            n_numeric_data += 1
        elif self.hypotenuse.label.raw_value == "":
            unknown_side = 'hypotenuse'

        if n_numeric_data != 2:
            raise error.ImpossibleAction("creation of a pythagorean equality "
                                         "when the number of known numeric "
                                         "values is different from 2.")

        # Now create the SubstitutableEquality
        # (so, also create the dictionnary)
        if unknown_side == 'leg0':
            subst_dict = {Value(self.leg[1].length_name): self.leg[1].label,
                          Value(self.hypotenuse.length_name):
                          self.hypotenuse.label}
            objcts = [Item(('+', self.leg[0].length_name, 2)),
                      Sum([Item(('+', self.hypotenuse.length_name, 2)),
                           Item(('-', self.leg[1].length_name, 2))])]

        elif unknown_side == 'leg1':
            subst_dict = {Value(self.leg[0].length_name): self.leg[0].label,
                          Value(self.hypotenuse.length_name):
                          self.hypotenuse.label}
            objcts = [Item(('+', self.leg[1].length_name, 2)),
                      Sum([Item(('+', self.hypotenuse.length_name, 2)),
                           Item(('-', self.leg[0].length_name, 2))])]

        elif unknown_side == 'hypotenuse':
            subst_dict = {Value(self.leg[0].length_name): self.leg[0].label,
                          Value(self.leg[1].length_name): self.leg[1].label}
            objcts = [Item(('+', self.hypotenuse.length_name, 2)),
                      Sum([Item(('+', self.leg[0].length_name, 2)),
                           Item(('+', self.leg[1].length_name, 2))])]

        else:
            raise error.ImpossibleAction("creation of a pythagorean equality "
                                         "because no unknown side was found")

        return SubstitutableEquality(objcts, subst_dict)


class InterceptTheoremConfiguration(Triangle):

    def __init__(self,
                 points_names=None,  # 'AMBCN'
                 butterfly=False,
                 sketch=True,
                 build_ratio=None,  # Decimal('0.75')
                 build_dimensions=None,
                 # {'side0': Decimal('5'),
                 #  'angle1': Decimal('50'),
                 #  'side1': Decimal('7')}
                 rotate_around_isobarycenter='no',
                 ):
        """
        Intercept theorem configuration initialization.

        Beware, build_ratio and build_dimensions are used to draw the figure,
        not as the "fake" ratio and lengths used in the exercise, what will
        be set by set_lengths(). build_ratio is a ratio to reduce the bigger
        triangle to form the smaller, whereas enlargement_ratio is the
        enlargement ratio *of the exercise* to enlarge the smaller triangle
        to form the bigger.

        :param points_names: a list of 5 points names.
        :type points_names: a list of str
        :param butterfly: turn to True if you want to use the "butterfly"
        configuration. Not implemented yet (0.7.1dev2).
        :type butterfly: boolean
        :param sketch: turn to False if you want to use custom values for
        sides, angles and ratio. As long as it is True, these values will be
        randomly defined (inside of a reasonable range), and
        rotate_around_isobarycenter will be turned to 'randomly'
        :type sketch: boolean
        :param build_ratio: the ratio to compute the "small" triangle inside
        :type build_ratio: numeric Value
        :param build_dimensions: dimensions of the main (biggest) triangle
        :type build_dimensions: dict providing 'side0', 'angle1', and 'side1'
        keys. Any other possibility is not implemented yet (0.7.1dev2)
        :param rotate_around_isobarycenter: tells if the main triangle should
        be rotated around its barycenter. If sketch is True, it will be
        considered as 'randomly'.
        :type rotate_around_isobarycenter: either 'no', 'randomly', or a Value
        (the number of degrees to use)
        """
        self._enlargement_ratio = None

        if points_names is None:
            points_names = 'AMBCN'
        if build_ratio is None:
            build_ratio = Decimal('0.75')
        self._ratio = build_ratio
        if build_dimensions is None:
            build_dimensions = {'side0': Decimal('5'),
                                'angle1': Decimal('50'),
                                'side1': Decimal('7')}
        r = rotate_around_isobarycenter
        if sketch:
            super().__init__(((points_names[0],
                               points_names[2],
                               points_names[3]),
                              'sketch'))
        else:
            super().__init__(((points_names[0],
                               points_names[2],
                               points_names[3]),
                              build_dimensions),
                             rotate_around_isobarycenter=r)

        x_A, x_B, x_C = (self.vertex[0].x_exact,
                         self.vertex[1].x_exact,
                         self.vertex[2].x_exact)
        y_A, y_B, y_C = (self.vertex[0].y_exact,
                         self.vertex[1].y_exact,
                         self.vertex[2].y_exact)
        k = Decimal(str(build_ratio))
        self._point = [Point([points_names[1],
                             (x_A + k * (x_B - x_A),
                              y_A + k * (y_B - y_A))]),
                       Point([points_names[4],
                              (x_A + k * (x_C - x_A),
                               y_A + k * (y_C - y_A))])]
        self._small = [Segment((self._vertex[0], self._point[0])),
                       Segment((self._point[0], self._point[1])),
                       Segment((self._point[1], self._vertex[0]))]
        self._chunk = [Segment((self._point[0], self._vertex[1])),
                       Segment((self._vertex[2], self._point[1]))]

        AB = Vector((self._vertex[1], self._vertex[0]))
        AC = Vector((self._vertex[2], self._vertex[0]))
        u = AB.orthogonal_unit_vector(clockwise=False)
        v = AC.orthogonal_unit_vector()

        self._U0U1 = [Point(['U0', (x_A + u.x_exact, y_A + u.y_exact)]),
                      Point(['U1', (x_B + u.x_exact, y_B + u.y_exact)])]
        self._V0V1 = [Point(['V1', (x_C + v.x_exact, y_C + v.y_exact)]),
                      Point(['V0', (x_A + v.x_exact, y_A + v.y_exact)])]

        self._u = Segment(tuple(self._U0U1))
        self._v = Segment(tuple(self._V0V1))

        self._ortho_u = u
        self._ortho_v = v

    def into_euk(self, **options):
        """Create the euk string to save in the file"""
        points_list_for_the_box = copy.deepcopy(self.vertex)
        if self.u.label != Value(''):
            points_list_for_the_box += self._U0U1
        if self.v.label != Value(''):
            points_list_for_the_box += self._V0V1
        box_values = self.work_out_euk_box(vertices=points_list_for_the_box)
        result = "box {val0}, {val1}, {val2}, {val3}\n"\
                 .format(val0=str(box_values[0]),
                         val1=str(box_values[1]),
                         val2=str(box_values[2]),
                         val3=str(box_values[3]))

        result += "\n"

        for l in [self.vertex, self._point, self._U0U1, self._V0V1]:
            for p in l:
                result += "{name} = point({x}, {y})\n".format(name=p.name,
                                                              x=p.x,
                                                              y=p.y)
        result += "u = vector({}, {})\n"\
            .format(self._U0U1[0].name, self._U0U1[1].name)
        result += "v = vector({}, {})\n"\
            .format(self._V0V1[0].name, self._V0V1[1].name)

        result += "\ndraw\n  "
        result += "("
        result += '.'.join([v.name for v in self.vertex])
        result += ")\n"
        result += '  ' + '.'.join([p.name for p in self._point])
        result += "\n"

        names_angles_list = [Vector((a.points[0], a.points[1]))
                             .bisector_vector(Vector((a.points[2],
                                                      a.points[1])))
                             .slope for a in self.angle]
        for (i, v) in enumerate(self.vertex):
            result += '  "{n}" {n} {a} deg, font("sffamily")\n'\
                      .format(n=v.name, a=str(names_angles_list[i]))

        names_angles_list = [self._ortho_u.slope, self._ortho_v.slope]
        for (i, p) in enumerate(self._point):
            result += '  "{n}" {n} {a} deg, font("sffamily")\n'\
                      .format(n=p.name, a=str(names_angles_list[i]))

        if self.u.label not in [Value(''), Value('hidden')]:
            result += '  u {}\n'.format(self._U0U1[0].name)
            result += '  -u {}\n'.format(self._U0U1[1].name)
        if self.v.label not in [Value(''), Value('hidden')]:
            result += '  v {}\n'.format(self._V0V1[0].name)
            result += '  -v {}\n'.format(self._V0V1[1].name)

        for s in self._small + self._chunk + [self.u, self.v, self.side[1]]:
            result += s.label_into_euk()

        result += "end"
        return result

    def set_lengths(self, lengths_list, enlargement_ratio):
        """
        Set all ("fake") lengths of the figure.

        The given lengths' list matches the three small sides. The ratio
        will be used to compute all other segments' sides. As these lengths
        are the "fake" ones (not the ones used to draw the figure, but the
        ones that will show up on the figure), this ratio is the "fake" one
        (not the same as self.ratio).

        :param lengths_list: the list of the lengths for small0, small1, small2
        :type lengths_list: a list (of Values)
        :param enlargement_ratio: the enlargement ratio of the exercise.
        :type enlargement_ratio: any Evaluable
        """
        if len(lengths_list) != 3:
            raise ValueError('This list should contain 3 lengths, not {}.'
                             .format(str(len(lengths_list))))
        if not isinstance(enlargement_ratio, Evaluable):
            raise TypeError('Expected any Evaluable, got a {}.'
                            .format(str(type(enlargement_ratio))))
        self._enlargement_ratio = enlargement_ratio
        for i, s in enumerate(self._small):
            s.length = Value(lengths_list[i])
        for i, s in enumerate(self.side):
            s.length = Value(Product([lengths_list[i], enlargement_ratio])
                             .evaluate())
        self._u.length = Value(Product([lengths_list[0],
                               enlargement_ratio]).evaluate())
        self._v.length = Value(Product([lengths_list[2],
                               enlargement_ratio]).evaluate())
        self._chunk[0].length = Value(self._u.length
                                      - self.small[0].length)
        self._chunk[1].length = Value(self._v.length
                                      - self.small[2].length)

    def ratios_equalities(self) -> Table:
        """Return a Table matching the ratios equalities."""
        return Table([[Item(v.length_name) for v in self.small],
                      [Item(v.length_name) for v in self.side]])

    def ratios_equalities_substituted(self) -> Table_UP:
        """
        Return the ratios equalities containing known numbers.

        It is returned as a Table_UP object.
        """
        masks_on = [Value(''), Value('?')]
        infos = [(Item(s.length_name) if s.label in masks_on else None,
                  Item(b.length_name) if b.label in masks_on else None)
                 for s, b in zip(self.small, self.side)]
        return Table_UP(self.enlargement_ratio,
                        [s.length for s in self.small],
                        infos)

    @property
    def chunk(self):
        return self._chunk

    @property
    def point(self):
        return self._point

    @property
    def small(self):
        return self._small

    @property
    def u(self):
        return self._u

    @property
    def v(self):
        return self._v

    @property
    def enlargement_ratio(self):
        return self._enlargement_ratio
