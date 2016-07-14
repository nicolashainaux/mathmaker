# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
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

import random
import copy

from mathmaker.lib.core.root_calculus import Unit, Value
from mathmaker.lib.core.base_calculus import Product, Quotient, Item
from mathmaker.lib.core.base_geometry import Point
from mathmaker.lib.core.geometry import Rectangle, Square
from mathmaker.lib import error
from mathmaker.lib import shared
from mathmaker.lib.common.cst import COMMON_LENGTH_UNITS
from mathmaker.lib.tools.wording import setup_wording_format_of


class structure(object):

    def h(self, **options):
        if hasattr(self, 'hint'):
            return "\hfill" + Value("", unit=self.hint)\
                .into_str(display_SI_unit=True)
        else:
            return ""

    def setup(self, arg, shuffle_nbs=True, **options):
        if arg == "minimal":
            if 'variant' in options and options['variant'] == 'decimal':
                options['variant'] = random.choice(['decimal1', 'decimal2'])

            self.variant = options.get('variant', "default")
            self.context = options.get('context', "default")
            pic = options.get('picture', "false")
            self.picture = True if pic == "true" else False

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

        elif arg == "numbers":
            nb_list = list(options['nb'])
            if shuffle_nbs:
                random.shuffle(nb_list)
            for i in range(len(nb_list)):
                setattr(self, 'nb' + str(i + 1), nb_list[i])
            self.nb_nb = len(nb_list)

        elif arg == "nb_variants":
            if self.variant.startswith('decimal'):
                deci_nb = int(self.variant[-1])  # so, from decimal1 up to 9
                chosen_ones = random.sample([i for i in range(self.nb_nb)],
                                            deci_nb)
                for i in chosen_ones:
                    setattr(self, 'nb' + str(i + 1),
                            getattr(self, 'nb' + str(i + 1)) / 10)

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

            self.dividend_str = Item(self.dividend).printed
            self.divisor_str = Item(self.divisor).printed
            self.result_str = Item(self.result).printed
            q = Quotient(('+', self.dividend, self.divisor),
                         use_divide_symbol=True)
            self.quotient_str = q.printed

        elif arg == "rectangle":
            if hasattr(self, 'nb1') and hasattr(self, 'nb2'):
                nb1, nb2 = self.nb1, self.nb2
            elif 'nb' in options:
                nb1, nb2 = options['nb'][0], options['nb'][1]
            else:
                raise error.ImpossibleAction("Setup a rectangle if no width "
                                             "nor length have been provided"
                                             " yet.")
            if (not hasattr(self, 'unit_length')
                or not hasattr(self, 'unit_area')):
                self.setup(self, "units", **options)

            # nb1 = Decimal(str(nb1))
            # nb2 = Decimal(str(nb2))

            w = Value(min([nb1, nb2]), unit=self.unit_length)
            l = Value(max([nb1, nb2]), unit=self.unit_length)

            rectangle_name = "DCBA"
            if self.picture:
                rectangle_name = next(shared.four_letters_words_source)
            self.rectangle = Rectangle([Point([rectangle_name[3], (0, 0)]),
                                        3,
                                        1.5,
                                        rectangle_name[2],
                                        rectangle_name[1],
                                        rectangle_name[0]],
                                       read_name_clockwise=True)
            self.rectangle.set_lengths([l, w])
            self.rectangle.setup_labels([False, False, True, True])

        elif arg == "square":
            if hasattr(self, 'nb1'):
                nb1 = self.nb1
            elif 'nb' in options:
                nb1 = options['nb'][0]
            else:
                raise error.ImpossibleAction("Setup a square if no side's "
                                             "length have been provided "
                                             "yet.")
            if (not hasattr(self, 'unit_length')
                or not hasattr(self, 'unit_area')):
                # __
                self.setup(self, "units", **options)

            square_name = "DCBA"
            if self.picture:
                square_name = next(shared.four_letters_words_source)
            self.square = Square([Point([square_name[3], (0, 0)]),
                                 2,
                                 square_name[2],
                                 square_name[1],
                                 square_name[0]],
                                 read_name_clockwise=True)
            self.square.set_lengths([Value(nb1, unit=self.unit_length)])
            self.square.setup_labels([False, False, True, False])
            self.square.set_marks(random.choice(["simple", "double",
                                                 "triple"]))

        elif arg == 'mini_problem_wording':
            self.wording = _(shared.mini_problems_wordings_source
                             .next(q_id=options['q_id'],
                                   nb1_to_check=self.nb1,
                                   nb2_to_check=self.nb2))
            setup_wording_format_of(self)
