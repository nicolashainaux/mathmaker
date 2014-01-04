# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets with their answers
# Copyright 2006-2013 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

# -----------------------------------------------------------------------------
# --------------------------------------- PACKAGE:  core.geometry -------------
# -----------------------------------------------------------------------------
##
# @package core.geometry
# @brief Mathematical geometrical objects.

import math
import locale
from decimal import *
from base import *
from base_geometry import *
from lib import *
from lib import randomly
from lib.maths_lib import *
from core.calculus import *
from lib.common import cfg

if debug.ENABLED:
    from lib.common import latex
    import machine

markup_choice = cfg.get_value_from_file('MARKUP', 'USE')

if markup_choice == 'latex':
    from lib.common.latex import MARKUP

try:
    locale.setlocale(locale.LC_ALL, default.LANGUAGE + '.' + default.ENCODING)
except:
    locale.setlocale(locale.LC_ALL, '')

# GLOBAL
#expression_begins = True






# -----------------------------------------------------------------------------
# -------------------------------------------------- CLASS: Triangle ----------
# -----------------------------------------------------------------------------
##
# @class Triangle
# @brief
class Triangle(Drawable):





    # -------------------------------------------------- CONSTRUCTOR ----------
    ##
    #   @brief Constructor.
    #   @param arg : Triangle |
    #                ((str, str, str), (not implemented yet)'sketch'
    #        OR :                      {'side0':nb0, 'angle1':nb1, 'side1':nb2}
    #        OR : (not implemented yet){'side0':nb0, 'side1':nb1, 'side2':nb2}
    #        OR : (not implemented yet) etc.
    #                )
    #            NB : the three str will be the vertices' names
    #            NB : 'sketch' will just choose (reasonnably) random values
    #   @param options
    #   Options details :
    #   - rotate_around_gravity_center = 'no'|'any'|nb
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

        self._vertices = [None, None, None]
        self._sides = [None, None, None]
        self._angles = [None, None, None]
        self._name = ""
        self._rotation_angle = 0

        if type(arg) == tuple:
            if not len(arg) == 2:
                raise error.WrongArgument(' tuple of length 2 ',
                                          ' tuple of length ' \
                                          + str(len(arg))
                                         )

            vertices_names = arg[0]
            construction_data = arg[1]

            if not type(vertices_names) == tuple:
                raise error.WrongArgument(' a tuple ', str(vertices_names))

            if not type(vertices_names[0]) == str \
                and type(vertices_names[1]) == str \
                and type(vertices_names[2]) == str:
            #___
                raise error.WrongArgument(' three strings ',
                                        ' one of them at least is not a string')

            if not (construction_data == 'sketch' \
                    or (type(construction_data) == dict \
                        and 'side0' in construction_data \
                        and is_.a_number(construction_data['side0']) \
                        and (('side1' in construction_data \
                              and is_.a_number(construction_data['side1']) \
                             ) \
                             or \
                             (('angle1' in construction_data \
                              and is_.a_number(construction_data['angle1']) \
                              ) \
                             ) \
                            ) \
                        ) \
                    ):
            #___
                raise error.WrongArgument(" 'sketch' | " \
                              + "{'side0':nb0, 'angle1':nb1, 'side1':nb2} | ",
                              str(construction_data))

            start_vertex = [None, None, None]

            side0_length = construction_data['side0']
            side1_length = construction_data['side1']

            if 'rotate_around_isobarycenter' in options:
                if options['rotate_around_isobarycenter'] == 'randomly':
                    self._rotation_angle = randomly.integer(0, 35) * 10
                elif is_.a_number(options['rotate_around_isobarycenter']):
                    self._rotation_angle = \
                                          options['rotate_around_isobarycenter']

            start_vertex[0] = Point([vertices_names[0],
                                     (0, 0)
                                    ]
                                   )
            start_vertex[1] = Point([vertices_names[1],
                                     (side0_length, 0)
                                    ]
                                   )
            start_vertex[2] = Point([vertices_names[2],
                                     (side0_length \
                                       - side1_length*Decimal(str(math.cos(\
                                     deg_to_rad(construction_data['angle1'])))),
                                      side1_length*Decimal(str(math.sin( \
                                     deg_to_rad(construction_data['angle1']))))
                                     )
                                    ]
                                   )

            if self._rotation_angle != 0:
                G = barycenter([start_vertex[0],
                                start_vertex[1],
                                start_vertex[2]
                               ],
                               "G"
                               )

                self._vertices = (Point(\
                                start_vertex[0].rotate(G,
                                                       self._rotation_angle,
                                                       keep_name=True
                                                      )
                                               ),
                                  Point(\
                                start_vertex[1].rotate(G,
                                                       self._rotation_angle,
                                                       keep_name=True
                                                      )
                                                ),
                                  Point(\
                                start_vertex[2].rotate(G,
                                                       self._rotation_angle,
                                                       keep_name=True
                                                      )
                                                )
                                  )

            else:
                self._vertices = (start_vertex[0].deep_copy(),
                                  start_vertex[1].deep_copy(),
                                  start_vertex[2].deep_copy()
                                 )

            self._sides = (Segment((self._vertices[0],
                                    self._vertices[1]
                                   )
                                  ),
                           Segment((self._vertices[1],
                                    self._vertices[2]
                                   )
                                  ),
                           Segment((self._vertices[2],
                                    self._vertices[0]
                                   )
                                  )
                          )

            self._angles[0] = Angle((self.vertex1, self.vertex0, self.vertex2))
            self._angles[1] = Angle((self.vertex2, self.vertex1, self.vertex0))
            self._angles[2] = Angle((self.vertex0, self.vertex2, self.vertex1))

            self._angles[0].set_label_display_angle(self._angles[0].measure/2)
            self._angles[1].set_label_display_angle(180 \
                                                    - self._angles[1].measure/2)
            self._angles[2].set_label_display_angle(180 \
                                                    + self._angles[0].measure \
                                                    + self._angles[2].measure/2)

        else:
            # copy of a given Triangle
            self._vertices = [arg.vertex0.deep_copy(),
                              arg.vertex1.deep_copy(),
                              arg.vertex2.deep_copy()
                             ]
            self._rotation_angle = arg.rotation_angle
            self._sides = [arg.side0.deep_copy(),
                           arg.side1.deep_copy(),
                           arg.side2.deep_copy()
                          ]
            self._angles = [arg.angle0.deep_copy(),
                            arg.angle1.deep_copy(),
                            arg.angle2.deep_copy()
                           ]

        self._name = self.vertex0.name + self.vertex1.name + self.vertex2.name

        random_number = ""
        for i in xrange(8):
            random_number += str(randomly.integer(0, 9))

        self._filename = _("Triangle") + "_" + self.name \
                         + "-" + random_number







    # -------------------------------------------------- GET VERTEX0 ----------
    ##
    #   @brief Returns vertex0 (as a Point)
    def get_vertex0(self):
        return self._vertices[0]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    vertex0 = property(get_vertex0,
                       doc = "First vertex of the Triangle")





    # -------------------------------------------------- GET VERTEX1 ----------
    ##
    #   @brief Returns vertex1 (as a Point)
    def get_vertex1(self):
        return self._vertices[1]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    vertex1 = property(get_vertex1,
                       doc = "Second vertex of the Triangle")





    # -------------------------------------------------- GET VERTEX2 ----------
    ##
    #   @brief Returns vertex2 (as a Point)
    def get_vertex2(self):
        return self._vertices[2]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    vertex2 = property(get_vertex2,
                       doc = "Third vertex of the Triangle")





    # ------------------------------------------------- GET VERTICES ----------
    ##
    #   @brief Returns the three vertices (as a list of Points)
    def get_vertices(self):
        return self._vertices
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    vertices = property(get_vertices,
                        doc = "The three vertices (in a list)")





    # ------------------------------------------- GET ROTATION ANGLE ----------
    ##
    #   @brief Returns the angle of rotation around the isobarycenter
    def get_rotation_angle(self):
        return self._rotation_angle
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    rotation_angle = property(get_rotation_angle,
                              doc = "Angle of rotation around the isobarycenter")





    # --------------------------------------------------- GET ANGLE0 ----------
    ##
    #   @brief Returns angle0 (as an Angle)
    def get_angle0(self):
        return self._angles[0]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    angle0 = property(get_angle0,
                      doc = "First angle of the Triangle")





    # --------------------------------------------------- GET ANGLE1 ----------
    ##
    #   @brief Returns angle1 (as an Angle)
    def get_angle1(self):
        return self._angles[1]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    angle1 = property(get_angle1,
                      doc = "Second angle of the Triangle")





    # --------------------------------------------------- GET ANGLE2 ----------
    ##
    #   @brief Returns angle2 (as an Angle)
    def get_angle2(self):
        return self._angles[2]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    angle2 = property(get_angle2,
                      doc = "Third angle of the Triangle")





    # --------------------------------------------------- GET ANGLES ----------
    ##
    #   @brief Returns [angles]   (as a list of Angles)
    def get_angles(self):
        return self._angles
    # ---------------------------------------- ASSOCIATED PROPERTIES ----------
    angles = property(get_angles,
                      doc = "The angles' list of the Triangle")





    # ---------------------------------------------------- GET SIDE0 ----------
    ##
    #   @brief Returns side0 (as a Segment)
    def get_side0(self):
        return self._sides[0]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    side0 = property(get_side0,
                     doc = "First side of the Triangle")





    # ---------------------------------------------------- GET SIDE1 ----------
    ##
    #   @brief Returns side1 (as a Segment)
    def get_side1(self):
        return self._sides[1]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    side1 = property(get_side1,
                     doc = "Second side of the Triangle")





    # ---------------------------------------------------- GET SIDE2 ----------
    ##
    #   @brief Returns side2 (as a Segment)
    def get_side2(self):
        return self._sides[2]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    side2 = property(get_side2,
                     doc = "Third side of the Triangle")





    # ---------------------------------------------------- GET SIDES ----------
    ##
    #   @brief Returns [sides]   (as a list of Segments)
    def get_sides(self):
        return self._sides
    # ---------------------------------------- ASSOCIATED PROPERTIES ----------
    sides = property(get_sides,
                     doc = "The sides' list of the Triangle")





    # ----------------------------------------------------- GET NAME ----------
    ##
    #   @brief Returns the name of the triangle
    def get_name(self):
        return self._name
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    name = property(get_name,
                    doc = "Name of the right triangle")





    # ---------- FUNCTION CREATING THE EUKLEIDES STRING OF THE OBJECT ---------
    ##
    #   @brief Creates the euk string to put in the file
    #   @param options Any options
    #   @return The string to put in the picture file
    def into_euk(self, **options):
        box_values = self.work_out_euk_box()
        result = "box " + str(box_values[0]) + ", " \
                        + str(box_values[1]) + ", " \
                        + str(box_values[2]) + ", " \
                        + str(box_values[3])

        result += "\n\n"

        for vertex in self.vertices:
            result += vertex.name + " = point(" + str(vertex.x) \
                                              + ", " \
                                              + str(vertex.y) + ")\n"

        result += "\n\n"

        result += "draw"

        result += "\n  "

        result += "(" + self.vertex0.name + "." \
                      + self.vertex1.name + "." \
                      + self.vertex2.name + ")"

        scale_factor = 1
        angle_correction = 0

        sides_angles_offsets = {self.sides[0] : 0,
                                self.sides[1] : 180 - self.angle1.measure,
                                self.sides[2] : self.angle0.measure
                               }

        labels_angle_correction_signs = {self.sides[0] : "-",
                                         self.sides[1] : "-",
                                         self.sides[2] : "+"
                                        }

        labels_ref_points = {self.sides[0] : self.vertex0.name,
                             self.sides[1] : self.vertex1.name,
                             self.sides[2] : self.vertex0.name
                            }


        for side in self.sides:
            if side.label != None and side.label != Value(""):
                x = side.length
                scale_factor = round(Decimal(str(1.6*x)),
                                     Decimal('0.1'),
                                     rounding=ROUND_UP
                                    )
                if x <= 3:
                    angle_correction = round(Decimal(str(-8*x + 33)),
                                             Decimal('0.1'),
                                             rounding=ROUND_UP
                                            )
                else:
                    angle_correction = round(Decimal(str( \
                                                1.1/(1-0.95*math.exp(-0.027*x))
                                                        )
                                                    ),
                                             Decimal('0.1'),
                                             rounding=ROUND_UP
                                            )

                label_position_angle = round(Decimal(str(self.rotation_angle))\
                                             + \
                                             Decimal(str(\
                                                    sides_angles_offsets[side])),
                                             Decimal('1'),
                                             rounding=ROUND_HALF_EVEN
                                            )

                rotate_box_angle = Decimal(label_position_angle)

                if (rotate_box_angle >= 90 \
                    and rotate_box_angle <= 270):
                #___
                    rotate_box_angle -= Decimal("180")
                elif (rotate_box_angle <= -90 \
                    and rotate_box_angle >= -270):
               #___
                    rotate_box_angle += Decimal("180")

                result += "\n  "
                result += "$\\rotatebox{"
                result += str(rotate_box_angle)
                result += "}{"
                result += side.label.into_str(display_unit='yes',
                                           graphic_display='yes')
                result += "}$ "
                result += labels_ref_points[side] + " "
                result += str(label_position_angle)
                result += " " + labels_angle_correction_signs[side] + " "
                result += str(angle_correction) + " deg "
                result += str(scale_factor)
                result += "\n"


        for angle in self.angles:
            if angle.label != None and angle.label != Value(""):
                scale_factor = Decimal('2.7')
                if Decimal(str(angle.measure)) < Decimal('28.5'):
                    scale_factor = round(Decimal('38.1')\
                                              *pow(Decimal(str(angle.measure)),
                                                   Decimal('-0.8')
                                                  ),
                                         Decimal('0.01'),
                                         rounding=ROUND_HALF_UP
                                         )

                label_position_angle = Decimal(str(angle.label_display_angle)) \
                                       + Decimal(str(self.rotation_angle))
                rotate_box_angle = Decimal(label_position_angle)

                if (rotate_box_angle >= 90 \
                    and rotate_box_angle <= 270):
                #___
                    rotate_box_angle -= Decimal("180")
                elif (rotate_box_angle <= -90 \
                    and rotate_box_angle >= -270):
                #___
                    rotate_box_angle += Decimal("180")

                result += "\n  "
                result += "$\\rotatebox{"
                result += str(rotate_box_angle)
                result += "}{"
                result += angle.label.into_str(display_unit='yes',
                                            graphic_display='yes')
                result += "}$ "
                result += angle.vertex.name + " "
                result += str(label_position_angle) + " deg "
                result += str(scale_factor)
                result += "\n"

        result += "\nend"

        result += "\n\n"

        result += "label"

        result += "\n"

        for angle in self.angles:
            if angle.mark != "":
                result += "  " + angle.point0.name + ", " \
                        + angle.vertex.name + ", " \
                        + angle.point2.name \
                        + " " \
                        + angle.mark
                result += "\n"

        result += "  " + self.vertex0.name + " " \
               + str(self.rotation_angle) + " + 200 deg"

        result += "\n"

        result += "  " + self.vertex1.name + " " \
               + str(self.rotation_angle) + " - 45 deg"

        result += "\n"

        result += "  " + self.vertex2.name + " " \
               + str(self.rotation_angle) + " + 65 deg"

        result += "\nend"

        return result





    # --------------------------- WORKS OUT THE DIMENSIONS OF THE BOX ---------
    ##
    #   @brief Works out the dimensions of the box
    #   @param options Any options
    #   @return (x1, y1, x2, y2)
    def work_out_euk_box(self, **options):
        x_list = [self.vertex0.x,
                  self.vertex1.x,
                  self.vertex2.x
                  ]
        y_list = [self.vertex0.y,
                  self.vertex1.y,
                  self.vertex2.y
                  ]

        return (min(x_list)-Decimal("0.6"), min(y_list)-Decimal("0.6"),
                max(x_list)+Decimal("0.6"), max(y_list)+Decimal("0.6"))






