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

from mathmakerlib.calculus import Number, Unit, physical_quantity

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import post_process
from mathmaker.lib.tools.wording import setup_wording_format_of


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup('minimal', **options)
        super().setup('numbers', nb=build_data, shuffle_nbs=False,
                      **options)
        source_id = options.get('nb_source')
        if source_id == r'10%of...':
            self.transduration = 12
        elif source_id in [r'25%of...', r'50%of...'] and self.nb2 < 40:
            self.transduration = 16
        else:
            self.transduration = 20
        if self.nb_variant.startswith('decimal'):
            deci_nb = int(self.nb_variant[-1])
            self.nb2 = self.nb2 / Number(10) ** Number(deci_nb)

        self.result = self.nb1 * self.nb2 / Number(100)
        self.n1 = self.nb1.printed
        hint = ''
        if self.context == 'simple_unit':
            u = shared.unitspairs_source.next(direction='left', level=1)[0]
            pq = physical_quantity(u)
            self.n2 = Number(self.nb2, unit=Unit(u)).printed
            hint = ' |hint:{}_unit|'.format(pq)
            setattr(self, pq + '_unit', u)
            self.result = Number(self.result, unit=u)
        else:
            self.n2 = self.nb2.printed
        # This default wording is meant for mental calculation.
        self.wording = options.get('wording',
                                   _('{n1} {percent_symbol} of {n2}?')
                                   + hint)
        setup_wording_format_of(self)

    def q(self, **options):
        return post_process(self.wording.format(**self.wording_format))

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.result.printed

    def js_a(self, **kwargs):
        return [Number(self.result, unit=None).uiprinted]
