# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2014 Nicolas Hainaux <nico_h@users.sourceforge.net>

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

from core.base_calculus import *
from . import mc_module
from lib.wordings_handling_tools import reformat, setup_wording_format_of
from lib.common import shared

class sub_object(mc_module.structure):

    def __init__(self, M, numbers_to_use, **options):
        super().setup(M, "minimal", **options)
        super().setup(M, "nb_variants", nb=numbers_to_use, **options)
        super().setup(M, "length_units", **options)
        super().setup(M, "rectangle", **options)

        self.w_str = self.rectangle.width.into_str(force_expression_begins=True)
        self.l_str = self.rectangle.length.into_str(\
                                                   force_expression_begins=True)
        self.perimeter_str = self.rectangle.perimeter.into_str(\
                                                   force_expression_begins=True)
        if self.picture:
            self.rectangle.rename(next(shared.four_letters_words_source))
            self.wording = _("Perimeter of this rectangle? |hint:length_unit|")
            setup_wording_format_of(self, M)
        else:
            self.wording = reformat(_("Perimeter of a rectangle whose width \
is {w} <length_unit> and length is {l} <length_unit>? |hint:length_unit|")\
                                    .format(w=M.write_math_style2(self.w_str),
                                            l=M.write_math_style2(self.l_str)))
            setup_wording_format_of(self, M)

    def q(self, M, **options):
        if self.picture:
            return M.write_layout((1, 2),
                                  [5, 8],
                                  [M.insert_picture(self.rectangle,
                                                    scale=0.75,
                                         vertical_alignment_in_a_tabular=True),
                                   self.wording.format(**self.wording_format)])
        else:
            return self.wording.format(**self.wording_format)

    def a(self, M, **options):
        u = ""
        if hasattr(self, 'hint'):
            u = M.insert_nonbreaking_space() + self.hint
        return M.write_math_style2(self.perimeter_str) + u
