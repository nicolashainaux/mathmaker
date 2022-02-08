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

from mathmakerlib.calculus import Fraction

from mathmaker.lib import shared
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        """
        :param build_data: data used to build the question, in the form of a
        triple of numbers (a, b, c). Question will be "Simplify N / P"
        where N = a × b and P = a × c. Note: b and c must not be coprimes.
        :type build_data: tuple
        """
        super().setup("minimal", **options)
        super().setup("numbers", nb=build_data, shuffle_nbs=False, **options)
        # super().setup("nb_variants", nb=build_data, **options)
        self.transduration = 30

        self.fraction = Fraction(self.nb1 * self.nb2, self.nb1 * self.nb3)
        self.answer = self.fraction.reduced()

    def q(self, **options):
        return _('Reduce: {fraction}').format(
            fraction=shared.machine.write_math_style2(self.fraction.printed))

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return shared.machine.write_math_style2(self.answer.printed)

    def js_a(self, **kwargs):
        return [self.answer.uiprinted]
