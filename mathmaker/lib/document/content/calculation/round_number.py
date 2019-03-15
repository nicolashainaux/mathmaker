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

from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        WORDINGS = {Number(10): _('Round {nb1} to the nearest ten.'),
                    Number(1): _('Round {nb1} to the nearest unit.'),
                    Number(0.1): _('Round {nb1} to the nearest tenth.'),
                    Number(0.01): _('Round {nb1} to the nearest hundredth.'),
                    Number(0.001): _('Round {nb1} to the nearest thousandth.')}
        super().setup("minimal", **options)
        self.transduration = 24
        self.place = Number(build_data[0])
        self.nb1 = Number(build_data[1])
        if self.place < Number(0.01):
            self.nb1 += Number(random.randint(1, 9)) / Number(10000)
        if self.place > Number(0.01):
            self.nb1 += Number(random.randint(1, 9))
        if self.place >= Number(1):
            self.nb1 += Number(random.randint(1, 9) * 10)

        self.wording = WORDINGS[self.place]
        self.wording = self.wording.format(nb1=self.nb1.printed)

    def q(self, **options):
        return self.wording

    def a(self, **options):
        return self.nb1.rounded(self.place).printed

    def js_a(self, **kwargs):
        return [self.nb1.rounded(self.place).uiprinted]
