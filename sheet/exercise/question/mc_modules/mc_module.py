# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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
import copy
from decimal import Decimal

from core.root_calculus import Unit, Value
from core.base_calculus import Product, Quotient, Item
from core.base_geometry import Point
from core.geometry import Rectangle
from lib import error
from lib.common import shared
from lib.common.cst import COMMON_LENGTH_UNITS
from lib.common.wordings import mini_problems_wordings
from lib.wordings_handling_tools import setup_wording_format_of

class structure(object):

    def h(self, M, **options):
        if hasattr(self, 'hint'):
            return "..............." + M.insert_nonbreaking_space() \
                    + self.hint
        else:
            return ""

    def setup(self, M, arg, **options):
        if arg == "minimal":
            if 'variant' in options and options['variant'] == 'decimal':
                    options['variant'] = random.choice(['decimal1',
                                                        'decimal2'])

            self.variant = options['variant'] if 'variant' in options \
                                              else "default"
            self.context = options['context'] if 'context' in options \
                                              else "default"
            self.picture = True if 'picture' in options \
                                   and options['picture'] == "true" \
                                else False

        elif arg == "length_units":
            if 'unit' in options:
                self.unit_length = Unit(options['unit'])
                self.unit_area = Unit(self.unit_length.name, exponent=2)
                self.length_unit = self.unit_length.name
            else:
                if hasattr(self, 'length_unit'):
                    self.unit_length = Unit(self.length_unit)
                    self.unit_area = Unit(self.unit_length.name, exponent=2)
                elif hasattr(self, 'unit_length'):
                    self.length_unit = self.unit_length.name
                    self.unit_area = Unit(self.unit_length.name, exponent=2)
                else:
                    length_units_names = copy.deepcopy(COMMON_LENGTH_UNITS)
                    self.unit_length = Unit(random.choice(length_units_names))
                    self.unit_area = Unit(self.unit_length.name, exponent=2)
                    self.length_unit = self.unit_length.name

        elif arg == "nb_variants":
            nb_list = list(options['nb'])
            nb1 = nb_list.pop(random.choice([0, 1]))
            nb2 = nb_list.pop()
            if self.variant == 'decimal1':
                nb1 /= 10
            elif self.variant == 'decimal2':
                nb1 /= 10
                nb2 /= 10
            nb_list = [nb1, nb2]
            self.nb1 = nb_list.pop(random.choice([0, 1]))
            self.nb2 = nb_list.pop()

        elif arg == "division":
            nb_list = list(options['nb'])
            self.divisor = self.result = self.dividend = 0
            self.result_str = self.quotient_str = ""

            if '10_100_1000' in options and options['10_100_1000']:
                self.divisor, self.dividend = nb_list[0], nb_list[1]
                self.result = Quotient(('+', self.dividend, self.divisor))\
                              .evaluate()
            else:
                self.divisor = nb_list.pop(random.choice([0, 1]))
                self.result = nb_list.pop()
                if self.variant[:-1] == 'decimal':
                    self.result /= 10
                self.dividend = Product([self.divisor, self.result]).evaluate()

            if self.context == "from_area":
                self.subcontext = "w" if self.result < self.divisor else "l"

            self.dividend_str = Item(self.dividend)\
                                .into_str(force_expression_begins=True)
            self.divisor_str = Item(self.divisor)\
                               .into_str(force_expression_begins=True)
            self.result_str = Item(self.result)\
                              .into_str(force_expression_begins=True)
            q = Quotient(('+', self.dividend, self.divisor),
                         use_divide_symbol=True)
            self.quotient_str = q.into_str(force_expression_begins=True)

        elif arg == "rectangle":
            if hasattr(self, 'nb1') and hasattr(self, 'nb2'):
                nb1, nb2 = self.nb1, self.nb2
            elif 'nb' in options:
                nb1, nb2 = options['nb'][0], options['nb'][1]
            else:
                raise error.ImpossibleAction("Setup a rectangle if no width " \
                                             + "nor length have been provided"\
                                             + " yet.")
            if not hasattr(self, 'unit_length') \
            or not hasattr(self, 'unit_area'):
                self.setup(self, "units", **options)

            #nb1 = Decimal(str(nb1))
            #nb2 = Decimal(str(nb2))

            w = Value(min([nb1, nb2]), unit=self.unit_length)
            l = Value(max([nb1, nb2]), unit=self.unit_length)

            rectangle_name = next(shared.four_letters_words_source)
            self.rectangle = Rectangle([Point([rectangle_name[3], (0,0)]),
                                        3,
                                        1.5,
                                        rectangle_name[2],
                                        rectangle_name[1],
                                        rectangle_name[0]],
                                        read_name_clockwise=True)
            self.rectangle.set_lengths([l, w])
            self.rectangle.setup_labels([False, False, True, True])

        elif arg == 'mini_problem_wording':
            d = {"addi": 0, "substr": 1, "multi": 2, "divi": 3}
            if not mini_problems_wordings.initialized:
                mini_problems_wordings.init()
            self.wording = mini_problems_wordings.mini_problems_wordings_source\
                           .next(choice=d[options['mini_pb_type']])
            setup_wording_format_of(self, M)