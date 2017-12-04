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

# This module will add a question about the half|third|quarter of a number

from . import vocabulary_questions


class sub_object(vocabulary_questions.structure):

    def __init__(self, numbers_to_use, **options):
        PARTS_QUESTIONS = {2: _('What is the half of {result}?'),
                           3: _('What is the third of {result}?'),
                           4: _('What is the quarter of {result}?')}
        if numbers_to_use[0] not in PARTS_QUESTIONS:
            numbers_to_use = sorted(numbers_to_use)[::-1]
            numbers_to_use = [numbers_to_use[0] // 10, numbers_to_use[1] * 10]
        super().__init__(numbers_to_use,
                         result_fct=lambda x, y: x * y,
                         wording=PARTS_QUESTIONS[numbers_to_use[0]],
                         shuffle_nbs=False,
                         answer='{nb2}')
