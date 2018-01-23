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

import random

from mathmakerlib.calculus import Number

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import setup_wording_format_of


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        super().setup("length_units", **options)
        self.transduration = 16
        if self.picture:
            self.transduration = 12

        if self.context == "from_area":
            super().setup("division", nb=build_data, **options)
            self.nb1, self.nb2, self.nb3 = (self.result, self.divisor,
                                            self.dividend)
            super().setup("rectangle", **options)
            wordings = {'w': _("A rectangle has an area of {nb3} {area_unit} "
                               "and a length of {nb2} {length_unit}. What is "
                               "its width? |hint:length_unit|"),
                        'l': _("A rectangle has an area of {nb3} {area_unit} "
                               "and a width of {nb2} {length_unit}. What is "
                               "its length? |hint:length_unit|")
                        }
            self.wording = wordings[self.subcontext]
            setup_wording_format_of(self)

        elif self.context == "from_perimeter":
            super().setup("numbers", nb=build_data, **options)
            super().setup("nb_variants", nb=build_data, **options)
            super().setup("rectangle", **options)
            self.subcontext = random.choice(['w', 'l'])
            self.nb1 = self.rectangle.lbl_perimeter
            if self.subcontext == 'l':
                self.nb2, self.nb3 = (self.rectangle.lbl_width,
                                      self.rectangle.lbl_width)
            else:
                self.nb2, self.nb3 = (self.rectangle.lbl_length,
                                      self.rectangle.lbl_width)
            self.result = self.nb3
            wordings = {'w': _("What is the width of a rectangle whose "
                               "perimeter is {nb1} {length_unit} and length "
                               "is {nb2} {length_unit}? |hint:length_unit|"),
                        'l': _("What is the length of a rectangle whose "
                               "perimeter is {nb1} {length_unit} and width "
                               "is {nb2} {length_unit}? |hint:length_unit|")
                        }
            self.wording = wordings[self.subcontext]
            setup_wording_format_of(self)

        else:
            raise RuntimeError('Impossible to create this question without '
                               'any context.')

        if self.subcontext == 'w':
            self.rectangle.setup_labels(labels=[self.rectangle.lbl_width,
                                                self.rectangle.lbl_length],
                                        masks=[' ', ' ', None, '?'])
        elif self.subcontext == 'l':
            self.rectangle.setup_labels(labels=[self.rectangle.lbl_width,
                                                self.rectangle.lbl_length],
                                        masks=[' ', ' ', '?', None])

    def q(self, **options):
        if self.picture:
            if self.slideshow:
                return '{}\n{}'\
                    .format(self.rectangle.drawn,
                            self.wording.format(**self.wording_format))
            else:
                return shared.machine.write_layout(
                    (1, 2), [3.5, 9.5],
                    [self.rectangle.drawn,
                     self.wording.format(**self.wording_format)])
        else:
            return self.wording.format(**self.wording_format)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return Number(self.result, unit=self.hint).printed

    def js_a(self, **kwargs):
        return [Number(self.result).uiprinted]
