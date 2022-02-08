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
from mathmakerlib.calculus import Number, Unit, physical_quantity

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import setup_wording_format_of, post_process


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        """
        :param build_data: data used to build the question, in the form of a
        triple of numbers (a, b, c). a is a single int; b/c is a fraction.
        Question will be "How much is b/c of Q?" where Q = a × c.
        :type build_data: tuple
        """
        super().setup("minimal", **options)
        super().setup("numbers", nb=build_data, shuffle_nbs=False, **options)
        self.transduration = 30

        self.quantity = self.nb1 * self.nb3
        self.fraction = Fraction(self.nb2, self.nb3).printed
        self.answer = self.nb1 * self.nb2
        hint = ''

        if self.context == 'simple_unit':
            u = shared.unitspairs_source.next(direction='left', level=1)[0]
            self.pq = physical_quantity(u)
            hint = ' |hint:{}_unit|'.format(self.pq)
            setattr(self, self.pq + '_unit', u)
            self.quantity = Number(self.quantity, unit=Unit(u))

        self.quantity = self.quantity.printed
        self.fraction = shared.machine.write_math_style2(self.fraction)

        # This default wording is meant for mental calculation.
        self.wording = _('{fraction} of {quantity}?') + hint
        setup_wording_format_of(self)

    def q(self, **options):
        return post_process(self.wording.format(**self.wording_format))

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        u = getattr(self, self.pq + '_unit')
        return Number(self.answer, unit=u).printed

    def js_a(self, **kwargs):
        return [Number(self.answer, unit=None).uiprinted]
