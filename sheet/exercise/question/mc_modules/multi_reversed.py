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

from lib import shared
from core.root_calculus import Value
from core.base_calculus import Product


class sub_object(object):

    def __init__(self, numbers_to_use, **options):
        nb_list = list(numbers_to_use)
        self.nb1, self.nb2 = random.sample(nb_list, 2)
        self.product = Product([self.nb1, self.nb2]).evaluate()

    def q(self, **options):
        return _("In the multiplication tables (from 2 to 9), "\
                +"which product is equal to:") + " "\
               + Value(self.product).into_str() \
               + " ?"

    def a(self, **options):
        if self.product == 12:
            return shared.machine.write_math_style2(Product([2, 6]).into_str(\
                                                force_expression_begins=True
                                                                 )
                                  ) \
                  + " " + _("or") + " " \
                  + shared.machine.write_math_style2(Product([3, 4]).into_str(\
                                                force_expression_begins=True
                                                                 )
                                        )

        elif self.product == 16:
            return shared.machine.write_math_style2(Product([2, 8]).into_str(\
                                                force_expression_begins=True
                                                                 )
                                  ) \
                   + " " + _("or") + " " \
                  + shared.machine.write_math_style2(Product([4, 4]).into_str(\
                                                force_expression_begins=True
                                                                 )
                                        )

        elif self.product == 18:
            return shared.machine.write_math_style2(Product([2, 9]).into_str(\
                                                force_expression_begins=True
                                                                 )
                                  ) \
                   + " " + _("or") + " " \
                  + shared.machine.write_math_style2(Product([3, 6]).into_str(\
                                                force_expression_begins=True
                                                                 )
                                        )

        elif self.product == 24:
            return shared.machine.write_math_style2(Product([4, 6]).into_str(\
                                                force_expression_begins=True
                                                                 )
                                  ) \
                   + " " + _("or") + " " \
                  + shared.machine.write_math_style2(Product([3, 8]).into_str(\
                                                force_expression_begins=True
                                                                 )
                                        )

        elif self.product == 36:
            return shared.machine.write_math_style2(Product([6, 6]).into_str(\
                                                force_expression_begins=True
                                                                 )
                                  ) \
                   + " " + _("or") + " " \
                  + shared.machine.write_math_style2(Product([4, 9]).into_str(\
                                                force_expression_begins=True
                                                                 )
                                        )

        else:
            return shared.machine.write_math_style2(Product([self.nb1,
                                                self.nb2]).into_str(\
                                                force_expression_begins=True
                                                                 )

                                      )
