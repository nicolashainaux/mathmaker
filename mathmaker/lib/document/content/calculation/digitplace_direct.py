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

# This module will ask to tell the place of a digit in a given number.

from mathmaker.lib.constants.numeration import DIGITSPLACES_WORDS
from . import digitplace_reversed
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, **options):
        digitplace_reversed.sub_object.__init__(self, **options)
        self.transduration = 16

    def q(self, **options):
        if self.preset == 'mental calculation':
            result = _('Position of the digit {figure}'
                       ' in: {decimal_number}?')
        else:
            result = _('What is the position of the figure {figure}'
                       ' in the number {decimal_number}?')
        return result.format(decimal_number=self.chosen_deci_str,
                             figure=self.chosen_figure)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return _(str(DIGITSPLACES_WORDS[self.chosen_digitplace]))

    def js_a(self, **kwargs):
        return [self.a(**kwargs)]
