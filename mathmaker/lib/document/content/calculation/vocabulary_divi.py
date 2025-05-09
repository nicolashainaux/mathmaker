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

# This module will add a question about the quotient of two numbers

from mathmakerlib.calculus import Fraction

from . import vocabulary_questions


class sub_object(vocabulary_questions.structure):

    def __init__(self, build_data, **options):
        if isinstance(build_data[1], Fraction):
            super().__init__((build_data[1].denominator, build_data[1]),
                             result_fct=None,
                             result=build_data[1].numerator,
                             wording=_('How much is the quotient of {result} '
                                       'by {nb1}?'),
                             answer='{nb2}',
                             shuffle_nbs=False,
                             **options)
        else:
            super().__init__(build_data,
                             result_fct=lambda x, y: x * y,
                             wording=_('How much is the quotient of {result} '
                                       'by {nb1}?'),
                             answer='{nb2}',
                             **options)
