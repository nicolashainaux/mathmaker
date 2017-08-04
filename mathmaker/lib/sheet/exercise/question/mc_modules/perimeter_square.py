# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

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
from .. import submodule
from mathmaker.lib.tools.wording import setup_wording_format_of


class sub_object(submodule.structure):

    def __init__(self, numbers_to_use, **options):
        super().setup("minimal", **options)
        super().setup("numbers", nb=numbers_to_use, **options)
        super().setup("nb_variants", nb=numbers_to_use, **options)
        super().setup("length_units", **options)
        super().setup("square", **options)

        if self.picture:
            self.wording = _("Perimeter of this square? |hint:length_unit|")
            setup_wording_format_of(self)
        else:
            self.nb1 = self.square.side_length
            self.wording = _("Perimeter of a square whose side's length \
is {nb1} {length_unit}? |hint:length_unit|")
            setup_wording_format_of(self)

    def q(self, **options):
        if self.picture:
            return shared.machine.write_layout(
                (1, 2),
                [5, 8],
                [shared.machine.insert_picture(
                 self.square,
                 scale=0.75,
                 vertical_alignment_in_a_tabular=True),
                 self.wording.format(**self.wording_format)])
        else:
            return self.wording.format(**self.wording_format)

    def a(self, **options):
        return self.square.perimeter.into_str(display_SI_unit=True)
