# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets with their answers
# Copyright 2006-2015 Nicolas Hainaux <nico_h@users.sourceforge.net>

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
import locale
from decimal import *
from .base import *
from core.base_calculus import Value
from lib import *
from lib.maths_lib import *
from maintenance import debug
from lib.common import cfg

markup_choice = cfg.get_value_from_file('MARKUP', 'USE')

if markup_choice == 'latex':
    from lib.common.latex import MARKUP

if debug.ENABLED:
    from lib.common import latex
    import machine

try:
    locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
except:
    locale.setlocale(locale.LC_ALL, '')

# the mark 'dashed' has been removed from the available list since it may
# produce buggy results sometimes from euktopst
AVAILABLE_ANGLE_MARKS = ['', 'simple', 'double', 'triple', 'right',
                         'forth', 'back', 'dotted']
AVAILABLE_SEGMENT_MARKS = []

# GLOBAL
#expression_begins = True


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
    #   @param arg : [String, (nb,nb)]|Point
    #   Types details :
    #   -
    #   @param options
    #   Options details :
    #   -
    #   @warning Might raise...
    def __init__(self, arg, **options):
        if not (type(arg) == list or isinstance(arg, Point)):
            raise error.WrongArgument(' list|Point ', str(type(arg)))

        elif type(arg) == list:
            if not len(arg) == 2:
                raise error.WrongArgument(' a list of length 2 ',
                                          ' a list of length ' \
                                          + str(len(arg))
                                          )

            if not type(arg[0]) == str:
                raise error.WrongArgument(' a str ', str(type(arg[0])))

            if not (type(arg[1]) == tuple \
                and len(arg[1]) == 2 \
                and is_.a_number(arg[1][0]) \
                and is_.a_number(arg[1][1])):
            #___
                raise error.WrongArgument(' (x, y) ', str(arg))

            self._name = arg[0]
            self._x = Decimal(arg[1][0])
            self._y = Decimal(arg[1][1])

        else:
            self._name = arg.name
            self._x = arg.x
            self._y = arg.y




    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the abscissa of the Point, rounded up to the tenth
    def get_x(self):
        return round(Decimal(str(self._x)),
                     Decimal('0.01'),
                     rounding=ROUND_HALF_UP
                    )





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the exact abscissa of the Point
    def get_x_exact(self):
        return self._x





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the ordinate of the Point, rounded up to the tenth
    def get_y(self):
        return round(Decimal(str(self._y)),
                     Decimal('0.01'),
                     rounding=ROUND_HALF_UP
                    )





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the exact ordinate of the Point
    def get_y_exact(self):
        return self._y






    x = property(get_x, doc = "Abscissa of the Point (rounded)")

    x_exact = property(get_x_exact, doc = "Abscissa of the Point (exact)")

    y = property(get_y, doc = "Ordinate of the Point (exact)")

    y_exact = property(get_y_exact, doc = "Ordinate of the Point (rounded)")








    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the abscissa of the Point
    def set_x(self, arg):
        if not is_.a_number(arg):
            raise error.WrongArgument(' a number ', str(arg))

        self._x = arg




    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the ordinate of the Point
    def set_y(self, arg):
        if not is_.a_number(arg):
            raise error.WrongArgument(' a number ', str(arg))

        self._y = arg





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

        rx = delta_x*Decimal(str(math.cos(deg_to_rad(angle)))) \
             - delta_y*Decimal(str(math.sin(deg_to_rad(angle)))) \
             + center.x_exact
        ry = delta_x*Decimal(str(math.sin(deg_to_rad(angle)))) \
             + delta_y*Decimal(str(math.cos(deg_to_rad(angle)))) \
             + center.y_exact

        new_name = self.name + "'"

        if 'keep_name' in options and options['keep_name'] == True:
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
    #   Types details :
    #   -
    #   @param options
    #   Options details :
    #   -
    #   @warning Might raise...
    def __init__(self, arg, **options):
        if not (type(arg) == tuple or isinstance(arg, Segment)):
            raise error.WrongArgument(' tuple|Segment ', str(type(arg)))

        elif type(arg) == tuple:
            if not (isinstance(arg[0], Point) and isinstance(arg[1], Point)):
            #___
                raise error.WrongArgument(' (Point, Point) ', str(arg))

            self._points = (arg[0].clone(), arg[1].clone())

            self._label  = None

            if 'label' in options and type(options['label']) == str:
                self._label = options['label']

        else:
            self._points = (arg.points[0].clone(),
                            arg.points[1].clone()
                           )
            self._label = arg.label

        self._mark = None

        self._name = "[" + self.points[0].name + self.points[1].name + "]"




    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the two points
    def get_points(self):
        return self._points





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the label of the Segment
    def get_label(self):
        return self._label






    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the length of the Segment
    def get_length(self):
        x_delta = self.points[0].x - self.points[1].x
        y_delta = self.points[0].y - self.points[1].y
        return math.hypot(x_delta, y_delta)





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the length name of the Segment
    def get_length_name(self):
        return self.points[0].name + self.points[1].name





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the mark of the Segment
    def get_mark(self):
        return self._mark






    # --------------------------------------------------------------------------
    points = property(get_points,
                      doc = "The couple of points ending the segment")





    label = property(get_label,
                     doc = "Label of the Segment")

    length = property(get_length,
                      doc = "Name of the Segment")

    length_name = property(get_length_name,
                           doc = "Length's name of the Segment")

    mark = property(get_mark,
                    doc = "Mark of the Segment")





    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the label of the Segment
    def set_label(self, arg):
        if not type(arg) == Value:
            raise error.WrongArgument(' Value ', str(type(arg)))

        self._label = arg





    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the mark of the Segment
    def set_mark(self, arg):
        if not type(arg) == str:
            raise error.WrongArgument(' str ', str(type(arg)))

        if not arg in AVAILABLE_SEGMENT_MARKS:
            raise error.WrongArgument(arg, 'a string from this list : ' \
                                      + str(AVAILABLE_SEGMENT_MARKS))

        self._mark = arg





    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the points of the Segment (is this useful at all ?)
    def set_point(self, nb, arg):
        if not is_.a_number(nb):
            raise error.WrongArgument(' a number ', str(nb))
        if not isinstance(arg, Point):
            raise error.WrongArgument(' a Point ', str(arg))


        self._points[nb] = arg.clone()




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
    #   @param arg : (Point, Point)
    #   @param options : label
    #   Options details :
    #   @warning Might raise...
    def __init__(self, arg, **options):
        self._point0 = None # the initial point
        self._point1 = None
        self._name = None

        if isinstance(arg, tuple) and len(arg) == 2 \
            and isinstance(arg[0], Point) \
            and isinstance(arg[1], Point):
        #___
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
    #   @param arg : (Point, Point, Point)
    #   @param options : label
    #   Options details :
    #   @warning Might raise...
    def __init__(self, arg, **options):
        self._ray0 = None
        self._ray1 = None
        self._points = None
        self._measure = None
        self._mark = ""
        self._label = Value("")
        self._name = None

        if isinstance(arg, tuple) and len(arg) == 3 \
            and isinstance(arg[0], Point) \
            and isinstance(arg[1], Point) \
            and isinstance(arg[2], Point):
        #___
            self._ray0 = Ray((arg[1], arg[0]))
            self._ray1 = Ray((arg[1], arg[2]))
            self._points = [arg[0].clone(),
                            arg[1].clone(),
                            arg[2].clone()]

            # Let's determine the measure of the angle :
            aux_side0 = Segment((self._points[0], self._points[1]))
            aux_side1 = Segment((self._points[1], self._points[2]))
            aux_side2 = Segment((self._points[2], self._points[0]))
            aux_num = aux_side0.length * aux_side0.length \
                    + aux_side1.length * aux_side1.length \
                    - aux_side2.length * aux_side2.length
            aux_denom = 2 * aux_side0.length * aux_side1.length
            aux_cos = aux_num / aux_denom
            self._measure = Decimal(str(math.degrees(math.acos(aux_cos))))

            if 'label' in options and type(options['label']) == str:
                self._label = options['label']

            if 'mark' in options and type(options['mark']) == str:
                self._mark = options['mark']

            self._name = MARKUP['opening_widehat']
            self._name += arg[0].name + arg[1].name + arg[2].name
            self._name += MARKUP['closing_widehat']

        else:
            raise error.WrongArgument(' (Point, Point, Point) ', str(type(arg)))

        self._label_display_angle = round(Decimal(str(self._measure)),
                                          Decimal('0.1'),
                                          rounding=ROUND_HALF_UP
                                         ) / 2





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the measure of the angle
    def get_measure(self):
        return self._measure





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the point0 of the angle
    def get_point0(self):
        return self._points[0]






    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the vertex of the angle, as a Point
    def get_point1(self):
        return self._points[1]





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the point2 of the angle
    def get_point2(self):
        return self._points[2]





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the label of the angle
    def get_label(self):
        return self._label





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the angle (for display) of label's angle
    def get_label_display_angle(self):
        return self._label_display_angle





    # --------------------------------------------------------------------------
    ##
    #   @brief Returns the mark of the angle
    def get_mark(self):
        return self._mark





    measure = property(get_measure,
                       doc = "Measure of the angle")

    point0 = property(get_point0,
                      doc = "Point0 of the angle")

    point1 = property(get_point1,
                      doc = "Vertex of the angle")

    point2 = property(get_point2,
                      doc = "Point2 of the angle")

    vertex = property(get_point1,
                      doc = "Vertex of the angle")

    label = property(get_label,
                     doc = "Label of the angle")

    label_display_angle = property(get_label_display_angle,
                                doc = "Display angle of the label of the angle")

    mark = property(get_mark,
                          doc = "Mark of the angle")





    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the label of the angle
    def set_label(self, arg):
        if type(arg) == str or isinstance(arg, Value):
            self._label = Value(arg)

        else:
            raise error.WrongArgument(arg, 'str or Value')





    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the angle (for display) of label's angle
    def set_label_display_angle(self, arg):
        if not is_.a_number(arg):
            raise error.WrongArgument(arg, ' a number ')
        else:
            self._label_display_angle = round(Decimal(str(arg)),
                                              Decimal('0.1'),
                                              rounding=ROUND_HALF_UP
                                             )





    # --------------------------------------------------------------------------
    ##
    #   @brief Sets the mark of the angle
    def set_mark(self, arg):
        if type(arg) == str:
            if arg in AVAILABLE_ANGLE_MARKS:
                self._mark = arg
            else:
                raise error.WrongArgument(arg, 'a string from this list : ' \
                                               + str(AVAILABLE_ANGLE_MARKS))

        else:
            raise error.WrongArgument(arg, 'str')









