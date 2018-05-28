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

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import setup_wording_format_of


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup('minimal', **options)
        super().setup('numbers', nb=build_data, **options)
        super().setup('length_units', **options)

        direction = options.get('direction', shared.directions_source.next())
        if 'variant' in options:
            variant = int(options['variant'])
        else:
            faces_nb, variant = shared.rightcuboids_source.next()

        # We know the wording will be in two lines:
        super().setup('rightcuboid', variant=variant, labels=self.nb_list,
                      direction=direction)

        self.wording = _(r'Volume of this right cuboid?\newline '
                         r'(length unit: {length_unit}) |hint:volume_unit|')

        self.transduration = 21

        setup_wording_format_of(self)
        self.wording = self.wording.format(**self.wording_format)

    def q(self, **options):
        if self.slideshow:
            return '{}{}{}'.format(self.wording,
                                   shared.machine.addvspace(height='10pt'),
                                   self.drawn_solid)
        else:
            return shared.machine.write_layout(
                (1, 2), [5, 8], [self.drawn_solid, self.wording])

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.solid.lbl_volume.printed

    def js_a(self, **kwargs):
        return [self.solid.lbl_volume.uiprinted]
