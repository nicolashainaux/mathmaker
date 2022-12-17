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

from intspan import intspan

from mathmaker.lib import shared
from mathmaker.lib.document.content import component
from mathmaker.lib.document.content.expression_creator import ExpressionCreator
from mathmaker.lib.tools.frameworks import process_autofit
from mathmaker.lib.LaTeX import SlideContent

# Possible variants
# (where A, B, C... represent provided constants
#  while x, y, z... represent variables)

# 100   A + Bx              104   A + x/B
# 101   A - Bx              105   A - x/B
# 102   Bx + A              106   x/A + B
# 103   Bx - A              107   x/A - B

# 108   A + B/x             112   A(x + B)
# 109   A - B/x             113   A(x - B)
# 110   B/x + A             114   A/(x + B)
# 111   B/x - A             115   A/(x - B)

# 116  A(B + x)             120   (x + B)/A
# 117  A(B - x)             121   (x - B)/A
# 118  A/(B + x)            122   (B + x)/A
# 119  A/(B - x)            123   (B - x)/A

# 124   x² + A              128   x²
# 125   A + x²              129   Ax²
# 126   x² - A              130   x²/A
# 127   A - x²              131   A/x²

# 132   x² + x              136   x×A + B
# 133   x + x²              137   x×A - B
# 134   x² - x              138   B + x×A
# 135   x²×A                139   B - x×A

# 140   x² + Ax

# 200   x + Ay              204   Ax + y
# 201   x - Ay              205   Ax - y
# 202   x + A/y             206   A/x + y
# 203   x - A/y             207   A/x - y

# 208   (x + A)(y + B)      212   Ax + By
# 209   (A + x)(y + B)      213   Ax + y/B
# 210   (x + A)(B + y)      214   x/A + By
# 211   (A + x)(B + y)      215   x/A + y/B

# variants:
# @xid‣100,101,102,103:
# @at1‣3-9,11-19,21-29,31-39   OR   @pr1·nb_variant=decimal1
#

EXPRESSIONS = {
    '100': 'A+Bx', '101': 'A-Bx', '102': 'Bx+A', '103': 'Bx-A',
    '104': 'A+\dfrac{x}{B}', '105': 'A-\dfrac{x}{B}', '106': '\dfrac{x}{B}+A',
    '107': '\dfrac{x}{B}-A',
    '108': 'A+\dfrac{B}{x}', '109': 'A-\dfrac{B}{x}', '110': '\dfrac{B}{x}+A',
    '111': '\dfrac{B}{x}-A',
    '112': 'A(x+B)', '113': 'A(x-B)', '114': '\dfrac{A}{x+B}',
    '115': '\dfrac{A}{x-B}',
    '116': 'A(B+x)', '117': 'A(B-x)', '118': '\dfrac{A}{B+x}',
    '119': '\dfrac{A}{B-x}',
    '120': '\dfrac{x+B}{A}', '121': '\dfrac{x-B}{A}', '122': '\dfrac{B+x}{A}',
    '123': '\dfrac{B-x}{A}',
    '124': 'x^{2}+A', '125': 'A+x^{2}', '126': 'x^{2}-A', '127': 'A-x^{2}',
    '128': 'x^{2}', '129': 'Ax^{2}', '130': '\dfrac{x^{2}}{A}',
    '131': '\dfrac{A}{x^{2}}',
    '132': 'x^{2} + x', '133': 'x + x^{2}', '134': 'x^{2} - x',
    '135': r'x^{2}\times{A}', '136': r'x\times{B}+A', '137': r'x\times{B}-A',
    '138': r'A+x\times{B}', r'139': r'A-x\times{B}',
    '140': 'x^{2} + Ax'
}


class sub_object(ExpressionCreator, component.structure):

    def __init__(self, build_data, **options):
        # Since minimal setup will be called later for each source, do not call
        # it here, it would be overriden. Save it instead.
        self.options = options
        build_data = process_autofit(build_data[0])
        variant_span = intspan(
            build_data['xid']['source'][len('expressions:'):])
        if len(variant_span) == 1:
            self.variant_id = str(list(variant_span)[0])
        else:
            self.variant_id = shared.expressions_source.next(
                nb1_in=list(variant_span))[0]
        self.setup_sources(build_data)
        letters = ['a', 'b', 'c', 'd', 'x', 'y', 'z', 't']
        random.shuffle(letters)
        self.var1 = letters.pop()
        self.var2 = letters.pop()
        self.expression = EXPRESSIONS[self.variant_id]
        getattr(self, f'_create_variant_{self.variant_id}')(build_data)
        self.setup_expression_values()

        self.wording1 = _('Evaluate the expression {expression}')\
            .format(expression=self.expression)
        self.wording2 = _('for {values}').format(values=self.values)
        self.wording = f'{self.wording1} {self.wording2}'
        self.transduration = 30

    def q(self, **options):
        if self.slideshow:
            output = SlideContent(wording1=self.wording1,
                                  height1='0.25pt',
                                  wording2=self.wording2)
        else:
            output = self.wording
        return str(output)

    def a(self, **options):
        # This is actually meant for self.preset == 'mental calculation'
        return self.answer.printed

    def js_a(self, **kwargs):
        return [self.answer.uiprinted]

    def setup_expression_values(self):
        self.expression = self.expression.replace('A', self.nb1.printed)\
            .replace('B', self.nb2.printed)\
            .replace('x', self.var1)
        self.values = shared.machine.write_math_style2(
            f'{self.var1} = {self.nb3.printed}')
        self.expression = shared.machine.write_math_style2(self.expression)
