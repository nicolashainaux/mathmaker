# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
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

import math
from decimal import Decimal

from lib import *
from lib import utils
from lib.common import alphabet
from lib.common import pythagorean
from lib.common import vocabulary
from lib.common.cst import *
from lib.maths_lib import *
from Q_Structure import Q_Structure
#from core.calculus import Equality
from core.base_calculus import *
from core.calculus import *
#from core.base_geometry import *
from core.geometry import *
#from core.base import *


AVAILABLE_Q_KIND_VALUES = {'pythagorean_theorem' : ['calculate_hypotenuse',
                                                    'calculate_one_leg'],
                           'converse_of_pythagorean_theorem' : ['default'],
                           'contrapositive_of_pythagorean_theorem': ['default'],
                           'cosinus' : ['calculate_hypotenuse',
                                        'calculate_one_leg',
                                        'calculate_angle'],
                           'sinus' : ['calculate_hypotenuse',
                                      'calculate_one_leg',
                                      'calculate_angle'],
                           'tangente' : ['calculate_hypotenuse',
                                         'calculate_one_leg',
                                         'calculate_angle'],
                          }



# -----------------------------------------------------------------------------
# ------------------------------------------- CLASS: Q_RightTriangle ----------
# -----------------------------------------------------------------------------
##
# @class Q_RightTriangle
# @brief All questions about the right triangle
class Q_RightTriangle(Q_Structure):





    # -------------------------------------------------- CONSTRUCTOR ----------
    ##
    #   @brief Constructor.
    #   @param embedded_machine The machine to be used
    #   @options
    #   @return One instance of question.Q_RightTriangle
    def __init__(self, embedded_machine, q_kind='default_nothing', **options):
        self.derived = True

        # The call to the mother class __init__() method will set the
        # fields matching optional arguments which are so far :
        # self.q_kind, self.q_subkind
        # plus self.machine, self.options (modified)
        Q_Structure.__init__(self, embedded_machine,
                             q_kind, AVAILABLE_Q_KIND_VALUES,
                             **options)
        # The purpose of this next line is to get the possibly modified
        # value of **options
        options = self.options



        # Set the default values of the different options
        use_pythagorean_triples = False
        if ('use_pythagorean_triples' in options \
            and options['use_pythagorean_triples'] in YES) \
           or (self.q_kind == 'converse_of_pythagorean_theorem') :
        #___
            use_pythagorean_triples = True

        use_decimals = True
        if 'use_decimals' in options \
            and not options['use_decimals'] in YES:
        #___
            use_decimals = False

        self.round_to = ""

        if 'round_to' in options and options['round_to'] in PRECISION:
            self.round_to = options['round_to']

        if not use_pythagorean_triples:
            if self.round_to == "":
                if use_decimals:
                    self.round_to = HUNDREDTH
                else:
                    self.round_to = TENTH

        self.use_pythagorean_triples = use_pythagorean_triples

        self.figure_in_the_text = True

        if 'figure_in_the_text' in options \
            and not options['figure_in_the_text'] in YES:
        #___
            self.figure_in_the_text = False

        rotation_option = 'no'

        if 'rotate_around_barycenter' in options:
            rotation_option = options['rotate_around_barycenter']

        self.final_unit = ""

        if 'final_unit' in options \
            and options['final_unit'] in LENGTH_UNITS:
        #___
            self.final_unit = options['final_unit']

        sides_units = [self.final_unit,
                       self.final_unit,
                       self.final_unit]

        # Later, allow to use a different length unit for the sides
        # than the final expected unit ; allow different units for different
        # sides (for instance giving a list in option 'sides_units')...
        # So far we will do with only ONE unit
        #if 'sides_units' in options \
        #    and options['sides_units'] in LENGTH_UNITS:
        ##___
        #    sides_units = options['sides_units']

        self.right_triangle = None

        self.unknown_side = None
        self.known_sides = []


        # Now set some randomly values
        letters = [elt for elt in alphabet.UPPERCASE]

        vertices_names = (randomly.pop(letters),
                          randomly.pop(letters),
                          randomly.pop(letters))


        # Here you can begin to write code for the different
        # q_kinds & q_subkinds
        if self.q_kind == 'pythagorean_theorem':
            sides_values = [None, None, None]

            if use_pythagorean_triples:
                triples = pythagorean.ALL_TRIPLES_5_100

                if use_decimals:
                    triples = pythagorean.ALL_TRIPLES_5_100 \
                            + pythagorean.TRIPLES_101_200_WO_TEN_MULTIPLES

                sides_values = randomly.pop(triples)

                if use_decimals:
                    sides_values = [Decimal(str(Decimal(sides_values[0])/10)),
                                    Decimal(str(Decimal(sides_values[1])/10)),
                                    Decimal(str(Decimal(sides_values[2])/10))
                                   ]

                if self.q_subkind == 'calculate_hypotenuse':
                    sides_values[2] = ""
                    sides_units[2] = ""

                else:
                    # case : self.q_subkind == 'calculate_one_leg'
                    leg0_or_1 = randomly.pop([0, 1])
                    sides_values[leg0_or_1] = ""
                    sides_units[leg0_or_1] = ""

            else:
                # NO pythagorean triples.
                # The two generated values must NOT match any pythagorean
                # triple
                if use_decimals:
                    min_side_value = 5
                    max_side_value = 200
                else:
                    min_side_value = 5
                    max_side_value = 100

                if self.q_subkind == 'calculate_hypotenuse':
                    first_leg = randomly.integer(min_side_value,
                                                 max_side_value)

                    # we will take the leg values between
                    # at least 25% and at most 150% of the length of first leg
                    # (and smaller than max_side_value)
                    second_leg_values = []
                    for i in xrange(int(first_leg*1.5)):
                        if i+int(first_leg*0.25) <= 1.5*first_leg \
                            and i+int(first_leg*0.25) <= max_side_value:
                        #___
                            second_leg_values += [i+int(first_leg*0.25)]

                    second_leg_unauthorized_values = \
                        pythagorean.get_legs_matching_given_leg(first_leg)

                    second_leg_possible_values = utils.take_away(\
                                                second_leg_values,
                                                second_leg_unauthorized_values)

                    if randomly.heads_or_tails():
                        sides_values = [first_leg,
                                        randomly.pop(second_leg_possible_values),
                                        ""
                                        ]
                        sides_units[2] = ""

                    else:
                        sides_values = [randomly.pop(second_leg_possible_values),
                                        first_leg,
                                        ""
                                        ]
                        sides_units[2] = ""

                else:
                    # case : self.q_subkind == 'calculate_one_leg'

                    hypotenuse = randomly.integer(min_side_value,
                                                  max_side_value)

                    # we will take the leg values between
                    # at least 25% and at most 90% of the length of hypotenuse
                    # to avoid "weird" cases (with a very subtle difference
                    # between the given values and the one to calculate)
                    leg_values = []
                    for i in xrange(int(hypotenuse*0.9)):
                        if i+int(hypotenuse*0.25) <= 0.9*hypotenuse:
                            leg_values += [i+int(hypotenuse*0.25)]

                    leg_unauthorized_values = \
                        pythagorean.get_legs_matching_given_hypotenuse(\
                                                                     hypotenuse)

                    leg_possible_values = utils.take_away(leg_values,
                                                        leg_unauthorized_values)

                    if randomly.heads_or_tails():
                        sides_values = ["",
                                        randomly.pop(leg_possible_values),
                                        hypotenuse
                                        ]
                        sides_units[0] = ""

                    else:
                        sides_values = [randomly.pop(leg_possible_values),
                                        "",
                                        hypotenuse
                                        ]
                        sides_units[1] = ""

            self.right_triangle = \
                RightTriangle((vertices_names,
                               'sketch'
                              ),
                               rotate_around_isobarycenter=rotation_option
                              )

            self.right_triangle.leg0.set_label(Value(sides_values[0],
                                                     unit=sides_units[0])
                                              )
            self.right_triangle.leg1.set_label(Value(sides_values[1],
                                                     unit=sides_units[1])
                                              )
            self.right_triangle.hypotenuse.set_label(Value(sides_values[2],
                                                           unit=sides_units[2])
                                                    )

            for side in self.right_triangle.sides:
                if side.label.value == "":
                    self.unknown_side = side.deep_copy()
                else:
                    self.known_sides += [side.deep_copy()]



        elif self.q_kind == 'converse_of_pythagorean_theorem' \
             or self.q_kind == 'contrapositive_of_pythagorean_theorem':
        #___
            sides_values = [None, None, None]
            triples = pythagorean.ALL_TRIPLES_5_100

            if use_decimals:
                triples = pythagorean.ALL_TRIPLES_5_100 \
                        + pythagorean.TRIPLES_101_200_WO_TEN_MULTIPLES

            sides_values = randomly.pop(triples)

            if self.q_kind == 'contrapositive_of_pythagorean_theorem':
                # We'll change exactly one value to be sure the triplet
                # is NOT pythagorean
                if randomly.heads_or_tails():
                    # We will decrease the lowest value
                    max_delta = int(0.1 * sides_values[0])
                    min_delta = 1
                    if min_delta > max_delta:
                        max_delta = min_delta
                    chosen_delta = randomly.pop(\
                        [i+min_delta for i in xrange(max_delta-min_delta+1)])

                    sides_values = [sides_values[0]-chosen_delta,
                                    sides_values[1],
                                    sides_values[2]
                                   ]

                else:
                    # We will increase the highest value
                    max_delta = int(0.1 * sides_values[2])
                    min_delta = 1
                    if min_delta > max_delta:
                        max_delta = min_delta
                    chosen_delta = randomly.pop(\
                        [i+min_delta for i in xrange(max_delta-min_delta+1)])

                    sides_values = [sides_values[0],
                                    sides_values[1],
                                    sides_values[2]+chosen_delta
                                   ]

            if use_decimals:
                sides_values = [Decimal(str(Decimal(sides_values[0])/10)),
                                Decimal(str(Decimal(sides_values[1])/10)),
                                Decimal(str(Decimal(sides_values[2])/10))
                               ]


            self.right_triangle = \
                RightTriangle((vertices_names,
                               'sketch'
                              ),
                               rotate_around_isobarycenter=rotation_option
                             )

            self.right_triangle.leg0.set_label(Value(sides_values[0],
                                                     unit=sides_units[0])
                                              )
            self.right_triangle.leg1.set_label(Value(sides_values[1],
                                                     unit=sides_units[1])
                                              )
            self.right_triangle.hypotenuse.set_label(Value(sides_values[2],
                                                           unit=sides_units[2])
                                                    )

            self.right_triangle.right_angle.set_mark("")













    # --------------------------------- TEXT OF THE QUESTION --> STR ----------
    ##
    #   @brief Returns the text of the question as a str
    def text_to_str(self):
        M = self.machine
        result = self.displayable_number

        if self.q_kind == 'pythagorean_theorem':
            if self.figure_in_the_text:
                result += M.insert_picture(self.right_triangle)

            else:
                result += _("The triangle %(triangle_name)s has a right \
                angle in %(right_vertex)s.") \
                       % {'triangle_name' : str(self.right_triangle.name),
                          'right_vertex' : str(self.right_triangle.vertex1.name)
                         }
                result += " " + str(self.known_sides[0].length_name) \
                       + " = " \
                       + self.known_sides[0].label.into_str(display_unit='yes')\
                       + ". " \
                       + str(self.known_sides[1].length_name) \
                       + " = " \
                       + self.known_sides[1].label.into_str(display_unit='yes')\
                       + ". " + M.write_new_line()

            result += _("Calculate the length of") \
                   + " " \
                   + self.unknown_side.name \
                   + "."

            if self.final_unit != "":
                result += " " + _("Give the result in") + " " \
                       + self.final_unit + "."

            if self.round_to != "":
                result += " " + _("Round the result") + " " \
                       + vocabulary.PRECISION_IDIOMS[self.round_to] + "."

        elif self.q_kind == 'converse_of_pythagorean_theorem' \
             or self.q_kind == 'contrapositive_of_pythagorean_theorem':
        #___
            if self.figure_in_the_text:
                result += M.insert_picture(self.right_triangle)

            else:
                sides_copy = [self.right_triangle.sides[0].deep_copy(),
                              self.right_triangle.sides[1].deep_copy(),
                              self.right_triangle.sides[2].deep_copy()
                             ]
                side0 = randomly.pop(sides_copy)
                side1 = randomly.pop(sides_copy)
                side2 = randomly.pop(sides_copy)

                result += _("%(triangle_name)s is a triangle such as")\
                          %{'triangle_name' : str(self.right_triangle.name)
                           }

                result += " " + str(side0.length_name)
                result += " = "
                result += side0.label.into_str(display_unit=True) + ", "

                result += str(side1.length_name)
                result += " = "
                result += side1.label.into_str(display_unit=True)
                result += " "
                result += _("and")
                result += " "

                result += str(side2.length_name)
                result += " = "
                result += side2.label.into_str(display_unit=True) + "."
                result += " "


            result += _("Is it a right triangle ? Prove your answer and if the \
            triangle is right, give the name of the right angle.")

            result += M.write_new_line()


        return result + M.write_new_line()






    # ------------------------------- ANSWER OF THE QUESTION --> STR ----------
    ##
    #   @brief Returns the answer of the question as a str
    def answer_to_str(self):
        M = self.machine

        if self.q_kind == 'pythagorean_theorem':
            # Resolution (and the part with the figure will be dealed later)
            result = _("The triangle %(triangle_name)s has a right angle in \
                       %(right_vertex)s.") \
                    % {'triangle_name' : str(self.right_triangle.name),
                       'right_vertex' : str(self.right_triangle.vertex1.name)
                      }

            result += M.write_new_line()

            result += _("Then by Pythagoras theorem") + " :"

            pyth_eq = self.right_triangle.pythagorean_substequality()

            result += M.write_math_style1(pyth_eq.into_str())

            if self.use_pythagorean_triples:
                result += M.write(Equation(pyth_eq.substitute()).\
                                        auto_resolution( \
                                            dont_display_equations_name=True,
                                            pythagorean_mode='yes',
                                            unit=self.final_unit,
                                            underline_result='yes')
                                 )


            else:
                result += M.write(Equation(pyth_eq.substitute()).\
                                        auto_resolution( \
                                            dont_display_equations_name=True,
                                            decimal_result=self.round_to,
                                            pythagorean_mode='yes',
                                            unit=self.final_unit,
                                            underline_result='yes')
                                  )



            if self.figure_in_the_text:
                return self.displayable_number + result
            else:
                content = [self.displayable_number \
                           + _("Sketch") + " :" \
                           + M.write_new_line() \
                           + M.insert_picture(self.right_triangle),
                           result]
                return M.write_layout((1, 2), [9, 9], content)


        elif self.q_kind == 'converse_of_pythagorean_theorem' \
             or self.q_kind == 'contrapositive_of_pythagorean_theorem':
        #___
            hyp_equality = Equality([Item(('+',
                                          self.right_triangle.\
                                               hypotenuse.length_name,
                                          2)),
                                     Item(('+',
                                          self.right_triangle.\
                                               hypotenuse.label.value,
                                          2))
                                    ])
            hyp_equality_step2 = Equality([Item(('+',
                                          self.right_triangle.\
                                               hypotenuse.length_name,
                                          2)),
                                     Item(Item(('+',
                                          self.right_triangle.\
                                               hypotenuse.label.value,
                                          2)).evaluate()
                                          )
                                    ])

            legs_equality = Equality([Sum([Item(('+',
                                           self.right_triangle.leg0.length_name,
                                           2)),
                                           Item(('+',
                                           self.right_triangle.leg1.length_name,
                                           2))
                                         ]),
                                      Sum([Item(('+',
                                           self.right_triangle.leg0.label.value,
                                           2)),
                                           Item(('+',
                                           self.right_triangle.leg1.label.value,
                                           2))
                                         ])
                                     ])
            legs_equality_step2 = Equality([\
                                  Sum([Item(('+',
                                       self.right_triangle.leg0.length_name,
                                       2)),
                                       Item(('+',
                                       self.right_triangle.leg1.length_name,
                                       2))
                                      ]),
                                  Item(Sum([Item(('+',
                                       self.right_triangle.leg0.label.value,
                                       2)),
                                       Item(('+',
                                       self.right_triangle.leg1.label.value,
                                       2))
                                          ]).evaluate()
                                       )
                                           ])


            result = _("On one hand:") + M.write_new_line()
            result += M.write_math_style1(hyp_equality.into_str())
            result += M.write_math_style1(hyp_equality_step2.into_str())

            result += _("On the other hand:") + M.write_new_line()
            result += M.write_math_style1(legs_equality.into_str())
            result += M.write_math_style1(legs_equality_step2.into_str())

            result += _("Hence:")

            if self.q_kind == 'converse_of_pythagorean_theorem':
                result += M.write_math_style1(\
                        self.right_triangle.pythagorean_equality().into_str())
                result += _("So, by the converse of the pythagorean theorem,")
                #result += M.write_new_line()
                result += " "
                result += _("%(triangle_name)s has a right angle\
                 in %(right_vertex)s.")\
                     % {'triangle_name' : str(self.right_triangle.name),
                        'right_vertex' : str(self.right_triangle.vertex1.name)
                       }

            elif self.q_kind == 'contrapositive_of_pythagorean_theorem':
                result += M.write_math_style1(\
                        self.right_triangle.pythagorean_equality(\
                        equal_signs=['neq']).into_str())

                result += _("So, by the contrapositive of the pythagorean\
                 theorem,")
                #result += M.write_new_line()
                result += " "
                result += _("%(triangle_name)s has no right angle.")\
                     % {'triangle_name' : str(self.right_triangle.name)
                       }



            if self.figure_in_the_text:
                return self.displayable_number + result
            else:
                content = [self.displayable_number \
                           + _("Sketch") + " :" \
                           + M.write_new_line() \
                           + M.insert_picture(self.right_triangle),
                           result]
                return M.write_layout((1, 2), [6, 12], content)






