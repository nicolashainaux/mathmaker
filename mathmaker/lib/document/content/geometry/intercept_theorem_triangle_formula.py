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
from mathmaker.lib.tools.wording import setup_wording_format_of
from mathmaker.lib.document.content import component


class sub_object(component.structure):

    def __init__(self, build_data, picture='true', **options):
        super().setup("minimal", **options)
        super().setup("intercept_theorem_figure", set_lengths=False,
                      **options)

        all_segments = self.figure.small \
            + self.figure.side \
            + [self.figure.u, self.figure.v]\
            + self.figure.chunk

        self.figure.setup_labels([False for _ in range(len(all_segments))],
                                 segments_list=all_segments)

        self.ratios = shared.machine.write_math_style1(
            self.figure.ratios_equalities().into_str())

        self.wording = _(' {line1} {parallel_to} {line2}')
        self.line1 = self.figure.small[1].length_name
        self.line2 = self.figure.side[1].length_name
        setup_wording_format_of(self)

    def q(self, **options):
        return self.wording.format(**self.wording_format) + ' \\newline '\
            + shared.machine.insert_picture(self.figure, scale=0.85)

    def a(self, **options):
        return self.ratios