# -----------------------------------------------------------------------------
# --------------------------------------------- CLASS: RightTriangle ----------
# -----------------------------------------------------------------------------
##
# @class RightTriangle
# @brief
class RightTriangle(Triangle):





    # -------------------------------------------------- CONSTRUCTOR ----------
    ##
    #   @brief Constructor.
    #   @param arg : RightTriangle |
    #                ((str, str, str), 'sketch'
    #        OR :                      {'leg0' : nb0, 'leg1' : nb1}
    #        OR : (not implemented yet){'leg0' : nb0, 'angle0' : nb1}
    #                )
    #            NB : the three str will be the vertices' names
    #                 The second name will be the right corner
    #                 so, hypotenuse will be vertices_names[0] & [2]
    #            NB : 'sketch' will just choose (reasonnably) random values
    #   @param options
    #   Options details :
    #   - rotate_around_gravity_center = 'no'|'any'|nb
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

        self._vertices = [None, None, None]
        self._rotation_angle = 0
        self._sides = [None, None, None]
        self._name = ""

        if type(arg) == tuple:
            if not len(arg) == 2:
                raise error.WrongArgument(' tuple of length 2 ',
                                          ' tuple of length ' \
                                          + str(len(arg))
                                         )
            vertices_names = arg[0]
            construction_data = arg[1]

            if not type(vertices_names) == tuple:
                raise error.WrongArgument(' a tuple ', str(vertices_names))

            if not type(vertices_names[0]) == str \
                and type(vertices_names[1]) == str \
                and type(vertices_names[2]) == str:
            #___
                raise error.WrongArgument(' three strings ',
                                        ' one of them at least is not a string')

            rotation = 0

            if 'rotate_around_isobarycenter' in options \
                and options['rotate_around_isobarycenter'] == 'randomly':
            #___
                rotation = randomly.integer(0, 35) * 10

            elif 'rotate_around_isobarycenter' in options \
                and is_.a_number(options['rotate_around_isobarycenter']):
            #___
                rotation = options['rotate_around_isobarycenter']

            leg0_length = 0
            leg1_length = 0

            if construction_data == 'sketch':
                leg0_length = Decimal(str(randomly.integer(35, 55)))/10
                leg1_length = Decimal(str(randomly.integer(7, 17))) \
                              / Decimal("20") * leg0_length

            elif type(construction_data) == dict \
                and 'leg0' in construction_data \
                and is_.a_number(construction_data['leg0']) \
                and 'leg1' in construction_data \
                and is_.a_number(construction_data['leg1']):
            #___
                leg0_length = construction_data['leg0']
                leg1_length = construction_data['leg1']

            else:
                raise error.WrongArgument(" 'sketch' | " \
                                        + "{'leg0' : nb0, 'leg1' : nb1}",
                                          str(construction_data))

            Triangle.__init__(self,
                              ((vertices_names[0],
                                vertices_names[1],
                                vertices_names[2]
                                ),
                               {'side0' : leg0_length,
                                'angle1' : 90,
                                'side1' : leg1_length
                               }
                              ),
                              rotate_around_isobarycenter=rotation
                             )

        else:
            # copy of a given RightTriangle
            self._vertices = [arg.vertex0.deep_copy(),
                              arg.vertex1.deep_copy(),
                              arg.vertex2.deep_copy()
                             ]
            self._rotation_angle = arg.rotation_angle
            self._sides = [arg.side0.deep_copy(),
                           arg.side1.deep_copy(),
                           arg.side2.deep_copy()
                          ]
            self._angles = [arg.angle0.deep_copy(),
                            arg.angle1.deep_copy(),
                            arg.angle2.deep_copy()
                           ]
            # the other fields are re-created hereafter

        self._name = self.vertex0.name + self.vertex1.name + self.vertex2.name

        self.right_angle.set_mark("right")

        random_number = ""
        for i in xrange(8):
            random_number += str(randomly.integer(0, 9))

        self._filename = _("RightTriangle") + "_" + self.name \
                         + "-" + random_number







    # ----------------------------------------------------- GET LEG0 ----------
    ##
    #   @brief Returns leg0 (as a Segment)
    def get_leg0(self):
        return self._sides[0]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    leg0 = property(get_leg0,
                    doc = "First leg of the Triangle")





    # ----------------------------------------------------- GET LEG1 ----------
    ##
    #   @brief Returns leg1 (as a Segment)
    def get_leg1(self):
        return self._sides[1]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    leg1 = property(get_leg1,
                    doc = "Second leg of the Triangle")





    # ----------------------------------------------------- GET LEGS ----------
    ##
    #   @brief Returns legs (as a Segment)
    def get_legs(self):
        return [self.leg0, self.leg1]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    legs = property(get_legs,
                    doc = "The two legs of the Right Triangle (in a list)")





    # ----------------------------------------------- GET HYPOTENUSE ----------
    ##
    #   @brief Returns hypotenuse (as a Segment)
    def get_hypotenuse(self):
        return self._sides[2]
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    hypotenuse = property(get_hypotenuse,
                          doc = "Hypotenuse of the Right Triangle")





    # ---------------------------------------------- GET RIGHT ANGLE ----------
    ##
    #   @brief Returns Tthe right angle (as an Angle)
    def get_right_angle(self):
        return self.angle1
    # ------------------------------------------ ASSOCIATED PROPERTY ----------
    right_angle = property(get_right_angle,
                           doc = "Right Angle of the Right Triangle")





    # ------------------------------------ PYTHAGOREAN (RAW) EQUALITY ---------
    ##
    #   @brief Creates the correct pythagorean equality hyp²=leg0²+leg1²
    #   @return an Equality but not usable to calculate (see substequality)
    def pythagorean_equality(self, **options):

        objcts = [Item(('+', self.hypotenuse.length_name, 2)),
                  Sum([Item(('+', self.leg0.length_name, 2)),
                       Item(('+', self.leg1.length_name, 2))]
                     )]

        return Equality(objcts, **options)




