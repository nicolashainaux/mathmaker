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
        super().setup("rectangle", **options)
        self.transduration = 8

        if self.picture:
            self.wording = _("Area of this rectangle? |hint:area_unit|")
            setup_wording_format_of(self)
        else:
            self.transduration = 12
            self.nb1, self.nb2 = \
                self.rectangle.lbl_width, self.rectangle.lbl_length
            self.wording = _("Area of a rectangle whose width is {nb1} \
{length_unit} and length is {nb2} {length_unit}? |hint:area_unit|")
            setup_wording_format_of(self)

    def q(self, **options):
        if self.picture:
            if self.slideshow:
                return '{}\n{}'\
                    .format(self.rectangle.drawn,
                            self.wording.format(**self.wording_format))
            else:
                return shared.machine.write_layout(
                    (1, 2), [5, 8],
                    [self.rectangle.drawn,
                     self.wording.format(**self.wording_format)])
        else:
            return self.wording.format(**self.wording_format)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.rectangle.lbl_area.printed

    def js_a(self, **kwargs):
        return [Number(self.rectangle.lbl_area, unit=None).uiprinted]
