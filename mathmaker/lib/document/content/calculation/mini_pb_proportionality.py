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
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import post_process


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        self.coeff = Number(str(build_data[0]))
        nb1 = Number(build_data[1]).rounded(Number('0.01'))
        nb2 = Number(build_data[2]).rounded(Number('0.01'))
        try:
            nb3 = Number(build_data[3]).rounded(Number('0.01'))
            solution = Number(build_data[4]).rounded(Number('0.01'))
        except IndexError:
            nb3 = self.coeff * nb1
            solution = self.coeff * nb2
        super().setup("numbers",
                      nb=[nb1, nb2, nb3, solution],
                      shuffle_nbs=False,
                      **options)
        self.transduration = 24
        super().setup('mini_problem_wording', proportionality=True, **options)

    def q(self, **options):
        return post_process(self.wording.format(**self.wording_format))

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        u = self.hint if hasattr(self, 'hint') else None
        return Number(Number(self.solution), unit=u).printed

    def js_a(self, **kwargs):
        return [Number(self.solution).uiprinted]
