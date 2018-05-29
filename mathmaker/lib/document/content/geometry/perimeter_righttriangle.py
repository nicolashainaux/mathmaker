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

from decimal import Decimal

from mathmakerlib.calculus import Number

from mathmaker.lib import shared
# from mathmaker.lib.core.base_calculus import *
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import setup_wording_format_of


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        super().setup("numbers", nb=build_data, **options)
        super().setup("nb_variants", nb=build_data, **options)
        super().setup("length_units", **options)
        hypotenuse_length = \
            Number(Number(build_data[0]) * Number(build_data[0])
                   + Number(build_data[1]) * Number(build_data[1]))\
            .sqrt().rounded(Decimal('0.1'))
        super().setup("polygon",
                      polygon_data=(3, 'triangle', 'right_triangle',
                                    'triangle_1_1_1', 'all_different', 2, 1,
                                    0, 0, 0, 0, 0, build_data[0],
                                    build_data[1], hypotenuse_length),
                      wlines_nb=1)
        self.transduration = 18

        if self.slideshow:
            self.polygon.scale = 2
            self.wording = _('Perimeter?')
            self.part2_wording = r'{\small' + _('(Length unit: {})')\
                .format(self.length_unit) + '}'
        else:
            self.wording = _('Perimeter of this triangle? '
                             '|hint:length_unit|')
            self.part2_wording = r'{\small' + _('(Lengths in {})')\
                .format(self.length_unit) + '}'
        setup_wording_format_of(self)

    def q(self, **options):
        if self.slideshow:
            return r'{}\par {} \par {}'\
                .format(self.wording.format(**self.wording_format),
                        self.polygon.drawn,
                        self.part2_wording)
        else:
            return shared.machine.write_layout(
                (1, 2), [3, 10],
                [self.polygon.drawn,
                 r'{} {}'
                 .format(self.wording.format(**self.wording_format),
                         self.part2_wording)])

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return Number(self.polygon.lbl_perimeter,
                      unit=self.unit_length).printed

    def js_a(self, **kwargs):
        return [Number(self.polygon.lbl_perimeter, unit=None).uiprinted]
