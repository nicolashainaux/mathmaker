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
from mathmaker.lib.tools.wording import setup_wording_format_of


class sub_object(component.structure):

    def __init__(self, build_data, **kwargs):
        """
        The two numbers in build_data are the factors of the product.

        The first number will be the possible divisor (i.e. questions will be:
        "... is divisible by nb1. (True or false?)").

        kwargs may contain a 'variant' parameter.
        It can contain these values:
        - 'random' (default), then it will randomly be replaced by 'true'
          or 'false'
        - 'true', then the answer will be true
        - 'false', then a non zero remainder will be added:
          result = nb1 × nb2 + remainder
           and the answer will be false

        :param build_data: a tuple of 2 numbers
        :type build_data: tuple
        """
        super().setup('minimal', **kwargs)
        super().setup('division', nb=build_data, order='divisor,quotient',
                      **kwargs)

        variant = kwargs.get('variant', 'random')
        variant2 = kwargs.get('variant2', 'default')
        if variant == 'random':
            variant = random.choice(['true', 'false'])
        self.n1 = self.divisor
        if variant == 'true':
            self.answer = _('True')
            self.n2 = self.dividend
            if (self.n1 == 4
                and variant2 == 'ensure_no_confusion_between_rules'):
                if Number(self.n2).digits_sum() % 4 == 0:
                    self.n2 += 100
        else:
            self.answer = _('False')
            remainder = random.randint(1, self.divisor - 1)
            correction = 0
            if variant2 == 'ensure_no_confusion_between_rules':
                if self.n1 == 3:
                    if ((self.dividend - 1) % 100) % 3 == 0:
                        remainder = -1
                    else:
                        remainder = 1
                elif self.n1 == 9:
                    remainder = 9 - (self.dividend % 100) % 9
                elif self.n1 == 4:
                    remainder = 2
                    mod4 = Number(self.dividend + remainder).digits_sum() % 4
                    if mod4 != 0:
                        if Number(self.dividend + remainder).digit(100) < 7:
                            correction = 100 * (4 - mod4)
                        else:
                            correction = -100 * mod4
            self.n2 = self.dividend + remainder + correction
        statement = _('{n2} is divisible by {n1}.')
        nl = r'\newline' if self.slideshow else ''
        self.wording = r'{} {} {}'.format(statement, nl,
                                          _('(True or false?)'))
        setup_wording_format_of(self)
        self.transduration = 21

    def q(self, **kwargs):
        return self.wording.format(**self.wording_format)

    def a(self, **kwargs):
        # This is actually meant for self.preset == 'mental calculation'
        return str(self.answer)

    def js_a(self, **kwargs):
        return [self.answer, self.answer.lower(),
                self.answer[0], self.answer[0].lower()]
