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


from mathmaker.lib.constants.numeration import DIGITSPLACES_HOW_MANY
from mathmaker.lib.core.base_calculus import Item
from mathmaker.lib.document.content import component
from . import digitplace_reversed


class sub_object(component.structure):

    def __init__(self, **options):
        digitplace_reversed.sub_object.__init__(self, numberof=True, **options)
        self.transduration = 12
        n = self.chosen_deci
        r = self.chosen_digitplace
        self.result = Item(((n - n % r) / r))

    def q(self, **options):
        return _('{how_many_digitplace} are there in {decimal_number}?')\
            .format(decimal_number=self.chosen_deci_str,
                    how_many_digitplace=_(str(
                        DIGITSPLACES_HOW_MANY[self.chosen_digitplace])))

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.result.printed

    def js_a(self, **kwargs):
        return [self.result.jsprinted]
