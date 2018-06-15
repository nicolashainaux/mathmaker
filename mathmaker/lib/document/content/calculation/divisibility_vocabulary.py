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

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.tools.wording import setup_wording_format_of


class sub_object(component.structure):

    def __init__(self, build_data, **kwargs):
        """
        The two numbers in build_data are the factors of the product.

        kwargs may contain a 'variant' parameter.
        It can contain these values:
        - 'random' (default), then it will randomly be replaced by 'true'
          or 'false'
        - 'true', then the answer will be true
        - 'false', then it will randomly replaced by 'remainder' or 'reversed'
        - 'remainder' then a non zero remainder will be added:
          result = nb1 × nb2 + remainder
           and the answer will be false
        - 'reversed' then the result and nb1 or nb2 will be exchanged and the
          answer will be false

        :param nb_to_use: a tuple of 2 numbers
        :type nb_to_use: tuple
        """
        super().setup('minimal', **kwargs)
        # super().setup("numbers", nb=nb_to_use, **kwargs)
        # super().setup("nb_variants", nb=nb_to_use, **kwargs)
        super().setup('division', nb=build_data, **kwargs)

        variant = kwargs.get('variant', 'random')
        if variant == 'random':
            variant = random.choice(['true', 'false'])
        if variant == 'true':
            self.n2 = self.dividend
            self.n1 = self.divisor
            self.answer = _('True')
        else:
            if variant == 'false':
                variant = random.choice(['remainder', 'reversed'])
            self.answer = _('False')
            if variant == 'remainder':
                remainder = random.randint(1, self.divisor - 1)
                self.n2 = self.dividend + remainder
                self.n1 = self.divisor
            elif variant == 'reversed':
                self.n1 = self.dividend
                self.n2 = self.divisor
        statement = _(next(shared.divisibility_statements_source)[0])
        nl = r'\newline' if self.slideshow else ''
        self.wording = r'{} {} {}'.format(statement, nl,
                                          _('(True or false?)'))
        setup_wording_format_of(self)
        self.transduration = 18

    def q(self, **kwargs):
        return self.wording.format(**self.wording_format)

    def a(self, **kwargs):
        # This is actually meant for self.preset == 'mental calculation'
        return str(self.answer)

    def js_a(self, **kwargs):
        return [self.answer, self.answer.lower(),
                self.answer[0], self.answer[0].lower()]
