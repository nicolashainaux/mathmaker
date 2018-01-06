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

from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import post_process
from mathmaker.lib.tools.wording import setup_wording_format_of


class sub_object(component.structure):

    def __init__(self, build_data, **options):
        super().setup("minimal", **options)
        # Possible options: allow_null_remainder (defaults to False)
        #                   force_null_remainder (defaults to False)
        super().setup("euclidean_division", nb=build_data, **options)
        self.transduration = 15
        if self.divisor > 5 and self.divisor % 10 != 0:
            self.transduration += 3
        if self.divisor > 10 and self.divisor % 10 != 0:
            self.transduration += 3
        self.wording = _('Euclidean division of {dividend} by {divisor}?')
        setup_wording_format_of(self)
        # This is actually meant for self.preset == 'mental calculation'
        self.answer = '{quotient} r {remainder}'\
            .format(quotient=self.quotient, remainder=self.remainder)

    def q(self, **options):
        return post_process(self.wording.format(**self.wording_format))

    def a(self, **options):
        return self.answer

    def js_a(self, **kwargs):
        alt_answer1 = 'q {quotient} r {remainder}'\
            .format(quotient=self.quotient, remainder=self.remainder)
        alt_answer2 = '{quotient} R {remainder}'\
            .format(quotient=self.quotient, remainder=self.remainder)
        return [self.answer, alt_answer1, alt_answer2]
