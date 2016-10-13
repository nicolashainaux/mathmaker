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
# @package core.base_geometry
# @brief Mathematical elementary geometrical objects.

import math
from decimal import Decimal, ROUND_UP, ROUND_HALF_EVEN, ROUND_HALF_UP

from mathmaker.lib import error, is_
from mathmaker.lib.maths_lib import deg_to_rad, round
from mathmaker.lib.core.base import Drawable
from mathmaker.lib.core.base_calculus import Value
from mathmaker.lib.common.latex import MARKUP


# the mark 'dashed' has been removed from the available list since it may
# produce buggy results sometimes from euktopst
AVAILABLE_ANGLE_MARKS = ['', 'simple', 'double', 'triple', 'right',
                         'forth', 'back', 'dotted']
AVAILABLE_SEGMENT_MARKS = ['', 'simple', 'double', 'triple', 'cross']


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Point
# @brief
class Point(Drawable):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param arg: [String, (nb,nb)]|Point
    #   Types details:
    #   -
    #   @param options
    #   Options details:
    #   -
    #   @warning Might raise...
    def __init__(self, arg, **options):
        if not (type(arg) == list or isinstance(arg, Point)):
            raise error.WrongArgument(' list|Point ', str(type(arg)))

        elif type(arg) == list:
            if not len(arg) == 2:
                raise error.WrongArgument(' a list of length '
                                          + str(len(arg)),
                                          ' a list of length 2 ')

            if not type(arg[0]) == str:
                raise error.WrongArgument(str(type(arg[0])), ' a str ')

            if not (type(arg[1]) == tuple
                    and len(arg[1]) == 2
                    and is_.a_number(arg[1][0])
                    and is_.a_number(arg[1][1])):
                # __
                raise error.WrongArgument(str(arg), ' (x, y) ')

            self._name = arg[0]
            self._x = Decimal(arg[1][0])
            self._y = Decimal(arg[1][1])

        else:
            self._name = arg.name
            self._x = arg.x
            self._y = arg.y

        self._x_exact = self._x
        self._y_exact = self._y

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the abscissa of the Point, rounded up to the tenth
    @property
    def x(self):
        return round(Decimal(str(self._x)),
                     Decimal('0.01'),
                     rounding=ROUND_HALF_UP)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the exact abscissa of the Point
    @property
    def x_exact(self):
        return self._x

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the ordinate of the Point, rounded up to the tenth
    @property
    def y(self):
        return round(Decimal(str(self._y)),
                     Decimal('0.01'),
                     rounding=ROUND_HALF_UP)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the exact ordinate of the Point
    @property
    def y_exact(self):
        return self._y

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the abscissa of the Point
    @x.setter
    def x(self, arg):
        if not is_.a_number(arg):
            raise error.WrongArgument(' a number ', str(arg))

        self._x = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the ordinate of the Point
    @y.setter
    def y(self, arg):
        if not is_.a_number(arg):
            raise error.WrongArgument(' a number ', str(arg))

        self._y = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the name of the object
    @property
    def name(self):
        return self._name

    # --------------------------------------------------------------------------
    ##
    #   @brief Allows to rename Points (other Drawables are not allowed to).
    @name.setter
    def name(self, arg):
        if not (type(arg) == str):
            raise TypeError("Expected a string")
        if not (len(arg) == 1):
            raise ValueError("Expected a string of one char only")
        self._name = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns a new Point after rotation of self
    def rotate(self, center, angle, **options):
        if not isinstance(center, Point):
            raise error.WrongArgument(' a Point ', str(type(center)))

        if not is_.a_number(angle):
            raise error.WrongArgument(' a number ', str(type(angle)))

        delta_x = self.x_exact - center.x_exact
        delta_y = self.y_exact - center.y_exact

        rx = delta_x * Decimal(str(math.cos(deg_to_rad(angle)))) \
            - delta_y * Decimal(str(math.sin(deg_to_rad(angle)))) \
            + center.x_exact
        ry = delta_x * Decimal(str(math.sin(deg_to_rad(angle)))) \
            + delta_y * Decimal(str(math.cos(deg_to_rad(angle)))) \
            + center.y_exact

        new_name = self.name + "'"

        if 'keep_name' in options and options['keep_name']:
            new_name = self.name

        elif 'new_name' in options and type(options['new_name']) == str:
            new_name = options['new_name']

        return Point([new_name, (rx, ry)])


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Segment
# @brief
class Segment(Drawable):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param arg (Point, Point)
    #   Types details:
    #   -
    #   @param options
    #   Options details:
    #   -
    #   @warning Might raise...
    def __init__(self, arg, **options):
        self._label = Value("")
        if not (type(arg) == tuple or isinstance(arg, Segment)):
            raise error.WrongArgument(' tuple|Segment ', str(type(arg)))
        elif type(arg) == tuple:
            if not (isinstance(arg[0], Point) and isinstance(arg[1], Point)):
                # __
                raise error.WrongArgument(' (Point, Point) ', str(arg))

            self._points = (arg[0].clone(), arg[1].clone())

            if 'label' in options and type(options['label']) == str:
                self._label = options['label']
        else:
            self._points = (arg.points[0].clone(),
                            arg.points[1].clone())
            self._label = arg.label
        self._mark = ""
        self._name = "[" + self.points[0].name + self.points[1].name + "]"
        self._length = Value(0)
        self._length_has_been_set = False
        self._length_name = self._points[0].name + self._points[1].name

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the two points
    @property
    def points(self):
        return self._points

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the label of the Segment
    @property
    def label(self):
        return self._label

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the length of the Segment
    @property
    def real_length(self):
        x_delta = self.points[0].x - self.points[1].x
        y_delta = self.points[0].y - self.points[1].y
        return math.hypot(x_delta, y_delta)

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the "fake" length of the Segment (the one used in a
    #          problem)
    @property
    def length(self):
        return self._length

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the length_has_been_set flag of the Segment
    @property
    def length_has_been_set(self):
        return self._length_has_been_set

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the length name of the Segment
    @property
    def length_name(self):
        return self._length_name

    def invert_length_name(self):
        """Swap points' names in the length name. E.g. AB becomes BA."""
        self._length_name = self._length_name[::-1]

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the mark of the Segment
    @property
    def mark(self):
        return self._mark

    # --------------------------------------------------------------------------
    ##
    #   @brief Will set length as the Segment's label, or "?", or nothing
    #   @param flag If flag evaluates to "?"|None, the Segment's label will be
    #               set to "?". Otherwise, if it evaluates to False, it will be
    #               set to '', and to True, it will be set to its length.
    def setup_label(self, flag):
        if flag is None or flag == '?':
            self.label = Value('?')
        elif flag in ['hid', 'hidden', 'known_but_hidden']:
            self.label = Value('hidden')
        elif flag:
            self.label = Value(self.length)
        elif not flag:
            self.label = Value('')

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the label of the Segment
    @label.setter
    def label(self, arg):
        if not type(arg) == Value:
            raise error.WrongArgument(' Value ', str(type(arg)))

        self._label = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the fake length of the Segment (the one used in a problem)
    @length.setter
    def length(self, arg):
        if not isinstance(arg, Value):
            raise TypeError('Expected a Value, got ' + str(type(arg)) + " "
                            'instead.')
        if not arg.is_numeric():
            raise error.WrongArgument('numeric Value',
                                      'a Value but not numeric, it contains '
                                      + str(arg.raw_value))
        self._length = arg
        self._length_has_been_set = True

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the mark of the Segment
    @mark.setter
    def mark(self, arg):
        if not type(arg) == str:
            raise error.WrongArgument(' str ', str(type(arg)))

        if arg not in AVAILABLE_SEGMENT_MARKS:
            raise error.WrongArgument(arg, 'a string from this list: '
                                      + str(AVAILABLE_SEGMENT_MARKS))

        self._mark = arg

    def label_into_euk(self):
        """Return the label correctly positionned along the Segment."""
        if self.label in [Value(''), Value('hidden')]:
            return ''
        else:
            result = ''
            x = self.real_length
            scale_factor = round(Decimal(str(1.6 * x)),
                                 Decimal('0.1'),
                                 rounding=ROUND_UP)
            if x <= 3:
                angle_correction = round(Decimal(str(-8 * x + 33)),
                                         Decimal('0.1'),
                                         rounding=ROUND_UP)
            else:
                angle_correction = \
                    round(
                        Decimal(
                            str(1.1 / (1 - 0.95 * math.exp(-0.027 * x)))),
                        Decimal('0.1'),
                        rounding=ROUND_UP)

            side_angle = Vector((self.points[0], self.points[1])).slope

            label_position_angle = round(side_angle,
                                         Decimal('1'),
                                         rounding=ROUND_HALF_EVEN)

            label_position_angle %= Decimal("360")

            rotate_box_angle = Decimal(label_position_angle)

            if (rotate_box_angle >= 90 and rotate_box_angle <= 270):
                rotate_box_angle -= Decimal("180")
            elif (rotate_box_angle <= -90 and rotate_box_angle >= -270):
                rotate_box_angle += Decimal("180")

            rotate_box_angle %= Decimal("360")

            result += "  $\\rotatebox{"
            result += str(rotate_box_angle)
            result += "}{\sffamily "
            result += self.label.into_str(display_unit=True,
                                          graphic_display=True)
            result += "}$ "
            result += self.points[0].name + " "
            result += str(label_position_angle)
            result += " - "
            result += str(angle_correction) + " deg "
            result += str(scale_factor)
            result += "\n"
            return result


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Vector
# @brief
class Vector(Point):

    # --------------------------------------------------------------------------
    ##
    #   @brief Vector's constructor.
    #   @param arg (Point, Point) | Point | (x, y)
    def __init__(self, arg, **options):
        self._x_exact = Decimal('1')
        self._y_exact = Decimal('1')
        if isinstance(arg, Point):
            Point.__init__(self,
                           Point(["", (arg.x_exact, arg.y_exact)]),
                           **options)

        elif isinstance(arg, tuple) and len(arg) == 2:
            if all([isinstance(elt, Point) for elt in arg]):
                Point.__init__(self,
                               Point(["", (arg[1].x_exact - arg[0].x_exact,
                                           arg[1].y_exact - arg[0].y_exact)]))
            elif all([is_.a_number(elt) for elt in arg]):
                Point.__init__(self, Point(["", (arg[0], arg[1])]))
            else:
                raise error.WrongArgument("a tuple not only of Points or"
                                          " numbers",
                                          "(Point,Point)|(x,y)")
        else:
            raise error.WrongArgument(str(type(arg)), "Point|(,)")

    # --------------------------------------------------------------------------
    ##
    #   @brief Adds two vectors
    #   @param arg Vector
    def __add__(self, arg):
        if not isinstance(arg, Vector):
            raise error.WrongArgument(str(type(arg)), "a Vector")

        return Vector((self.x_exact + arg.x_exact,
                       self.y_exact + arg.y_exact))

    @property
    def norm(self):
        """Return the norm of self."""
        return Decimal(str(math.hypot(self._x_exact, self._y_exact)))

    @property
    def slope(self):
        """Return the slope of self."""
        theta = round(Decimal(str(math.degrees(
                                  math.acos(self._x_exact / self.norm)))),
                      Decimal('0.1'),
                      rounding=ROUND_HALF_UP)
        return theta if self._y_exact > 0 else Decimal("360") - theta

    def unit_vector(self):
        """Return the unit vector built from self"""
        return Vector((self._x_exact / self.norm,
                       self._y_exact / self.norm))

    def bisector_vector(self, arg):
        """
        Return a vector colinear to the bisector of self and another vector.

        :param arg: the other vector
        :type arg: Vector
        """
        if not isinstance(arg, Vector):
            raise error.WrongArgument(str(type(arg)), "a Vector")
        return self.unit_vector() + arg.unit_vector()

    def orthogonal_unit_vector(self, clockwise=True):
        """
        Return a unit vector that's (default clockwise) orthogonal to self.

        If clockwise is set to False, then the anti-clockwise orthogonal
        vector is returned.
        """
        u = self.unit_vector()
        if clockwise:
            return Vector((u._y_exact, -u._x_exact))
        else:
            return Vector((-u._y_exact, u._x_exact))


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Ray
# @brief
class Ray(Drawable):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param arg: (Point, Point)
    #   @param options: label
    #   Options details:
    #   @warning Might raise...
    def __init__(self, arg, **options):
        self._point0 = None  # the initial point
        self._point1 = None
        self._name = None

        if (isinstance(arg, tuple) and len(arg) == 2
            and isinstance(arg[0], Point)
            and isinstance(arg[1], Point)):
            # __
            self._point0 = arg[0].clone()
            self._point1 = arg[1].clone()
            self._name = MARKUP['opening_square_bracket']
            self._name += arg[0].name + arg[1].name
            self._name += MARKUP['closing_bracket']


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Angle
# @brief
class Angle(Drawable):

    # --------------------------------------------------------------------------
    ##
    #   @brief Constructor.
    #   @param arg: (Point, Point, Point)
    #   @param options: label
    #   Options details:
    #   @warning Might raise...
    def __init__(self, arg, **options):
        self._ray0 = None
        self._ray1 = None
        self._points = None
        self._measure = None
        self._mark = ""
        self._label = Value("")
        self._name = None

        if (isinstance(arg, tuple) and len(arg) == 3
            and isinstance(arg[0], Point)
            and isinstance(arg[1], Point)
            and isinstance(arg[2], Point)):
            # __
            self._ray0 = Ray((arg[1], arg[0]))
            self._ray1 = Ray((arg[1], arg[2]))
            self._points = [arg[0].clone(),
                            arg[1].clone(),
                            arg[2].clone()]

            # Let's determine the measure of the angle:
            aux_side0 = Segment((self._points[0], self._points[1]))
            aux_side1 = Segment((self._points[1], self._points[2]))
            aux_side2 = Segment((self._points[2], self._points[0]))
            aux_num = aux_side0.real_length * aux_side0.real_length \
                + aux_side1.real_length * aux_side1.real_length \
                - aux_side2.real_length * aux_side2.real_length
            aux_denom = 2 * aux_side0.real_length * aux_side1.real_length
            aux_cos = aux_num / aux_denom
            self._measure = Decimal(str(math.degrees(math.acos(aux_cos))))

            if 'label' in options and type(options['label']) == str:
                self._label = Value(options['label'])

            if 'mark' in options and type(options['mark']) == str:
                self._mark = options['mark']

            self._name = MARKUP['opening_widehat']
            self._name += arg[0].name + arg[1].name + arg[2].name
            self._name += MARKUP['closing_widehat']
        else:
            raise error.WrongArgument(' (Point, Point, Point) ',
                                      str(type(arg)))

        self._label_display_angle = round(Decimal(str(self._measure)),
                                          Decimal('0.1'),
                                          rounding=ROUND_HALF_UP) / 2

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the measure of the angle
    @property
    def measure(self):
        return self._measure

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the points of the angle
    @property
    def points(self):
        return self._points

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the label of the angle
    @property
    def label(self):
        return self._label

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the angle (for display) of label's angle
    @property
    def label_display_angle(self):
        return self._label_display_angle

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the mark of the angle
    @property
    def mark(self):
        return self._mark

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the vertex of the angle
    @property
    def vertex(self):
        return self._points[1]

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the label of the angle
    @label.setter
    def label(self, arg):
        if type(arg) == str or isinstance(arg, Value):
            self._label = Value(arg)

        else:
            raise error.WrongArgument(arg, 'str or Value')

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the angle (for display) of label's angle
    @label_display_angle.setter
    def label_display_angle(self, arg):
        if not is_.a_number(arg):
            raise error.WrongArgument(arg, ' a number ')
        else:
            self._label_display_angle = round(Decimal(str(arg)),
                                              Decimal('0.1'),
                                              rounding=ROUND_HALF_UP)

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the mark of the angle
    @mark.setter
    def mark(self, arg):
        if type(arg) == str:
            if arg in AVAILABLE_ANGLE_MARKS:
                self._mark = arg
            else:
                raise error.WrongArgument(arg, 'a string from this list: '
                                               + str(AVAILABLE_ANGLE_MARKS))

        else:
            raise error.WrongArgument(arg, 'str')
