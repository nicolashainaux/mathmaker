# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets with their answers
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

# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @package core.base_geometry
# @brief Mathematical elementary geometrical objects.

import math
from decimal import Decimal, ROUND_UP, ROUND_HALF_EVEN

from mathmakerlib import required
from mathmakerlib.calculus import is_number, Number

from mathmaker.lib.core.base import Drawable, Printable
from mathmaker.lib.core.base_calculus import Value
from mathmaker.lib.constants.latex import MARKUP


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

    def __init__(self, name=None, x=None, y=None):
        """
        Initialize Point

        :param name: the Point's name (e.g. 'A') or another Point to copy
        :type name: str
        :param x: the Point's abscissa
        :type x: a number
        :param y: the Point's ordinate
        :type y: a number
        """
        if isinstance(name, Point):
            Point.__init__(self, name=name.name, x=name.x, y=name.y)
        else:
            if type(name) is not str:
                raise TypeError('A Point\'s name must be a str')
            if any([not is_number(n) for n in [x, y]]):
                raise TypeError('x and y must be numbers')
            self._name = name
            self._x = Decimal(str(x))
            self._y = Decimal(str(y))
            self._x_exact = self._x
            self._y_exact = self._y

    def __repr__(self):
        return '#{}({}; {})#'.format(self.name, self.x, self.y)

    def __eq__(self, other):
        return all([self.x == other.x, self.y == other.y,
                    self.name == other.name])

    def __ne__(self, other):
        return any([self.x != other.x, self.y != other.y,
                    self.name != other.name])

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the abscissa of the Point, rounded up to the tenth
    @property
    def x(self):
        return Number(str(self._x)).rounded(Decimal('0.01'))

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
        return Number(str(self._y)).rounded(Decimal('0.01'))

    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the exact ordinate of the Point
    @property
    def y_exact(self):
        return self._y

    @property
    def xy(self):
        return str(self.x_exact) + str(self.y_exact)

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the abscissa of the Point
    @x.setter
    def x(self, arg):
        if not is_number(arg):
            raise ValueError('Instead of a number, got: ' + str(arg))

        self._x = arg

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the ordinate of the Point
    @y.setter
    def y(self, arg):
        if not is_number(arg):
            raise ValueError('Instead of a number, got: ' + str(arg))

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
            raise ValueError('Instead of a Point, got: ' + str(type(center)))

        if not is_number(angle):
            raise ValueError('Instead of a number, got: ' + str(type(angle)))

        delta_x = self.x_exact - center.x_exact
        delta_y = self.y_exact - center.y_exact

        rx = delta_x * Decimal(str(math.cos(math.radians(angle)))) \
            - delta_y * Decimal(str(math.sin(math.radians(angle)))) \
            + center.x_exact
        ry = delta_x * Decimal(str(math.sin(math.radians(angle)))) \
            + delta_y * Decimal(str(math.cos(math.radians(angle)))) \
            + center.y_exact

        new_name = self.name + "'"

        if 'keep_name' in options and options['keep_name']:
            new_name = self.name

        elif 'new_name' in options and type(options['new_name']) == str:
            new_name = options['new_name']

        return Point(new_name, rx, ry)

    def into_euk(self):
        return '{name} = point({x}, {y})\n'.format(name=self.name,
                                                   x=self.x, y=self.y)


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
            raise ValueError('Instead of tuple|Segment, got: '
                             + str(type(arg)))
        elif type(arg) == tuple:
            if not (isinstance(arg[0], Point) and isinstance(arg[1], Point)):
                # __
                raise ValueError('Instead of (Point, Point) got: ' + str(arg))

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

    def revert(self):
        reverted = self.clone()
        reverted._points = reverted._points[::-1]
        return reverted

    @property
    def label(self):
        """Label of the Segment (the displayed information)."""
        return self._label

    @property
    def real_length(self):
        """Real length (build length) of the Segment."""
        x_delta = self.points[0].x - self.points[1].x
        y_delta = self.points[0].y - self.points[1].y
        return math.hypot(x_delta, y_delta)

    @property
    def length(self):
        """Fake length of the Segment (the one used in a problem)."""
        return self._length

    @property
    def length_has_been_set(self):
        """Whether the (fake) length has been set or not."""
        return self._length_has_been_set

    @property
    def length_name(self):
        """Length's name of the Segment, like AB."""
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
            raise ValueError('Instead of Value, got: ' + str(type(arg)))

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
            raise ValueError('Instead of numeric Value, got: '
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
            raise ValueError('Instead of str, got: ' + str(type(arg)))

        if arg not in AVAILABLE_SEGMENT_MARKS:
            raise ValueError('Got: ' + str(arg)
                             + ' instead of a string from this list: '
                             + str(AVAILABLE_SEGMENT_MARKS))

        self._mark = arg

    def dividing_points(self, n=1, prefix='a'):
        """
        Create the list of Points that divide the Segment in n parts.

        :param n: the number of parts (so it will create n - 1 points)
                  n must be greater or equal to 1
        :type n: int
        """
        if type(n) is not int:
            raise TypeError('n must be an int')
        if not n >= 1:
            raise ValueError('n must be greater or equal to 1')
        x0 = Decimal(str(self.points[0].x_exact))
        x1 = Decimal(str(self.points[1].x_exact))
        xstep = (x1 - x0) / n
        x_list = [x0 + (i + 1) * xstep for i in range(n - 1)]
        y0 = Decimal(str(self.points[0].y_exact))
        y1 = Decimal(str(self.points[1].y_exact))
        ystep = (y1 - y0) / n
        y_list = [y0 + (i + 1) * ystep for i in range(n - 1)]
        return [Point(prefix + str(i + 1), x, y)
                for i, (x, y) in enumerate(zip(x_list, y_list))]

    def label_into_euk(self):
        """Return the label correctly positionned along the Segment."""
        if self.label in [Value(''), Value('hidden')]:
            return ''
        else:
            result = ''
            x = self.real_length
            scale_factor = Number(str(1.6 * x))\
                .rounded(Decimal('0.1'), rounding=ROUND_UP)
            if x <= 3:
                angle_correction = Number(str(-8 * x + 33))\
                    .rounded(Decimal('0.1'), rounding=ROUND_UP)
            else:
                angle_correction = \
                    Number(str(1.1 / (1 - 0.95 * math.exp(-0.027 * x))))\
                    .rounded(Decimal('0.1'), rounding=ROUND_UP)

            side_angle = Vector((self.points[0], self.points[1])).slope

            label_position_angle = Number(side_angle) \
                .rounded(Decimal('1'), rounding=ROUND_HALF_EVEN)

            label_position_angle %= Decimal("360")

            rotate_box_angle = Decimal(label_position_angle)

            if (rotate_box_angle >= 90 and rotate_box_angle <= 270):
                rotate_box_angle -= Decimal("180")
            elif (rotate_box_angle <= -90 and rotate_box_angle >= -270):
                rotate_box_angle += Decimal("180")

            rotate_box_angle %= Decimal("360")

            result += "  $\\rotatebox{"
            required.package['graphicx'] = True
            result += str(rotate_box_angle)
            result += "}{\sffamily "
            result += self.label.into_str(display_unit=True, textwrap=False)
            result += "}$ "
            result += self.points[0].name + " "
            result += str(label_position_angle)
            result += " - "
            result += str(angle_correction) + " deg "
            result += str(scale_factor)
            result += "\n"
            return result

    def into_euk(self):
        return self.points[0].name + '.' + self.points[1].name


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
            Point.__init__(self, Point('', arg.x_exact, arg.y_exact))

        elif isinstance(arg, tuple) and len(arg) == 2:
            if all([isinstance(elt, Point) for elt in arg]):
                Point.__init__(self, Point('',
                                           arg[1].x_exact - arg[0].x_exact,
                                           arg[1].y_exact - arg[0].y_exact))
            elif all([is_number(elt) for elt in arg]):
                Point.__init__(self, Point('', arg[0], arg[1]))
            else:
                raise ValueError('Got a tuple not only of Points or numbers, '
                                 'instead of (Point,Point)|(x,y)')
        else:
            raise ValueError('Got: ' + str(type(arg))
                             + ' instead of Point|(,)')

    # --------------------------------------------------------------------------
    ##
    #   @brief Adds two vectors
    #   @param arg Vector
    def __add__(self, arg):
        if not isinstance(arg, Vector):
            raise ValueError('Got: ' + str(type(arg)) + ' instead of a Vector')

        return Vector((self.x_exact + arg.x_exact,
                       self.y_exact + arg.y_exact))

    @property
    def norm(self):
        """Return the norm of self."""
        return Decimal(str(math.hypot(self._x_exact, self._y_exact)))

    @property
    def slope(self):
        """Return the slope of self."""
        theta = Number(
            str(math.degrees(math.acos(self._x_exact / self.norm))))\
            .rounded(Decimal('0.1'))
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
            raise ValueError('Got: ' + str(type(arg)) + ' instead of a Vector')
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

    def into_euk(self):
        raise NotImplementedError


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

        elif isinstance(arg, Ray):
            self._point0 = arg._point0.clone()
            self._point1 = arg._point1.clone()
            self._name = arg._name

    def into_euk(self):
        raise NotImplementedError


# ------------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ------------------------------------------------------------------------------
##
# @class Angle
# @brief
class Angle(Drawable, Printable):

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
            self._label_display_angle = Number(str(self._measure)) \
                .rounded(Decimal('0.1')) / 2
        elif isinstance(arg, Angle):
            self._ray0 = arg._ray0.clone()
            self._ray1 = arg._ray1.clone()
            self._points = [p.clone() for p in arg._points]
            self._measure = arg._measure
            self._mark = arg._mark
            self._label = arg._label.clone()
            self._name = arg._name
            self._label_display_angle = arg._label_display_angle
        else:
            raise ValueError('Expected (Point, Point, Point) '
                             + ' instead of: ' + str(type(arg)))

    def __repr__(self):
        return ' ∡ ' + self._name + ' ∡ '

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other_objct):
        if not isinstance(other_objct, Angle):
            return False
        return self._name == other_objct._name

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

    @label.setter
    def label(self, arg):
        """Properly set the Angle's label."""
        if type(arg) == str or isinstance(arg, Value):
            self._label = Value(arg)
        else:
            raise TypeError('Expected a str or a Value. Got {t} instead.'
                            .format(t=str(type(arg))))

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the angle (for display) of label's angle
    @label_display_angle.setter
    def label_display_angle(self, arg):
        if not is_number(arg):
            raise ValueError('arg should be a number ')
        else:
            self._label_display_angle = Number(str(arg))\
                .rounded(Decimal('0.1'))

    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the mark of the angle
    @mark.setter
    def mark(self, arg):
        if type(arg) == str:
            if arg in AVAILABLE_ANGLE_MARKS:
                self._mark = arg
            else:
                raise ValueError('Got: ' + arg
                                 + ' instead of a string from this list: '
                                 + str(AVAILABLE_ANGLE_MARKS))

        else:
            raise ValueError('arg should be a str')

    def into_str(self, **options):
        return self._name

    def into_euk(self):
        return ''