# ---------------------------- PYTHAGOREAN SUBSTITUTABLE EQUALITY ---------
    ##
    #   @brief Creates the correct (substitutable) pythagorean equality
    #   @brief Uses the labels to determine the result...
    #   @return a SubstitutableEquality
    def pythagorean_substequality(self, **options):
        # First, check the number of numeric data
        # and find the unknown side
        n_numeric_data = 0
        unknown_side = ""
        if self.leg0.label.is_numeric():
            n_numeric_data += 1
        elif self.leg0.label.value == "":
            unknown_side = 'leg0'
        if self.leg1.label.is_numeric():
            n_numeric_data += 1
        elif self.leg1.label.value == "":
            unknown_side = 'leg1'
        if self.hypotenuse.label.is_numeric():
            n_numeric_data += 1
        elif self.hypotenuse.label.value == "":
            unknown_side = 'hypotenuse'

        if n_numeric_data != 2:
            raise error.ImpossibleAction("creation of a pythagorean equality "\
                                         "when the number of known numeric " \
                                         "values is different from 2.")

        # Now create the SubstitutableEquality (so, also create the dictionnary)
        if unknown_side == 'leg0':
            subst_dict = {Value(self.leg1.length_name): self.leg1.label,
                          Value(self.hypotenuse.length_name): \
                                                        self.hypotenuse.label
                         }
            objcts = [Item(('+', self.leg0.length_name, 2)),
                      Sum([Item(('+', self.hypotenuse.length_name, 2)),
                           Item(('-', self.leg1.length_name, 2))]
                         )]

        elif unknown_side == 'leg1':
            subst_dict = {Value(self.leg0.length_name): self.leg0.label,
                          Value(self.hypotenuse.length_name): \
                                                        self.hypotenuse.label
                         }
            objcts = [Item(('+', self.leg1.length_name, 2)),
                      Sum([Item(('+', self.hypotenuse.length_name, 2)),
                           Item(('-', self.leg0.length_name, 2))]
                         )]

        elif unknown_side == 'hypotenuse':
            subst_dict = {Value(self.leg0.length_name): self.leg0.label,
                          Value(self.leg1.length_name): self.leg1.label
                         }
            objcts = [Item(('+', self.hypotenuse.length_name, 2)),
                      Sum([Item(('+', self.leg0.length_name, 2)),
                           Item(('+', self.leg1.length_name, 2))]
                         )]

        else:
            raise error.ImpossibleAction("creation of a pythagorean equality "\
                                         "because no unknown side was found")


        return SubstitutableEquality(objcts, subst_dict)


